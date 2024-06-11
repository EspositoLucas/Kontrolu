from .macro_vista import MacroVista
class ElementoControl(MacroVista):
    def __init__(self, controlador, main_window):
        super().__init__(120, 210,controlador,main_window)
