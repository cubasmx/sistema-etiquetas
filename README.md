# Sistema de Etiquetas ZPL

Sistema de impresión de etiquetas con soporte para impresoras ZPL y transformación de archivos Excel a CSV.

## Requisitos

- Python 3.8 o superior
- PyQt6
- pandas
- openpyxl

## Instalación

1. Clone este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd sistema-etiquetas
```

2. Instale las dependencias:
```bash
pip install PyQt6 pandas openpyxl
```

## Configuración

1. Configure la impresora ZPL:
   - La dirección IP predeterminada es "10.10.2.34"
   - El puerto predeterminado es 9100
   - Puede modificar estos valores en `PythonApplication1.py`

2. Prepare sus archivos:
   - Use archivos CSV para los datos de productos
   - O utilice el transformador incluido para convertir archivos Excel a CSV

## Uso

1. Ejecute la aplicación:
```bash
python PythonApplication1.py
```

2. Funcionalidades principales:
   - Carga y lectura de archivos CSV
   - Búsqueda de productos por ID o nombre
   - Impresión de etiquetas con códigos de barras
   - Transformación de archivos Excel a CSV
   - Soporte para versiones SGC y números de OP
   - Impresión múltiple de etiquetas

## Características

- Interfaz gráfica intuitiva con PyQt6
- Soporte para caracteres especiales (UTF-8 y Latin-1)
- Generación de códigos de barras en formato ZPL
- Transformador de Excel a CSV incluido
- Funcionamiento local sin necesidad de conexión a internet

## Notas

- La aplicación ha sido probada y funciona correctamente en Windows
- Asegúrese de que la impresora ZPL esté conectada y accesible en la red
- Los archivos CSV deben estar correctamente formateados con las columnas necesarias 