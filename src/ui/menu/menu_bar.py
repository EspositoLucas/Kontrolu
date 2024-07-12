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
                padding: 5px 5px;  /* Ajustar el relleno para cambiar el ancho */
            }
            
            QMenuBar::item {
                padding: 5px;
                background-color: #555;
                border-radius: 3px;
            }      
        """)
        
        font = QFont("Arial", 12)
        self.setFont(font)
