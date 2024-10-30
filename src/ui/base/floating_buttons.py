from PyQt5 import QtWidgets, QtGui, QtCore
from ..base.boton_circulo import QGraphicCircleItem

class FloatingButtons(QtWidgets.QGraphicsView):
    def __init__(self, parent=None,padre=None):
        super().__init__(parent)
        self.padre = padre
        self.setStyleSheet("background: transparent;")  # Fondo transparente
        self.setFrameShape(QtWidgets.QFrame.NoFrame)  # Sin bordes
        self.setRenderHints(QtGui.QPainter.Antialiasing)  # Suavizar bordes
        
        # Crear una escena para la vista de elipses
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.set_buttons()

    def set_buttons(self):
        RADIO_C = 40
        scene_width = self.scene.width()
        scene_height = self.scene.height()
        y = scene_height-RADIO_C*9

        self.clear_button = QGraphicCircleItem(RADIO_C*3, y, RADIO_C, 'fa5s.trash-alt', self.padre.clear_all, self,message='Limpiar todo')
        self.scene.addItem(self.clear_button)
        self.select_button = QGraphicCircleItem(RADIO_C*6, y, RADIO_C, 'fa5s.mouse-pointer', self.padre.set_seleccion_multiple, self,toggle = True,message='Seleccionar varios microbloques')
        self.scene.addItem(self.select_button)
        self.json_button = QGraphicCircleItem(RADIO_C*9, y, RADIO_C, 'fa5s.file-code', self.padre.vista_json, self,message='Editar JSON')
        self.scene.addItem(self.json_button)
        self.help_button = QGraphicCircleItem(RADIO_C*12, y, RADIO_C, 'fa5s.question-circle', self.padre.show_help, self,message='Ayuda')
        self.scene.addItem(self.help_button)
