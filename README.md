# Exportador de Lista de Materiales (BOM)

Aplicación de escritorio para exportar listas de materiales desde Odoo a Excel.

## Características

- Interfaz gráfica intuitiva
- Conexión directa a Odoo
- Exportación a Excel con formato profesional
- Soporte para múltiples productos
- Configuración personalizable

## Requisitos

- Python 3.8 o superior
- Acceso a un servidor Odoo
- Credenciales de usuario con permisos para acceder a las listas de materiales

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/sistema-etiquetas.git
cd sistema-etiquetas
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
python main.py
```

2. En el primer inicio, configurar la conexión a Odoo:
   - URL del servidor
   - Base de datos
   - Usuario
   - Contraseña
   - Puerto (443 para Odoo SaaS, 8069 para instalaciones locales)

3. Seleccionar un producto de la lista desplegable

4. Hacer clic en "Exportar BOM"

Los archivos exportados se guardarán en la carpeta `exports` con el formato:
`BOM_[nombre_producto]_[fecha]_[hora].xlsx`

## Estructura del Proyecto

```
sistema-etiquetas/
├── src/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── config_dialog.py
│   ├── odoo/
│   │   ├── __init__.py
│   │   └── connection.py
│   └── export/
│       ├── __init__.py
│       └── excel_exporter.py
├── exports/
├── main.py
├── requirements.txt
└── README.md
```

## Soporte

Para reportar problemas o sugerir mejoras, por favor crear un issue en el repositorio. 