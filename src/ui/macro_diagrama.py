
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
from PyQt5.QtWidgets import QGraphicsTextItem,QGraphicsView,QGraphicsScene,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor,QBrush
from PyQt5.QtCore import QRectF
from .base.text2svgMain import SVGView
from .text2svgError import SVGViewError
from .base.estabilidad_texto import EstabilidadTexto

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
COLOR_FONDO = QColor("#F1FAEE")

class MacroDiagrama(QGraphicsView):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        
        self.main_window = mainWindow

        self.sesion = mainWindow.sesion
        self.setup_scene()

    def setup_scene(self):
        self.setBackgroundBrush(COLOR_FONDO)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.mostrar_diagrama()

    def mostrar_diagrama(self):
        scene_rect = self.sceneRect()
        self.ANCHO_TOTAL = scene_rect.width()
        self.ALTO_TOTAL = scene_rect.height()
        self.X_MEDIO = scene_rect.width() / 2
        self.Y_MEDIO = scene_rect.height() / 2

        self.scene.setBackgroundBrush(QBrush(COLOR_FONDO))

        # ACTUADOR
        x_actuador = self.X_MEDIO - ANCHO_ELEMENTO / 2
        y_actuador = self.Y_MEDIO
        pos_act = QRectF(x_actuador, y_actuador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        actuador = ElementoActuador(self.sesion.actuador, pos_act,self)
        self.scene.addItem(actuador)

        # CONTROLADOR
        x_controlador = x_actuador - DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL - ANCHO_ELEMENTO
        y_controlador = self.Y_MEDIO
        pos_con = QRectF(x_controlador, y_controlador, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        controlador = ElementoControl(self.sesion.controlador, pos_con,self)
        self.scene.addItem(controlador)

        # ENTRADA
        x_entrada = x_controlador - DISTANCIA_HORIZONTAL_EXTRA - ANCHO_ELEMENTO
        y_entrada = self.Y_MEDIO
        pos_ent = QRectF(x_entrada, y_entrada, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        entrada = ElementoEntrada(self.sesion.entrada, pos_ent,self)
        self.scene.addItem(entrada)

        # PROCESO
        x_proceso = self.X_MEDIO + ANCHO_ELEMENTO / 2 + DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL
        y_proceso = self.Y_MEDIO
        pos_pro = QRectF(x_proceso, y_proceso, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        proceso = ElementoProceso(self.sesion.proceso, pos_pro,self)
        self.scene.addItem(proceso)

        # MEDIDOR
        x_medidor = x_actuador
        y_medidor = self.Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL
        pos_med = QRectF(x_medidor, y_medidor, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        medidor = ElementoMedicion(self.sesion.medidor, pos_med,self)
        self.scene.addItem(medidor)

        # CARGA
        x_carga = x_proceso + ANCHO_ELEMENTO + DISTANCIA_HORIZONTAL_EXTRA
        y_carga = self.Y_MEDIO
        pos_car = QRectF(x_carga, y_carga, ANCHO_ELEMENTO, ALTO_ELEMENTO)
        carga = ElementoCarga(self.sesion.carga, pos_car,self)
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
        self.x_subida = x_subida
        self.x_bajada = x_bajada
        puntoSuma = PuntoSuma(x_medio=x_subida, y_medio=y_linea_1, RADIO_PERTURBACION=20, izq=2, abajo=1)
        self.scene.addItem(puntoSuma)

        self.draw_title()
        self.draw_fdt()
        self.draw_error()
        self.draw_estabilidad()

        # Deshabilitar el desplazamiento
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Evitar que la vista se desplace
        self.setDragMode(QGraphicsView.NoDrag)



    def update_estabilidad(self):
        
        self.scene.removeItem(self.estabilidad)
        self.draw_estabilidad()

    def update_estabilidad_state(self):
        
        self.estabilidad.update_text()
        self.estabilidad_update_pos()
    
    def draw_estabilidad(self):
        
        self.estabilidad = EstabilidadTexto(self.sesion)
        self.scene.addItem(self.estabilidad)
        self.estabilidad_update_pos()
    
    def estabilidad_update_pos(self):
        
        text_rect = self.estabilidad.boundingRect()
        self.estabilidad.setPos(self.X_MEDIO - text_rect.width() / 2, self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*8)
    



    def update_fdt(self):
        
        self.scene.removeItem(self.svg)
        self.draw_fdt()

    def draw_fdt(self):
    
        self.svg = SVGView(self.sesion,self.x_bajada,self.Y_MEDIO -  DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5,self)

        self.scene.addItem(self.svg)

        #self.fdt_update_pos()



    def fdt_update_pos(self):

        text_rect = self.svg.boundingRect()

        self.svg.setPos(self.x_bajada - (text_rect.width() / 2), self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5)

    
    def error_update_pos(self):
        
        text_rect = self.error_svg.boundingRect()

        self.error_svg.setPos(self.x_subida -  (text_rect.width() / 2), self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5)


    def update_error(self):
            
        self.scene.removeItem(self.error_svg)
        self.draw_error()

    def draw_error(self):

        self.error_svg = SVGViewError(self.sesion,self,self.x_subida, self.Y_MEDIO - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5)

        self.scene.addItem(self.error_svg)

        #self.error_update_pos()

    def draw_title(self):

        self.title_item = QGraphicsTextItem(self.sesion.nombre)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        font = QtGui.QFont("Arial", 50, QtGui.QFont.Bold)
        self.title_item.setFont(font)
        self.title_item.setDefaultTextColor(LETRA_COLOR)
        text_rect = self.title_item.boundingRect()
        self.title_item.setAcceptHoverEvents(True)
        self.title_item.hoverEnterEvent = lambda event: QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.title_item.hoverLeaveEvent = lambda event: QApplication.restoreOverrideCursor()
        self.title_item.setPos(self.X_MEDIO - (text_rect.width() / 2), self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*10)
        self.title_item.focusOutEvent = self.update_model_title
        self.title_item.mousePressEvent = self.enable_text_editing
        self.scene.addItem(self.title_item)

        

    def update_model_title(self, event):
        new_title = self.title_item.toPlainText()  # Obtener el texto actualizado del título
        self.sesion.nombre = new_title  # Actualizar el nombre en self.modelo
        current_pos = self.title_item.pos()
        text_rect = self.title_item.boundingRect()
        new_x = self.X_MEDIO - (text_rect.width() / 2)
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
    
    

        
