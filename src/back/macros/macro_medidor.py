from .macro_bloque import MacroBloque
import numpy as np

class MacroMedidor(MacroBloque):
    def __init__(self):
        super().__init__()
        self.nombre = "Medidor"
        self.precision = 0.1
        self.ruido = 0.005
        
        
    def medir(self, valor_real):
        # Simula una medición con cierta precisión y ruido
        error = np.random.normal(0, self.precision)
        ruido = np.random.normal(0, self.ruido)
        return valor_real + error + ruido