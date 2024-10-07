from .macro_bloque import MacroBloque
from .tipos_macro import MACROS

class MacroActuador(MacroBloque):
    def __init__(self,sesion=None,from_json=None) -> None:
        if from_json:
            super().__init__(from_json=from_json)
            return
        super().__init__(nombre="Actuador",sesion=sesion, tipo=MACROS.ACTUADOR)

    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_actuador(unidad)

    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_actuador(unidad) 
    
    def unidad_saliente(self)-> str:
        print("Unidad esperada en actuador: ", self.sesion.unidad_esperada_actuador())
        return self.sesion.unidad_esperada_actuador() 
    
    def unidad_entrante(self)-> str:
        print("Unidad recibida en actuador: ", self.sesion.unidad_recibida_actuador())
        return self.sesion.unidad_recibida_actuador()