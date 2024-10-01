from .macro_bloque import MacroBloque

class MacroControlador(MacroBloque):
    def __init__(self,sesion=None) -> None:
        super().__init__(nombre="Controlador",sesion=sesion)

    def validar_entrada(self, unidad: str)-> bool:
        return self.sesion.validar_entrada_controlador(unidad)
    def validar_salida(self, unidad: str)-> bool:
        return self.sesion.validar_salida_controlador(unidad)
    
    def proxima_salida(self)-> str:
        return self.sesion.proxima_salida_controlador()
    
    def proxima_entrada(self)-> str:
        return self.sesion.proxima_entrada_controlador()