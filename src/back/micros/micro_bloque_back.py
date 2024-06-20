
# class MicroBloqueBack():
#     def __init__(self, modelo):
#         self.modelo = modelo

class MicroBloqueBack():
    def __init__(self, modelo, nombre):
        self.modelo = modelo
        self.nombre = nombre

    def __str__(self):
        return self.nombre