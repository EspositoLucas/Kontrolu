from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QFont, QPen, QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem

class AddButton(QGraphicsRectItem):
    def __init__(self, x, y, width, height, direction, parent=None):
        super().__init__(x, y, width, height, parent)
        self.direction = direction
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(2)

        # Añadir el símbolo "+"
        self.text = QGraphicsTextItem("+", self)
        self.text.setFont(QFont("Arial", int(min(width, height) * 0.5)))
        self.text.setDefaultTextColor(QColor(Qt.black))
        self.center_text()

    def center_text(self):
        text_rect = self.text.boundingRect()
        button_rect = self.rect()
        x = (button_rect.width() - text_rect.width()) / 2
        y = (button_rect.height() - text_rect.height()) / 2
        self.text.setPos(self.rect().left() + x, self.rect().top() + y)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        drawing_area = self.scene().views()[0]
        drawing_area.show_add_menu(self.direction, event.scenePos())