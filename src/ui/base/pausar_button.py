import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QWidget,QStyle
from .drawing_area import DrawingArea
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor, QFont,QFontMetrics
from PyQt5.QtCore import Qt, QRectF
import qtawesome as qta
import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem


LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")
VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFCC66")



class BotonPausar(QGraphicsRectItem):
    def __init__(self, pos, parent):
        self.parent = parent
        qrect = pos
        super().__init__(qrect)

        self.fondo_simular = AMARILLO
        self.borde_simular = AMARILLO.darker(150)
        self.fondo_claro = AMARILLO.lighter(150)
        self.color_texto = LETRA_COLOR

        self.hover_brush = QBrush(self.fondo_claro)  # Fondo aclarado al pasar el mouse
        self.default_brush = QBrush(self.fondo_simular)

        self.borde_pen = QPen(self.borde_simular, 4)  # Borde azul con grosor de 4px

        self.setBrush(self.default_brush)  # Fondo amarillo suave
        self.setPen(self.borde_pen)  # Borde más oscuro
        self.setRect(qrect)  # Establecer el tamaño del rectángulo

        self.text = "PAUSAR"
        self.font = QFont("Arial", 32, QFont.Bold)  # Estilo del texto
        self.setAcceptHoverEvents(True)

        # Crear el icono de QtAwesome como pixmap
        self.icon = qta.icon('fa5s.pause').pixmap(48, 48)  # Tamaño del ícono en 64x64 px

    def paint(self, painter, option, widget=None):
        # Dibujar un rectángulo con esquinas redondeadas
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Dibujar el texto centrado en los primeros 3/4 del rectángulo
        painter.setFont(self.font)
        painter.setPen(self.color_texto)  # Color del texto
        margin = 10  # Margen entre el texto y las paredes del rectángulo
        text_rect = QRectF(self.rect().left() + margin, self.rect().top(), self.rect().width() * 0.75 - margin, self.rect().height())
        painter.drawText(text_rect, Qt.AlignCenter, self.text)

        # Dibujar el icono en el último 1/4 del rectángulo
        icon_x = self.rect().left() + self.rect().width() * 0.75  # Inicio del último 1/4
        icon_y = (self.rect().height() - self.icon.height()) / 2 + self.rect().top()  # Centrando verticalmente
        painter.drawPixmap(int(icon_x), int(icon_y), self.icon)  # Dibujar el ícono

    def hoverEnterEvent(self, event):
        # Cambia el fondo al pasar el mouse sobre el rectángulo
        self.setBrush(self.hover_brush)
        self.update()  # Actualizar el rectángulo para que se vea el cambio

    def hoverLeaveEvent(self, event):
        # Restaura el fondo original cuando el mouse sale del rectángulo
        self.setBrush(self.default_brush)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("esperar")
            self.parent.pausar_button()
