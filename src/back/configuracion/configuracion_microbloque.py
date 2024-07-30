from back.configuracion.configuracion import Configuracion, EfectoConfiguracion

class ConfiguracionMicrobloque:
    def __init__(self):
        self.configuraciones = {}

    def agregar_configuracion(self, nombre, tipo, valor_por_defecto):
        self.configuraciones[nombre] = Configuracion(nombre, tipo, valor_por_defecto)

    def set_configuracion(self, nombre, valor):
        if nombre in self.configuraciones:
            self.configuraciones[nombre].set_valor(valor)

    def get_configuracion(self, nombre):
        return self.configuraciones.get(nombre)

    def aplicar_efecto(self, funcion_transferencia):
        for configuracion in self.configuraciones.values():
            configuracion.aplicar_efecto(funcion_transferencia)
            