from .macro_vista import MacroVista

class ElementoProceso(MacroVista):
    def __init__(self, medidor):
        MacroVista.__init__(self, medidor, (520, 210), (121, 41))

    # TODO: Agregar funcionalidad propia del elemento "Proceso" al metodo "click" (ej: barra de elementos, etc.)
    # (la funcionalidad general para todos los macrobloques DEBE QUEDAR en MACRO VISTA)
