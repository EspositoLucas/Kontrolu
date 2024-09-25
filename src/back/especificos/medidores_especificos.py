from dataclasses import dataclass
from enum import Enum


class Ambito(Enum):
    SISTEMAS = "Sistemas"
    ELECTRONICA = "Electronica"

class Tipo(Enum):
    ENTRADA = "Entrada"
    CONTROLADOR = "Controlador"
    PROCESO = "Proceso"
    ACTUADOR = "Actuador"
    MEDIDOR = "Medidor"
    CARGA = "Carga"

@dataclass
class MicroBloqueDto:
    nombre: str
    descripcion: str
    fdt: str
    ambito: Ambito
    tipo: Tipo
    entrada_limite_inferior: float
    entrada_limite_superior: float
    entrada_limite_por_ciclo: float
    entrada_error_maximo: float
    entrada_proporcion: float
    entrada_tipo: str
    entrada_ultimo_valor: float
    entrada_propabilidad: float
    salida_limite_inferior: float
    salida_limite_superior: float
    salida_limite_por_ciclo: float
    salida_error_maximo: float
    salida_proporcion: float
    salida_tipo: str
    salida_ultimo_valor: float
    salida_propabilidad: float




