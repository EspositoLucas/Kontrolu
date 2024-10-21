from PyQt5 import QtWidgets, QtGui, QtCore
from ..base.boton_circulo import QGraphicCircleItem
from .simular_button import BotonSimular
from .pausar_button import BotonPausar
from .reanudar_button import BotonReanudar
from .detener_button import BotonDetener
from PyQt5.QtCore import QRectF


class FloatingButtonsMainView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None,padre=None):
        super().__init__(parent)
        self.padre = padre
        self.setStyleSheet("background: transparent;")  # Fondo transparente
        self.setFrameShape(QtWidgets.QFrame.NoFrame)  # Sin bordes
        self.setRenderHints(QtGui.QPainter.Antialiasing)  # Suavizar bordes
        
        # Crear una escena para la vista de elipses
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.set_buttons()

    def set_buttons(self):
        RADIO_C = 40
        scene_width = self.scene.width()
        scene_height = self.scene.height()
        y = scene_height-RADIO_C*9

        x = -1000  # Starting x position for the first button
        y = scene_height  # y position for the buttons

        # Create and add the first button
        circulo = QGraphicCircleItem(x, y, RADIO_C, 'fa5s.cog', self.padre.configurar_simulacion, self, message="Configurar simulación")
        self.scene.addItem(circulo)

        # Update x position for the next button
        x += RADIO_C * 2 + 40  # Add some spacing between buttons

        # Create and add the second button
        icono_analisis = QGraphicCircleItem(x, y, RADIO_C, 'fa5s.chart-line', self.padre.mostrar_analisis_estabilidad, self, message="Análisis de estabilidad")
        self.scene.addItem(icono_analisis)
        #json_button = QGraphicCircleItem(RADIO_C*9, y, RADIO_C, 'fa5s.file-code', self.padre.ver_json, self, message="Ver JSON")
        #self.scene.addItem(json_button)
        #archivo_button = QGraphicCircleItem(RADIO_C*12, y, RADIO_C, 'fa5s.chart-line', self.padre.mostrar_analisis_estabilidad, self,message="Archivo")
        #self.scene.addItem(archivo_button)

        self.draw_simu_buttons(scene_width,scene_height)

    
    def draw_simu_buttons(self,sene_width,scene_height):

        y = scene_height

        pos_simular = QRectF(sene_width+200, scene_height-37.5, 300, 75)

        self.simular_buton = BotonSimular(pos_simular,self)
        self.scene.addItem(self.simular_buton)

        pos_pausar = QRectF(sene_width-200, scene_height-37.5, 300, 75)

        self.pausar_buton = BotonPausar(pos_pausar,self)
        self.scene.addItem(self.pausar_buton)
        self.pausar_buton.hide()


        self.reanudar_boton = BotonReanudar(pos_pausar,self)
        self.scene.addItem(self.reanudar_boton)
        self.reanudar_boton.hide()

        self.boton_detener = BotonDetener(pos_simular,self)
        self.scene.addItem(self.boton_detener)
        self.boton_detener.hide()

    def simular_button(self):
        self.simulando_buttons()
        self.padre.iniciar_simulacion()
    
    def simulando_buttons(self):
        self.simular_buton.hide()
        self.pausar_buton.show()
        self.boton_detener.show()
        self.reanudar_boton.hide()

    def deteniendo_buttons(self):
        self.simular_buton.show()
        self.pausar_buton.hide()
        self.boton_detener.hide()
        self.reanudar_boton.hide()

    def detener_button(self):
        self.deteniendo_buttons()
        self.padre.detener_simulacion()
    
    def pausar_button(self):
        self.pausando_buttons()
        self.padre.pausar_simulacion()
    
    def pausando_buttons(self):
        self.simular_buton.hide()
        self.pausar_buton.hide()
        self.boton_detener.show()
        self.reanudar_boton.show()

    def reanudar_button(self):
        self.reanudando_buttons()
        self.padre.reanudar_simulacion()
    
    def reanudando_buttons(self):
        self.simular_buton.hide()
        self.pausar_buton.show()
        self.boton_detener.show()
        self.reanudar_boton.hide()
    
    def no_buttons(self):
        self.simular_buton.hide()
        self.pausar_buton.hide()
        self.boton_detener.hide()
        self.reanudar_boton.hide()