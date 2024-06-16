
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from .micro_bloque import Microbloque

class DrawingArea(QWidget):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.arrows = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")

    def add_microbloque(self, nombre):
        x_offset = len(self.microbloques) * 110  # Para que no se superpongan
        microbloque = Microbloque(nombre, self)
        microbloque.setGeometry(x_offset, 50, 100, 50)
        self.microbloques.append(microbloque)
        microbloque.show()

    def delete_microbloque(self):
        if self.selected_microbloque:
            self.microbloques.remove(self.selected_microbloque)
            self.selected_microbloque.deleteLater()
            self.selected_microbloque = None
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for arrow in self.arrows:
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(arrow['start'], arrow['end'])

    def mousePressEvent(self, event):
        for microbloque in self.microbloques:
            if microbloque.geometry().contains(event.pos()):
                self.selected_microbloque = microbloque
                break

    def add_arrow(self, start, end):
        self.arrows.append({'start': start, 'end': end})
        self.update()

    def delete_arrow(self):
        if self.arrows:
            self.arrows.pop()
            self.update()