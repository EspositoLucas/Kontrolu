from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPixmapItem
from PyQt5.QtGui import QBrush, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt
import qtawesome as qta

LINEA_GROSOR = 6
LINEA_COLOR = QColor("#A9A9A9")
FONDO_CICULO_COLOR = QColor("#D3D3D3")
ACLARADO = FONDO_CICULO_COLOR.lighter(150)
LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")

class QGraphicCircleItem(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, icono, metodo, parent=None,toggle=False, message=None,menu=None):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius)
        self.parent = parent
        self.brush_claro = QBrush(ACLARADO)
        self.brush_normal = QBrush(FONDO_CICULO_COLOR)
        self.default_brush = self.brush_normal
        self.setBrush(self.default_brush)
        self.setPen(QPen(LINEA_COLOR, LINEA_GROSOR))
        self.setAcceptHoverEvents(True)
        self.metodo = metodo
        self.toggle = toggle
        # Add gear icon
        icon = qta.icon(icono, color=LINEA_COLOR)
        pixmap = icon.pixmap(int(2 * radius - 4), int(2 * radius - 4))
        self.icon_item = QGraphicsPixmapItem(pixmap, self)
        self.icon_item.setOffset(x - radius + 2, y - radius + 2)
        self.selected = False
        self.message = message
        self.menu= menu

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
        self.setBrush(self.brush_claro)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.default_brush)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if self.menu is not None:
            # Si tiene un menú asociado, lo muestra
            self.menu.exec_(event.screenPos())
        elif self.toggle:
            # Código existente para toggle
            if self.selected:
                self.selected = False
                self.default_brush = self.brush_normal
                self.setBrush(self.default_brush)
            else:
                self.selected = True
                self.default_brush = self.brush_claro
                self.setBrush(self.default_brush)
            self.metodo(self.selected)
        else:
            # Código existente para otros casos
            self.metodo()
        super().mousePressEvent(event)
    
    def hoverMoveEvent(self, event):
        # Cambia el cursor a una mano al pasar el mouse sobre el rectángulo
        self.setCursor(Qt.PointingHandCursor)
        if self.message:
            self.setToolTip(self.message)
    
    def show_popup_menu(self, menu, event):
        pos = event.screenPos()
        menu.exec_(pos)
