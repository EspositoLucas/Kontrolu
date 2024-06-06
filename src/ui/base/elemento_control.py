from .macro_vista import MacroVista
class ElementoControl(MacroVista):
    def __init__(self, controlador):
        MacroVista.__init__(self,(50, 50),(150, 100),controlador)
