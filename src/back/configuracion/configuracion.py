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
    def __init__(self, nombre, tipo, valor_por_defecto, efecto):
        self.nombre = nombre
        self.tipo = tipo 
        self.efecto = efecto
        self.set_valor(valor_por_defecto, efecto)
    
    def get_valor(self):
        if self.tipo == TipoConfiguracion.NUMERICA:
            return self.valor
        elif self.tipo == TipoConfiguracion.BOOLEANA:
            pass
        elif self.tipo == TipoConfiguracion.ENUMERADA:
            return self.valores_posibles
        elif self.tipo == TipoConfiguracion.FUNCION:
            return self.funcion_efecto, self.efecto

    def set_valor(self, valor=None, efecto=None): 
        if self.tipo == TipoConfiguracion.NUMERICA:
            self.valor = valor
        elif self.tipo == TipoConfiguracion.BOOLEANA:
            pass
        elif self.tipo == TipoConfiguracion.ENUMERADA:
            self.valores_posibles = valor
        elif self.tipo == TipoConfiguracion.FUNCION:
            self.funcion_efecto = valor
            self.efecto = efecto

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
            elif self.tipo == TipoConfiguracion.BOOLEANA:
                return f"({funcion_transferencia})" if self.valor else "0"
            elif self.tipo == TipoConfiguracion.ENUMERADA:
                return f"({self.valores_posibles[self.valor]}) * ({funcion_transferencia})"
        else:
            if self.efecto:
                return f"limitar({funcion_transferencia}, {self.funcion_efecto(self.valor)})"
            if self.tipo == TipoConfiguracion.NUMERICA:
                return f"limitar({funcion_transferencia}, {self.valor})"
        return funcion_transferencia
    
    def actualizar_configuracion(self, nombre_nuevo, tipo_nuevo, valor_nuevo, efecto_nuevo):
        self.nombre = nombre_nuevo
        self.tipo = tipo_nuevo
        self.set_valor(valor_nuevo, efecto_nuevo)



