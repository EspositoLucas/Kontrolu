from dataclasses import dataclass

@dataclass
class MicroBloqueDto:
    nombre: str
    descripcion: str
    fdt: str
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
    unidad_entrada: str
    unidad_salida: str

@dataclass
class TipoMicroBloqueDto:
    nombre_tipo: str
    descripcion_tipo: str
    micro_bloques : list[MicroBloqueDto]

@dataclass
class DominioDto:
    nombre: str
    tipos : list[TipoMicroBloqueDto]


