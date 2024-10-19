from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPixmapItem
from PyQt5.QtGui import QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt
import qtawesome as qta

LINEA_GROSOR = 6
LINEA_COLOR = QColor("#457B9D")
FONDO_CICULO_COLOR = QColor("#A8DADC")
ACLARADO = QColor("#F1FAEE")
LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")

class QGraphicCircleItem(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, icono, metodo, parent=None):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius)
        self.parent = parent
        self.setBrush(QBrush(FONDO_CICULO_COLOR))
        self.setPen(QPen(LINEA_COLOR, LINEA_GROSOR))
        self.setAcceptHoverEvents(True)
        self.metodo = metodo
        # Add gear icon
        icon = qta.icon(icono, color=LINEA_COLOR)
        pixmap = icon.pixmap(int(2 * radius - 4), int(2 * radius - 4))
        self.icon_item = QGraphicsPixmapItem(pixmap, self)
        self.icon_item.setOffset(x - radius + 2, y - radius + 2)

    def set_color(self, color):
        self.setBrush(QBrush(color))

    def set_border_color(self, color):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)

    def set_border_width(self, width):
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(ACLARADO))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(FONDO_CICULO_COLOR))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        print("Circle clicked!")
        self.metodo()
        super().mousePressEvent(event)
