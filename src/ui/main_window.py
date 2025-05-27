from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QComboBox, QLabel, QMessageBox,
                               QApplication)
from PySide6.QtCore import Qt, Slot
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.setGeometry(100, 100, 400, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Botón de prueba
        test_button = QPushButton("Click Me")
        test_button.clicked.connect(self.on_button_click)
        
        # Añadir al layout
        layout.addWidget(test_button)
    
    def on_button_click(self):
        QMessageBox.information(self, "Test", "Button clicked!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())                                                                                                                                                                                                                                                                                                                    