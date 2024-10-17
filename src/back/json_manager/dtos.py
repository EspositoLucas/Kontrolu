from dataclasses import dataclass
from typing import Optional

@dataclass
class MicroBloqueDto:
    nombre: str = None
    descripcion: str = None
    fdt: str = None
    entrada_limite_inferior: Optional[float] = None
    entrada_limite_superior: Optional[float] = None
    entrada_limite_por_ciclo: Optional[float] = None
    entrada_error_maximo: Optional[float] = None
    entrada_proporcion: Optional[float] = None
    entrada_tipo: Optional[str] = None
    entrada_ultimo_valor: Optional[float] = None
    entrada_propabilidad: Optional[float] = None
    salida_limite_inferior: Optional[float] = None
    salida_limite_superior: Optional[float] = None
    salida_limite_por_ciclo: Optional[float] = None
    salida_error_maximo: Optional[float] = None
    salida_proporcion: Optional[float] = None
    salida_tipo: Optional[str] = None
    salida_ultimo_valor: Optional[float] = None
    salida_propabilidad: Optional[float] = None
    unidad_entrada: str = None
    unidad_salida: str = None

@dataclass
class TipoMicroBloqueDto:
    nombre_tipo: str
    descripcion_tipo: str
    micro_bloques : list[MicroBloqueDto]

@dataclass
class DominioDto:
    nombre: str
    tipos : list[TipoMicroBloqueDto]


