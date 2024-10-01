from .macro_bloque import MacroBloque

class MacroProceso(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Proceso",sesion=sesion)
    
    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_proceso(unidad)
    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_proceso(unidad)
    
    def proxima_salida(self)-> str:
        return self.sesion.proxima_salida_proceso()
    
    def proxima_entrada(self)-> str:   
        return self.sesion.proxima_entrada_proceso()