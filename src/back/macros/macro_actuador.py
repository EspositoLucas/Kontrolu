from .macro_bloque import MacroBloque
from .tipos_macro import MACROS

class MacroActuador(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Actuador",sesion=sesion, tipo=MACROS.ACTUADOR)

    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_actuador(unidad)

    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_actuador(unidad) 
    
    def proxima_salida(self)-> str:
        return self.sesion.proxima_salida_actuador() 
    
    def proxima_entrada(self)-> str:
        return self.sesion.proxima_entrada_actuador()