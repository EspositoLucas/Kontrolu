class InterfazTopologia():
    def __init__(self) -> None:
        self.hijos = []
        pass

    def ancho(self) -> int:
        pass

    def alto(self) -> int:
        pass

    def tamanio(self) -> tuple(int,int):
        pass

    def obtenerHijo(self):
        pass

    def obtenerPadre(self):
        pass

    def borrar_elemento(self,elemento):
        self.hijos.remove(elemento)

    def reemplazar_elemento(self,elemento,nuevo):
        self.hijos[self.hijos.index(elemento)] = nuevo