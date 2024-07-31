from back.configuracion.configuracion import Configuracion, EfectoConfiguracion

class ConfiguracionMicrobloque:
    def __init__(self):
        self.configuraciones = {}

    def agregar_configuracion(self, nombre, tipo, valor_por_defecto, efecto):
        self.configuraciones[nombre] = Configuracion(nombre, tipo, valor_por_defecto, efecto)

    def set_configuracion(self, nombre, valor):
        if nombre in self.configuraciones:
            self.configuraciones[nombre].set_valor(valor)

    def actualizar_configuracion(self, nombre_viejo, nombre_nuevo, tipo_nuevo, valor_nuevo, efecto_nuevo):
        configuracion_a_actualizar = self.configuraciones.pop(nombre_viejo)
        configuracion_a_actualizar.actualizar_configuracion(nombre_nuevo, tipo_nuevo, valor_nuevo, efecto_nuevo)
        self.configuraciones[nombre_nuevo] = configuracion_a_actualizar

    def get_configuracion(self, nombre):
        return self.configuraciones.get(nombre)

    def aplicar_efecto(self, funcion_transferencia):
        for configuracion in self.configuraciones.values():
            configuracion.aplicar_efecto(funcion_transferencia)
            