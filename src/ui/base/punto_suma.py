
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
    def __init__(self, parent=None,RADIO_PERTURBACION = 10,x_medio = 0, y_medio = 0,izq = 0,derecha = 0,arriba =0,abajo=0,color_linea = BORDE_COLOR,color_fondo = FONDO_COLOR):
        super().__init__(parent)

        ANCHO_SIGNOS = (RADIO_PERTURBACION/20)*3
        ANCHO_LINEA = RADIO_PERTURBACION/5

        self.circulo = QGraphicsEllipseItem(x_medio - RADIO_PERTURBACION, y_medio - RADIO_PERTURBACION, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.circulo.setBrush(QBrush(color_fondo))
        self.circulo.setPen(QPen(color_linea, ANCHO_LINEA))
        
        angle = pi / 4
        cruz_cos = RADIO_PERTURBACION * cos(angle)
        cruz_sen = RADIO_PERTURBACION * sin(angle)

        self.cruz1 = QGraphicsLineItem(x_medio - cruz_cos, y_medio - cruz_sen, x_medio + cruz_cos, y_medio + cruz_sen)
        self.cruz2 = QGraphicsLineItem(x_medio - cruz_cos, y_medio + cruz_sen, x_medio + cruz_cos, y_medio - cruz_sen)
        self.cruz1.setPen(QPen(color_linea, ANCHO_LINEA))
        self.cruz2.setPen(QPen(color_linea, ANCHO_LINEA))
        
        self.addToGroup(self.circulo)
        self.addToGroup(self.cruz1)
        self.addToGroup(self.cruz2)


        if izq:
            x_medio_izq = x_medio - RADIO_PERTURBACION/1.75
            y_medio_izq = y_medio

            menos_izq = QGraphicsLineItem(x_medio_izq-RADIO_PERTURBACION/5, y_medio_izq, x_medio_izq+RADIO_PERTURBACION/5, y_medio_izq)
            menos_izq.setPen(QPen(color_linea, ANCHO_SIGNOS))

            self.addToGroup(menos_izq)
            if izq>1:
                mas_izq = QGraphicsLineItem(x_medio_izq, y_medio_izq-RADIO_PERTURBACION/5, x_medio_izq, y_medio_izq+RADIO_PERTURBACION/5)
                mas_izq.setPen(QPen(color_linea, ANCHO_SIGNOS))
                self.addToGroup(mas_izq)

        if derecha:
            x_medio_der = x_medio + RADIO_PERTURBACION/1.75
            y_medio_der = y_medio

            menos_der = QGraphicsLineItem(x_medio_der-RADIO_PERTURBACION/5, y_medio_der, x_medio_der+RADIO_PERTURBACION/5, y_medio_der)
            menos_der.setPen(QPen(color_linea, ANCHO_SIGNOS))

            self.addToGroup(menos_der)
            if derecha>1:
                mas_der = QGraphicsLineItem(x_medio_der, y_medio_der-RADIO_PERTURBACION/5, x_medio_der, y_medio_der+RADIO_PERTURBACION/5)
                mas_der.setPen(QPen(color_linea, ANCHO_SIGNOS))
                self.addToGroup(mas_der)
        
        if arriba:
            x_medio_arriba = x_medio
            y_medio_arriba = y_medio - RADIO_PERTURBACION/1.75

            menos_arriba = QGraphicsLineItem(x_medio_arriba-RADIO_PERTURBACION/5, y_medio_arriba, x_medio_arriba+RADIO_PERTURBACION/5, y_medio_arriba)
            menos_arriba.setPen(QPen(color_linea, ANCHO_SIGNOS))

            self.addToGroup(menos_arriba)
            if arriba>1:
                mas_arriba = QGraphicsLineItem(x_medio_arriba, y_medio_arriba-RADIO_PERTURBACION/5, x_medio_arriba, y_medio_arriba+RADIO_PERTURBACION/5)
                mas_arriba.setPen(QPen(color_linea, ANCHO_SIGNOS))
                self.addToGroup(mas_arriba)
        
        if abajo:
            x_medio_abajo = x_medio
            y_medio_abajo = y_medio + RADIO_PERTURBACION/1.75

            menos_abajo = QGraphicsLineItem(x_medio_abajo-RADIO_PERTURBACION/5, y_medio_abajo, x_medio_abajo+RADIO_PERTURBACION/5, y_medio_abajo)
            menos_abajo.setPen(QPen(color_linea, ANCHO_SIGNOS))

            self.addToGroup(menos_abajo)
            if abajo>1:
                mas_abajo = QGraphicsLineItem(x_medio_abajo, y_medio_abajo-RADIO_PERTURBACION/5, x_medio_abajo, y_medio_abajo+RADIO_PERTURBACION/5)
                mas_abajo.setPen(QPen(color_linea, ANCHO_SIGNOS))
                self.addToGroup(mas_abajo)

    def actualizar_color(self, color):
        self.circulo.setBrush(color)
        self.update()
        