from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QColor



VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFD700")  # Un amarillo brillante

# Colores aclarados al 150%
VERDE_ACLARADO = VERDE.lighter(150)
ROJO_ACLARADO = ROJO.lighter(150)
AMARILLO_ACLARADO = AMARILLO.lighter(150)

class EstabilidadTexto(QGraphicsTextItem):

    def __init__(self, parent=None):

        super().__init__(parent)