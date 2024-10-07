import numpy as np
from math import inf
from enum import Enum

class TipoError(Enum):
    GAUSS = "gauss"
    ALEATORIO = "aleatorio"
    PROPORCIONAL = "proporcional"
    NINGUNO = "ninguno"

class Configuracion:
    def __init__(self, nombre="Configuracion", limite_inferior=-inf, limite_superior=inf, limite_por_ciclo=inf, error_maximo=inf, proporcion=0, tipo=TipoError.NINGUNO, ultimo_valor=0, probabilidad=0, unidad="V",from_json=None):
        if from_json:
            self.from_json(from_json)
            return
        self.unidad = unidad
        self.nombre = nombre
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.limite_por_ciclo = limite_por_ciclo
        self.error_maximo = error_maximo
        self.proporcion = proporcion
        self.tipo = tipo 
        self.ultimo_valor = ultimo_valor
        self.probabilidad = probabilidad
        self.datos = {'tiempo': [], 'valor_original': [], 'error_base': [], 'error_limite': [], 'error_total': [], 'resultado': []}
    
    def calcular_error(self, valor):
        if np.random.uniform(0, 1) < self.probabilidad:
            return 0

        if self.tipo == TipoError.GAUSS:
            error = np.random.normal(0, valor * self.proporcion)
        elif self.tipo == TipoError.ALEATORIO:
            error = np.random.uniform(-valor * self.proporcion, valor * self.proporcion)
        elif self.tipo == TipoError.PROPORCIONAL:
            error = valor * self.proporcion
        else:
            error = 0
        
        return max(min(error, self.error_maximo), -self.error_maximo)
    
    def calcular_limite(self, valor):
        if self.limite_por_ciclo:
            ultimo = self.ultimo_valor
            diferencia = valor - ultimo
            delta_real = max(min(diferencia, self.limite_por_ciclo), -self.limite_por_ciclo)
            posible = ultimo + delta_real
        else:
            posible = valor

        return min(max(posible, self.limite_inferior), self.limite_superior)
    
    def borrar_configuraciones(self):
        self.nombre = "Configuracion"
        self.limite_inferior = -inf
        self.limite_superior = inf
        self.limite_por_ciclo = inf
        self.error_maximo = inf
        self.proporcion = 0
        self.tipo = TipoError.NINGUNO
        self.ultimo_valor = 0
    
    def default_limite_inferior(self):
        self.limite_inferior = -inf
    
    def default_limite_superior(self):
        self.limite_superior = inf
    
    def default_limite_por_ciclo(self):
        self.limite_por_ciclo = inf
    
    def default_error_maximo(self):
        self.error_maximo = inf
    
    def default_proporcion(self):
        self.proporcion = 0
    
    def default_tipo(self):
        self.tipo = TipoError.NINGUNO
    
    def default_ultimo_valor(self):
        self.ultimo_valor = 0

    def default_probabilidad(self):
        self.probabilidad = 0
    
    def set_limite_inferior(self, valor):
        self.limite_inferior = valor
        if valor is None:
            self.limite_inferior = -inf
    
    def set_limite_superior(self, valor):
        self.limite_superior = valor
        if valor is None:
            self.limite_superior = inf
    
    def set_limite_por_ciclo(self, valor):
        self.limite_por_ciclo = valor
        if valor is None:
            self.limite_por_ciclo = inf
    
    def set_error_maximo(self, valor):
        self.error_maximo = valor
        if valor is None:
            self.error_maximo = inf
    
    def set_proporcion(self, valor):
        self.proporcion = valor
        if valor is None:
            self.proporcion = 0
    
    def set_tipo(self, valor):
        self.tipo = valor
        if valor is None:
            self.tipo = TipoError.NINGUNO
    
    def set_ultimo_valor(self, valor):
        self.ultimo_valor = valor
        if valor is None:
            self.ultimo_valor = 0

    def es_default_limite_inferior(self):
        return self.limite_inferior == -inf
    
    def es_default_limite_superior(self):
        return self.limite_superior == inf
    
    def es_default_limite_por_ciclo(self):
        return self.limite_por_ciclo == inf
    
    def es_default_error_maximo(self):
        return self.error_maximo == inf
    
    def es_default_proporcion(self):
        return self.proporcion == 0
    
    def es_default_tipo(self):
        return self.tipo == TipoError.NINGUNO
    
    def es_default_ultimo_valor(self):
        return self.ultimo_valor == 0
    
    def es_default_probabilidad(self):
        return self.probabilidad == 0
    
    def actualizar(self, valor, tiempo):
        error = self.calcular_error(valor)
        nuevo = self.calcular_limite(valor + error)
        self.ultimo_valor = nuevo
        self.datos['tiempo'].append(tiempo)
        self.datos['valor_original'].append(valor)
        self.datos['error_base'].append(error)
        self.datos['error_limite'].append(nuevo - valor + error)
        self.datos['error_total'].append(nuevo - valor)
        self.datos['resultado'].append(nuevo)
        return nuevo
    
    def to_json(self):
        return {
            "limite_inferior": self.limite_inferior if not self.es_default_limite_inferior() else "default",
            "limite_superior": self.limite_superior if not self.es_default_limite_superior() else "default",
            "limite_por_ciclo": self.limite_por_ciclo if not self.es_default_limite_por_ciclo() else "default",
            "error_maximo": self.error_maximo if not self.es_default_error_maximo() else "default",
            "proporcion": self.proporcion if not self.es_default_proporcion() else "default",
            "tipo": self.tipo.value if not self.es_default_tipo() else "default",
            "ultimo_valor": self.ultimo_valor if not self.es_default_ultimo_valor() else "default",
            "probabilidad": self.probabilidad if not self.es_default_probabilidad() else "default",
            "unidad": self.unidad
        }
    
    def from_json(self, json):
        self.set_limite_inferior(json['limite_inferior'] if json['limite_inferior'] != "default" else None)
        self.set_limite_superior(json['limite_superior'] if json['limite_superior'] != "default" else None)
        self.set_limite_por_ciclo(json['limite_por_ciclo'] if json['limite_por_ciclo'] != "default" else None)
        self.set_error_maximo(json['error_maximo'] if json['error_maximo'] != "default" else None)
        self.set_proporcion(json['proporcion'] if json['proporcion'] != "default" else None)
        self.set_tipo(TipoError(json['tipo']) if json['tipo'] != "default" else None)
        self.set_ultimo_valor(json['ultimo_valor'] if json['ultimo_valor'] != "default" else None)
        self.set_probabilidad(json['probabilidad'] if json['probabilidad'] != "default" else None)
        self.unidad = json['unidad']
        return self
    
    def set_probabilidad(self, valor):
        self.probabilidad = valor
        if valor is None:
            self.probabilidad = 0
    