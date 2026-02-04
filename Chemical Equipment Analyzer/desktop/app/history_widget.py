from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from datetime import datetime


class HistoryWidget(QWidget):
    def __init__(self, api_client, on_view_item_callback):
        super().__init__()
        self.api_client = api_client
        self.on_view_item = on_view_item_callback
        self.init_ui()
        self.refresh_history()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QHBoxLayout()
        title = QLabel('Upload History (Last 5)')
        title.setStyleSheet('font-size: 16px; font-weight: bold;')
        header.addWidget(title)
        header.addStretch()
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.refresh_history)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.history_list)
    
    def refresh_history(self):
        """Load and display history"""
        self.history_list.clear()
        
        try:
            history = self.api_client.get_history()
            
            if not history:
                item = QListWidgetItem('No uploads yet. Upload a CSV file to get started.')
                item.setFlags(Qt.NoItemFlags)
                self.history_list.addItem(item)
                return
            
            for item_data in history:
                item_text = self.format_history_item(item_data)
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, item_data)
                self.history_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history: {str(e)}')
    
    def format_history_item(self, item_data):
        """Format history item for display"""
        filename = item_data.get('filename', 'Unknown')
        uploaded_at = item_data.get('uploaded_at', '')
        
        try:
            dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_date = uploaded_at
        
        count = item_data.get('total_equipment_count', 0)
        avg_flow = item_data.get('avg_flowrate', 0)
        avg_press = item_data.get('avg_pressure', 0)
        avg_temp = item_data.get('avg_temperature', 0)
        
        return (
            f"{filename}\n"
            f"Uploaded: {formatted_date} | "
            f"Count: {count} | "
            f"Avg Flowrate: {avg_flow:.2f} | "
            f"Avg Pressure: {avg_press:.2f} | "
            f"Avg Temperature: {avg_temp:.2f}"
        )
    
    def on_item_double_clicked(self, item):
        """Handle double-click on history item"""
        item_data = item.data(Qt.UserRole)
        if item_data:
            self.on_view_item(item_data)
    
    def download_pdf_for_item(self, item_data):
        """Download PDF for a history item"""
        summary_id = item_data.get('id')
        if not summary_id:
            return
        
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

