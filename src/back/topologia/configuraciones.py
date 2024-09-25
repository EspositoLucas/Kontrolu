import numpy as np
from math import inf
from enum import Enum

class TipoError(Enum):
    GAUSS = "gauss"
    ALEATORIO = "aleatorio"
    PROPORCIONAL = "proporcional"
    NINGUNO = "ninguno"
class Configuracion:
    def __init__(self, nombre="Configuracion", limite_inferior=-inf, limite_superior=inf,limite_por_ciclo=inf,error_maximo=inf,proporcion=0,tipo=TipoError.NINGUNO,ultimo_valor=0,propabilidad=0):
        self.nombre = nombre
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.limite_por_ciclo = limite_por_ciclo
        self.error_maximo = error_maximo
        self.proporcion = proporcion
        self.tipo = tipo
        self.ultimo_valor = ultimo_valor
        self.probablidad = propabilidad
        self.datos = {'tiempo': [], 'valor_original': [], 'error_base': [], 'error_limite': [], 'error_total':[],'resultado': []}
    
    def calcular_error(self,valor):
        if np.random.uniform(0,1) < self.probablidad: return 0

        if self.tipo == TipoError.GAUSS:
            error =  np.random.normal(0,valor*self.proporcion)
        elif self.tipo == TipoError.ALEATORIO:
            error = np.random.uniform(-valor*self.proporcion,valor*self.proporcion)
        elif self.tipo == TipoError.PROPORCIONAL:
            error = valor*self.proporcion
        else:
            error = 0
        
        return max(min(error,self.error_maximo),-self.error_maximo)
    
    def calcular_limite(self,valor):
        if self.limite_por_ciclo:
            ultimo = self.ultimo_valor
            diferencia =   valor - ultimo
            delta_real = max(min(diferencia,self.limite_por_ciclo),-self.limite_por_ciclo)

        posible = ultimo + delta_real

        return min(max(posible,self.limite_inferior),self.limite_superior)
    
    def borrar_configuraciones(self):
        self.nombre = "Configuracion"
        self.limite_inferior = -inf
        self.limite_superior = inf
        self.limite_por_ciclo = inf
        self.error_maximo = inf
        self.proporcion = 0
        self.tipo = TipoError.NINGUNO
        self.ultimo_valor = 0
    
    def borrar_limite_inferior(self):
        self.limite_inferior = -inf
    
    def borrar_limite_superior(self):
        self.limite_superior = inf
    
    def borrar_limite_por_ciclo(self):
        self.limite_por_ciclo = inf
    
    def borrar_error_maximo(self):
        self.error_maximo = inf
    
    def borrar_proporcion(self):
        self.proporcion = 0
    
    def borrar_tipo(self):
        self.tipo = TipoError.NINGUNO
    
    def borrar_ultimo_valor(self):
        self.ultimo_valor = 0
    
    def set_limite_inferior(self,valor):
        self.limite_inferior = valor
        if valor is None: self.limite_inferior = -inf
    
    def set_limite_superior(self,valor):
        self.limite_superior = valor
        if valor is None: self.limite_superior = inf
    
    def set_limite_por_ciclo(self,valor):
        self.limite_por_ciclo = valor
        if valor is None: self.limite_por_ciclo = inf
    
    def set_error_maximo(self,valor):
        self.error_maximo = valor
        if valor is None: self.error_maximo = inf
    
    def set_proporcion(self,valor):
        self.proporcion = valor
        if valor is None: self.proporcion = 0
    
    def set_tipo(self,valor):
        self.tipo = valor
        if valor is None: self.tipo = TipoError.NINGUNO
    
    def set_ultimo_valor(self,valor):
        self.ultimo_valor = valor
        if valor is None: self.ultimo_valor = 0
    

    def actualizar(self,valor,tiempo):
        error = self.calcular_error(valor)
        nuevo = self.calcular_limite(valor+error)
        self.ultimo_valor = nuevo
        self.datos['tiempo'].append(tiempo)
        self.datos['valor_original'].append(valor)
        self.datos['error_base'].append(error)
        self.datos['error_limite'].append(nuevo-valor+error)
        self.datos['error_total'].append(nuevo-valor)
        self.datos['resultado'].append(nuevo)
        return nuevo