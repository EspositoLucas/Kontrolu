from .macro_vista import MacroVista

class Proceso(MacroVista):
    def __init__(self,medidor):
        MacroVista.__init__(self,(350, 50), (450, 100),medidor)
