from .macros.macro_actuador import MacroActuador
from .macros.macro_controlador import MacroControlador
from .macros.macro_medidor import MacroMedidor
from .macros.macro_proceso import MacroProceso
from .macros.macro_punto_suma import MacroPuntoSuma
from .topologia.topologia_serie import MicroBloque
from .topologia.carga import Carga
class Sesion():
    def __init__(self):
        self.entrada = MicroBloque(nombre="Entrada")
        self.controlador = MacroControlador(sesion=self)
        self.actuador = MacroActuador(sesion=self)
        self.proceso = MacroProceso(sesion=self)
        self.medidor = MacroMedidor(sesion=self)
        self.punto_suma = MacroPuntoSuma()
        self.carga = Carga()
    
    def validar_entrada_controlador(self, unidad: str)-> bool:
        return self.medidor.unidad_salida() == unidad
    def validar_salida_controlador(self, unidad: str)-> bool:
        return self.actuador.unidad_entrada() == unidad
    
    def validar_entrada_actuador(self, unidad: str)-> bool:
        return self.controlador.unidad_salida() == unidad
    def validar_salida_actuador(self, unidad: str)-> bool:
        return self.proceso.unidad_entrada() == unidad
    
    def validar_entrada_proceso(self, unidad: str)-> bool:
        return self.actuador.unidad_salida() == unidad
    def validar_salida_proceso(self, unidad: str)-> bool:
        return self.medidor.unidad_entrada() == unidad
    
    def validar_entrada_medidor(self, unidad: str)-> bool:
        return self.proceso.unidad_salida() == unidad
    def validar_salida_medidor(self, unidad: str)-> bool:
        return self.controlador.unidad_entrada() == unidad
    
    def proxima_salida_controlador(self)-> str:
        return self.medidor.unidad_salida()
    def proxima_salida_actuador(self)-> str:
        return self.controlador.unidad_salida()
    def proxima_salida_proceso(self)-> str:
        return self.actuador.unidad_salida()
    def proxima_salida_medidor(self)-> str:
        return self.proceso.unidad_salida()
    
    def proxima_entrada_controlador(self)-> str:
        return self.actuador.unidad_entrada()
    def proxima_entrada_actuador(self)-> str:
        return self.proceso.unidad_entrada()
    def proxima_entrada_proceso(self)-> str:
        return self.medidor.unidad_entrada()
    def proxima_entrada_medidor(self)-> str:
        return self.controlador.unidad_entrada()
    
