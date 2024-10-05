
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
    def __init__(self,funcion_de_transferencia="1",tipo_carga=TipoCarga.FINAL,estados=estados,escalamiento_sigmoide=1,desplazamiento_sigmoide=0,nombre="Carga",entrada=None):
        self.entrada = entrada
        self.nombre = nombre
        self.funcion_de_transferencia = funcion_de_transferencia
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
        resultado = 0 if np.exp(-k * (x_norm - x_0)) == -1 else (1 / (1 + np.exp(-k * (x_norm - x_0))))
        return resultado
    
    def basic(self,x, x_min, x_max):
        return 1 if x_max == x_min and x == x_max else 0 if x_max == x_min else (x - x_min) / (x_max - x_min)
    
    def normalizar(self,valor, minimo, maximo):
        if((valor<minimo) or (valor>maximo)): 

            return 0
        if(self.desplazamiento_sigmoide): 

            sigmo = self.sigmoide(valor, minimo, maximo)
            return sigmo
        otro = self.basic(valor, minimo, maximo)
        return otro

    def obtener_estado(self,valor_normal):
        posibles = list(filter(lambda x: x["minimo"] <= valor_normal, self.estados))

        if(not posibles):
            posibles = [{"minimo":0,"nombre":"ESTADO NO CONTEMPLADO","prioridad":0}]

        
        return max(posibles,key=lambda x: x["minimo"])


    def salida_final(self,salida_real,valor_esperado):

        distancia = abs(salida_real - valor_esperado)

        carga = self.normalizar(-distancia,-abs(valor_esperado),0)

        return carga

    def salida_integral(self,salida_real,valor_esperado):
        self.total += abs(valor_esperado)
        self.errores += salida_real - valor_esperado
        return self.normalizar(self.total - abs(self.errores),0,self.total)

    def salida_error(self,salida_real,valor_esperado):
        self.total += abs(valor_esperado)
        self.errores += abs(salida_real - valor_esperado)
        return self.normalizar(self.total - self.errores,0,self.total)

    def salida_integral_proporcional(self,salida_real,valor_esperado):
        self.total += 1
        self.errores += (salida_real - valor_esperado)/valor_esperado
        return self.normalizar(self.total - abs(self.errores),0,self.total)

    def salida_error_proporcional(self,salida_real,valor_esperado):
        self.total += 1
        self.errores += abs((salida_real - valor_esperado)/valor_esperado)
        return self.normalizar(self.total - self.errores,0,self.total)

    def salida_esperada(self,tiempo):
        
        funcion = self.funcion_de_transferencia
        
        if ((not funcion) or (funcion == " ")):
            funcion = self.entrada.funcion_transferencia

        s,t = symbols('s t')
        funcion_transferencia = latex2sympy(funcion)
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