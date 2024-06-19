import os
from .macro_vista import MacroVista
from PyQt5 import QtCore, QtGui, QtWidgets

class PuntoSuma(MacroVista):
    def __init__(self, puntoSuma):
        MacroVista.__init__(self, puntoSuma, QtCore.QRect(140, 205, 51, 51))
        self.setText("") # el punto suma no tiene texto
        self.setDisabled(True) # el punto suma no se puede apretar
        self.setStyleSheet("background-color: transparent;") # Establecer fondo transparente

        # ICONO
        icon = QtGui.QIcon()
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'puntoSuma.png')
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(51, 51)) # Ajustar el tamaño del icono al tamaño del botón