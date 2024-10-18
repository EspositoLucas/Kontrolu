
from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, 
    QGraphicsItemGroup,
    QGraphicsLineItem,
)
from PyQt5.QtGui import QBrush, QColor, QPen
from math import pi, cos, sin

FONDO_COLOR = QColor("#A8DADC")
BORDE_COLOR = QColor("#457B9D")

class PuntoSuma(QGraphicsItemGroup):
    def __init__(self, parent=None,RADIO_PERTURBACION = 10,x_medio = 0, y_medio = 0):
        super().__init__(parent)
        self.circulo = QGraphicsEllipseItem(x_medio - RADIO_PERTURBACION, y_medio - RADIO_PERTURBACION, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.circulo.setBrush(QBrush(FONDO_COLOR))
        self.circulo.setPen(QPen(BORDE_COLOR, 4))
        

        angle = pi / 4
        cruz_cos = RADIO_PERTURBACION * cos(angle)
        cruz_sen = RADIO_PERTURBACION * sin(angle)

        self.cruz1 = QGraphicsLineItem(x_medio - cruz_cos, y_medio - cruz_sen, x_medio + cruz_cos, y_medio + cruz_sen)
        self.cruz2 = QGraphicsLineItem(x_medio - cruz_cos, y_medio + cruz_sen, x_medio + cruz_cos, y_medio - cruz_sen)
        self.cruz1.setPen(QPen(BORDE_COLOR, 4))
        self.cruz2.setPen(QPen(BORDE_COLOR, 4))
        

        cruz_cos_2 = RADIO_PERTURBACION*2 * cos(angle)
        cruz_sen_2 = RADIO_PERTURBACION*2 * sin(angle)

        centro_mas_x = x_medio - cruz_cos_2
        centro_mas_y = y_medio - cruz_sen_2

        centro_menos_x = x_medio + cruz_cos_2
        centro_menos_y = y_medio + cruz_sen_2


        self.mas_horizontal = QGraphicsLineItem(centro_mas_x - RADIO_PERTURBACION/2, centro_mas_y, centro_mas_x + RADIO_PERTURBACION/2, centro_mas_y)
        self.mas_vertical = QGraphicsLineItem(centro_mas_x , centro_mas_y-RADIO_PERTURBACION/2, centro_mas_x , centro_mas_y+RADIO_PERTURBACION/2)
        self.mas_horizontal.setPen(QPen(BORDE_COLOR, 4))
        self.mas_vertical.setPen(QPen(BORDE_COLOR, 4))

        self.menos = QGraphicsLineItem(centro_menos_x-RADIO_PERTURBACION/2, centro_menos_y, centro_menos_x+RADIO_PERTURBACION/2, centro_menos_y)
        self.menos.setPen(QPen(BORDE_COLOR, 4))

        self.addToGroup(self.mas_horizontal)
        self.addToGroup(self.mas_vertical)
        self.addToGroup(self.menos)
        self.addToGroup(self.circulo)
        self.addToGroup(self.cruz1)
        self.addToGroup(self.cruz2)
        

        