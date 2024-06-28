from __future__ import annotations
import itertools
class InterfazTopologia():
    def __init__(self) -> None:
        self.hijos = []
        pass

    def ancho(self) -> int:
        pass

    def alto(self) -> int:
        pass

    def tamanio(self) -> tuple(int,int):
        return(self.ancho(),self.alto())

    def obtenerHijo(self):
        pass

    def obtenerPadre(self):
        pass

    def borrar_elemento(self,elemento):
        self.hijos.remove(elemento)

    def reemplazar_elemento(self,elemento,nuevo):
        self.hijos[self.hijos.index(elemento)] = nuevo

    def cambiar_padre(self,padre: InterfazTopologia):
        self.padre = padre

    def obtener_micros(self):
        return list(itertools.chain.from_iterable(map(lambda x: x.obtener_micros(),self.hijos)))