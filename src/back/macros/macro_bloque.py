from src.back.topologia.topologia_serie import TopologiaSerie

class MacroBloque():
    
    def __init__(self):
        self.topologia = TopologiaSerie()
        self.nombre = "MacroBloque"
        self.representacion = None # ESTA SERÍA LA REPRESENTACIÓN VISUAL DEL ELEMENTO (TODO: VINCULARLO CON LAS CLASES DEFINIDAS EN LA CARPETA "ui")

    def __str__(self):
        return f"{self.nombre}"
    