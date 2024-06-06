from .macro_vista import MacroVista

class ElementoCorreccion(MacroVista):
    def __init__(self,actuador):
        MacroVista.__init__(self,(200, 50),(300, 100),actuador)