from .macro_vista import MacroVista
from PyQt5 import QtCore
class ElementoControl(MacroVista):
    def __init__(self, controlador):
        MacroVista.__init__(self, controlador, QtCore.QRect(120, 210, 121, 41))
