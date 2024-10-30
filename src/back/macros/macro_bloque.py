from back.topologia.topologia_serie import TopologiaSerie
from back.topologia.topologia_serie import TopologiaParalelo

from back.topologia.interfaz_topologia import InterfazTopologia
from .tipos_macro import MACROS

class MacroBloque(InterfazTopologia):
    def __init__(self,nombre="",sesion=None, tipo:MACROS=None,from_json=None) -> None:
        if from_json:
            self.from_json(from_json)
            return
        self.tipo = tipo
        self.sesion = sesion
        self.topologia = TopologiaSerie(padre=self)
        self.nombre = nombre
        super().__init__()

    def __str__(self):
        return f"{self.nombre}: {str(self.topologia)}"
        
    def tamanio(self):
        return self.topologia.tamanio()
    
    def obtenerPadre(self):
        return self.topologia.obtenerPadre()
    
    def borrar_elemento(self, elemento):
        pass

    def obtener_microbloques(self):
        return self.topologia.obtener_micros()
    
    def reset_topologia(self):
        self.topologia = TopologiaSerie(padre=self)
    
    def agregar_abajo_de(self, microbloque, actual):
        self.topologia = TopologiaSerie(
            micro=TopologiaParalelo(
                microbloqueNuevo=microbloque,
                serie=actual,
                arriba=True
                ),
            padre=self
            )
        
    
    def agregar_arriba_de(self,microbloque,actual):
        self.topologia = TopologiaSerie(
            micro=TopologiaParalelo(
                microbloqueNuevo=microbloque,
                serie=actual,
                arriba=False
                ),
            padre=self
            )
    
    def simular(self, tiempo, delta, entrada):

        salida =  self.topologia.simular(tiempo, delta, entrada)
        
        return salida
    
    def validar_unidades(self):
        self.topologia.validar_unidades()


    def validar_entrada(self, unidad: str)-> bool:
        pass
    def validar_salida(self, unidad: str)-> bool:
        pass

    def unidad_entrada(self):
        return self.topologia.unidad_entrada()
    
    def unidad_salida(self):
        return self.topologia.unidad_salida()
    
    def unidad_entrante(self):
        pass

    def unidad_saliente(self):
        pass

    def to_json(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo.value,
            "topologia": self.topologia.to_json()
        }
    
    def from_json(self, json):
        self.nombre = json['nombre']
        self.tipo = MACROS(json['tipo'])
        self.topologia = TopologiaSerie(from_json=json['topologia'],padre=self)

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["nombre", "tipo", "topologia"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")

        if not isinstance(datos["nombre"], str):
            raise Exception(f"El nombre debe ser un string")

        try:
            MACROS(datos["tipo"])
        except ValueError:
            raise Exception(f"El tipo de {datos['nombre']} debe ser un valor válido de MACROS")

        if not isinstance(datos["topologia"], dict):
            raise Exception(f"La topología de {datos['nombre']} debe ser un diccionario")
        
        try:
            TopologiaSerie.validar_dict(datos["topologia"])
        except Exception as e:
            raise Exception(f"Error en la topología de {datos['nombre']}: {e}")
        
        return True
    
    
    def calcular_fdt(self,tiempo=0):

        return self.topologia.calcular_fdt(tiempo=tiempo)
    
    def vaciar_datos(self):
        self.topologia.vaciar_datos()
    
    def operar_fdt(self,input,tiempo=0):

        return self.calcular_fdt(tiempo=tiempo) * input