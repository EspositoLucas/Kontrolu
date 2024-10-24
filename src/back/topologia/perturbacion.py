from __future__ import annotations
from latex2sympy2 import latex2sympy
from sympy import  inverse_laplace_transform, symbols,laplace_transform,simplify
from .hoja import Hoja

class Perturbacion(Hoja):

    def __init__(self,funcion_transferencia:str="1",inicio=0,duracion=1,from_json=None,padre=None) -> None:
        self.observer = None
        if from_json:
            self.from_json(from_json)
            self.padre = padre
            return
        self.inicio = inicio
        self.duracion = duracion
        self.ahora = False
        self.datos = {'tiempo': [], 'valor_original': [], 'perturbacion': [], 'resultado': []}
        super().__init__(funcion_transferencia=funcion_transferencia,nombre="Perturbacion")
    
    def set_observer(self,observer):
        self.observer = observer
    
    def notificar(self, estado):
        if self.observer:
            try:
                self.observer.actualizar(estado)
            except Exception as e:
                print("Error al notificar: ", e)

    def simular(self,tiempo,entrada):

        if (not self.get_estado(tiempo)):
            self.notificar(False)
            return entrada
        self.notificar(True)


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

    def to_json(self):
        return {
            "tipo": "perturbacion",
            "nombre": self.nombre,
            "fdt": self.funcion_transferencia,
            "inicio": self.inicio,
            "duracion": self.duracion,
            "ahora": self.ahora
        }
    
    def from_json(self, json):
        self.nombre = json['nombre']
        self.funcion_transferencia = json['fdt']
        self.inicio = json['inicio']
        self.duracion = json['duracion']
        self.ahora = json['ahora']

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["tipo", "nombre", "fdt", "inicio", "duracion", "ahora"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")

        if datos["tipo"] != "perturbacion":
            raise Exception(f"El tipo debe ser 'perturbacion'")

        if not isinstance(datos["nombre"], str):
            raise Exception(f"El nombre debe ser una cadena de caracteres")

        if not isinstance(datos["fdt"], str):
            raise Exception(f"La funcion de transferencia debe ser una cadena de caracteres")

        if not isinstance(datos["inicio"], (int, float)):
            raise Exception(f"El inicio debe ser un número")

        if not isinstance(datos["duracion"], (int, float)):
            raise Exception(f"La duracion debe ser un número")

        if not isinstance(datos["ahora"], bool):
            raise Exception(f"El valor de 'ahora' debe ser booleano")

        return True
    
    def operar_fdt(self,input):

        return self.calcular_fdt() + input