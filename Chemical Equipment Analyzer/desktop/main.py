import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from app.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application properties
    app.setApplicationName("Chemical Equipment Analyzer")
    app.setOrganizationName("Equipment Analyzer")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

