from .macro_vista import MacroVista

class ElementoMedicion(MacroVista):
    def __init__(self, medicion):
        MacroVista.__init__(self, medicion, (370, 280), (121, 41))

    # TODO: Agregar funcionalidad propia del elemento "Medicion" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
