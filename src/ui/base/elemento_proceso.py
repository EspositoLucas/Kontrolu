from PyQt5.QtCore import QRectF
from .elemento_base import ElementoBase

class Proceso(ElementoBase):
    def draw(self, painter):
        painter.drawRect(QRectF(self.start, self.end))