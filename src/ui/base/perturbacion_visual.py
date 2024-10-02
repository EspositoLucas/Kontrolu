from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu, QAction, QMessageBox, QDialog, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QPushButton, QGraphicsItem, QGraphicsSceneContextMenuEvent
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor

RADIO_PERTURBACION = 10

class PerturbacionVisual(QGraphicsEllipseItem):
    def __init__(self, perturbacion_back):
        super().__init__(0, 0, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.perturbacion_back = perturbacion_back
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(QColor("#FFD700")))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(1)