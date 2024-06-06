from .macro_bloque import MacroBloque

class MacroProceso(MacroBloque):
    def __init__(self):
        super().__init__()
        self.nombre = "Proceso"