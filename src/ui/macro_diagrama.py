from PyQt5 import QtWidgets, QtCore
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.elemento_entrada import ElementoEntrada
from .base.elemento_carga import ElementoCarga
from .base.macro_vista import MacroVista
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

# Constantes de diseño base (para una resolución de referencia, ej. 1920x1080)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
DISTANCIA_ENTRE_ELEMENTOS_HORIZONTAL = 75
DISTANCIA_ENTRE_ELEMENTOS_VERTICAL = 32.5
ANCHO_ELEMENTO = 150
ALTO_ELEMENTO = 65
# X_MEDIO y Y_MEDIO se calcularán basados en sceneRect
DISTANCIA_HORIZONTAL_EXTRA = (75+37.5)
LETRA_COLOR = QColor("#2B2D42")
COLOR_FONDO = QColor("#F1FAEE")

class MacroDiagrama(QGraphicsView):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        self.main_window = mainWindow

        self.sesion = mainWindow.sesion
        self.setup_scene()
        # Llamar a fitInView inicialmente para ajustar al tamaño actual
        # Se necesita un pequeño retraso para asegurar que la vista tenga tamaño
        QtCore.QTimer.singleShot(0, self.initial_fit_in_view)


    def setup_scene(self):
        self.setBackgroundBrush(COLOR_FONDO)
        self.scene = QGraphicsScene(self)
        # Establecer un tamaño base grande para la escena
        self.scene.setSceneRect(0, 0, BASE_WIDTH, BASE_HEIGHT)
        self.setScene(self.scene)
        self.mostrar_diagrama()

    def mostrar_diagrama(self):
        # Usar el sceneRect definido como base para los cálculos
        scene_rect = self.sceneRect()
        self.ANCHO_TOTAL = scene_rect.width()
        self.ALTO_TOTAL = scene_rect.height()
        self.X_MEDIO = scene_rect.width() / 2
        self.Y_MEDIO = scene_rect.height() / 2

        self.scene.setBackgroundBrush(QBrush(COLOR_FONDO))

        # Limpiar la escena antes de redibujar (si es necesario)
        # self.scene.clear() # Descomentar si se llama repetidamente y causa duplicados

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

        # Verificar si el medidor tiene FDT = 1 para mostrar solo la línea
        fdt_medidor = self.sesion.medidor.obtener_fdt_simpy()
        if fdt_medidor == 1:
            # Solo creamos las líneas sin el rectángulo del medidor visible
            self.medidor_visible = False
            # Crear un elemento medidor invisible que manejará los eventos de clic
            self.medidor_invisible_item = ElementoMedicion(self.sesion.medidor, pos_med, self)
            self.medidor_invisible_item.setOpacity(0)  # Hacerlo completamente transparente
            self.scene.addItem(self.medidor_invisible_item)
        else:
            # Crear el elemento medidor normal
            self.medidor_item = ElementoMedicion(self.sesion.medidor, pos_med, self)
            self.scene.addItem(self.medidor_item)
            self.medidor_visible = True

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
        line = Flecha(QtCore.QPointF(desde_controlador, y_linea_1), QtCore.QPointF(x_actuador - head, y_linea_1), ah, aw, lw)  # controlador a actuador
        self.scene.addItem(line)

        desde_actuador = x_actuador + ANCHO_ELEMENTO
        self.line_1 = Flecha(QtCore.QPointF(desde_actuador, y_linea_1), QtCore.QPointF(x_proceso - head, y_linea_1), ah, aw, lw)  # actuador a proceso
        self.scene.addItem(self.line_1)

        desde_entrada = x_entrada + ANCHO_ELEMENTO
        self.line_8 = Flecha(QtCore.QPointF(desde_entrada, y_linea_1), QtCore.QPointF(x_controlador - head, y_linea_1), ah, aw, lw)  # entrada a controlador
        self.scene.addItem(self.line_8)

        x_bajada = x_carga - DISTANCIA_HORIZONTAL_EXTRA / 2
        self.line_3 = Flecha(QtCore.QPointF(x_bajada, y_linea_1), QtCore.QPointF(x_bajada, y_linea_2), ah, aw, lw, arrow=False)  # proceso a medidor (lazo realimentado - vertical)
        self.scene.addItem(self.line_3)

        x_bajada_2 = x_carga - DISTANCIA_HORIZONTAL_EXTRA / 4
        self.line_9 = Flecha(QtCore.QPointF(x_bajada_2, y_linea_1), QtCore.QPointF(x_bajada_2, y_linea_2+15), ah, aw, lw, arrow=False, color=QColor("#6B9D8F"))  # proceso a medidor (lazo realimentado - vertical)
        self.scene.addItem(self.line_9)

        carga_texto = MacroVista(None,QtCore.QRectF(x_bajada_2-35, y_linea_2+14, 70, 40),self,"Carga")
        self.scene.addItem(carga_texto)

        x_subida = x_controlador - DISTANCIA_HORIZONTAL_EXTRA / 2
        self.line_6 = Flecha(QtCore.QPointF(x_subida, y_linea_2), QtCore.QPointF(x_subida, y_linea_1), ah, aw, lw)  # medidor a punto suma (vertical)
        self.scene.addItem(self.line_6)

        self.line_2 = Flecha(QtCore.QPointF(x_bajada, y_linea_2), QtCore.QPointF(desde_actuador + head, y_linea_2), ah, aw, lw)  # proceso a medidor (lazo realimentado - horizontal)
        self.scene.addItem(self.line_2)

        desde_proceso = x_proceso + ANCHO_ELEMENTO
        self.line_4 = Flecha(QtCore.QPointF(desde_proceso, y_linea_1), QtCore.QPointF(x_carga - head, y_linea_1), ah, aw, lw)  # proceso a carga
        self.scene.addItem(self.line_4)

        # Guardar x_subida y x_bajada para uso posterior
        self.x_subida = x_subida
        self.x_bajada = x_bajada

        self.create_medidor_feedback_line() # Crear la línea de feedback y área interactiva si aplica

        # PUNTO SUMA
        puntoSuma = PuntoSuma(x_medio=x_subida, y_medio=y_linea_1, RADIO_PERTURBACION=20, izq=2, abajo=1)
        self.scene.addItem(puntoSuma)

        self.estabilidad = None
        self.svg = None # Inicializar atributos
        self.error_svg = None # Inicializar atributos
        self.title_item = None # Inicializar atributos

        self.draw_title()
        self.draw_funciones()

        # Permitir el escalado y panning interactivo si se desea, o mantenerlo fijo
        # self.setDragMode(QGraphicsView.ScrollHandDrag) # Opcional: permite arrastrar la vista
        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse) # Opcional: zoom centrado en el mouse
        # self.setResizeAnchor(QGraphicsView.AnchorViewCenter) # Opcional

    def create_medidor_feedback_line(self):
        # Limpiar línea y área interactiva anteriores si existen
        if hasattr(self, 'line_5') and self.line_5 in self.scene.items():
            self.scene.removeItem(self.line_5)
        if hasattr(self, 'area_interactiva_medidor') and self.area_interactiva_medidor in self.scene.items():
            self.scene.removeItem(self.area_interactiva_medidor)

        y_linea_2 = self.Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL + ALTO_ELEMENTO / 2
        x_medidor = self.X_MEDIO - ANCHO_ELEMENTO / 2 # Re-calcular por si acaso

        ah, aw, lw = 1, 1, 2
        head = 3 # Mismo valor que en otras flechas

        if not self.medidor_visible:
            # Caso FDT = 1: línea directa sin medidor visible
            self.line_5 = Flecha(QtCore.QPointF(self.x_bajada, y_linea_2), QtCore.QPointF(self.x_subida + head, y_linea_2), ah, aw, lw, arrow=False)
            self.scene.addItem(self.line_5)

            # Añadir un área interactiva sobre la línea para capturar clics
            self.area_interactiva_medidor = QtWidgets.QGraphicsRectItem(self.x_subida, y_linea_2 - 5, self.x_bajada - self.x_subida, 10)
            self.area_interactiva_medidor.setPen(QtGui.QPen(Qt.transparent))  # Borde invisible
            self.area_interactiva_medidor.setBrush(QtGui.QBrush(Qt.transparent))  # Relleno invisible
            self.area_interactiva_medidor.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            self.area_interactiva_medidor.setAcceptHoverEvents(True)

            # Conectar el evento de clic con el medidor invisible
            def handle_click(event):
                if event.button() == Qt.LeftButton and hasattr(self, 'medidor_invisible_item'):
                    # Asegurarse que el item existe antes de llamar al método
                    self.medidor_invisible_item.mousePressEvent(event)

            self.area_interactiva_medidor.mousePressEvent = handle_click
            self.scene.addItem(self.area_interactiva_medidor)
        else:
             # Caso normal: líneas conectando al elemento medidor
            self.line_5 = Flecha(QtCore.QPointF(x_medidor, y_linea_2), QtCore.QPointF(self.x_subida + head, y_linea_2), ah, aw, lw, arrow=False)  # medidor a punto suma (horizontal)
            self.scene.addItem(self.line_5)

    def resizeEvent(self, event):
        # Llama al método original para manejar el evento de redimensionamiento
        super().resizeEvent(event)
        # Ajusta la vista para que todo el contenido de la escena sea visible
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def initial_fit_in_view(self):
        # Ajuste inicial después de que la ventana se haya mostrado
        if self.sceneRect().isValid():
             self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)


    def update_estabilidad(self):
        if self.estabilidad and self.estabilidad in self.scene.items():
            self.scene.removeItem(self.estabilidad)
        # El texto se añadirá de nuevo en draw_funciones -> draw_estabilidad

    def update_estabilidad_state(self,estabilidad):
        if self.estabilidad:
            self.estabilidad.update_text(estabilidad)
            self.estabilidad_update_pos()

    def draw_estabilidad(self,estabilidad):
        if self.estabilidad and self.estabilidad in self.scene.items():
             self.scene.removeItem(self.estabilidad) # Remover si ya existe
        self.estabilidad = EstabilidadTexto(self.sesion,estabilidad)
        self.scene.addItem(self.estabilidad)
        self.estabilidad_update_pos()

    def estabilidad_update_pos(self):
        if self.estabilidad:
            text_rect = self.estabilidad.boundingRect()
            # Posicionar relativo al tamaño base de la escena
            self.estabilidad.setPos(self.X_MEDIO - text_rect.width() / 2, self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*8)


    def draw_fdt(self,fdts):
        if self.svg and self.svg in self.scene.items():
            self.scene.removeItem(self.svg) # Remover si ya existe
        self.svg = SVGView(self.sesion,self.x_bajada - (DISTANCIA_HORIZONTAL_EXTRA/2),self.Y_MEDIO -  DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5,self,fdts)
        self.scene.addItem(self.svg)

    def remove_funciones(self):
        if self.svg and self.svg in self.scene.items():
            self.scene.removeItem(self.svg)
            self.svg = None # Resetear referencia
        if self.error_svg and self.error_svg in self.scene.items():
            self.scene.removeItem(self.error_svg)
            self.error_svg = None # Resetear referencia
        # La estabilidad se maneja por separado

    def draw_funciones(self):
        fdts,estabilidad,errores = self.sesion.obtener_ecuaciones_inicio()

        self.draw_fdt(fdts)
        self.draw_error(errores)

        # Manejo de estabilidad (crear o actualizar)
        if self.estabilidad is None:
            self.draw_estabilidad(estabilidad)
        else:
            self.update_estabilidad_state(estabilidad)


    def update_funciones(self):
        medidor_visible_anterior = self.medidor_visible

        fdt_medidor = self.sesion.medidor.obtener_fdt_simpy()
        medidor_visible_nuevo = fdt_medidor != 1

        # Solo redibujar el medidor y su línea si su visibilidad cambió
        if medidor_visible_anterior != medidor_visible_nuevo:
            self.medidor_visible = medidor_visible_nuevo # Actualizar estado

            # Eliminar elementos visuales del medidor (visible o invisible)
            if medidor_visible_anterior: # Era visible
                 if hasattr(self, 'medidor_item') and self.medidor_item in self.scene.items():
                     self.scene.removeItem(self.medidor_item)
                     del self.medidor_item # Eliminar referencia
            else: # Era invisible
                 if hasattr(self, 'medidor_invisible_item') and self.medidor_invisible_item in self.scene.items():
                    self.scene.removeItem(self.medidor_invisible_item)
                    del self.medidor_invisible_item # Eliminar referencia
                 if hasattr(self, 'area_interactiva_medidor') and self.area_interactiva_medidor in self.scene.items():
                    self.scene.removeItem(self.area_interactiva_medidor)
                    del self.area_interactiva_medidor

            # Recrear el elemento medidor (visible o invisible)
            x_medidor = self.X_MEDIO - ANCHO_ELEMENTO / 2
            y_medidor = self.Y_MEDIO + ALTO_ELEMENTO + DISTANCIA_ENTRE_ELEMENTOS_VERTICAL
            pos_med = QRectF(x_medidor, y_medidor, ANCHO_ELEMENTO, ALTO_ELEMENTO)

            if not medidor_visible_nuevo: # Ahora es invisible (FDT=1)
                self.medidor_invisible_item = ElementoMedicion(self.sesion.medidor, pos_med, self)
                self.medidor_invisible_item.setOpacity(0)
                self.scene.addItem(self.medidor_invisible_item)
            else: # Ahora es visible
                self.medidor_item = ElementoMedicion(self.sesion.medidor, pos_med, self)
                self.scene.addItem(self.medidor_item)

            # Recrear la línea de feedback y el área interactiva (si aplica)
            self.create_medidor_feedback_line()

        # Actualizar las funciones (FDT, error, estabilidad)
        self.remove_funciones() # Quita FDT y error SVG
        self.update_estabilidad() # Quita texto estabilidad
        self.draw_funciones() # Vuelve a dibujar FDT, error y estabilidad

        # Forzar un reajuste de la vista por si los nuevos SVGs cambian el bounding rect
        self.initial_fit_in_view()


    def draw_error(self,errores):
        if self.error_svg and self.error_svg in self.scene.items():
            self.scene.removeItem(self.error_svg) # Remover si ya existe
        self.error_svg = SVGViewError(self.sesion,self,self.x_subida+(DISTANCIA_HORIZONTAL_EXTRA/2), self.Y_MEDIO - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*5,errores)
        self.scene.addItem(self.error_svg)


    def draw_title(self):
        if self.title_item and self.title_item in self.scene.items():
            self.scene.removeItem(self.title_item) # Remover si ya existe

        self.title_item = QGraphicsTextItem(self.sesion.nombre)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        font = QtGui.QFont("Arial", 50, QtGui.QFont.Bold) # Tamaño de fuente base
        self.title_item.setFont(font)
        self.title_item.setDefaultTextColor(LETRA_COLOR)
        text_rect = self.title_item.boundingRect()
        self.title_item.setAcceptHoverEvents(True)
        self.title_item.hoverEnterEvent = lambda event: QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.title_item.hoverLeaveEvent = lambda event: QApplication.restoreOverrideCursor()
        # Posicionar relativo al tamaño base de la escena
        self.title_item.setPos(self.X_MEDIO - (text_rect.width() / 2), self.Y_MEDIO - text_rect.height() - DISTANCIA_ENTRE_ELEMENTOS_VERTICAL*10)
        self.title_item.focusOutEvent = self.update_model_title
        self.title_item.mousePressEvent = self.enable_text_editing
        self.scene.addItem(self.title_item)



    def update_model_title(self, event):
        if not self.title_item: return # Salir si el item no existe
        new_title = self.title_item.toPlainText()
        self.sesion.nombre = new_title
        current_pos = self.title_item.pos()
        text_rect = self.title_item.boundingRect()
        # Recalcular posición X basado en el nuevo ancho del texto
        new_x = self.X_MEDIO - (text_rect.width() / 2)
        self.title_item.setPos(new_x, current_pos.y())
        self.title_item.clearFocus()
        cursor = self.title_item.textCursor()
        cursor.clearSelection()
        self.title_item.setTextCursor(cursor)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.title_item.mousePressEvent = self.enable_text_editing
        # Llamar al método original de la superclase si es necesario
        # super(type(self.title_item), self.title_item).focusOutEvent(event)
        # Es mejor no llamar al focusOutEvent de la superclase directamente aquí
        # ya que estamos manejando la lógica de actualización nosotros mismos.

    def enable_text_editing(self, event):
        if not self.title_item: return # Salir si el item no existe
        self.title_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.title_item.setFocus()

        # Posicionar el cursor en la posición exacta del clic
        cursor = self.title_item.textCursor()
        # Mapear la posición del evento (vista) a la escena
        scene_pos = self.mapToScene(event.pos())
        # Mapear la posición de la escena a las coordenadas del item
        item_pos = self.title_item.mapFromScene(scene_pos)
        doc_layout = self.title_item.document().documentLayout()
        if doc_layout:
            hit_pos = doc_layout.hitTest(item_pos, Qt.FuzzyHit)
            if hit_pos != -1:
                 cursor.setPosition(hit_pos)

        self.title_item.setTextCursor(cursor)

        # Llamar al método original de mousePressEvent de QGraphicsTextItem
        # Esto asegura que la edición de texto estándar funcione (selección, etc.)
        QtWidgets.QGraphicsTextItem.mousePressEvent(self.title_item, event)


        
