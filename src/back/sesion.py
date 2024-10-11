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
        self.nueva_sesion()
    
    def nueva_sesion(self):
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
    
    def from_json(self, datos: dict):
        self.entrada = MicroBloque(from_json = datos["entrada"])
        self.controlador = MacroControlador(from_json = datos["controlador"])
        self.controlador.sesion = self
        self.actuador = MacroActuador(from_json = datos["actuador"])
        self.actuador.sesion = self
        self.proceso = MacroProceso(from_json = datos["proceso"])
        self.proceso.sesion = self
        self.medidor = MacroMedidor(from_json = datos["medidor"])
        self.medidor.sesion = self
        self.carga = Carga(from_json = datos["carga"])
        self.carga.entrada = self.entrada
        self.nombre = datos["nombre"]

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["entrada", "controlador", "actuador", "proceso", "medidor", "carga", "nombre"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")
        
        if not isinstance(datos["nombre"], str):
            raise Exception("El nombre de la sesión debe ser un string")
        

        try:
            MicroBloque.validar_dict(datos["entrada"])
        except Exception as e:
            raise Exception(f"Error en la entrada: {e}")
        
        try:
            MacroControlador.validar_dict(datos["controlador"])
        except Exception as e:
            raise Exception(f"Error en el controlador: {e}")
        
        try:
            MacroActuador.validar_dict(datos["actuador"])
        except Exception as e:
            raise Exception(f"Error en el actuador: {e}")
        
        try:
            MacroProceso.validar_dict(datos["proceso"])
        except Exception as e:
            raise Exception(f"Error en el proceso: {e}")
        
        try:
            MacroMedidor.validar_dict(datos["medidor"])
        except Exception as e:
            raise Exception(f"Error en el medidor: {e}")

        try:   
            Carga.validar_dict(datos["carga"])
        except Exception as e:
            raise Exception(f"Error en la carga: {e}")
        
        return True