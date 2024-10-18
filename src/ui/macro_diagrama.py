
from PyQt5 import QtWidgets, QtCore
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.elemento_entrada import ElementoEntrada
from .base.elemento_carga import ElementoCarga
from .base.punto_suma import PuntoSuma
from .base.flecha import Flecha
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsTextItem, QGroupBox, QVBoxLayout, QPushButton,QGraphicsView,QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRectF
from .base.simular_button import BotonSimular
from .base.pausar_button import BotonPausar
from .base.detener_button import BotonDetener

#DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL = 75
#DISTANCIA_ENTRE_ELEMENTOS_VERTICAL = 32.5
#ANCHO_ELEMENTO = 150
#ALTO_ELEMENTO = 65
#X_MEDIO = 430.5
#Y_MEDIO = 210
#DISTANCIA_HORIZONTAL_EXTRA = 75+37.5
DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL = 75
DISTANCIA_ENTRE_ELEMENTOS_VERTICAL = 32.5
ANCHO_ELEMENTO = 150
ALTO_ELEMENTO = 65
X_MEDIO = 100
Y_MEDIO = 50
DISTANCIA_HORIZONTAL_EXTRA = (75+37.5)
LETRA_COLOR = QColor("#2B2D42")

class MacroDiagrama(QGraphicsView):

    def __init__(self, mainWindow):
        super().__init__()
        self.main_window = mainWindow

        self.sesion = mainWindow.sesion
        self.setup_scene()

    def setup_scene(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Establecer los límites de la escena
        self.scene.setSceneRect(0, 0, 1600, 1000)

        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        # Calcular el medio de la QGraphicsScene
        scene_rect = self.sceneRect()
        self.ANCHO_TOTAL = scene_rect.width()
        self.ALTO_TOTAL = scene_rect.height()
        self.X_MEDIO = scene_rect.width() / 2
        self.Y_MEDIO = scene_rect.height() / 2
        # ACTUADOR
        x_actuador = self.X_MEDIO - ANCHO_ELEMENTO / 2
        y_actuador = self.Y_MEDIO
        pos_act = QRectF(x_actuador, y_actuador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        actuador = ElementoActuador(self.sesion.actuador, pos_act)
        self.scene.addItem(actuador)

        # CONTROLADOR
        x_controlador = x_actuador - DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL - ANCHO_ELEMENTO
        y_controlador = self.Y_MEDIO
        pos_con = QRectF(x_controlador, y_controlador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        controlador = ElementoControl(self.sesion.controlador, pos_con)
        self.scene.addItem(controlador)

        # ENTRADA
        x_entrada = x_controlador - DISTANCIA_HORIZONTAL_EXTRA - ANCHO_ELEMENTO
        y_entrada = self.Y_MEDIO
        pos_ent = QRectF(x_entrada, y_entrada, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        entrada = ElementoEntrada(self.sesion.entrada, pos_ent)
        self.scene.addItem(entrada)

        # PROCESO
        x_proceso = self.X_MEDIO + ANCHO_ELEMENTO / 2 + DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL
        y_proceso = self.Y_MEDIO
        pos_pro = QRectF(x_proceso, y_proceso, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        proceso = ElementoProceso(self.sesion.proceso, pos_pro)
        self.scene.addItem(proceso)

        # MEDIDOR
        x_medidor = x_actuador
        y_medidor = self.Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL
        pos_med = QRectF(x_medidor, y_medidor, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        medidor = ElementoMedicion(self.sesion.medidor, pos_med)
        self.scene.addItem(medidor)

        # CARGA
        x_carga = x_proceso + ANCHO_ELEMENTO + DISTANCIA_HORIZONTAL_EXTRA
        y_carga = self.Y_MEDIO
        pos_car = QRectF(x_carga, y_carga, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        carga = ElementoCarga(self.sesion.carga, pos_car)
        self.scene.addItem(carga)

        y_linea_1 = self.Y_MEDIO + ALTO_ELEMENTO / 2
        y_linea_2 = self.Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL + ALTO_ELEMENTO / 2
        head = 3

        ah, aw, lw = 1, 1, 2

        # LINEAS:
        desde_controlador = x_controlador + ANCHO_ELEMENTO
        line = Flecha(QtCore.QPointF(desde_controlador, y_linea_1), QtCore.QPointF(x_actuador - head, y_linea_1), ah, aw, lw, color=QColor("#A8DADC"))  # controlador a actuador
        self.scene.addItem(line)

        desde_actuador = x_actuador + ANCHO_ELEMENTO
        self.line_1 = Flecha(QtCore.QPointF(desde_actuador, y_linea_1), QtCore.QPointF(x_proceso - head, y_linea_1), ah, aw, lw, color=QColor("#A8DADC"))  # actuador a proceso
        self.scene.addItem(self.line_1)

        desde_entrada = x_entrada + ANCHO_ELEMENTO
        self.line_8 = Flecha(QtCore.QPointF(desde_entrada, y_linea_1), QtCore.QPointF(x_controlador - head, y_linea_1), ah, aw, lw, color=QColor("#A8DADC"))  # entrada a controlador
        self.scene.addItem(self.line_8)

        x_bajada = x_carga - DISTANCIA_HORIZONTAL_EXTRA / 2
        self.line_3 = Flecha(QtCore.QPointF(x_bajada, y_linea_1), QtCore.QPointF(x_bajada, y_linea_2), ah, aw, lw, arrow=False, color=QColor("#A8DADC"))  # proceso a medidor (lazo realimentado - vertical)
        self.scene.addItem(self.line_3)

        x_subida = x_controlador - DISTANCIA_HORIZONTAL_EXTRA / 2
        self.line_6 = Flecha(QtCore.QPointF(x_subida, y_linea_2), QtCore.QPointF(x_subida, y_linea_1), ah, aw, lw, color=QColor("#A8DADC"))  # medidor a punto suma (vertical)
        self.scene.addItem(self.line_6)

        self.line_2 = Flecha(QtCore.QPointF(x_bajada, y_linea_2), QtCore.QPointF(desde_actuador + head, y_linea_2), ah, aw, lw, color=QColor("#A8DADC"))  # proceso a medidor (lazo realimentado - horizontal)
        self.scene.addItem(self.line_2)

        desde_proceso = x_proceso + ANCHO_ELEMENTO
        self.line_4 = Flecha(QtCore.QPointF(desde_proceso, y_linea_1), QtCore.QPointF(x_carga - head, y_linea_1), ah, aw, lw, color=QColor("#A8DADC"))  # proceso a carga
        self.scene.addItem(self.line_4)

        self.line_5 = Flecha(QtCore.QPointF(x_medidor, y_linea_2), QtCore.QPointF(x_subida + head, y_linea_2), ah, aw, lw, arrow=False, color=QColor("#A8DADC"))  # medidor a punto suma (horizontal)
        self.scene.addItem(self.line_5)

        # PUNTO SUMA
        puntoSuma = PuntoSuma(x_medio=x_subida, y_medio=y_linea_1, RADIO_PERTURBACION=20, izq=2, abajo=1)
        self.scene.addItem(puntoSuma)

        self.draw_title()

        # Deshabilitar el desplazamiento
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Evitar que la vista se desplace
        self.setDragMode(QGraphicsView.NoDrag)

        self.agregar_botones()

        pos_simular = QRectF(self.ANCHO_TOTAL-400, self.ALTO_TOTAL-300, 350, 100)

        self.simular_buton = BotonSimular(pos_simular,self)
        self.scene.addItem(self.simular_buton)

        pos_pausar = QRectF(self.ANCHO_TOTAL-400 - 400 , self.ALTO_TOTAL-300, 350, 100)

        self.pausar_buton = BotonPausar(pos_pausar,self)
        self.scene.addItem(self.pausar_buton)
        self.pausar_buton.hide()

        pos_detener = QRectF(self.ANCHO_TOTAL-400, self.ALTO_TOTAL-300, 350, 100)

        self.boton_detener = BotonDetener(pos_detener,self)
        self.scene.addItem(self.boton_detener)
        self.boton_detener.hide()

    def draw_title(self):

        self.title_item = QGraphicsTextItem(self.sesion.nombre)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.title_item.setFont(font)
        self.title_item.setDefaultTextColor(LETRA_COLOR)
        text_rect = self.title_item.boundingRect()
        self.title_item.setPos(self.X_MEDIO - (text_rect.width() / 2), self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL)
        self.title_item.focusOutEvent = self.update_model_title
        self.title_item.mousePressEvent = self.enable_text_editing
        self.scene.addItem(self.title_item)

    def agregar_botones(self):
        recuadro = QGroupBox()
        recuadro.setStyleSheet("""
            QGroupBox {
                background-color: #A8DADC;
                border: 3px solid #457B9D;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout()
        estilos_botones = """
            QPushButton {
                    background-color: #A8DADC;  
                    color: #2B2D42;
                    font-weight: bold;
                    border: 3px solid #457B9D;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #F1FAEE;
                }
        """
        boton_config_sim = QPushButton("Configurar Simulación")
        boton_config_sim.setStyleSheet(estilos_botones)
        boton_config_sim.clicked.connect(self.main_window.configurar_simulacion)
        layout.addWidget(boton_config_sim)

        boton_iniciar_sim = QPushButton("Iniciar Simulación")
        boton_iniciar_sim.setStyleSheet(estilos_botones)
        boton_iniciar_sim.clicked.connect(self.simular_button)
        layout.addWidget(boton_iniciar_sim)

        boton_estabilidad = QPushButton("Análisis de Estabilidad")
        boton_estabilidad.setStyleSheet(estilos_botones)
        boton_estabilidad.clicked.connect(self.main_window.mostrar_analisis_estabilidad)
        layout.addWidget(boton_estabilidad)
        
        recuadro_width = recuadro.geometry().width()
        recuadro_height = recuadro.geometry().height()

        recuadro.setLayout(layout)
        #recuadro.setGeometry(int(self.ANCHO_TOTAL - recuadro_width - 10),int(self.ALTO_TOTAL - recuadro_height - 10), 200, 150)
        recuadro.setGeometry(5,5, 200, 150)

        self.scene.addWidget(recuadro)

    def update_model_title(self, event):
        new_title = self.title_item.toPlainText()  # Obtener el texto actualizado del título
        self.sesion.nombre = new_title  # Actualizar el nombre en self.modelo
        current_pos = self.title_item.pos()
        text_rect = self.title_item.boundingRect()
        new_x = current_pos.x() + (text_rect.width() / 2) - (self.title_item.boundingRect().width() / 2)
        
        self.title_item.setPos(new_x, current_pos.y())
        self.title_item.clearFocus()
        cursor = self.title_item.textCursor()
        cursor.clearSelection()
        self.title_item.setTextCursor(cursor)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.title_item.mousePressEvent = self.enable_text_editing
        super(type(self.title_item), self.title_item).focusOutEvent(event)

    def enable_text_editing(self, event):
        self.title_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.title_item.setFocus()
        
        # Posicionar el cursor en la posición exacta del clic
        cursor = self.title_item.textCursor()
        cursor.setPosition(self.title_item.document().documentLayout().hitTest(event.pos(), Qt.FuzzyHit))
        self.title_item.setTextCursor(cursor)
        
        # Llamar al método original de mousePressEvent
        super(type(self.title_item), self.title_item).mousePressEvent(event)

    def mostrarElementos(self):
        for item in self.items():
            if isinstance(item, QtWidgets.QWidget):
                item.show()
    
    def simular_button(self):
        self.simular_buton.hide()
        self.pausar_buton.show()
        self.boton_detener.show()
        self.main_window.iniciar_simulacion()
        self.pausar_buton.hide()
        self.boton_detener.hide()
        self.simular_buton.show()

        
