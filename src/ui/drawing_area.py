from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QPoint, QLineF
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt

from .base.elemento_control import ElementoControl
from .base.elemento_correccion import ElementoCorreccion
from .base.elemento_proceso import Proceso
from .base.elemento_medicion import ElementoMedicion

class DrawingArea(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.current_arrow = None
        self.drawing_shape = False
        self.shape_type = None
        self.start_point = None
        self.init_base_elements()

    def drawBackground(self, painter, rect):
        gridPen = QPen(Qt.gray, 1, Qt.DashLine)
        painter.setPen(gridPen)

        # Dibujar líneas horizontales
        left = int(rect.left())
        right = int(rect.right())
        y = rect.top()
        while y <= rect.bottom():
            painter.drawLine(QLineF(left, y, right, y))
            y += 20  # Ajusta el espaciado de la cuadrícula según tus necesidades

        # Dibujar líneas verticales
        top = int(rect.top())
        bottom = int(rect.bottom())
        x = rect.left()
        while x <= rect.right():
            painter.drawLine(QLineF(x, top, x, bottom))
            x += 20  # Ajusta el espaciado de la cuadrícula según tus necesidades

    def drawForeground(self, painter, rect):
        self.drawBackground(painter, rect)

    def init_base_elements(self):
        control = ElementoControl(QPoint(50, 50), QPoint(150, 100))
        self.addShape(control)
        correccion = ElementoCorreccion(QPoint(200, 50), QPoint(300, 100))
        self.addShape(correccion)
        proceso = Proceso(QPoint(350, 50), QPoint(450, 100))
        self.addShape(proceso)
        medicion = ElementoMedicion(QPoint(500, 50), QPoint(600, 100))
        self.addShape(medicion)

    def addShape(self, shape):
        self.addItem(shape)

    def clear(self):
        for shape in self.shapes:
            self.removeItem(shape)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.shapes:
            shape.draw(painter)
