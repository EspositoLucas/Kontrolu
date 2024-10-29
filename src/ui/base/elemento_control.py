from .macro_vista import MacroVista
from PyQt5.QtCore import QRectF
class ElementoControl(MacroVista):
    def __init__(self, controlador,pos,padre):
        MacroVista.__init__(self, controlador,pos,padre)

    # TODO: Agregar funcionalidad propia del elemento "Control" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)    
