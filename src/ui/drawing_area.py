from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

from .base.elemento_base import ElementoBase
from .base.elemento_control import ElementoControl
from .base.elemento_correccion import ElementoCorreccion
from .base.elemento_proceso import Proceso
from .base.elemento_medicion import ElementoMedicion

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.current_arrow = None
        self.drawing_shape = False
        self.shape_type = None
        self.start_point = None
        self.init_base_elements()

    def init_base_elements(self):
        self.shapes.append(ElementoControl(QPoint(50, 50), QPoint(150, 100)))
        self.shapes.append(ElementoCorreccion(QPoint(200, 50), QPoint(300, 100)))
        self.shapes.append(Proceso(QPoint(350, 50), QPoint(450, 100)))
        self.shapes.append(ElementoMedicion(QPoint(500, 50), QPoint(600, 100)))

    def clear(self):
        self.shapes = [shape for shape in self.shapes if isinstance(shape, ElementoBase)]
        self.update()

