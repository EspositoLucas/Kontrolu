from .macro_vista import MacroVista
from PyQt5 import QtCore

class ElementoMedicion(MacroVista):
    def __init__(self, medicion):
        MacroVista.__init__(self, medicion, QtCore.QRect(270, 280, 121, 41))
