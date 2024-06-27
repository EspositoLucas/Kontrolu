from src.back.topologia.topologia_serie import TopologiaSerie
from src.back.topologia.interfaz_topologia import InterfazTopologia

class MacroBloque(InterfazTopologia):
    
    def __init__(self,sesion):
        self.padre = sesion
        self.topologia = TopologiaSerie(self)
        self.nombre = "MacroBloque"
        self.representacion = None # ESTA SERÍA LA REPRESENTACIÓN VISUAL DEL ELEMENTO (TODO: VINCULARLO CON LAS CLASES DEFINIDAS EN LA CARPETA "ui")

    def __str__(self):
        return f"{self.nombre}: {self.topologia.__str__()}"
    
    def tamanio(self):
        return self.topologia.tamanio()
    
    def obtenerPadre(self):
        return self.topologia.obtenerPadre()
    
    def borrar_elemento(self, elemento):
        pass
    