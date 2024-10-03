
from PyQt5.QtGui import QColor
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy
from back.topologia.configuraciones import Configuracion
from .hoja import Hoja
from back.json_manager.dtos import MicroBloqueDto

class MicroBloque(Hoja):
    def __init__(self, nombre: str= "Microbloque",color: QColor=None, funcion_transferencia: str="1", padre=None, descripcion = "Esto es un microbloque", datos: MicroBloqueDto = None ) -> None:
        self.color = color
        self.descripcion = descripcion
        self.configuracion_entrada = Configuracion(nombre="Configuracion Entrada")
        self.configuracion_salida = Configuracion(nombre="Configuracion Salida")
        super().__init__(nombre=nombre, funcion_transferencia=funcion_transferencia)
        if datos:
            self.set_dto(datos)

    def set_dto(self, datos: MicroBloqueDto):
        self.funcion_transferencia = datos.fdt
        self.nombre = datos.nombre
        self.descripcion = datos.descripcion
        self.configuracion_entrada.unidad = datos.unidad_entrada
        self.configuracion_salida.unidad = datos.unidad_salida
        self.configuracion_entrada.error_maximo = datos.entrada_error_maximo
        self.configuracion_salida.error_maximo = datos.salida_error_maximo
        self.configuracion_entrada.limite_inferior = datos.entrada_limite_inferior
        self.configuracion_salida.limite_inferior = datos.salida_limite_inferior
        self.configuracion_entrada.limite_superior = datos.entrada_limite_superior
        self.configuracion_salida.limite_superior = datos.salida_limite_superior
        self.configuracion_entrada.limite_por_ciclo = datos.entrada_limite_por_ciclo
        self.configuracion_salida.limite_por_ciclo = datos.salida_limite_por_ciclo
        self.configuracion_entrada.proporcion = datos.entrada_proporcion
        self.configuracion_salida.proporcion = datos.salida_proporcion
        self.configuracion_entrada.probabilidad = datos.entrada_propabilidad
        self.configuracion_salida.probabilidad = datos.salida_propabilidad
        self.configuracion_entrada.tipo = datos.entrada_tipo
        self.configuracion_salida.tipo = datos.salida_tipo
        self.configuracion_entrada.ultimo_valor = datos.entrada_ultimo_valor
        self.configuracion_salida.ultimo_valor = datos.salida_ultimo_valor

    def get_dto(self) -> MicroBloqueDto:
        return MicroBloqueDto(
            nombre=self.nombre,
            descripcion=self.descripcion,
            fdt=self.funcion_transferencia,
            entrada_limite_inferior=self.configuracion_entrada.limite_inferior,
            entrada_limite_superior=self.configuracion_entrada.limite_superior,
            entrada_limite_por_ciclo=self.configuracion_entrada.limite_por_ciclo,
            entrada_error_maximo=self.configuracion_entrada.error_maximo,
            entrada_proporcion=self.configuracion_entrada.proporcion,
            entrada_tipo=self.configuracion_entrada.tipo,
            entrada_ultimo_valor=self.configuracion_entrada.ultimo_valor,
            entrada_propabilidad=self.configuracion_entrada.probabilidad,
            salida_limite_inferior=self.configuracion_salida.limite_inferior,
            salida_limite_superior=self.configuracion_salida.limite_superior,
            salida_limite_por_ciclo=self.configuracion_salida.limite_por_ciclo,
            salida_error_maximo=self.configuracion_salida.error_maximo,
            salida_proporcion=self.configuracion_salida.proporcion,
            salida_tipo=self.configuracion_salida.tipo,
            salida_ultimo_valor=self.configuracion_salida.ultimo_valor,
            salida_propabilidad=self.configuracion_salida.probabilidad,
            unidad_entrada=self.configuracion_entrada.unidad,
            unidad_salida=self.configuracion_salida.unidad
        )

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
    