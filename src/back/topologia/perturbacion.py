from __future__ import annotations
from latex2sympy2 import latex2sympy
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from .hoja import Hoja

class Perturbacion(Hoja):

    def __init__(self,funcion_transferencia:str="1",inicio=0,duracion=1):
        self.inicio = inicio
        self.duracion = duracion
        self.ahora = False
        self.datos = {'tiempo': [], 'valor_original': [], 'perturbacion': [], 'resultado': []}
        super().__init__(funcion_transferencia=funcion_transferencia,nombre="Perturbacion")
    
    
    def simular(self,tiempo,entrada):

        if (not self.get_estado(tiempo)):
            return entrada


        s,t = symbols('s t')

        perturbacion_laplace = latex2sympy(self.funcion_transferencia)

        perturbacion_tiempo = inverse_laplace_transform(perturbacion_laplace,s,t)

        perturbado = perturbacion_tiempo.subs(t,tiempo)


        nuevo_valor = perturbado + entrada

        self.datos['tiempo'].append(tiempo)
        self.datos['valor_original'].append(entrada)
        self.datos['perturbacion'].append(perturbado)
        self.datos['resultado'].append(nuevo_valor)


        return nuevo_valor
    

    def set_funcion_transferencia(self, funcion):
        print("Nueva funcion de transferencia: ", funcion)
        self.funcion_transferencia = funcion

    def get_estado(self,tiempo):
        if self.ahora:
            self.ahora = False
            self.inicio = tiempo
        return self.inicio <= tiempo <= (self.inicio + self.duracion)

    def perturbar_ahora(self,duracion):
        self.ahora = True
        self.duracion = duracion

    def set_valores(self,inicio,duracion,ahora):
        self.inicio = inicio
        self.duracion = duracion
        self.ahora = ahora

    def radio(self) -> int:
        return 10
    
    def alto(self) -> int:
        return 2 * self.radio()
    
    def ancho(self) -> int:
        return 2 * self.radio()
    

    def unidad_entrada(self):
        return self.padre.unidad_saliente(self)
    
    def unidad_salida(self):
        return self.padre.unidad_entrante(self)

    