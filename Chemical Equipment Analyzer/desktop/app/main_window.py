from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QMessageBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

from .login_dialog import LoginDialog
from .api_client import APIClient
from .history_widget import HistoryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_data = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Analyzer')
        self.setGeometry(100, 100, 1200, 800)
        
        # Check if authenticated
        if not self.api_client.token:
            self.show_login()
            return
        
        self.setup_main_ui()
    
    def setup_main_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Header
        header = QHBoxLayout()
        title = QLabel('Chemical Equipment Analyzer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        
        layout.addLayout(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_upload_tab(), 'Upload CSV')
        self.tabs.addTab(self.create_visualization_tab(), 'Visualization')
        self.tabs.addTab(HistoryWidget(self.api_client, self.on_view_history_item), 'History')
        
        layout.addWidget(self.tabs)
    
    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        info_label = QLabel(
            'Upload a CSV file containing columns: Equipment Name, Type, Flowrate, Pressure, Temperature'
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        upload_btn = QPushButton('Select CSV File')
        upload_btn.setMinimumHeight(50)
        upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(upload_btn)
        
        layout.addStretch()
        return widget
    
    def create_visualization_tab(self):
        widget = QWidget()
        self.viz_layout = QVBoxLayout()
        widget.setLayout(self.viz_layout)
        
        placeholder = QLabel('Upload a CSV file to see visualization')
        placeholder.setAlignment(Qt.AlignCenter)
        self.viz_layout.addWidget(placeholder)
        
        return widget
    
    def show_login(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == LoginDialog.Accepted:
            self.api_client.set_token(dialog.token)
            self.setup_main_ui()
        else:
            self.close()
    
    def logout(self):
        self.api_client.set_token(None)
        self.show_login()
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if not file_path:
            return
        
        try:
            data = self.api_client.upload_csv(file_path)
            self.current_data = data
            self.update_visualization(data)
            self.tabs.setCurrentIndex(1)  # Switch to visualization tab
            
            # Refresh history tab
            history_widget = self.tabs.widget(2)
            if isinstance(history_widget, HistoryWidget):
                history_widget.refresh_history()
            
            QMessageBox.information(self, 'Success', 'File uploaded and analyzed successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to upload file: {str(e)}')
    
    def on_view_history_item(self, item):
        """Called when user clicks on a history item"""
        try:
            data = self.api_client.get_summary(item['id'])
            self.current_data = data
            self.update_visualization(data)
            self.tabs.setCurrentIndex(1)  # Switch to visualization tab
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load summary: {str(e)}')
    
    def update_visualization(self, data):
        """Update visualization tab with data"""
        # Clear existing widgets
        for i in reversed(range(self.viz_layout.count())):
            self.viz_layout.itemAt(i).widget().setParent(None)
        
        # Stats cards
        stats_group = QGroupBox('Summary Statistics')
        stats_layout = QGridLayout()
        
        stats_data = [
            ('Total Equipment', str(data['total_equipment_count'])),
            ('Avg Flowrate', f"{data['avg_flowrate']:.2f}"),
            ('Avg Pressure', f"{data['avg_pressure']:.2f}"),
            ('Avg Temperature', f"{data['avg_temperature']:.2f}"),
        ]
        
        for i, (label, value) in enumerate(stats_data):
            label_widget = QLabel(f'<b>{label}:</b>')
            value_widget = QLabel(value)
            stats_layout.addWidget(label_widget, i // 2, (i % 2) * 2)
            stats_layout.addWidget(value_widget, i // 2, (i % 2) * 2 + 1)
        
        stats_group.setLayout(stats_layout)
        self.viz_layout.addWidget(stats_group)
        
        # Average values chart
        avg_fig = Figure(figsize=(8, 4))
        avg_canvas = FigureCanvas(avg_fig)
        ax = avg_fig.add_subplot(111)
        
        categories = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            data['avg_flowrate'],
            data['avg_pressure'],
            data['avg_temperature']
        ]
        
        bars = ax.bar(categories, values, color=['#667eea', '#764ba2', '#ff6384'])
        ax.set_ylabel('Average Value')
        ax.set_title('Average Values')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}', ha='center', va='bottom')
        
        avg_fig.tight_layout()
        self.viz_layout.addWidget(avg_canvas)
        
        # Equipment type distribution chart
        type_dist = data.get('equipment_type_distribution', {})
        if type_dist:
            dist_fig = Figure(figsize=(8, 6))
            dist_canvas = FigureCanvas(dist_fig)
            ax2 = dist_fig.add_subplot(111)
            
            types = list(type_dist.keys())
            counts = list(type_dist.values())
            
            ax2.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Equipment Type Distribution')
            
            dist_fig.tight_layout()
            self.viz_layout.addWidget(dist_canvas)
        
        # Data table
        if 'raw_data' in data and data['raw_data']:
            table_group = QGroupBox('Data Table (First 100 rows)')
            table_layout = QVBoxLayout()
            
            table = QTableWidget()
            table.setRowCount(len(data['raw_data']))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels([
                'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
            ])
            
            for i, row in enumerate(data['raw_data']):
                table.setItem(i, 0, QTableWidgetItem(str(row.get('Equipment Name', ''))))
                table.setItem(i, 1, QTableWidgetItem(str(row.get('Type', ''))))
                table.setItem(i, 2, QTableWidgetItem(str(row.get('Flowrate', ''))))
                table.setItem(i, 3, QTableWidgetItem(str(row.get('Pressure', ''))))
                table.setItem(i, 4, QTableWidgetItem(str(row.get('Temperature', ''))))
            
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_layout.addWidget(table)
            table_group.setLayout(table_layout)
            self.viz_layout.addWidget(table_group)
        
        # Download PDF button
        download_btn = QPushButton('Download PDF Report')
        download_btn.clicked.connect(lambda: self.download_pdf(data['id']))
        self.viz_layout.addWidget(download_btn)
        
        self.viz_layout.addStretch()
    
    def download_pdf(self, summary_id):
        """Download PDF report"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save PDF Report', f'report_{summary_id}.pdf', 'PDF Files (*.pdf)'
        )
        
        if not file_path:
            return
        
        try:
            self.api_client.download_pdf(summary_id, file_path)
            QMessageBox.information(self, 'Success', f'PDF report saved to {file_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download PDF: {str(e)}')

