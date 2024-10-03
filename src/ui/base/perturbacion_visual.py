from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu, QAction, QMessageBox, QDialog, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QPushButton, QGraphicsItem, QGraphicsSceneContextMenuEvent
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor

RADIO_PERTURBACION = 10

class PerturbacionVisual(QGraphicsEllipseItem):
    def __init__(self, perturbacion_back, drawing_area):
        super().__init__(0, 0, 2 * RADIO_PERTURBACION, 2 * RADIO_PERTURBACION)
        self.perturbacion_back = perturbacion_back
        self.drawing_area = drawing_area
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(QColor("#FFD700")))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
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