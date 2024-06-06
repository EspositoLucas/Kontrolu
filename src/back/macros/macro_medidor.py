from .macro_bloque import MacroBloque

class MacroMedidor(MacroBloque):
    def __init__(self):
        super().__init__()
        self.nombre = "Medidor"