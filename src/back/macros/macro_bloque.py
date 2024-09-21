from back.topologia.topologia_serie import TopologiaSerie
from back.topologia.topologia_serie import TopologiaParalelo

from back.topologia.interfaz_topologia import InterfazTopologia

class MacroBloque(InterfazTopologia):
    def __init__(self):
        self.topologia = TopologiaSerie(padre=self)
        self.nombre = "MacroBloque"
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