from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtGui import QFont

from .archivo import Archivo

class Menu(QMenuBar):
    def __init__(self,main_window):
        super().__init__(main_window)
        self.setup(main_window)
    
    def setup(self,main_window):
        archivo = Archivo(main_window)
        self.addMenu(archivo)

        self.setStyleSheet("""
            QMenuBar {
                background-color: #333;
                color: white;
                font-size: 14px;
            }
            
            QMenuBar::item {
                padding: 4px 10px;
                background-color: #555;
                border-radius: 3px;
            }
            
            QMenuBar::item:selected {
                background-color: #666;
            }
            
            QMenu {
                background-color: #555;
                border: 1px solid #777;
            }
            
            QMenu::item {
                padding: 8px 20px;
            }
            
            QMenu::item:selected {
                background-color: #666;
            }
        """)
        
        font = QFont("Arial", 12)
        self.setFont(font)
