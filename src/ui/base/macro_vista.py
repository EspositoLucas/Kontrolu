
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow

class MacroVista(QPushButton):
    def __init__(self, elementoBack, geometria):
        super().__init__()
        self.modelo = elementoBack
        self.setText(self.modelo.nombre)
        self.setGeometry(geometria)
        self.setCheckable(True)
        self.clicked.connect(self.click) # Conecta el evento click con el método click
    
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        self.ventana.setGeometry(0, 0, 600, 600)
        self.ventana.show()