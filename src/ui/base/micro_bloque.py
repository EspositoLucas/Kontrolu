
from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QFrame
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QSize
from back.micros.micro_bloque_back import MicroBloqueBack

class ResizeHandle(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 10, 10)
        self.setStyleSheet("background-color: blue;")

class Microbloque(QWidget):
    def __init__(self, nombre, parent=None, color=None):
        super().__init__(parent)
        self.nombre = nombre
        self.color = color or QColor(255, 255, 0)  # Amarillo por defecto si no se proporciona color
        self.setGeometry(50, 50, 100, 50)  # Geometría por defecto
        self.setMouseTracking(True)
        self.is_resizing = False
        self.is_moving = False
        self.last_mouse_pos = None
        self.micro_back = MicroBloqueBack(parent.modelo, nombre)  # Pasamos el nombre aquí

        # Añadir handles para redimensionar
        self.handles = {
            'bottom_right': ResizeHandle(self)
        }
        self.update_handles()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(self.color)
        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignCenter, self.nombre)

    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog.getText(self, 'Editar nombre', 'Nuevo nombre:', QLineEdit.Normal, self.nombre)
        if ok and text:
            self.nombre = text
            self.micro_back.nombre = text  # Actualizar también el nombre en el backend
            self.update()
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.is_moving = True

            for handle in self.handles.values():
                if handle.geometry().contains(event.pos()):
                    self.is_resizing = True
                    self.is_moving = False
                    break

    def mouseMoveEvent(self, event):
        if self.is_moving:
            delta = event.pos() - self.last_mouse_pos
            self.move(self.pos() + delta)
        elif self.is_resizing:
            delta = event.pos() - self.last_mouse_pos
            new_size = self.size() + QSize(delta.x(), delta.y())
            self.resize(new_size)
            self.update_handles()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_moving = False
        self.is_resizing = False

    def update_handles(self):
        # Actualizar la posición de los handles para redimensionar
        self.handles['bottom_right'].move(self.width() - 10, self.height() - 10)