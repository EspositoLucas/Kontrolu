from back.topologia.topologia_serie import TopologiaSerie
from back.topologia.topologia_serie import TopologiaParalelo

from back.topologia.interfaz_topologia import InterfazTopologia

class MacroBloque(InterfazTopologia):
    def __init__(self,nombre="",sesion=None):
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
    
    def simular(self, tiempo, entrada):
        entrada_alterada = self.alterar_entrada(entrada, tiempo)
        salida =  self.topologia.simular(tiempo, entrada_alterada)
        salida_alterada = self.alterar_salida(salida, tiempo)
        return salida_alterada
    
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