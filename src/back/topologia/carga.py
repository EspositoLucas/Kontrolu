
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy
import numpy as np
from enum import Enum

class TipoCarga(Enum):
    INTEGRAL = "integral"
    FINAL = "final"
    ERROR = "error"
    INTEGRAL_PROPORCIONAL = "integral_proporcional"
    ERROR_PROPORCIONAL = "error_proporcional"


estados = [
    {
        "minimo":0.9,
        "nombre":"Excelente",
        "prioridad":5
    },
    {
        "minimo":0.7,
        "nombre":"Bueno",
        "prioridad":4
    },
    {
        "minimo":0.5,
        "nombre":"Regular",
        "prioridad":3
    },
    {
        "minimo":0.3,
        "nombre":"Malo",
        "prioridad":2
    },
    {
        "minimo":0.1,
        "nombre":"Pésimo",
        "prioridad":1
    }
]

class Carga:
    def __init__(self,funcion_de_trasnferencia,tipo_carga=TipoCarga.FINAL,estados=estados,escalamiento_sigmoide=1,desplazamiento_sigmoide=0):
        self.funcion_de_transferencia = funcion_de_trasnferencia
        self.tipo_carga = tipo_carga
        self.escalamiento_sigmoide = escalamiento_sigmoide
        self.desplazamiento_sigmoide = desplazamiento_sigmoide
        self.estados = estados
        self.errores = 0
        self.total = 0
        self.datos = {'tiempo': [], 'estado': [], 'carga': []}
    
    
    def sigmoide(self,x, x_min, x_max):
        k = self.escalamiento_sigmoide
        x_0 = self.desplazamiento_sigmoide

        # Normalizar x para que esté entre 0 y 1
        x_norm = self.basic(x, x_min, x_max)
        
        # Aplicar la función sigmoide ajustada
        return 1 / (1 + np.exp(-k * (x_norm - x_0)))
    
    def basic(self,x, x_min, x_max):
        return (x - x_min) / (x_max - x_min)
    
    def normalizar(self,valor, minimo, maximo):
        if((valor<minimo) or (valor>maximo)): return 0
        if(self.desplazamiento_sigmoide): return self.sigmoide(valor, minimo, maximo)
        return self.basic(valor, minimo, maximo)

    def obtener_estado(self,valor_normal):
        return max(filter(lambda x: x["minimo"] <= valor_normal, self.estados),key=lambda x: x["minimo"])


    def salida_final(self,salida_real,valor_esperado):
        if(salida_real<valor_esperado): return self.normalizar(valor_esperado,0,salida_real)
        return self.normalizar(valor_esperado,salida_real,salida_real*2)

    def salida_integral(self,salida_real,valor_esperado):
        self.total += abs(valor_esperado)
        self.errores += salida_real - valor_esperado
        self.normalizar(self.total - abs(self.errores),0,self.total)

    def salida_error(self,salida_real,valor_esperado):
        self.total += abs(valor_esperado)
        self.errores += abs(salida_real - valor_esperado)
        self.normalizar(self.total - self.errores,0,self.total)

    def salida_integral_proporcional(self,salida_real,valor_esperado):
        self.total += 1
        self.errores += (salida_real - valor_esperado)/valor_esperado
        self.normalizar(self.total - abs(self.errores),0,self.total)

    def salida_error_proporcional(self,salida_real,valor_esperado):
        self.total += 1
        self.errores += abs((salida_real - valor_esperado)/valor_esperado)
        self.normalizar(self.total - self.errores,0,self.total)

    def salida_esperada(self,tiempo):
        s,t = symbols('s t')
        funcion_transferencia = latex2sympy(self.funcion_de_transferencia)
        salida = inverse_laplace_transform(funcion_transferencia,s,t)
        return salida.subs(t,tiempo)

    def simular(self,tiempo,salida_real):
        valor_esperado = self.salida_esperada(tiempo)

        if self.tipo_carga == TipoCarga.INTEGRAL:
            carga = self.salida_integral(salida_real,valor_esperado)
        elif self.tipo_carga == TipoCarga.FINAL:
            carga = self.salida_final(salida_real,valor_esperado)
        elif self.tipo_carga == TipoCarga.ERROR:
            carga = self.salida_error(salida_real,valor_esperado)
        elif self.tipo_carga == TipoCarga.INTEGRAL_PROPORCIONAL:
            carga = self.salida_integral_proporcional(salida_real,valor_esperado)
        elif self.tipo_carga == TipoCarga.ERROR_PROPORCIONAL:
            carga = self.salida_error_proporcional(salida_real,valor_esperado)
        else:
            carga = 0

        estado = self.obtener_estado(carga)

        self.datos['tiempo'].append(tiempo)
        self.datos['estado'].append(estado)
        self.datos['carga'].append(carga)

        return estado