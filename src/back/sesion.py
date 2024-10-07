from .macros.macro_actuador import MacroActuador
from .macros.macro_controlador import MacroControlador
from .macros.macro_medidor import MacroMedidor
from .macros.macro_proceso import MacroProceso
from .macros.macro_punto_suma import MacroPuntoSuma
from back.topologia.microbloque import MicroBloque
from .topologia.carga import Carga
from .json_manager import json_manager
import json

class Sesion():
    def __init__(self):
        self.entrada = MicroBloque(nombre="Entrada")
        self.controlador = MacroControlador(sesion=self)
        self.actuador = MacroActuador(sesion=self)
        self.proceso = MacroProceso(sesion=self)
        self.medidor = MacroMedidor(sesion=self)
        self.punto_suma = MacroPuntoSuma()
        self.carga = Carga(entrada=self.entrada)
        self.nombre = "Sistema de Control"
    
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
    
    def unidad_recibida_controlador(self)-> str:
        return self.medidor.unidad_salida()
    def unidad_recibida_actuador(self)-> str:
        return self.controlador.unidad_salida()
    def unidad_recibida_proceso(self)-> str:
        return self.actuador.unidad_salida()
    def unidad_recibida_medidor(self)-> str:
        return self.proceso.unidad_salida()
    
    def unidad_esperada_controlador(self)-> str:
        return self.actuador.unidad_entrada()
    def unidad_esperada_actuador(self)-> str:
        return self.proceso.unidad_entrada()
    def unidad_esperada_proceso(self)-> str:
        return self.medidor.unidad_entrada()
    def unidad_esperada_medidor(self)-> str:
        return self.controlador.unidad_entrada()
    
    def to_json(self) -> str:
        return {
            "entrada": self.entrada.to_json(),
            "controlador": self.controlador.to_json(),
            "actuador": self.actuador.to_json(),
            "proceso": self.proceso.to_json(),
            "medidor": self.medidor.to_json(),
            "carga": self.carga.to_json(),
            "nombre": self.nombre
        }
    
    def from_json(self, datos: str):
        datos = json.loads(datos)
        self.entrada = MicroBloque.from_json(datos["entrada"])
        self.controlador = MacroControlador.from_json(datos["controlador"])
        self.actuador = MacroActuador.from_json(datos["actuador"])
        self.proceso = MacroProceso.from_json(datos["proceso"])
        self.medidor = MacroMedidor.from_json(datos["medidor"])
        self.carga = Carga.from_json(datos["carga"])
        self.nombre = datos["nombre"]