from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QComboBox, QLabel, QMessageBox,
                               QApplication)
from PySide6.QtCore import Qt, Slot
from src.ui.config_dialog import ConfigDialog
from src.odoo.odoo_client import OdooClient
import json
import os
import sys
import traceback

def exception_handler(exc_type, exc_value, exc_traceback):
    """Manejador global de excepciones no capturadas"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Error no capturado:\n{error_msg}")
    if QApplication.instance():
        QMessageBox.critical(None, "Error Fatal", 
                           f"Ha ocurrido un error inesperado:\n\n{str(exc_value)}\n\n"
                           "La aplicación se cerrará.")
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    QApplication.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exportador de BOM")
        self.setGeometry(100, 100, 600, 400)  # Ventana más grande
        
        # Crear widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)  # Espacio entre widgets
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes
        
        # Crear y configurar widgets
        title_label = QLabel("Exportador de Lista de Materiales")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        
        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("Seleccione un producto")
        self.product_combo.setMinimumWidth(400)
        
        self.export_button = QPushButton("Exportar BOM")
        self.export_button.setEnabled(False)
        self.export_button.setMinimumWidth(120)
        
        self.config_button = QPushButton("Configuración")
        self.config_button.setMinimumWidth(120)
        
        # Añadir widgets al layout
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        
        layout.addWidget(QLabel("Productos con Lista de Materiales:"))
        layout.addWidget(self.product_combo)
        layout.addSpacing(10)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.config_button)
        layout.addLayout(button_layout)
        
        layout.addStretch()  # Espacio flexible al final
        
        # Conectar señales
        self.config_button.clicked.connect(self.show_config_dialog)
        self.export_button.clicked.connect(self.export_bom)
        self.product_combo.currentIndexChanged.connect(self.on_product_selected)
        
        # Inicializar cliente Odoo
        self.odoo_client = None
        self.load_config_and_connect()

    def load_config_and_connect(self):
        """Carga la configuración y conecta con Odoo"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    
                self.odoo_client = OdooClient(
                    url=config['url'],
                    db=config['database'],
                    username=config['username'],
                    password=config['password'],
                    port=config['port']
                )
                
                # Cargar productos
                self.load_products()
            else:
                QMessageBox.warning(
                    self,
                    "Configuración no encontrada",
                    "Por favor configure la conexión a Odoo"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error de conexión",
                str(e)
            )

    def load_products(self):
        """Carga la lista de productos en el combo"""
        try:
            self.product_combo.clear()
            self.product_combo.addItem("Cargando productos...", None)
            self.product_combo.setEnabled(False)
            QApplication.processEvents()  # Permitir que la UI se actualice
            
            products = self.odoo_client.get_products()
            
            self.product_combo.clear()
            self.product_combo.setEnabled(True)
            
            if not products:
                self.product_combo.addItem("No se encontraron productos con BOM", None)
                return
                
            for product in products:
                self.product_combo.addItem(product['name'], product['id'])
                
        except Exception as e:
            self.product_combo.clear()
            self.product_combo.setEnabled(True)
            QMessageBox.critical(
                self,
                "Error",
                f"Error al cargar productos: {str(e)}"
            )

    @Slot()
    def show_config_dialog(self):
        """Muestra el diálogo de configuración"""
        dialog = ConfigDialog(self)
        if dialog.exec():
            self.load_config_and_connect()

    @Slot()
    def export_bom(self):
        """Exporta la lista de materiales del producto seleccionado"""
        try:
            product_id = self.product_combo.currentData()
            if product_id and self.odoo_client:
                self.export_button.setEnabled(False)
                self.export_button.setText("Exportando...")
                QApplication.processEvents()  # Permitir que la UI se actualice
                
                filename = self.odoo_client.export_bom(product_id)
                
                self.export_button.setEnabled(True)
                self.export_button.setText("Exportar BOM")
                
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"BOM exportada correctamente a:\n{filename}"
                )
        except Exception as e:
            self.export_button.setEnabled(True)
            self.export_button.setText("Exportar BOM")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al exportar BOM: {str(e)}"
            )

    @Slot(int)
    def on_product_selected(self, index):
        """Habilita/deshabilita el botón de exportar según la selección"""
        self.export_button.setEnabled(index >= 0 and self.product_combo.currentData() is not None)

def main():
    # Configurar el manejador de excepciones global
    sys.excepthook = exception_handler
    
    # Crear y ejecutar la aplicación
    app = QApplication(sys.argv)
    
    # Establecer el estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el bucle de eventos
    return app.exec()

if __name__ == '__main__':
    sys.exit(main()) 