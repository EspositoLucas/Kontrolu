from .macro_vista import MacroVista

class ElementoMedicion(MacroVista):
    def __init__(self,medidor):
        MacroVista.__init__(self,(500, 50), (600, 100),medidor)