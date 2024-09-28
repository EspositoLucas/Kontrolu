from .macro_vista import MacroVista
from PyQt5 import QtCore
class ElementoControl(MacroVista):
    def __init__(self, controlador):
        MacroVista.__init__(self, controlador,(220, 210),(121, 41))

    # TODO: Agregar funcionalidad propia del elemento "Control" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)    
