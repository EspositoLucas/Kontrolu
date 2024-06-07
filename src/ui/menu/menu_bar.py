from PyQt5.QtWidgets import QMenuBar

from .archivo import Archivo

class Menu(QMenuBar):
    def __init__(self,main_window):
        super().__init__(main_window)
        self.setup(main_window)
    
    def setup(self,main_window):
        archivo = Archivo(main_window)
        self.addMenu(archivo)

