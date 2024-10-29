from .macro_vista import MacroVista
from PyQt5.QtCore import QRectF

class ElementoActuador(MacroVista):
    def __init__(self, actuador,pos,padre):
        #MacroVista.__init__(self, actuador, 355.5,210)
        MacroVista.__init__(self, actuador, pos,padre)
    
    # TODO: Agregar funcionalidad propia del elemento "Actuador" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
