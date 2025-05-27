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
        print("Iniciando MainWindow...")
        super().__init__()
        self.setWindowTitle("Exportador de BOM")
        self.setGeometry(100, 100, 600, 400)
        print("Configurando ventana principal...")
        
        # Crear widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        print("Layout principal configurado...")
        
        try:
            # Crear y configurar widgets
            print("Creando widgets...")
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
            print("Widgets creados exitosamente...")
            
            # Añadir widgets al layout
            print("Añadiendo widgets al layout...")
            layout.addWidget(title_label, alignment=Qt.AlignCenter)
            layout.addSpacing(20)
            
            layout.addWidget(QLabel("Productos con Lista de Materiales:"))
            layout.addWidget(self.product_combo)
            layout.addSpacing(10)
            
            button_layout = QVBoxLayout()
            button_layout.addWidget(self.export_button)
            button_layout.addWidget(self.config_button)
            layout.addLayout(button_layout)
            
            layout.addStretch()
            print("Widgets añadidos al layout...")
            
            # Conectar señales
            print("Conectando señales...")
            self.config_button.clicked.connect(self.show_config_dialog)
            self.export_button.clicked.connect(self.export_bom)
            self.product_combo.currentIndexChanged.connect(self.on_product_selected)
            print("Señales conectadas...")
            
            # Inicializar cliente Odoo
            print("Inicializando cliente Odoo...")
            self.odoo_client = None
            self.load_config_and_connect()
            print("Inicialización completada...")
            
        except Exception as e:
            print(f"Error durante la inicialización: {str(e)}")
            traceback.print_exc()
            raise

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
            print(f"Error en load_config_and_connect: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error de conexión",
                str(e)
            )

    def load_products(self):
        """Carga la lista de productos en el combo"""
        try:
            print("Iniciando carga de productos...")
            self.product_combo.clear()
            self.product_combo.addItem("Cargando productos...", None)
            self.product_combo.setEnabled(False)
            QApplication.processEvents()
            
            products = self.odoo_client.get_products()
            print(f"Productos obtenidos: {len(products)}")
            
            self.product_combo.clear()
            self.product_combo.setEnabled(True)
            
            if not products:
                self.product_combo.addItem("No se encontraron productos con BOM", None)
                return
                
            for product in products:
                self.product_combo.addItem(product['name'], product['id'])
            print("Productos cargados exitosamente")
                
        except Exception as e:
            print(f"Error en load_products: {str(e)}")
            traceback.print_exc()
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
        try:
            print("Mostrando diálogo de configuración...")
            dialog = ConfigDialog(self)
            if dialog.exec():
                self.load_config_and_connect()
            print("Diálogo de configuración cerrado")
        except Exception as e:
            print(f"Error en show_config_dialog: {str(e)}")
            traceback.print_exc()

    @Slot()
    def export_bom(self):
        """Exporta la lista de materiales del producto seleccionado"""
        try:
            print("Iniciando exportación de BOM...")
            product_id = self.product_combo.currentData()
            if product_id and self.odoo_client:
                self.export_button.setEnabled(False)
                self.export_button.setText("Exportando...")
                QApplication.processEvents()
                
                filename = self.odoo_client.export_bom(product_id)
                print(f"BOM exportada a: {filename}")
                
                self.export_button.setEnabled(True)
                self.export_button.setText("Exportar BOM")
                
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"BOM exportada correctamente a:\n{filename}"
                )
        except Exception as e:
            print(f"Error en export_bom: {str(e)}")
            traceback.print_exc()
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
        try:
            self.export_button.setEnabled(index >= 0 and self.product_combo.currentData() is not None)
        except Exception as e:
            print(f"Error en on_product_selected: {str(e)}")
            traceback.print_exc()

def main():
    try:
        print("\n=== Iniciando aplicación ===")
        # Configurar el manejador de excepciones global
        sys.excepthook = exception_handler
        
        # Crear y ejecutar la aplicación
        print("Creando aplicación Qt...")
        app = QApplication(sys.argv)
        
        # Establecer el estilo de la aplicación
        print("Configurando estilo...")
        app.setStyle('Fusion')
        
        # Crear y mostrar la ventana principal
        print("Creando ventana principal...")
        window = MainWindow()
        print("Mostrando ventana principal...")
        window.show()
        
        # Ejecutar el bucle de eventos
        print("Iniciando bucle de eventos...")
        return app.exec()
    except Exception as e:
        print(f"Error fatal en main: {str(e)}")
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    print("Iniciando programa...")
    sys.exit(main()) 