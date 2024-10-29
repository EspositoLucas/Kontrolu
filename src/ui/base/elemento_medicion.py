from .macro_vista import MacroVista
from PyQt5.QtCore import QRectF

class ElementoMedicion(MacroVista):
    def __init__(self, medicion,pos,padre):
        MacroVista.__init__(self, medicion, pos,padre)

    # TODO: Agregar funcionalidad propia del elemento "Medicion" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
