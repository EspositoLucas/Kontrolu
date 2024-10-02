from __future__ import annotations
from latex2sympy2 import latex2sympy
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from .hoja import Hoja

class Perturbacion(Hoja):

    def __init__(self,funcion_transferencia:str="0",ciclos=0,dentro_de=0):
        self.ciclos = ciclos
        self.dentro_de = dentro_de
        self.datos = {'tiempo': [], 'valor_original': [], 'perturbacion': [], 'resultado': []}
        super().__init__(funcion_transferencia=funcion_transferencia,nombre="Perturbacion")
    
    
    def simular(self,entrada,tiempo):

        self.dentro_de -= 1
        
        if not self.get_estado(): return entrada

        self.ciclos -= 1


        s,t = symbols('s t')
        
        if self.ciclos <= 0: self.estado = False

        perturbacion_laplace = latex2sympy(self.funcion_transferencia)

        perturbacion_tiempo = inverse_laplace_transform(perturbacion_laplace,s,t)

        perturbado = perturbacion_tiempo.subs(t,tiempo)

        nuevo_valor = perturbado + entrada

        self.datos['tiempo'].append(tiempo)
        self.datos['valor_original'].append(entrada)
        self.datos['perturbacion'].append(perturbado)
        self.datos['resultado'].append(nuevo_valor)

        return nuevo_valor
    
    def activa(self):
        return self.estado

    def generar_perturbacion(self,ft,ciclos,dentro_de=0):
        self.funcion_transferencia = ft
        self.ciclos = ciclos
        self.dentro_de = dentro_de
    
    def reactivar_perturbacion(self,ciclos,dentro_de=0):
        self.ciclos = ciclos
        self.dentro_de = dentro_de
    

    def get_estado(self):
        if (self.ciclos > 0) and (self.dentro_de < 0):
            self.estado = True
        else:
            self.estado = False

    def cancelar_perturbacion(self):
        self.ciclos = 0
        self.dentro_de = 0
    
    def radio(self) -> int:
        return 10
    
    def alto(self) -> int:
        return 2 * self.radio()
    
    def ancho(self) -> int:
        return 2 * self.radio()
    

    def unidad_entrada(self):
        return self.padre.unidad_entrante(self)
    
    def unidad_salida(self):
        return self.padre.unidad_saliente(self)

    