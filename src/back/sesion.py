from .macros.macro_actuador import MacroActuador
from .macros.macro_controlador import MacroControlador
from .macros.macro_medidor import MacroMedidor
from .macros.macro_proceso import MacroProceso

class Sesion():
    def __init__(self):
        self.controlador = MacroActuador()
        self.actuador = MacroActuador()
        self.proceso = MacroProceso()
        self.mediciones = MacroMedidor()
    