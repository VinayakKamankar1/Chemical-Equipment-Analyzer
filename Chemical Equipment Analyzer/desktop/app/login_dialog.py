from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from .api_client import APIClient


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = APIClient()
        self.token = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login - Chemical Equipment Analyzer')
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel('Chemical Equipment Analyzer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 18px; font-weight: bold; margin-bottom: 20px;')
        layout.addWidget(title)
        
        # Username
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Email (for registration)
        email_label = QLabel('Email (optional, for registration):')
        self.email_input = QLineEdit()
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        
        # Register checkbox
        self.register_checkbox = QCheckBox('Register new account')
        layout.addWidget(self.register_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton('Login / Register')
        login_btn.clicked.connect(self.handle_login)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(login_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        layout.addStretch()
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Username and password are required')
            return
        
        try:
            if self.register_checkbox.isChecked():
                result = self.api_client.register(username, password, email)
                QMessageBox.information(self, 'Success', 'Registration successful!')
            else:
                result = self.api_client.login(username, password)
            
            self.token = result.get('token')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Authentication failed: {str(e)}')

