from .macro_bloque import MacroBloque
from .tipos_macro import MACROS


class MacroProceso(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Proceso",sesion=sesion, tipo=MACROS.PROCESO)
    
    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_proceso(unidad)
    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_proceso(unidad)
    
    def unidad_saliente(self)-> str:
        return self.sesion.unidad_esperada_proceso()
    
    def unidad_entrante(self)-> str:   
        return self.sesion.unidad_recibida_proceso()