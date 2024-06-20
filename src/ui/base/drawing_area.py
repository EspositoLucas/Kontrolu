from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from .micro_bloque import Microbloque

class DrawingArea(QWidget):
    microbloque_created = pyqtSignal(Microbloque)

    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.arrows = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")

    def start_creating_microbloque(self, config):
        self.creating_microbloque = True
        self.new_microbloque_config = config
        self.setCursor(Qt.CrossCursor)

    def add_microbloque(self, pos):
        nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
        color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)  # Amarillo por defecto
        microbloque = Microbloque(nombre, self, color)
        microbloque.setGeometry(pos.x() - 50, pos.y() - 25, 100, 50)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.microbloque_created.emit(microbloque)
        
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
        if self.creating_microbloque:
            self.add_microbloque(event.pos())
            self.creating_microbloque = False
            self.setCursor(Qt.ArrowCursor)
        else:
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
