from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import Qt

class Proceso(QGraphicsRectItem):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end
        self.draw()

    def draw(self):
        rect = QRectF(self.start, self.end)
        self.setRect(rect)
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.white)
        self.setPen(pen)
        self.setBrush(brush)