
class ElementoBase():
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.representacion = None # ESTA SERÍA LA REPRESENTACIÓN VISUAL DEL ELEMENTO (TODO: VINCULARLO CON LAS CLASES DEFINIDAS EN LA CARPETA "ui")

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"
    