from enum import Enum
from typing import Union, Callable

class TipoConfiguracion(Enum):
    NUMERICA = 1
    BOOLEANA = 2
    ENUMERADA = 3
    FUNCION = 4

class EfectoConfiguracion(Enum):
    DIRECTO = 1
    INDIRECTO = 2

class Configuracion:
    def __init__(self, nombre, tipo, valor_por_defecto, efecto, valores_posibles, funcion_efecto):
        self.nombre = nombre
        self.tipo = tipo 
        self.efecto = efecto
        self.valor = valor_por_defecto
        self.valores_posibles = valores_posibles
        self.funcion_efecto = funcion_efecto
    
    def set_valor(self, valor):
        self.valor = valor

    def set_efecto(self, efecto):
        self.efecto = efecto
    
    def set_funcion_efecto(self, funcion):
        self.funcion_efecto = funcion
    
    def aplicar_efecto(self, funcion_transferencia):
        if self.efecto == EfectoConfiguracion.DIRECTO:
            if self.tipo == TipoConfiguracion.FUNCION:
                return f"({self.funcion_efecto}) * ({funcion_transferencia})"
            elif self.tipo == TipoConfiguracion.NUMERICA:
                return f"({self.valor}) * ({funcion_transferencia})"
            
        else:
            # TODO: Aplicar efecto indirecto
            pass
