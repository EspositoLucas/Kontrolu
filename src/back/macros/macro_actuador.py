from .macro_bloque import MacroBloque

class MacroActuador(MacroBloque):
    def __init__(self):
        super().__init__()
        self.nombre = "Actuador"