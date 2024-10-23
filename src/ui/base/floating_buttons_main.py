from PyQt5 import QtWidgets, QtGui, QtCore
from ..base.boton_circulo import QGraphicCircleItem
from .simular_button import BotonSimular
from .pausar_button import BotonPausar
from .reanudar_button import BotonReanudar
from .detener_button import BotonDetener
from PyQt5.QtCore import QRectF
from ..menu.archivo import Archivo
from .vista_json import VistaJson
from PyQt5.QtWidgets import (QPushButton, QWidget,QMenu,QHBoxLayout)
from PyQt5.QtCore import Qt


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
        y = scene_height

        x = -1000  # Posición x inicial para el primer botón
        spacing = RADIO_C * 2 + 40  # Espacio entre botones

        # Botón de configuración
        circulo = QGraphicCircleItem(x, y, RADIO_C, 'fa5s.cog', 
                                    self.padre.configurar_simulacion, 
                                    self, 
                                    message="Configurar simulación")
        self.scene.addItem(circulo)

        # Botón de análisis
        x += spacing  # Actualizar x para el siguiente botón
        icono_analisis = QGraphicCircleItem(x, y, RADIO_C, 
                                        'fa5s.chart-line', 
                                        self.padre.mostrar_analisis_estabilidad, 
                                        self, 
                                        message="Análisis de estabilidad")
        self.scene.addItem(icono_analisis)
        
        # Botón de archivo
        x += spacing  # Actualizar x para el siguiente botón
        archivo_menu = self.create_archivo_menu()
        archivo_button = QGraphicCircleItem(x, y, RADIO_C, 
                                        'fa5s.file', 
                                        lambda: None,
                                        self, 
                                        message="Archivo",
                                        menu=archivo_menu)
        self.scene.addItem(archivo_button)

        self.draw_simu_buttons(scene_width, scene_height)

        # Botón de JSON
        x += spacing  # Actualizar x para el siguiente botón
        json_button = QGraphicCircleItem(x, y, RADIO_C, 
                                    'fa5s.file-code', 
                                    self.padre.vista_json,
                                    self, 
                                    message=" Editar JSON")
        self.scene.addItem(json_button)

    
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
    
    def nuevo_archivo(self):
        # Implementa la lógica del archivo original en menu_bar.txt
        archivo = Archivo(self.padre, self.padre.sesion)
        archivo.new_project()

    def abrir_archivo(self):
        archivo = Archivo(self.padre, self.padre.sesion)
        archivo.open_project()

    def guardar_archivo(self):
        archivo = Archivo(self.padre, self.padre.sesion)
        archivo.save_project()

    def create_archivo_menu(self):
        menu = QtWidgets.QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #444;
                color: white;
                border: 1px solid #2B2D42;
                border-radius: 10px;
            }
            QMenu::item {
                background-color: #666;
                padding: 5px 20px;
                border-radius: 5px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #777;
            }
        """)
        
        nuevo_action = menu.addAction("Nuevo Archivo")
        abrir_action = menu.addAction("Abrir Archivo")
        guardar_action = menu.addAction("Guardar Archivo")
        
        nuevo_action.triggered.connect(self.nuevo_archivo)
        abrir_action.triggered.connect(self.abrir_archivo)
        guardar_action.triggered.connect(self.guardar_archivo)
        
        return menu
