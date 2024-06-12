from .macro_vista import MacroVista
from PyQt5 import QtCore

class ElementoMedicion(MacroVista):
    def __init__(self, medicion):
        MacroVista.__init__(self, medicion, QtCore.QRect(370, 280, 121, 41))
