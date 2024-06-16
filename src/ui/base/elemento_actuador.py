from .macro_vista import MacroVista
from PyQt5 import QtCore

class ElementoActuador(MacroVista):
    def __init__(self, actuador):
        MacroVista.__init__(self, actuador, QtCore.QRect(370, 210, 121, 41))
    
    # TODO: Agregar funcionalidad propia del elemento "Actuador" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
