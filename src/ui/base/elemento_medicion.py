from .macro_vista import MacroVista

class ElementoMedicion(MacroVista):
    def __init__(self,medidor,main_window):
        super().__init__(270, 280,medidor,main_window)