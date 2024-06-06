from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint

class MacroVista(QPushButton):
    def __init__(self, start, end, modelo):
        super().__init__(modelo.nombre)
        self.modelo = modelo
        self.start = QPoint(*start)
        self.end = QPoint(*end)
        self.move(self.start)  # Mueve el botón a la posición especificada por start
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #000000; border-radius: 5px;")
        self.draw()
        self.clicked.connect(self.accion)

    def accion(self):
        print("boton apretado")

    def draw(self):
        self.show()
