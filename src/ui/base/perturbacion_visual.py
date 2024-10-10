from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, 
    QMenu, 
    QAction, 
    QMessageBox, 
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QSpinBox, 
    QHBoxLayout, 
    QPushButton, 
    QGraphicsItem, 
    QGraphicsItemGroup,
    QGraphicsPolygonItem,
    QGraphicsLineItem,
    QGraphicsTextItem, QCheckBox
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import os
from .latex_editor import LatexEditor
from .editar_perturbacion import EditarPerturbacion

RADIO_PERTURBACION = 10
LONGITUD_FLECHA = 10

class PerturbacionVisual(QGraphicsItemGroup):
    def __init__(self, perturbacion_back, drawing_area):
        super().__init__()
        self.perturbacion_back = perturbacion_back
        self.perturbacion_back.set_observer(self)
        self.drawing_area = drawing_area
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setCursor(Qt.PointingHandCursor)

        self.circulo = QGraphicsEllipseItem(0, 0, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.circulo.setBrush(QBrush(QColor("#FF0000")))
        self.circulo.setPen(QPen(Qt.black, 2))
        
        self.cruz1 = QGraphicsLineItem(4, 4, 2 * RADIO_PERTURBACION - 4, 2 * RADIO_PERTURBACION - 4)
        self.cruz2 = QGraphicsLineItem(4, 2 * RADIO_PERTURBACION - 4, 2 * RADIO_PERTURBACION - 4, 4)
        self.cruz1.setPen(QPen(Qt.black, 2))
        self.cruz2.setPen(QPen(Qt.black, 2))

        puntos_flecha = QPolygonF([
            QPointF(0, 0),  # Punta de la flecha
            QPointF(-5, -10),  # Esquina izquierda
            QPointF(5, -10)   # Esquina derecha
        ])
        self.flecha = QGraphicsPolygonItem(puntos_flecha)
        self.flecha.setBrush(QBrush(Qt.black))
        self.flecha.setPen(QPen(Qt.black, 2))
        self.flecha.setPos(RADIO_PERTURBACION, -LONGITUD_FLECHA + RADIO_PERTURBACION)
        
        self.linea_flecha = QGraphicsPolygonItem(QPolygonF([
            QPointF(RADIO_PERTURBACION, -2 * RADIO_PERTURBACION - LONGITUD_FLECHA),
            QPointF(RADIO_PERTURBACION, 0)
        ]))
        self.linea_flecha.setPen(QPen(Qt.black, 2))

        font = QFont()
        font.setBold(True)
        self.mas_arriba = QGraphicsTextItem("+")
        self.mas_arriba.setFont(font)
        self.mas_arriba.setPos(RADIO_PERTURBACION - 15, -2 * RADIO_PERTURBACION - LONGITUD_FLECHA)
        self.mas_izquierda = QGraphicsTextItem("+")
        self.mas_izquierda.setFont(font)
        self.mas_izquierda.setPos(-13, RADIO_PERTURBACION - 5)

        self.addToGroup(self.circulo)
        self.addToGroup(self.cruz1)
        self.addToGroup(self.cruz2)
        self.addToGroup(self.flecha)
        self.addToGroup(self.linea_flecha)
        self.addToGroup(self.mas_arriba)
        self.addToGroup(self.mas_izquierda)

    def actualizar(self, estado):
        color = QColor("#00FF00") if estado else QColor("#FF0000")
        self.circulo.setBrush(QBrush(color))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.eliminar_perturbacion()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setFocus()
            EditarPerturbacion(self.drawing_area, self.perturbacion_back).exec_()
        elif event.button() == Qt.RightButton:
            self.mostrar_menu_contextual(event)
        super().mousePressEvent(event)
    
    def mostrar_menu_contextual(self, event):
        menu = QMenu()
        eliminar_action = QAction("Eliminar perturbación", None)
        eliminar_action.triggered.connect(self.eliminar_perturbacion)
        menu.addAction(eliminar_action)
        
        scene_pos = event.scenePos()
        view = self.scene().views()[0]
        screen_pos = view.mapToGlobal(view.mapFromScene(scene_pos))
        menu.exec_(screen_pos)
           

    def eliminar_perturbacion(self):
        dialog = QMessageBox(None)
        dialog.setWindowTitle('Confirmar eliminación')
        dialog.setText('¿Está seguro que desea eliminar esta perturbación?')
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
        # Establecer el estilo de la ventana
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #333;
                color: white;
            }
            
            QMessageBox QLabel {
                color: white;
                background-color: black;
                padding: 10px;
            }
        """)
        
        # Cambiar el texto del botón "Yes" a "Si"
        yes_button = dialog.button(QMessageBox.Yes)
        if yes_button:
            yes_button.setText("Si")

        # Aplicar estilo a los botones específicos
        for button in dialog.buttons():
            button.setStyleSheet("""
                background-color: black;
                color: white;
                min-width: 80px;
                min-height: 30px;
                border: none;
            """)

        reply = dialog.exec_()
        
        if reply == QMessageBox.Yes:
            self.perturbacion_back.observer = None
            self.perturbacion_back.borrar_elemento()  # elimino la perturbacion de la topologia
            self.scene().removeItem(self)
            self.drawing_area.load_microbloques()
            
        