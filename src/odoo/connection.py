import xmlrpc.client
import json
import os
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse

class OdooConnection:
    def __init__(self):
        self.client = None
        self.uid = None
        self.models = None
        self.config = None
        
    def _format_url(self, url: str) -> str:
        """
        Formatea la URL para asegurar que sea válida para XML-RPC
        Args:
            url: URL del servidor Odoo
        Returns:
            str: URL formateada
        """
        # Asegurar que la URL comienza con https://
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Remover la barra final si existe
        url = url.rstrip('/')
        
        # Validar la URL
        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError("URL inválida")
            
        return url
        
    def connect(self) -> Tuple[bool, str]:
        """
        Establece la conexión con Odoo usando la configuración guardada
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Cargar configuración
            if not os.path.exists('config.json'):
                return False, "No existe archivo de configuración"
            
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            
            # Validar configuración
            required_fields = ['url', 'database', 'username', 'password']
            if not all(field in self.config for field in required_fields):
                return False, "Configuración incompleta"
            
            # Formatear URL
            try:
                base_url = self._format_url(self.config['url'])
            except ValueError as e:
                return False, f"URL inválida: {str(e)}"
            
            # Crear conexión
            common_url = f"{base_url}/xmlrpc/2/common"
            print(f"Conectando a: {common_url}")  # Debug
            common = xmlrpc.client.ServerProxy(common_url)
            
            # Autenticar
            try:
                self.uid = common.authenticate(
                    self.config['database'],
                    self.config['username'],
                    self.config['password'],
                    {}
                )
            except Exception as e:
                return False, f"Error de autenticación: {str(e)}"
            
            if not self.uid:
                return False, "Error de autenticación: credenciales inválidas"
            
            # Crear cliente
            self.models = xmlrpc.client.ServerProxy(f"{base_url}/xmlrpc/2/object")
            
            return True, "Conexión exitosa"
            
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
    
    def get_bom_products(self) -> List[Dict[str, Any]]:
        """
        Obtiene los productos que tienen lista de materiales
        Returns:
            List[Dict]: Lista de productos con sus IDs y nombres
        """
        if not self.models or not self.uid:
            raise ConnectionError("No hay conexión activa con Odoo")
        
        try:
            # Buscar productos con BOM
            bom_products = self.models.execute_kw(
                self.config['database'],
                self.uid,
                self.config['password'],
                'mrp.bom',
                'search_read',
                [[['active', '=', True]]],
                {
                    'fields': ['product_tmpl_id'],
                    'context': {'active_test': True}
                }
            )
            
            if not bom_products:
                return []
            
            # Obtener IDs únicos de productos
            product_ids = list(set(bom['product_tmpl_id'][0] for bom in bom_products))
            
            # Obtener detalles de los productos
            products = self.models.execute_kw(
                self.config['database'],
                self.uid,
                self.config['password'],
                'product.template',
                'read',
                [product_ids],
                {'fields': ['id', 'name', 'default_code']}
            )
            
            return products
            
        except Exception as e:
            raise ConnectionError(f"Error al obtener productos: {str(e)}")
    
    def get_bom_data(self, product_id: int, level: int = 0) -> Dict[str, Any]:
        """
        Obtiene los datos de la lista de materiales para un producto, incluyendo sub-BOMs
        Args:
            product_id: ID del producto
            level: Nivel de profundidad actual (para BOMs anidadas)
        Returns:
            Dict: Datos de la BOM
        """
        if not self.models or not self.uid:
            raise ConnectionError("No hay conexión activa con Odoo")
        
        try:
            # Buscar BOM activa para el producto
            bom = self.models.execute_kw(
                self.config['database'],
                self.uid,
                self.config['password'],
                'mrp.bom',
                'search_read',
                [[
                    ['product_tmpl_id', '=', product_id],
                    ['active', '=', True]
                ]],
                {
                    'fields': ['product_qty', 'code', 'product_uom_id', 'bom_line_ids', 'product_tmpl_id'],
                    'limit': 1
                }
            )
            
            if not bom:
                raise ValueError(f"No se encontró BOM para el producto {product_id}")
            
            bom = bom[0]
            
            # Obtener líneas de la BOM con campos adicionales
            lines = self.models.execute_kw(
                self.config['database'],
                self.uid,
                self.config['password'],
                'mrp.bom.line',
                'read',
                [bom['bom_line_ids']],
                {
                    'fields': [
                        'product_id',
                        'product_qty',
                        'product_uom_id',
                        'sequence',
                        'child_bom_id',
                    ]
                }
            )
            
            # Procesar las líneas para asegurar que son serializables
            processed_lines = []
            for line in lines:
                processed_line = {
                    'product_id': line['product_id'],  # Esto ya viene como tupla (id, name)
                    'product_qty': float(line['product_qty']),  # Convertir a float por si acaso
                    'product_uom_id': line['product_uom_id'],  # Esto ya viene como tupla (id, name)
                    'sequence': line['sequence'],
                    'level': level,
                    'sub_bom': None
                }
                
                # Si la línea tiene una BOM hija, obtenerla recursivamente
                if line['child_bom_id']:
                    try:
                        # Obtener el product_tmpl_id del producto en la línea
                        product_info = self.models.execute_kw(
                            self.config['database'],
                            self.uid,
                            self.config['password'],
                            'product.product',
                            'read',
                            [line['product_id'][0]],
                            {'fields': ['product_tmpl_id']}
                        )
                        if product_info:
                            child_product_tmpl_id = product_info[0]['product_tmpl_id'][0]
                            # Obtener la BOM del subproducto
                            sub_bom = self.get_bom_data(child_product_tmpl_id, level + 1)
                            processed_line['sub_bom'] = sub_bom
                    except Exception as e:
                        print(f"Error al obtener sub-BOM: {str(e)}")
                
                processed_lines.append(processed_line)
            
            # Ordenar las líneas por secuencia
            processed_lines.sort(key=lambda x: x['sequence'])
            
            # Estructurar respuesta asegurando tipos serializables
            return {
                'bom_id': int(bom['id']),
                'product_qty': float(bom['product_qty']),
                'code': str(bom['code']) if bom['code'] else '',
                'uom': str(bom['product_uom_id'][1]) if bom['product_uom_id'] else '',
                'product_name': str(bom['product_tmpl_id'][1]),
                'lines': processed_lines,
                'level': level
            }
            
        except Exception as e:
            raise ConnectionError(f"Error al obtener BOM: {str(e)}") 