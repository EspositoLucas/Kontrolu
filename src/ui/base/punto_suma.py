import os
from .macro_vista import MacroVista
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, 
    QMenu, 
    QAction, 
    QMessageBox,
    QGraphicsItem, 
    QGraphicsItemGroup,
    QGraphicsPolygonItem,
    QGraphicsLineItem,
    QGraphicsTextItem, 
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
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



        font = QFont()
        font.setBold(True)
        font.setPointSize(10)  # Adjust the size as needed
        self.mas_arriba = QGraphicsTextItem("+")
        self.mas_arriba.setDefaultTextColor(BORDE_COLOR)
        self.mas_arriba.setFont(font)
        text_rect = self.mas_arriba.boundingRect()

        self.mas_arriba.setPos(x_medio - text_rect.width()/1.5-RADIO_PERTURBACION, y_medio - text_rect.height()/1.5-RADIO_PERTURBACION)

        self.mas_izquierda = QGraphicsTextItem("-")
        self.mas_izquierda.setFont(font)
        self.mas_izquierda.setDefaultTextColor(BORDE_COLOR)
        self.mas_izquierda.setPos(x_medio+RADIO_PERTURBACION/2, y_medio)

        self.addToGroup(self.circulo)
        self.addToGroup(self.cruz1)
        self.addToGroup(self.cruz2)
        self.addToGroup(self.mas_arriba)
        self.addToGroup(self.mas_izquierda)
        

        