from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
from typing import Dict, List, Any
import os

class ExcelExporter:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Lista de Materiales"
        
        # Estilos
        self.header_font = Font(bold=True, color="FFFFFF")
        self.header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        self.header_alignment = Alignment(horizontal="center", vertical="center")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def export_bom(self, bom_data: Dict[str, Any], product_name: str) -> str:
        """
        Exporta los datos de la BOM a un archivo Excel
        Args:
            bom_data: Diccionario con los datos de la BOM
            product_name: Nombre del producto
        Returns:
            str: Ruta del archivo generado
        """
        try:
            # Configurar encabezados
            headers = ["Código", "Componente", "Cantidad", "Unidad"]
            for col, header in enumerate(headers, start=1):
                cell = self.ws.cell(row=1, column=col)
                cell.value = header
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.alignment = self.header_alignment
                cell.border = self.border
            
            # Ajustar ancho de columnas
            self.ws.column_dimensions['A'].width = 15  # Código
            self.ws.column_dimensions['B'].width = 40  # Componente
            self.ws.column_dimensions['C'].width = 12  # Cantidad
            self.ws.column_dimensions['D'].width = 12  # Unidad
            
            # Añadir datos
            for row, line in enumerate(bom_data['lines'], start=2):
                # Código
                cell = self.ws.cell(row=row, column=1)
                cell.value = line['product_id'][1].split(']')[0].strip('[') if '][' in line['product_id'][1] else ''
                cell.border = self.border
                cell.alignment = Alignment(horizontal="center")
                
                # Componente
                cell = self.ws.cell(row=row, column=2)
                cell.value = line['product_id'][1].split(']')[-1].strip() if '][' in line['product_id'][1] else line['product_id'][1]
                cell.border = self.border
                
                # Cantidad
                cell = self.ws.cell(row=row, column=3)
                cell.value = line['product_qty']
                cell.border = self.border
                cell.alignment = Alignment(horizontal="center")
                
                # Unidad
                cell = self.ws.cell(row=row, column=4)
                cell.value = line['product_uom_id'][1]
                cell.border = self.border
                cell.alignment = Alignment(horizontal="center")
            
            # Crear directorio de exportación si no existe
            export_dir = "exports"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c if c.isalnum() else "_" for c in product_name)
            filename = f"{export_dir}/BOM_{safe_name}_{timestamp}.xlsx"
            
            # Guardar archivo
            self.wb.save(filename)
            return filename
            
        except Exception as e:
            raise Exception(f"Error al exportar a Excel: {str(e)}") 