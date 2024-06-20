from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QCursor, QPalette, QColor
from PyQt5.QtCore import Qt, QPoint, QSize
from .micro_bloque import Microbloque

class DrawingArea(QWidget):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.arrows = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.deleting_microbloque = False
        self.init_ui()

    def init_ui(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.lightGray))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def add_microbloque(self, nombre):
        x_offset = len(self.microbloques) * 110
        microbloque = Microbloque(nombre, self)
        microbloque.setGeometry(x_offset, 50, 100, 50)
        self.microbloques.append(microbloque)
        microbloque.show()

    def delete_microbloque(self, microbloque):
        if microbloque in self.microbloques:
            self.microbloques.remove(microbloque)
            microbloque.deleteLater()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for arrow in self.arrows:
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(arrow['start'], arrow['end'])

    def mousePressEvent(self, event):
        if self.deleting_microbloque:
            microbloque_to_delete = None
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(event.pos()):
                    microbloque_to_delete = microbloque
                    break

            if microbloque_to_delete:
                self.delete_microbloque(microbloque_to_delete)
        else:
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(event.pos()):
                    self.selected_microbloque = microbloque
                    break

    def add_arrow(self,start_microbloque, end_microbloque):
        start = start_microbloque.pos() + QPoint(50, 25)
        end = end_microbloque.pos() + QPoint(50, 25)
        self.arrows.append({'start': start, 'end': end, 'start_microbloque': start_microbloque, 'end_microbloque': end_microbloque})
        self.update()

    def delete_arrow(self):
        if self.arrows:
            self.arrows.pop()
            self.update()

    def clear_all(self):
        while self.microbloques:
            microbloque = self.microbloques.pop()
            microbloque.deleteLater()

        self.arrows.clear()
        self.update()

    def set_deleting_microbloque(self, deleting):
        self.deleting_microbloque = deleting
        if deleting:
            self.setCursor(QCursor(Qt.CrossCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
    
    def update_arrows(self, microbloque):
        for arrow in self.arrows:
            if arrow['start_microbloque'] == microbloque:
                arrow['start'] = microbloque.pos() + QPoint(50, 25)
            if arrow['end_microbloque'] == microbloque:
                arrow['end'] = microbloque.pos() + QPoint(50, 25)
        self.update()
