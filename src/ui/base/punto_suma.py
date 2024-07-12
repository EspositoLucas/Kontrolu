import os
from .macro_vista import MacroVista
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class PuntoSuma(MacroVista):
    def __init__(self, parent=None):
        super(PuntoSuma, self).__init__(parent, QtCore.QRect(140, 206, 51, 51))
        self.setText("")
        self.setDisabled(True)
        self.setStyleSheet("background-color: transparent;")

        path = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(path, 'imgs', 'puntoSuma.png')
        self.pixmap = QtGui.QPixmap(self.image_path)
        
        if self.pixmap.isNull():
            print(f"Error al cargar la imagen: {self.image_path}")
        else:
            self.pixmap = self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    def paintEvent(self, event):
        if not self.pixmap.isNull():
            painter = QtGui.QPainter(self)
            painter.drawPixmap(self.rect(), self.pixmap)

        