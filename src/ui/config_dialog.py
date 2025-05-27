from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                                 QLineEdit, QPushButton, QSpinBox)
import json
import os

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Odoo")
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Crear campos de entrada
        self.url_input = QLineEdit()
        self.db_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.port_input = QSpinBox()
        
        # Configurar campos
        self.password_input.setEchoMode(QLineEdit.Password)
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(443)  # Puerto por defecto para Odoo SaaS
        
        # Añadir campos al formulario
        form_layout.addRow("URL:", self.url_input)
        form_layout.addRow("Base de datos:", self.db_input)
        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)
        form_layout.addRow("Puerto:", self.port_input)
        
        # Botones
        save_button = QPushButton("Guardar")
        cancel_button = QPushButton("Cancelar")
        
        # Conectar señales
        save_button.clicked.connect(self.save_config)
        cancel_button.clicked.connect(self.reject)
        
        # Añadir layouts y widgets
        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

    def load_config(self):
        """Carga la configuración existente si existe"""
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.url_input.setText(config.get('url', ''))
                    self.db_input.setText(config.get('database', ''))
                    self.username_input.setText(config.get('username', ''))
                    self.password_input.setText(config.get('password', ''))
                    self.port_input.setValue(int(config.get('port', 443)))
            except Exception as e:
                print(f"Error al cargar la configuración: {e}")

    def save_config(self):
        """Guarda la configuración en un archivo JSON"""
        config = {
            'url': self.url_input.text(),
            'database': self.db_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'port': self.port_input.value()
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            self.accept()
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
            self.reject() 