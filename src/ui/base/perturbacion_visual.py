from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, 
    QMenu, 
    QAction, 
    QMessageBox,
    QGraphicsItem, 
    QGraphicsItemGroup,
    QGraphicsPolygonItem,
    QGraphicsLineItem,
    QGraphicsTextItem, 
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import os
from .editar_perturbacion import EditarPerturbacion
from ..base.punto_suma import PuntoSuma
from math import pi, cos, sin


RADIO_PERTURBACION = 10
LONGITUD_FLECHA = 10
VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
LINEA_COLOR = QColor("#457B9D")

class PerturbacionVisual(QGraphicsItemGroup):
    def __init__(self, perturbacion_back, drawing_area):
        super().__init__()
        RADIO_PERTURBACION = 15
        self.perturbacion_back = perturbacion_back
        self.perturbacion_back.set_observer(self)
        self.drawing_area = drawing_area
        self.setAcceptHoverEvents(True)
        self.setZValue(1)

        angle = pi / 4
        x_medio = RADIO_PERTURBACION * cos(angle)
        y_medio = RADIO_PERTURBACION * sin(angle)

        self.color = ROJO

        self.punto_suma = PuntoSuma(self, x_medio=x_medio,y_medio=y_medio,RADIO_PERTURBACION=RADIO_PERTURBACION,izq=2,arriba=2,color_fondo=self.color)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setCursor(Qt.PointingHandCursor)

        puntos_flecha = QPolygonF([
            QPointF(0, 0),  # Punta de la flecha
            QPointF(-5, -10),  # Esquina izquierda
            QPointF(5, -10)   # Esquina derecha
        ])
        self.flecha = QGraphicsPolygonItem(puntos_flecha)
        self.flecha.setBrush(QBrush(LINEA_COLOR))
        self.flecha.setPen(QPen(LINEA_COLOR, 2))
        self.flecha.setPos(x_medio,y_medio-RADIO_PERTURBACION)
        
        self.linea_flecha = QGraphicsPolygonItem(QPolygonF([
            QPointF(x_medio, y_medio-RADIO_PERTURBACION-RADIO_PERTURBACION-RADIO_PERTURBACION),
            QPointF(x_medio,y_medio-RADIO_PERTURBACION)
        ]))
        self.linea_flecha.setPen(QPen(LINEA_COLOR, 4))



        self.addToGroup(self.flecha)
        self.addToGroup(self.linea_flecha)
        self.addToGroup(self.punto_suma)

    def actualizar(self, estado):
        self.color = VERDE if estado else ROJO
        self.punto_suma.actualizar_color(QBrush(self.color))

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
        
        # Agregamos opción para crear microbloque después de la perturbación
        agregar_micro_action_antes = QAction("Agregar microbloque antes", None)
        agregar_micro_action_antes.triggered.connect(lambda: self.drawing_area.create_new_microbloque_pre_perturbacion(self))
        menu.addAction(agregar_micro_action_antes)
        
        # Agregamos opción para crear microbloque después de la perturbación
        agregar_micro_action_despues = QAction("Agregar microbloque después", None)
        agregar_micro_action_despues.triggered.connect(lambda: self.drawing_area.create_new_microbloque_post_perturbacion(self))
        menu.addAction(agregar_micro_action_despues)
        
        eliminar_action = QAction("Eliminar perturbación", None)
        eliminar_action.triggered.connect(self.eliminar_perturbacion)
        menu.addAction(eliminar_action)
        
        # Obtenemos la posición de manera más segura
        if self.scene() and self.scene().views():
            scene_pos = event.scenePos()
            view = self.scene().views()[0]
            screen_pos = view.mapToGlobal(view.mapFromScene(scene_pos))
        else:
            # Si no podemos obtener la posición de la escena, usamos la posición del cursor
            screen_pos = event.screenPos()
        
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
                border-radius: 3px;
            """)

        reply = dialog.exec_()
        
        if reply == QMessageBox.Yes:
            self.perturbacion_back.observer = None
            self.perturbacion_back.borrar_elemento()  # elimino la perturbacion de la topologia
            self.scene().removeItem(self)
            self.drawing_area.load_microbloques()
            
    def hoverEnterEvent(self, event):
        print("hoverEnterEvent")
        self.punto_suma.actualizar_color(QBrush(self.color.lighter(150)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        print("hoverLeaveEvent")
        self.punto_suma.actualizar_color(QBrush(self.color))
        super().hoverLeaveEvent(event)