from .macro_vista import MacroVista

class ElementoCorreccion(MacroVista):
    def __init__(self,actuador,main_window):
        super().__init__(270, 210,actuador,main_window)