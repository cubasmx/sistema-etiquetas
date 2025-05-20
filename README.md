# Sistema de Impresión de Etiquetas

Aplicación de escritorio desarrollada con PyQt6 para la impresión de etiquetas con códigos de barras.

## Características

- Interfaz gráfica intuitiva
- Importación de datos desde archivos CSV
- Búsqueda de productos por ID
- Impresión de etiquetas con código de barras
- Configuración de cantidad de etiquetas a imprimir
- Soporte para impresoras Zebra (ZPL)

## Requisitos

- Python 3.x
- PyQt6

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Instalar dependencias:
```bash
pip install PyQt6
```

## Uso

1. Ejecutar la aplicación:
```bash
python PythonApplication1.py
```

2. Usar la interfaz para:
   - Importar archivo CSV con datos de productos
   - Buscar productos por ID
   - Configurar la orden de producción
   - Imprimir etiquetas

## Configuración de la Impresora

La aplicación está configurada para conectarse a una impresora Zebra en:
- IP: 10.10.2.34
- Puerto: 9100

Para cambiar esta configuración, modificar las variables `printer_ip` y `printer_port` en el código. 