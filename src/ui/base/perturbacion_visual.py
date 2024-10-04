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
    QGraphicsTextItem
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor

RADIO_PERTURBACION = 10
LONGITUD_FLECHA = 10

class PerturbacionVisual(QGraphicsItemGroup):
    def __init__(self, perturbacion_back, drawing_area):
        super().__init__()
        self.perturbacion_back = perturbacion_back
        self.drawing_area = drawing_area
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setCursor(Qt.PointingHandCursor)

        self.circulo = QGraphicsEllipseItem(0, 0, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.circulo.setBrush(QBrush(QColor("#FFD700")))
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.eliminar_perturbacion()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setFocus()
            self.editar_perturbacion()
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
    
    def editar_perturbacion(self):
        dialog = QDialog()
        dialog.setWindowTitle("Editar Perturbación")
        layout = QVBoxLayout()

        ft_label = QLabel("Función de Transferencia:")
        ft_editor = LatexEditor()
        ft_editor.set_latex(self.perturbacion_back.funcion_transferencia)
        layout.addWidget(ft_label)
        layout.addWidget(ft_editor)

        ciclos_label = QLabel("Cantidad de ciclos de simulación:")
        ciclos_editor = QSpinBox()
        ciclos_editor.setMinimum(1)
        ciclos_editor.setValue(self.perturbacion_back.ciclos)
        layout.addWidget(ciclos_label)
        layout.addWidget(ciclos_editor)

        dentro_de_label = QLabel("Activar dentro de (ciclos):")
        dentro_de_editor = QSpinBox()
        dentro_de_editor.setMinimum(0)
        dentro_de_editor.setValue(self.perturbacion_back.dentro_de)
        layout.addWidget(dentro_de_label)
        layout.addWidget(dentro_de_editor)

        buttons = QHBoxLayout()
        ok_button = QPushButton("Aceptar")
        cancel_button = QPushButton("Cancelar")
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

        dialog.setStyleSheet("background-color: #333; color: white;")
        dialog.setLayout(layout)

        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            self.perturbacion_back.funcion_transferencia = ft_editor.get_latex()
            self.perturbacion_back.ciclos = ciclos_editor.value()
            self.perturbacion_back.dentro_de = dentro_de_editor.value()
    
    def eliminar_perturbacion(self):
        reply = QMessageBox.question(
            None, 
            "Confirmar eliminación",
            "¿Está seguro que desea eliminar esta perturbación?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.perturbacion_back.borrar_elemento() # elimino la perturbacion de la topologia
            self.scene().removeItem(self)

            self.drawing_area.load_microbloques()