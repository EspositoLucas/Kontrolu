from .macro_bloque import MacroBloque

class MacroMedidor(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Medidor",sesion=sesion)

    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_medidor(unidad)
    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_medidor(unidad)
    
    def proxima_salida(self)-> str:
        return self.sesion.proxima_salida_medidor()
    
    def proxima_entrada(self)-> str:    
        return self.sesion.proxima_entrada_medidor()