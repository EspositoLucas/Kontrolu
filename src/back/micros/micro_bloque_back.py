
# class MicroBloqueBack():
#     def __init__(self, modelo):
#         self.modelo = modelo

# class MicroBloqueBack():
#     def __init__(self, modelo, nombre):
#         self.modelo = modelo
#         self.nombre = nombre

#     def __str__(self):
#         return self.nombre

class MicroBloqueBack():
    def __init__(self, modelo, nombre):
        self.modelo = modelo
        self.nombre = nombre
        self.funcion_transferencia = ""
        self.opciones_adicionales = {}

    def __str__(self):
        return self.nombre

    def set_funcion_transferencia(self, funcion):
        self.funcion_transferencia = funcion

    def set_opcion_adicional(self, clave, valor):
        self.opciones_adicionales[clave] = valor

    def get_opcion_adicional(self, clave):
        return self.opciones_adicionales.get(clave)