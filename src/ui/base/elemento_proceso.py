from .macro_vista import MacroVista
from PyQt5 import QtCore

class ElementoProceso(MacroVista):
    def __init__(self, medidor):
        MacroVista.__init__(self, medidor, QtCore.QRect(420, 210, 121, 41))
