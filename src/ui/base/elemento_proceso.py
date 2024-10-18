from .macro_vista import MacroVista
from PyQt5.QtCore import Qt, QRectF

class ElementoProceso(MacroVista):
    def __init__(self, medidor,pos):
        MacroVista.__init__(self, medidor,pos)

    # TODO: Agregar funcionalidad propia del elemento "Proceso" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
