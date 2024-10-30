from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont



VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFD700")  # Un amarillo brillante


# Colores aclarados al 150%
VERDE_ACLARADO = VERDE.lighter(150)
ROJO_ACLARADO = ROJO.lighter(150)
AMARILLO_ACLARADO = AMARILLO.lighter(150)

class EstabilidadTexto(QGraphicsTextItem):

    def __init__(self, sesion, parent=None):

        super().__init__(parent)

        self.sesion = sesion

        self.default_color = AMARILLO

        self.hoover_color = AMARILLO_ACLARADO

        self.update_text()

        font = QFont("Arial", 30, QFont.Bold)

        self.setFont(font)

        self.setAcceptHoverEvents(True)


        


    def update_text(self):

        estado =  self.sesion.calcular_estabilidad()        

        if estado == "ESTABLE":
            self.setPlainText("Estable")
            self.setDefaultTextColor(VERDE)
            self.default_color = VERDE
            self.hoover_color = VERDE_ACLARADO
        elif estado == "INESTABLE":
            self.setPlainText("Inestable")
            self.setDefaultTextColor(ROJO)
            self.default_color = ROJO
            self.hoover_color = ROJO_ACLARADO
        else:
            self.setPlainText("Criticamente Estable")
            self.setDefaultTextColor(AMARILLO)
            self.default_color = AMARILLO
            self.hoover_color = AMARILLO_ACLARADO

        self.update()
    
    def hoverEnterEvent(self, event):
        self.setDefaultTextColor(self.hoover_color)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(self.default_color)
        self.update()