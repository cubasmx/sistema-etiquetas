# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QSpinBox,
    QWidget,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QScrollArea,
    QHBoxLayout
)
import csv
import socket

class MainWindow(QWidget):
    def __init__(self):
        # Constructor de la ventana principal
        super().__init__()
        self.setWindowTitle('Impresión de Etiquetas')
        self.setGeometry(100, 100, 500, 500)  # Posición y tamaño inicial de la ventana

        # Botones y campos de entrada
        self.import_button = QPushButton('Examinar...')
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Buscar ID de Producto')
        self.search_button = QPushButton('Buscar')
        self.clear_button = QPushButton('Limpiar')

        # Layout de búsqueda horizontal
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_button)

        # Área de resultados
        self.result_label = QLabel('Resultados de la búsqueda:')
        self.results_area = QListWidget()
        self.results_area.itemClicked.connect(self.item_selected)
        self.results_area.setWordWrap(True)

        # Configuración del área de desplazamiento
        self.scroll_inner = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_inner)
        scroll_layout.addWidget(self.results_area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_inner)

        # Campos para la Orden de Producción
        self.op_description_label = QLabel('OP:')
        self.op_description_input = QLineEdit()
        self.quantity_label = QLabel('Cantidad a Imprimir:')
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setValue(1)

        # Layouts para OP y cantidad
        op_layout = QHBoxLayout()
        op_layout.addWidget(self.op_description_label)
        op_layout.addWidget(self.op_description_input)

        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(self.quantity_label)
        quantity_layout.addWidget(self.quantity_spinbox)

        # Botón de impresión
        self.print_button = QPushButton('Imprimir')

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.import_button)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.op_description_label)
        main_layout.addWidget(self.op_description_input)
        main_layout.addWidget(self.quantity_label)
        main_layout.addWidget(self.quantity_spinbox)
        main_layout.addWidget(self.print_button)

        # Conexiones de señales
        self.import_button.clicked.connect(self.open_file_dialog)
        self.search_button.clicked.connect(self.perform_search)
        self.clear_button.clicked.connect(self.clear_search_and_results)
        self.search_input.returnPressed.connect(self.perform_search)
        self.print_button.clicked.connect(self.handle_print)

        # Variables de datos
        self.csv_data = []
        self.selected_product = None

    def item_selected(self, item):
        # Procesa el elemento seleccionado de la lista
        texto_item = item.text()
        partes = texto_item.split(', ')
        seleccion = {}
        
        for parte in partes:
            clave_valor = parte.split(': ')
            if len(clave_valor) == 2:
                seleccion[clave_valor[0].strip()] = clave_valor[1].strip()

        if 'ID' in seleccion:
            self.selected_product = {
                'id_producto': seleccion['ID'],
                'code_128': seleccion['Code'],
                'nombre': seleccion['Nombre']
            }
            print(f"Producto seleccionado: {self.selected_product}")
        else:
            self.selected_product = None

    def open_file_dialog(self):
        # Abre diálogo para seleccionar archivo CSV
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo CSV",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    self.csv_data = list(reader)
                print(f"Archivo CSV leído con {len(self.csv_data)} registros.")
            except FileNotFoundError:
                print(f"Error: No se pudo encontrar el archivo en la ruta: {file_path}")
            except Exception as e:
                print(f"Error al leer el archivo CSV: {e}")

    def perform_search(self):
        # Realiza búsqueda en los datos del CSV
        text = self.search_input.text()
        if not self.csv_data:
            self.results_area.addItem('Por favor, importa un archivo CSV primero.')
            return

        results = []
        for row in self.csv_data:
            if text.lower() in row.get('id_producto', '').lower():
                results.append(f"ID: {row.get('id_producto', 'N/A')}, Code: {row.get('code_128', 'N/A')}, Nombre: {row.get('nombre', 'N/A')}")

        self.results_area.clear()
        if results:
            for result in results:
                self.results_area.addItem(result)
        else:
            self.results_area.addItem(f'No se encontraron coincidencias para: "{text}"')

    def clear_search_and_results(self):
        # Limpia el campo de búsqueda y resultados
        self.search_input.clear()
        self.results_area.clear()
        self.selected_product = None

    def handle_print(self):
        # Maneja la impresión de etiquetas
        if self.selected_product:
            op_description = self.op_description_input.text()
            quantity = self.quantity_spinbox.value()
            id_producto = self.selected_product.get('id_producto', 'N/A')
            code_128 = self.selected_product.get('code_128', 'N/A')
            nombre_producto = self.selected_product.get('nombre', 'N/A')

            print("--- Generando etiquetas ZPL ---")
            try:
                printer_ip = "10.10.2.34"
                printer_port = 9100

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((printer_ip, printer_port))
                    for i in range(1, quantity + 1):
                        zpl_label = f"""^XA
                        ^FO35,35^A0N,18,18^FD{nombre_producto}^FS
                        ^FO35,60^BCN,75,Y,N,N^FD{id_producto}^FS
                        ^FO35,168^A0N,20,20^FDOP:{op_description}^FS
                        ^FO35,188^A0N,18,18^FD{i}/{quantity}^FS
                        ^PQ1,1,1,Y^XZ"""

                        print(f"--- Enviando etiqueta {i}/{quantity} ---")
                        print(zpl_label)
                        sock.sendall(zpl_label.encode('utf-8'))
                        print(f"Se enviaron {quantity} etiquetas a la impresora!")

            except ConnectionRefusedError:
                self.results_area.addItem(f"Error: No se pudo conectar a la impresora en {printer_ip}:{printer_port}. Asegúrate de que la impresora está encendida y conectada a la red.")
            except Exception as e:
                self.results_area.addItem(f"Error al enviar a la impresora: {e}")
        else:
            self.results_area.addItem('Por favor, busca y selecciona un producto primero.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
