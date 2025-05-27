from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QComboBox, QLabel, QMessageBox,
                               QApplication)
from PySide6.QtCore import Qt, Slot
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exportador de BOM")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Exportador de Lista de Materiales")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        
        # Selector de productos
        layout.addWidget(QLabel("Productos con Lista de Materiales:"))
        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("Seleccione un producto")
        self.product_combo.setMinimumWidth(400)
        layout.addWidget(self.product_combo)
        layout.addSpacing(10)
        
        # Botones
        self.export_button = QPushButton("Exportar BOM")
        self.export_button.setEnabled(False)
        self.export_button.setMinimumWidth(120)
        
        self.config_button = QPushButton("Configuración")
        self.config_button.setMinimumWidth(120)
        
        # Añadir botones al layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.config_button)
        layout.addLayout(button_layout)
        
        # Espacio flexible al final
        layout.addStretch()
        
        # Conectar señales
        self.config_button.clicked.connect(self.show_config_dialog)
        self.export_button.clicked.connect(self.export_bom)
        self.product_combo.currentIndexChanged.connect(self.on_product_selected)
        
        # Añadir algunos productos de prueba
        self.product_combo.addItem("Producto de prueba 1", 1)
        self.product_combo.addItem("Producto de prueba 2", 2)
        self.product_combo.addItem("Producto de prueba 3", 3)

    @Slot()
    def show_config_dialog(self):
        QMessageBox.information(self, "Configuración", "Aquí se mostrará el diálogo de configuración")

    @Slot()
    def export_bom(self):
        product_name = self.product_combo.currentText()
        QMessageBox.information(self, "Exportar", f"Exportando BOM para: {product_name}")

    @Slot(int)
    def on_product_selected(self, index):
        self.export_button.setEnabled(index >= 0)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())                                                                                                                                                                                                                                                                                                                    