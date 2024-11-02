
from PyQt5 import QtWidgets, QtGui, QtCore
from ..base.boton_circulo import QGraphicCircleItem
from .simular_button import BotonSimular
from .pausar_button import BotonPausar
from .reanudar_button import BotonReanudar
from .detener_button import BotonDetener
from PyQt5.QtCore import QRectF
from ..menu.archivo import Archivo
from .vista_json import VistaJson
from PyQt5.QtWidgets import (QPushButton, QWidget,QMenu,QHBoxLayout,QDialog,QVBoxLayout,QTextEdit)
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

        x += spacing  # Actualizar x para el siguiente botón
        copy_button = QGraphicCircleItem(x, y, RADIO_C, 
                                    'fa5s.copy', 
                                    self.padre.copy_image,
                                    self, 
                                    message="Copiar y guardar diagrama")
        self.scene.addItem(copy_button)
        
        x += spacing  # Actualizar x para el siguiente botón
        copy_button = QGraphicCircleItem(x, y, RADIO_C, 
                                    'fa5s.question-circle', 
                                    self.mostrar_ayuda,
                                    self, 
                                    message="Ayuda")
        self.scene.addItem(copy_button)
        
    
    def mostrar_ayuda(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda")
        help_dialog.setMinimumSize(800, 800)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        help_dialog.setStyleSheet("""
            QDialog {
                background-color: #B0B0B0;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #505050;
            }
            QTextEdit {
                background-color: #D0D0D0;
                color: #2B2D42;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
            QPushButton {
                background-color: #808080;
                color: white;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
            QPushButton:hover {
                background-color: #606060;
                cursor: pointer;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        
        help_content = """
        <h2>Guía de Botones del Simulador</h2>

        <h3>Configurar Simulación</h3>
        <p>Este botón te permite ajustar los parámetros básicos de la simulación:</p>
        <ul>
            <li><strong>Tiempo total:</strong> Duración completa de la simulación</li>
            <li><strong>Variable a controlar:</strong> El valor objetivo que deseas mantener</li>
            <li><strong>Intervalo de tiempo:</strong> Tiempo entre cada paso de la simulación</li>
            <li><strong>Duración de ciclos:</strong> Tiempo real que toma cada ciclo</li>
            <li><strong>Simulación Precisa:</strong> Activa un modo más preciso pero que requiere más recursos</li>
        </ul>

        <h3>Archivo</h3>
        <p>Desde este menú puedes gestionar tus archivos de trabajo:</p>
        <ul>
            <li><strong>Nuevo Archivo:</strong> Comienza un nuevo proyecto desde cero</li>
            <li><strong>Abrir Archivo:</strong> Carga un proyecto existente</li>
            <li><strong>Guardar Archivo:</strong> Guarda tu trabajo actual</li>
        </ul>

        <h3>Editar JSON</h3>
        <p>Esta herramienta te permite:</p>
        <ul>
            <li>Ver y modificar los datos del modelo en formato JSON</li>
            <li>Copiar el contenido al portapapeles</li>
            <li>Cargar datos desde archivos JSON externos</li>
            <li>Guardar tus modificaciones</li>
        </ul>

        <h3>Copiar y Guardar Diagrama</h3>
        <p>Con un solo clic, puedes:</p>
        <ul>
            <li>Capturar el diagrama actual de tu sistema</li>
            <li>Guardarlo como imagen PNG en tu dispositivo</li>
        </ul>
        """

        help_text.setHtml(help_content)
        layout.addWidget(help_text)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(help_dialog.close)
        layout.addWidget(close_button)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()

    
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
        self.deshoverar()
        self.simular_buton.hide()
        self.pausar_buton.show()
        self.boton_detener.show()
        self.reanudar_boton.hide()

    def deteniendo_buttons(self):
        self.deshoverar()
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
        self.deshoverar()
        self.simular_buton.hide()
        self.pausar_buton.hide()
        self.boton_detener.show()
        self.reanudar_boton.show()

    def reanudar_button(self):
        self.reanudando_buttons()
        self.padre.reanudar_simulacion()
    
    def reanudando_buttons(self):
        self.deshoverar()
        self.simular_buton.hide()
        self.pausar_buton.show()
        self.boton_detener.show()
        self.reanudar_boton.hide()

    def deshoverar(self):
        self.simular_buton.hoverLeaveEvent(None)
        self.pausar_buton.hoverLeaveEvent(None)
        self.boton_detener.hoverLeaveEvent(None)
        self.reanudar_boton.hoverLeaveEvent(None)
    
    def no_buttons(self):
        self.deshoverar()
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
