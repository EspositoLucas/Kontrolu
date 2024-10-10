
from PyQt5.QtGui import QColor
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy
from back.topologia.configuraciones import Configuracion,TipoError
from .hoja import Hoja
from back.json_manager.dtos import MicroBloqueDto

class MicroBloque(Hoja):
    def __init__(self, nombre: str= "Microbloque",color: QColor=QColor(255, 255, 0), funcion_transferencia: str="1", padre=None, descripcion = "Esto es un microbloque", datos: MicroBloqueDto = None,from_json=None) -> None:
        if from_json:
            self.from_json(from_json)
            self.padre = padre
            return        
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
        self.configuracion_entrada.error_maximo = self._convert_to_float(datos.entrada_error_maximo)
        self.configuracion_salida.error_maximo = self._convert_to_float(datos.salida_error_maximo)
        self.configuracion_entrada.limite_inferior = self._convert_to_float(datos.entrada_limite_inferior)
        self.configuracion_salida.limite_inferior = self._convert_to_float(datos.salida_limite_inferior)
        self.configuracion_entrada.limite_superior = self._convert_to_float(datos.entrada_limite_superior)
        self.configuracion_salida.limite_superior = self._convert_to_float(datos.salida_limite_superior)
        self.configuracion_entrada.limite_por_ciclo = self._convert_to_float(datos.entrada_limite_por_ciclo)
        self.configuracion_salida.limite_por_ciclo = self._convert_to_float(datos.salida_limite_por_ciclo)
        self.configuracion_entrada.proporcion = self._convert_to_float(datos.entrada_proporcion)
        self.configuracion_salida.proporcion = self._convert_to_float(datos.salida_proporcion)
        self.configuracion_entrada.probabilidad = self._convert_to_float(datos.entrada_propabilidad)
        self.configuracion_salida.probabilidad = self._convert_to_float(datos.salida_propabilidad)
        self.configuracion_entrada.tipo = TipoError(datos.entrada_tipo)
        self.configuracion_salida.tipo = TipoError(datos.salida_tipo)
        self.configuracion_entrada.ultimo_valor = self._convert_to_float(datos.entrada_ultimo_valor)
        self.configuracion_salida.ultimo_valor = self._convert_to_float(datos.salida_ultimo_valor)
    def get_dto(self) -> MicroBloqueDto:

        return MicroBloqueDto(
            nombre=self.nombre,
            descripcion=self.descripcion,
            fdt=self.funcion_transferencia,
            entrada_limite_inferior=self._check_infinite(self.configuracion_entrada.limite_inferior),
            entrada_limite_superior=self._check_infinite(self.configuracion_entrada.limite_superior),
            entrada_limite_por_ciclo=self._check_infinite(self.configuracion_entrada.limite_por_ciclo),
            entrada_error_maximo=self._check_infinite(self.configuracion_entrada.error_maximo),
            entrada_proporcion=self._check_infinite(self.configuracion_entrada.proporcion),
            entrada_tipo=self.configuracion_entrada.tipo.value,
            entrada_ultimo_valor=self._check_infinite(self.configuracion_entrada.ultimo_valor),
            entrada_propabilidad=self._check_infinite(self.configuracion_entrada.probabilidad),
            salida_limite_inferior=self._check_infinite(self.configuracion_salida.limite_inferior),
            salida_limite_superior=self._check_infinite(self.configuracion_salida.limite_superior),
            salida_limite_por_ciclo=self._check_infinite(self.configuracion_salida.limite_por_ciclo),
            salida_error_maximo=self._check_infinite(self.configuracion_salida.error_maximo),
            salida_proporcion=self._check_infinite(self.configuracion_salida.proporcion),
            salida_tipo=self.configuracion_salida.tipo.value,
            salida_ultimo_valor=self._check_infinite(self.configuracion_salida.ultimo_valor),
            salida_propabilidad=self._check_infinite(self.configuracion_salida.probabilidad),
            unidad_entrada=self.configuracion_entrada.unidad,
            unidad_salida=self.configuracion_salida.unidad
        )

    def _convert_to_float(self, value):
        if value == 'inf':
            return float('inf')
        elif value == '-inf':
            return float('-inf')
        elif value == '-Infinity':
            return float('-inf')
        elif value == 'Infinity':
            return float('inf')
        return value

    def _check_infinite(self, value):
        if value == float('inf'):
            return 'inf'
        elif value == float('-inf'):
            return '-inf'
        return value

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
    
    def to_json(self):
        return {
            "tipo": "microbloque",
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fdt": self.funcion_transferencia,
            "configuracion_entrada": self.configuracion_entrada.to_json(),
            "configuracion_salida": self.configuracion_salida.to_json(),
            "color": self.color.name()
        }
    
    def from_json(self, json):
        self.nombre = json['nombre']
        self.descripcion = json['descripcion']
        self.funcion_transferencia = json['fdt']
        self.configuracion_entrada = Configuracion(from_json=json['configuracion_entrada'])
        self.configuracion_salida = Configuracion(from_json=json['configuracion_salida'])
        self.color = QColor(json['color'])
        print(f"Se ha creado el microbloque {self.nombre} con la configuración de entrada {self.configuracion_entrada} y la configuración de salida {self.configuracion_salida}")