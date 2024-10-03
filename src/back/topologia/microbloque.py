
from PyQt5.QtGui import QColor
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy
from back.topologia.configuraciones import Configuracion
from .hoja import Hoja

class MicroBloque(Hoja):
    def __init__(self, nombre: str= "Microbloque", color: QColor=None, funcion_transferencia: str="1", padre=None) -> None:
        self.color = color
        self.configuracion_entrada = Configuracion(nombre="Configuracion Entrada")
        self.configuracion_salida = Configuracion(nombre="Configuracion Salida")
        super().__init__(nombre=nombre, funcion_transferencia=funcion_transferencia)
    
    def alto(self) -> int:
        return 80
    
    def ancho(self) -> int:
        return 150
    
    def obtener_micros(self):
        return [self]
        
    def simular(self, tiempo, entrada=None):

        s,t = symbols('s t')

        tf_sympy = latex2sympy(self.funcion_transferencia)
        print(f"La función de transferencia es: {tf_sympy}")

        operacion_laplace = tf_sympy

        if entrada:


            entrada_con_error = self.configuracion_entrada.actualizar(entrada,tiempo)

            entrada_micro_bloque = laplace_transform(entrada_con_error,t,s)[0]
            print(f"La entrada es: {entrada_micro_bloque}")
            operacion_laplace = entrada_micro_bloque * tf_sympy
            print(f"La operación de Laplace es: {operacion_laplace}")
        
        operacion_tiempo = inverse_laplace_transform(operacion_laplace,s,t)
        print(f"La operación en tiempo es: {operacion_tiempo}")
        salida_micro_bloque = operacion_tiempo.subs(t,tiempo)
        print(f"La salida en tiempo es: {salida_micro_bloque}")

        salida_con_error = self.configuracion_salida.actualizar(salida_micro_bloque,tiempo)


        return salida_con_error

    def unidad_entrada(self):
        return self.configuracion_entrada.unidad
    
    def unidad_salida(self):
        return self.configuracion_salida.unidad
    