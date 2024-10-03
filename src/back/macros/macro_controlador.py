from .macro_bloque import MacroBloque
from .tipos_macro import MACROS


class MacroControlador(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Controlador",sesion=sesion, tipo=MACROS.CONTROLADOR)

    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_controlador(unidad)
    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_controlador(unidad)
    
    def unidad_saliente(self)-> str:
        return self.sesion.unidad_esperada_controlador()
    
    def unidad_entrante(self)-> str:
        return self.sesion.unidad_recibida_controlador()