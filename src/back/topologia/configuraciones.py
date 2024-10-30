import numpy as np
from math import inf
from enum import Enum

class TipoError(Enum):
    GAUSS = "gauss"
    ALEATORIO = "aleatorio"
    PROPORCIONAL = "proporcional"
    NINGUNO = "ninguno"

class Configuracion:
    def __init__(self, nombre="Configuración", limite_inferior=-inf, limite_superior=inf, limite_por_ciclo=inf, error_maximo=inf, proporcion=0, tipo=TipoError.NINGUNO, ultimo_valor=0, probabilidad=1, unidad="V",from_json=None):
        self.datos = {'tiempo': [], 'valor_original': [], 'error_base': [], 'error_limite': [], 'error_total': [], 'resultado': []}
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
        self.nombre = "Configuración"
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
            "nombre": self.nombre,
            "limite_inferior": self.limite_inferior if not self.es_default_limite_inferior() else "default",
            "limite_superior": self.limite_superior if not self.es_default_limite_superior() else "default",
            "limite_por_ciclo": self.limite_por_ciclo if not self.es_default_limite_por_ciclo() else "default",
            "error_maximo": self.error_maximo if not self.es_default_error_maximo() else "default",
            "proporcion": self.proporcion if not self.es_default_proporcion() else "default",
            "tipo": self.tipo.value,
            "ultimo_valor": self.ultimo_valor if not self.es_default_ultimo_valor() else "default",
            "probabilidad": self.probabilidad if not self.es_default_probabilidad() else "default",
            "unidad": self.unidad
        }
    
    def from_json(self, json):
        self.nombre = json['nombre']
        self.set_limite_inferior(json['limite_inferior'] if json['limite_inferior'] != "default" else None)
        self.set_limite_superior(json['limite_superior'] if json['limite_superior'] != "default" else None)
        self.set_limite_por_ciclo(json['limite_por_ciclo'] if json['limite_por_ciclo'] != "default" else None)
        self.set_error_maximo(json['error_maximo'] if json['error_maximo'] != "default" else None)
        self.set_proporcion(json['proporcion'] if json['proporcion'] != "default" else None)
        self.set_tipo(TipoError(json['tipo']))
        self.set_ultimo_valor(json['ultimo_valor'] if json['ultimo_valor'] != "default" else None)
        self.set_probabilidad(json['probabilidad'] if json['probabilidad'] != "default" else None)
        self.unidad = json['unidad']
        return self
    
    def set_probabilidad(self, valor):
        self.probabilidad = valor
        if valor is None:
            self.probabilidad = 0
    

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["nombre", "limite_inferior", "limite_superior", "limite_por_ciclo", "error_maximo", "proporcion", "tipo", "ultimo_valor", "probabilidad", "unidad"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")
        
        if not (isinstance(datos["limite_inferior"], (int, float)) or datos["limite_inferior"] == "default"):
            raise Exception("El limite_inferior debe ser un número o 'default'")
        
        if not (isinstance(datos["limite_superior"], (int, float)) or datos["limite_superior"] == "default"):
            raise Exception("El limite_superior debe ser un número o 'default'")
        
        if not (isinstance(datos["limite_por_ciclo"], (int, float)) or datos["limite_por_ciclo"] == "default"):
            raise Exception("El limite_por_ciclo debe ser un número o 'default'")
        
        if not (isinstance(datos["error_maximo"], (int, float)) or datos["error_maximo"] == "default"):
            raise Exception("El error_maximo debe ser un número o 'default'")
        
        if not (isinstance(datos["proporcion"], (int, float)) or datos["proporcion"] == "default"):
            raise Exception("El proporcion debe ser un número o 'default'")
        
        if not isinstance(datos["tipo"], str) or datos["tipo"] not in TipoError._value2member_map_:
            raise Exception("El tipo debe ser uno de los valores definidos en TipoError")
        
        if not (isinstance(datos["ultimo_valor"], (int, float)) or datos["ultimo_valor"] == "default"):
            raise Exception("El ultimo_valor debe ser un número o 'default'")
        
        if not (isinstance(datos["probabilidad"], (int, float)) or datos["probabilidad"] == "default"):
            raise Exception("El probabilidad debe ser un número o 'default'")
        
        if not isinstance(datos["unidad"], str):
            raise Exception("La unidad debe ser un string")
        
        return True