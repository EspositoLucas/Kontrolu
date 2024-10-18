
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
from PyQt5.QtWidgets import QGraphicsTextItem, QGroupBox, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRectF

DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL = 75
DISTANCIA_ENTRE_ELEMENTOS_VERTICAL = 32.5
ANCHO_ELEMENTO = 150
ALTO_ELEMENTO = 65
X_MEDIO = 430.5
Y_MEDIO = 210
DISTANCIA_HORIZONTAL_EXTRA = 75+37.5

class MacroDiagrama(QtWidgets.QWidget):
        
    def setupUi(self, mainWindow):
        self.main_window = mainWindow
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, mainWindow)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.sesion = mainWindow.sesion

        # ACTUADOR
        x_actuador = X_MEDIO - ANCHO_ELEMENTO/2
        y_actuador = Y_MEDIO
        pos_act = QRectF(x_actuador, y_actuador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        actuador = ElementoActuador(self.sesion.actuador,pos_act)
        self.scene.addItem(actuador)



        # CONTROLADOR
        x_controlador = x_actuador - DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL - ANCHO_ELEMENTO
        y_controlador = Y_MEDIO
        pos_con = QRectF(x_controlador, y_controlador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        controlador = ElementoControl(self.sesion.controlador,pos_con)
        self.scene.addItem(controlador)

        # ENTRADA
        x_entrada = x_controlador - DISTANCIA_HORIZONTAL_EXTRA - ANCHO_ELEMENTO
        y_entrada = Y_MEDIO
        pos_ent = QRectF(x_entrada, y_entrada, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        entrada = ElementoEntrada(self.sesion.entrada,pos_ent)
        self.scene.addItem(entrada)

        # PROCESO
        x_proceso = X_MEDIO + ANCHO_ELEMENTO/2 + DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL
        y_proceso = Y_MEDIO
        pos_pro = QRectF(x_proceso, y_proceso, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        proceso = ElementoProceso(self.sesion.proceso,pos_pro)
        self.scene.addItem(proceso)
        
        # MEDIDOR
        x_medidor = x_actuador
        y_medidor = Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL
        pos_med = QRectF(x_medidor, y_medidor, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        medidor = ElementoMedicion(self.sesion.medidor,pos_med)
        self.scene.addItem(medidor)

        #CARGA
        x_carga = x_proceso + ANCHO_ELEMENTO + DISTANCIA_HORIZONTAL_EXTRA
        y_carga = Y_MEDIO
        pos_car = QRectF(x_carga, y_carga, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        carga = ElementoCarga(self.sesion.carga,pos_car)
        self.scene.addItem(carga)
        


        y_linea_1 = Y_MEDIO + ALTO_ELEMENTO/2
        y_linea_2 = Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL + ALTO_ELEMENTO/2
        head = 3

        ah,aw,lw = 1,1,2

        # LINEAS: 
        desde_controlador = x_controlador + ANCHO_ELEMENTO
        line = Flecha(QtCore.QPointF(desde_controlador, y_linea_1), QtCore.QPointF(x_actuador-head, y_linea_1), ah, aw, lw,color=QColor("#A8DADC")) # controlador a actuador
        self.scene.addItem(line)
        
        desde_actuador = x_actuador + ANCHO_ELEMENTO
        self.line_1 = Flecha(QtCore.QPointF(desde_actuador, y_linea_1), QtCore.QPointF(x_proceso-head, y_linea_1), ah, aw, lw,color=QColor("#A8DADC")) # actuador a proceso
        self.scene.addItem(self.line_1)

        desde_entrada = x_entrada + ANCHO_ELEMENTO
        self.line_8 = Flecha(QtCore.QPointF(desde_entrada, y_linea_1), QtCore.QPointF(x_controlador-head, y_linea_1), ah, aw, lw,color=QColor("#A8DADC")) # entrada a controlador
        self.scene.addItem(self.line_8)


        x_bajada = x_carga - DISTANCIA_HORIZONTAL_EXTRA/2
        self.line_3 = Flecha(QtCore.QPointF(x_bajada, y_linea_1), QtCore.QPointF(x_bajada, y_linea_2), ah, aw, lw, arrow=False,color=QColor("#A8DADC")) # proceso a medidor (lazo realimentado - vertical)
        self.scene.addItem(self.line_3)

        x_subida = x_controlador - DISTANCIA_HORIZONTAL_EXTRA/2
        self.line_6 = Flecha(QtCore.QPointF(x_subida, y_linea_2), QtCore.QPointF(x_subida, y_linea_1), ah, aw, lw,color=QColor("#A8DADC")) # medidor a punto suma (vertical)
        self.scene.addItem(self.line_6)


        self.line_2 = Flecha(QtCore.QPointF(x_bajada, y_linea_2), QtCore.QPointF(desde_actuador+head, y_linea_2), ah, aw, lw,color=QColor("#A8DADC")) # proceso a medidor (lazo realimentado - horizontal)
        self.scene.addItem(self.line_2)




        desde_proceso = x_proceso + ANCHO_ELEMENTO
        self.line_4 = Flecha(QtCore.QPointF(desde_proceso, y_linea_1), QtCore.QPointF(x_carga-head, y_linea_1), ah, aw, lw,color=QColor("#A8DADC")) # proceso a carga
        self.scene.addItem(self.line_4)

        self.line_5 = Flecha(QtCore.QPointF(x_medidor, y_linea_2), QtCore.QPointF(x_subida+head, y_linea_2), ah, aw, lw, arrow=False,color=QColor("#A8DADC")) # medidor a punto suma (horizontal)
        self.scene.addItem(self.line_5)

        # PUNTO SUMA
        puntoSuma = PuntoSuma(x_medio = x_subida,y_medio = y_linea_1, RADIO_PERTURBACION = 20)
        self.scene.addItem(puntoSuma)

        #self.line_7 = Flecha(QtCore.QPointF(190, 230), QtCore.QPointF(221, 230),ah, aw, lw) # punto suma a controlador
        #self.scene.addItem(self.line_7)
        


        self.draw_title()
        self.agregar_botones()

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def draw_title(self):

        self.title_item = QGraphicsTextItem(self.sesion.nombre)

        self.title_item.setTextInteractionFlags(Qt.TextEditable)
        font = QtGui.QFont("Arial", 20)
        self.title_item.setFont(font)
        text_rect = self.title_item.boundingRect()

        self.title_item.setPos(430.5 - (text_rect.width()/2),1)

        self.title_item.focusOutEvent = self.update_model_title

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
        boton_iniciar_sim.clicked.connect(self.main_window.iniciar_simulacion)
        layout.addWidget(boton_iniciar_sim)

        boton_estabilidad = QPushButton("Análisis de Estabilidad")
        boton_estabilidad.setStyleSheet(estilos_botones)
        boton_estabilidad.clicked.connect(self.main_window.mostrar_analisis_estabilidad)
        layout.addWidget(boton_estabilidad)

        recuadro.setLayout(layout)
        recuadro.setGeometry(1200, -200, 200, 150)
        self.scene.addWidget(recuadro)

    def update_model_title(self, event):

        new_title = self.title_item.toPlainText()  # Obtener el texto actualizado del título
        self.sesion.nombre = new_title  # Actualizar el nombre en self.modelo
        # Reposicionar el título después de editar si cambió el ancho
        text_rect = self.title_item.boundingRect()
        title_x = 430.5 - (text_rect.width()/2) # Recalcular la posición central
        self.title_item.setPos(title_x, 1)  # Mantener la posición vertical
        


    def mostrarElementos(self):
        for item in self.scene.items():
            if isinstance(item, QtWidgets.QWidget):
                item.show()