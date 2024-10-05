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
        print("EDITAR")
        dialog = QDialog()
        dialog.setWindowTitle("Editar Perturbación")
        layout = QVBoxLayout()

        # Tengo que cargar dos cosas: la función de transferencia y la cantidad de ciclos de simulación que va a durar la perturbación
        ft_label = QLabel("Función de Transferencia:")
        ft_label.setStyleSheet("color: white;")
        ft_editor = LatexEditor(self.perturbacion_back.funcion_transferencia)
        ft_editor.set_latex("1")
        ft_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(ft_label)
        layout.addWidget(ft_editor)

        # Checkbox para "Perturbar ahora"
        perturbar_ahora_checkbox = QCheckBox("Perturbar ahora")
        perturbar_ahora_checkbox.setChecked(self.perturbacion_back.ahora)
        perturbar_ahora_checkbox.setStyleSheet("color: white;")
        layout.addWidget(perturbar_ahora_checkbox)

        # Editor de inicio de ciclos
        ciclos = QLabel("Tiempo de inicio (s):")
        ciclos.setStyleSheet("color: white;")
        ciclos_editor = QSpinBox()
        ciclos_editor.setValue(self.perturbacion_back.inicio)
        ciclos_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        ciclos_editor.setMinimum(0)
        layout.addWidget(ciclos)
        layout.addWidget(ciclos_editor)

        # Editor de duración
        dentro_de_label = QLabel("Duración (s):")
        dentro_de_editor = QSpinBox()
        dentro_de_editor.setValue(self.perturbacion_back.duracion)
        dentro_de_editor.setMinimum(0)
        dentro_de_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(dentro_de_label)
        layout.addWidget(dentro_de_editor)

        # Conectar el checkbox para ocultar/mostrar el editor de inicio
        def toggle_inicio_editor():
            ciclos.setVisible(not perturbar_ahora_checkbox.isChecked())
            ciclos_editor.setVisible(not perturbar_ahora_checkbox.isChecked())

        # Conectar el checkbox a la función para que oculte el editor de inicio
        perturbar_ahora_checkbox.stateChanged.connect(toggle_inicio_editor)
        toggle_inicio_editor()  # Para que se oculte/visualice según el estado inicial del checkbox

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
            print("MODIFICO")
            self.perturbacion_back.set_funcion_transferencia(ft_editor.get_latex())
            ahora = perturbar_ahora_checkbox.isChecked()
            inicio = ciclos_editor.value()
            duracion = dentro_de_editor.value()
            self.perturbacion_back.set_valores(inicio, duracion, ahora)
    
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