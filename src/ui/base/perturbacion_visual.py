from PyQt5.QtWidgets import QGraphicsEllipseItem, QMenu, QAction, QMessageBox, QDialog, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QPushButton, QGraphicsItem, QGraphicsSceneContextMenuEvent
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor

ANCHO = 150
ALTO = 80
MARGEN_PERTURBACION = 200
RADIO_PERTURBACION = 10

class PerturbacionVisual(QGraphicsEllipseItem):
    def __init__(self, microbloque, pos, tipo, drawing_area):
        super().__init__()
        self.microbloque = microbloque
        self.posicion = pos
        self.tipo = tipo  # "entrada" o "salida"
        self.drawing_area = drawing_area
        self.setup_apariencia()
        self.setup_tooltip()
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        
    def setup_apariencia(self):
        if self.tipo == "entrada":
            centro = QPointF(self.posicion.x() - ANCHO/2 + MARGEN_PERTURBACION, 
                            self.posicion.y() + ALTO/2)
        else:  # salida
            centro = QPointF(self.posicion.x() + ANCHO/2 + MARGEN_PERTURBACION - 50, 
                            self.posicion.y() + ALTO/2)
        self.centro = centro
        self.setRect(centro.x() - RADIO_PERTURBACION, 
                     centro.y() - RADIO_PERTURBACION, 
                     RADIO_PERTURBACION * 2, 
                     RADIO_PERTURBACION * 2)
        
        self.setBrush(QBrush(QColor(255, 0, 0)))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(1)

    def setup_tooltip(self):
        perturbacion = (self.microbloque.perturbacion_entrada 
                        if self.tipo == "entrada" 
                        else self.microbloque.perturbacion_salida)
        
        tooltip = f"Perturbación de {self.tipo}\n"
        tooltip += f"Función de transferencia: {perturbacion.funcion_transferencia}\n"
        tooltip += f"Ciclos: {perturbacion.ciclos}"
        self.setToolTip(tooltip)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.mostrar_menu_contextual(event)
            event.accept()
        else:
            super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        self.mostrar_menu_contextual(event)
        event.accept()

    def mostrar_menu_contextual(self, event):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #333;
                color: white;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #555;
            }
        """)
        
        eliminar_accion = QAction("Eliminar perturbación")
        eliminar_accion.triggered.connect(self.eliminar_perturbacion)
        menu.addAction(eliminar_accion)
        
        editar_accion = QAction("Editar perturbación")
        editar_accion.triggered.connect(self.editar_perturbacion)
        menu.addAction(editar_accion)
        
        if isinstance(event, QGraphicsSceneContextMenuEvent):
            global_pos = event.screenPos()
        else:  # QMouseEvent
            view = self.scene().views()[0]
            global_pos = view.viewport().mapToGlobal(view.mapFromScene(event.scenePos()))
        
        menu.exec_(global_pos)

    def eliminar_perturbacion(self):
        confirmacion = QMessageBox.question(
            None, 
            "Confirmar eliminación",
            f"¿Está seguro que desea eliminar la perturbación de {self.tipo}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            if self.tipo == "entrada":
                self.microbloque.perturbacion_entrada.cancelar_perturbacion()
            else:
                self.microbloque.perturbacion_salida.cancelar_perturbacion()
            
            self.drawing_area.load_microbloques()

    def editar_perturbacion(self):
        perturbacion = (self.microbloque.perturbacion_entrada 
                        if self.tipo == "entrada" 
                        else self.microbloque.perturbacion_salida)
        
        dialog = QDialog()
        dialog.setWindowTitle(f"Editar Perturbación de {self.tipo}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        ft_label = QLabel("Función de Transferencia:")
        ft_editor = LatexEditor(perturbacion.funcion_transferencia)
        ft_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(ft_label)
        layout.addWidget(ft_editor)

        ciclos_label = QLabel("Cantidad de ciclos de simulación:")
        ciclos_editor = QSpinBox()
        ciclos_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        ciclos_editor.setMinimum(1)
        ciclos_editor.setValue(perturbacion.ciclos)
        layout.addWidget(ciclos_label)
        layout.addWidget(ciclos_editor)

        buttons = QHBoxLayout()
        ok_button = QPushButton("Aceptar")
        ok_button.setStyleSheet("background-color: #444;")
        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("background-color: #444;")
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

        dialog.setLayout(layout)

        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            perturbacion.funcion_transferencia = ft_editor.get_latex()
            perturbacion.ciclos = ciclos_editor.value()
            self.setup_tooltip() 
            self.drawing_area.load_microbloques()

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor(200, 0, 0)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor(255, 0, 0)))
        super().hoverLeaveEvent(event)