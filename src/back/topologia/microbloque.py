
from PyQt5.QtGui import QColor
from back.topologia.configuraciones import Configuracion,TipoError
from .hoja import Hoja
from back.json_manager.dtos import MicroBloqueDto
from latex2sympy2 import latex2sympy

class MicroBloque(Hoja):
    def __init__(self, nombre: str= "Microbloque",color: QColor=QColor(255, 255, 255), funcion_transferencia: str="\\frac{1}{s}", padre=None, descripcion = "Esto es un microbloque", datos: MicroBloqueDto = None,from_json=None) -> None:
        super().__init__(nombre=nombre, funcion_transferencia=funcion_transferencia)
        if from_json:
            self.from_json(from_json)
            self.padre = padre
            return        
        self.color = color
        self.descripcion = descripcion
        self.configuracion_entrada = Configuracion(nombre="Configuracion Entrada")
        self.configuracion_salida = Configuracion(nombre="Configuracion Salida")
        
        if datos:
            self.set_dto(datos)
    
    def set_dto(self, datos: MicroBloqueDto):
        if datos.fdt is not None:
            self.funcion_transferencia = datos.fdt
        if datos.nombre is not None:
            self.nombre = datos.nombre
        if datos.descripcion is not None:
            self.descripcion = datos.descripcion
        if datos.unidad_entrada is not None:
            self.configuracion_entrada.unidad = datos.unidad_entrada
        if datos.unidad_salida is not None:
            self.configuracion_salida.unidad = datos.unidad_salida
        if datos.entrada_error_maximo is not None:
            self.configuracion_entrada.error_maximo = self._convert_to_float(datos.entrada_error_maximo)
        if datos.salida_error_maximo is not None:
            self.configuracion_salida.error_maximo = self._convert_to_float(datos.salida_error_maximo)
        if datos.entrada_limite_inferior is not None:
            self.configuracion_entrada.limite_inferior = self._convert_to_float(datos.entrada_limite_inferior)
        if datos.salida_limite_inferior is not None:
            self.configuracion_salida.limite_inferior = self._convert_to_float(datos.salida_limite_inferior)
        if datos.entrada_limite_superior is not None:
            self.configuracion_entrada.limite_superior = self._convert_to_float(datos.entrada_limite_superior)
        if datos.salida_limite_superior is not None:
            self.configuracion_salida.limite_superior = self._convert_to_float(datos.salida_limite_superior)
        if datos.entrada_limite_por_ciclo is not None:
            self.configuracion_entrada.limite_por_ciclo = self._convert_to_float(datos.entrada_limite_por_ciclo)
        if datos.salida_limite_por_ciclo is not None:
            self.configuracion_salida.limite_por_ciclo = self._convert_to_float(datos.salida_limite_por_ciclo)
        if datos.entrada_proporcion is not None:
            self.configuracion_entrada.proporcion = self._convert_to_float(datos.entrada_proporcion)
        if datos.salida_proporcion is not None:
            self.configuracion_salida.proporcion = self._convert_to_float(datos.salida_proporcion)
        if datos.entrada_propabilidad is not None:
            self.configuracion_entrada.probabilidad = self._convert_to_float(datos.entrada_propabilidad)
        if datos.salida_propabilidad is not None:
            self.configuracion_salida.probabilidad = self._convert_to_float(datos.salida_propabilidad)
        if datos.entrada_tipo is not None:
            self.configuracion_entrada.tipo = TipoError(datos.entrada_tipo)
        if datos.salida_tipo is not None:
            self.configuracion_salida.tipo = TipoError(datos.salida_tipo)
        if datos.entrada_ultimo_valor is not None:
            self.configuracion_entrada.ultimo_valor = self._convert_to_float(datos.entrada_ultimo_valor)
        if datos.salida_ultimo_valor is not None:
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
        return float(value)

    def _check_infinite(self, value):
        if value == float('inf'):
            return 'inf'
        elif value == float('-inf'):
            return '-inf'
        return float(value)

    def alto(self) -> int:
        return 80
    
    def ancho(self) -> int:
        return 150
    
    def obtener_micros(self):
        return [self]
        


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

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["nombre", "descripcion", "fdt", "configuracion_entrada", "configuracion_salida", "color"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")
        
        if not isinstance(datos['nombre'], str):
            raise Exception(f"El nombre de {datos['nombre']} debe ser un string")
        
        if not isinstance(datos['descripcion'], str):
            raise Exception(f"La descripción de {datos['nombre']} debe ser un string")
        
        if not isinstance(datos['fdt'], str):
            raise Exception(f"La función de transferencia de {datos['nombre']} debe ser un string")
        
        try:
            latex2sympy(datos['fdt'])
        except Exception as e:
            raise Exception(f"Error en la función de transferencia de {datos['nombre']}")
        
        try:
            Configuracion.validar_dict(datos['configuracion_entrada'])
        except Exception as e:
            raise Exception(f"Error en la configuración de entrada de {datos['nombre']}: {e}")
        try:
            Configuracion.validar_dict(datos['configuracion_salida'])
        except Exception as e:
            raise Exception(f"Error en la configuración de salida de {datos['nombre']}: {e}")

        if not isinstance(datos['color'], str):
            raise Exception(f"El color de {datos['nombre']} debe ser un string")
        
        return True
    


    def operar_fdt(self,input):

        return self.calcular_fdt() * input
