
from PyQt5 import QtWidgets, QtGui, QtCore
from ..base.boton_circulo import QGraphicCircleItem
from .simular_button import BotonSimular
from .pausar_button import BotonPausar
from .reanudar_button import BotonReanudar
from .detener_button import BotonDetener
from PyQt5.QtCore import QRectF
from ..menu.archivo import Archivo
from .vista_json import VistaJson
from PyQt5.QtWidgets import (QPushButton, QWidget,QMenu,QHBoxLayout,QDialog,QVBoxLayout,QTextEdit,QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

LINEA_COLOR = QColor("#A9A9A9")
FONDO_CICULO_COLOR = QColor("#D3D3D3")
ACLARADO = FONDO_CICULO_COLOR.lighter(150)
LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")

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
                                    message="Glosario")
        self.scene.addItem(copy_button)
        
        
    def mostrar_ayuda(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda de Kontrolu")
        help_dialog.setMinimumSize(800, 800)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        help_dialog.setStyleSheet("""
            QDialog {
                background-color: #B0B0B0;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #505050;
            }
            QTabWidget::pane {
                background-color: #D0D0D0;
                border: 2px solid #505050;
                border-radius: 10px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #808080;
                color: white;
                border: 2px solid #505050;
                min-width: 140px;   /* Tamaño mínimo para evitar solapamiento */
                border-radius: 5px;
                padding: 8px 20px;
                margin: 2px;
                font-size: 14px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
            QTabBar::tab:selected {
                background-color: #606060;
            }
            QTextEdit {
                background-color: #D0D0D0;
                color: #2B2D42;
                border: 2px solid transparent;
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
            }
        """)
        
        layout = QVBoxLayout()
        tab_widget = QTabWidget()
        
        # Tab 1: Bienvenida
        welcome_tab = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_text = QTextEdit()
        welcome_text.setReadOnly(True)
        
        welcome_content = """
        <h2>Bienvenido a Kontrolu</h2>

        <h3>¿Qué es Kontrolu?</h3>
        <p>Kontrolu es una herramienta educativa diseñada para el estudio de la teoría de control de forma práctica y dinámica. 
        Permite a los estudiantes y educadores explorar los conceptos fundamentales de control a través de una interfaz intuitiva y versátil.</p>

        <h3>¿Qué permite Kontrolu?</h3>
        <p>Kontrolu ofrece tres funcionalidades principales:</p>
        <ul>
            <li>Diagramación de sistemas de control con capacidad de exportación</li>
            <li>Simulación dinámica y en tiempo real de sistemas de control</li>
            <li>Análisis detallado de sistemas mediante datos de simulación y operaciones matemáticas</li>
        </ul>

        <h3>¿Qué es la teoría de control?</h3>
        <p>La teoría de control es una rama interdisciplinaria de la ingeniería y las matemáticas que se ocupa del comportamiento 
        de sistemas dinámicos. Se centra en cómo las entradas de un sistema afectan sus salidas y cómo podemos manipular estas 
        entradas para obtener el comportamiento deseado del sistema.</p>

        <h3>¿Cuándo usar Kontrolu?</h3>
        <p>Kontrolu está diseñado principalmente para fines educativos. No pretende ser un simulador de alta precisión, 
        sino una herramienta didáctica que permite explorar y comprender los conceptos de control más allá del ámbito 
        tradicional de la electrónica. Es ideal para estudiantes que desean visualizar y experimentar con diferentes 
        tipos de sistemas de control de manera accesible.</p>

        <h3>¿Cuáles son las ventajas que ofrece Kontrolu?</h3>
        <ul>
            <li>Facilidad de uso con una interfaz intuitiva</li>
            <li>Simulación rápida y eficiente de sistemas de control</li>
            <li>Alta capacidad de parametrización para adaptarse a diferentes necesidades</li>
            <li>Análisis y cálculos matemáticos en tiempo real</li>
        </ul>
        """
        
        welcome_text.setHtml(welcome_content)
        welcome_layout.addWidget(welcome_text)
        welcome_tab.setLayout(welcome_layout)
        
        # Tab 2: Uso
        usage_tab = QWidget()
        usage_layout = QVBoxLayout()
        usage_text = QTextEdit()
        usage_text.setReadOnly(True)
        
        usage_content = """
        <h2>Guía de Uso de la Pantalla Principal</h2>

        <h3>Elementos del Diagrama</h3>
        <p>Cada elemento en la pantalla principal es interactivo y puede ser configurado mediante un clic:</p>
        <ul>
            <li><strong>Entrada:</strong> Define la señal de referencia del sistema</li>
            <li><strong>Controlador:</strong> Ajusta los parámetros de control</li>
            <li><strong>Actuador:</strong> Configura el elemento que ejecuta la acción de control</li>
            <li><strong>Proceso:</strong> Representa el sistema a controlar</li>
            <li><strong>Medidor:</strong> Define cómo se mide la salida del sistema</li>
            <li><strong>Desempeño:</strong> Define como se mide el desempeño del sistema</li>
        </ul>

        <h3>Controles Principales</h3>
        <ul>
            <li><strong>Botón Simular (verde):</strong> Inicia la simulación del sistema</li>
            <li><strong>Configuración:</strong> Ajustes generales del sistema (abajo a la izquierda)</li>
            <li><strong>Gestión de Archivos:</strong> Botones para abrir, guardar o crear nuevos archivos</li>
            <li><strong>Editor JSON:</strong> Permite visualizar y editar el código del sistema</li>
            <li><strong>Captura de Pantalla:</strong> Guarda la vista actual como imagen PNG</li>
            <li><strong>Ayuda:</strong> Acceso a esta documentación</li>
        </ul>

        <h3>Navegación y Funciones Adicionales</h3>
        <ul>
            <li><strong>Click Derecho Superior:</strong> Navega entre funciones del sistema</li>
            <li><strong>Click Izquierdo Superior:</strong> Accede a las funciones seleccionadas</li>
            <li><strong>Indicador de Estabilidad:</strong> Muestra y proporciona información sobre la estabilidad del sistema</li>
            <li><strong>Nombre del Sistema:</strong> Editable con click izquierdo</li>
        </ul>
        """
        
        usage_text.setHtml(usage_content)
        usage_layout.addWidget(usage_text)
        usage_tab.setLayout(usage_layout)
        
        # Tab 3: Glosario
        glossary_tab = QWidget()
        glossary_layout = QVBoxLayout()
        glossary_text = QTextEdit()
        glossary_text.setReadOnly(True)
        
        glossary_content = """
        <h2>Glosario de Términos de Teoría de Control</h2>

        <h3>Conceptos Fundamentales</h3>
        <ul>
            <li><strong>Error en Estado Estable:</strong> Diferencia entre el valor deseado y el valor real cuando el sistema 
            ha alcanzado un estado estable. Es un indicador crucial de la precisión del sistema.</li>
            
            <li><strong>Estabilidad del Sistema:</strong> Capacidad del sistema para mantener un estado de equilibrio bajo 
            condiciones normales de operación. Un sistema es estable si, ante una entrada acotada, produce una salida también acotada.</li>
            
            <li><strong>Función de Transferencia:</strong> Representación matemática que relaciona la salida con la entrada de un 
            sistema en el dominio de Laplace. Se expresa como el cociente de polinomios en 's'.</li>
            
            <li><strong>Polos y Ceros:</strong> Los polos son las raíces del denominador de la función de transferencia y determinan 
            la estabilidad del sistema. Los ceros son las raíces del numerador y afectan la respuesta transitoria.</li>
            
            <li><strong>Matriz de Routh-Hurwitz:</strong> Método matemático para determinar la estabilidad de un sistema lineal 
            invariante en el tiempo, analizando los coeficientes de su ecuación característica.</li>
        </ul>

        <h3>Componentes del Sistema</h3>
        <ul>
            <li><strong>Entrada:</strong> Señal de referencia o valor deseado que el sistema debe alcanzar.</li>
            
            <li><strong>Controlador:</strong> Elemento que determina la acción de control basándose en la diferencia entre 
            la referencia y la medición.</li>
            
            <li><strong>Actuador:</strong> Dispositivo que convierte la señal de control en una acción física sobre el proceso.</li>
            
            <li><strong>Proceso:</strong> Sistema físico o planta que se desea controlar.</li>
            
            <li><strong>Medidor:</strong> Elemento que mide la variable controlada y la retroalimenta al sistema.</li>
            
            <li><strong>Carga:</strong> Perturbación externa que afecta al comportamiento del sistema.</li>
            
            <li><strong>Desempeño:</strong> Medida de la calidad del control basada en diversos criterios como tiempo de 
            respuesta, sobrepico, error en estado estable, etc.</li>
        </ul>

        <h3>Variables y Señales</h3>
        <ul>
            <li><strong>θᵢ (Theta i):</strong> Valor de referencia o señal de entrada del sistema</li>
            <li><strong>θ₀ (Theta cero):</strong> Señal de salida o respuesta del sistema</li>
        </ul>

        <h3>Funciones de Transferencia</h3>
        <ul>
            <li><strong>G Global:</strong> Función de transferencia que engloba todo el sistema</li>
            <li><strong>G Total:</strong> Función de transferencia resultante de la multiplicación de bloques en serie</li>
            <li><strong>G₀ (G cero):</strong> Transferencia a lazo abierto de un sistema de lazo cerrado</li>
            <li><strong>G:</strong> Transferencia en la trayectoria directa</li>
            <li><strong>H:</strong> Transferencia en la trayectoria inversa</li>
        </ul>

        <h3>Dominio de Laplace vs Tiempo</h3>
        <p>El uso del dominio de Laplace en lugar del dominio del tiempo se debe a:</p>
        <ul>
            <li>Simplifica el análisis convirtiendo ecuaciones diferenciales en algebraicas</li>
            <li>Facilita el estudio de la estabilidad del sistema</li>
            <li>Permite una representación más clara de la dinámica del sistema</li>
            <li>Simplifica la representación de sistemas complejos mediante funciones de transferencia</li>
        </ul>
        """
        
        glossary_text.setHtml(glossary_content)
        glossary_layout.addWidget(glossary_text)
        glossary_tab.setLayout(glossary_layout)
        
        # Add tabs to widget
        tab_widget.addTab(welcome_tab, "Bienvenida")
        tab_widget.addTab(usage_tab, "Guía de Uso")
        tab_widget.addTab(glossary_tab, "Glosario")
        
        layout.addWidget(tab_widget)
        
        # Close button
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
        menu.setStyleSheet(ESTILO)
        
        nuevo_action = menu.addAction("Nuevo Archivo")
        abrir_action = menu.addAction("Abrir Archivo")
        guardar_action = menu.addAction("Guardar Archivo")
        
        nuevo_action.triggered.connect(self.nuevo_archivo)
        abrir_action.triggered.connect(self.abrir_archivo)
        guardar_action.triggered.connect(self.guardar_archivo)
        
        return menu
        
ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #707070;  /* Un gris más oscuro para mayor contraste */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;  /* Texto en negrita */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
    }

    QLineEdit {
        background-color: #FAF8F6;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }
    
    QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
    }

    QLabel {
        color: #2B2D42;  /* Texto gris oscuro */
        background-color: transparent;
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox {
        background-color: #D0D0D0;  /* Fondo gris claro */
        color: #2B2D42;  /* Texto gris oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 5px;
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox QAbstractItemView {
        background-color: #D0D0D0;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: #2B2D42;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }

    QTabWidget::pane {
        border: 2px solid #505050;
        border-radius: 10px;
        background-color: #FAF8F6;
        padding: 10px;
    }

    QTabBar::tab {
        background-color: #D0D0D0;
        color: #2B2D42;
        border: 2px solid #505050;
        border-radius: 5px;
        padding: 12px 30px;  /* Aumentar el padding para más espacio */
        min-width: 140px;   /* Tamaño mínimo para evitar solapamiento */
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-weight: bold;  /* Texto en negrita */
    }

    QTabBar::tab:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco en la pestaña seleccionada */
    }

    QTabBar::tab:hover {
        background-color: #606060;  /* Fondo gris más oscuro al pasar el cursor */
        color: white;  /* Texto en blanco al pasar el cursor */
    }

    QTableWidget {
        background-color: #FAF8F6;  /* Color de fondo del área sin celdas */
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        gridline-color: #505050;  /* Color de las líneas de la cuadrícula */
    }

    QTableWidget::item {
        background-color: #D0D0D0;  /* Color de fondo de las celdas */
        border: none;
    }

    QHeaderView::section {
        background-color: #808080;
        color: white;
        padding: 5px;
        border: 1px solid #505050;
    }

    QTableCornerButton::section {
        background-color: #808080;  /* Color del botón de esquina */
        border: 1px solid #505050;
    }

    QListWidget {
        background-color: #D0D0D0;
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QListWidget::item:selected {
        background-color: #808080;
        color: white;
    }
    QMenu {
        background-color: #D3D3D3;  /* Fondo gris claro para el menú */
        border: 5px solid #A9A9A9;  /* Borde gris oscuro */
        border-radius: 10px;
        color: #7A7A7A;  /* Texto 150 más oscuro que el gris original */
        font-family: "Segoe UI", "Arial", sans-serif;
        font-size: 14px;
        font-weight: bold;  /* Texto en negrita */
    }

    QMenu::item {
        background-color: transparent;  /* Fondo transparente para los items */
        padding: 8px 20px;  /* Espaciado para los items */
        color: #7A7A7A;  /* Texto 150 más oscuro */
        font-weight: bold;  /* Texto en negrita */
    }

    QMenu::item:selected {
        background-color: #F5F5F5;  /* Fondo gris claro al seleccionar */
        color: #7A7A7A;  /* Mantiene el texto en gris oscuro */
        font-weight: bold;  /* Texto en negrita */
    }

    QMenuBar {
        background-color: #D3D3D3;  /* Fondo gris pastel oscuro para la barra de menú */
        border: 5px solid #A9A9A9;  /* Borde gris oscuro */
    }

    QMenuBar::item {
        background-color: transparent;  /* Fondo transparente para los items de la barra de menú */
        padding: 8px 16px;  /* Espaciado para los items */
        color: #7A7A7A;  /* Texto 150 más oscuro */
        font-weight: bold;  /* Texto en negrita */
    }

    QMenuBar::item:selected {
        background-color: #F5F5F5;  /* Fondo gris claro al seleccionar */
        color: #7A7A7A;  /* Mantiene el texto en gris oscuro */
        font-weight: bold;  /* Texto en negrita */
    }

    QMenuBar::item:pressed {
        background-color: #F5F5F5;  /* Fondo más oscuro al hacer clic */
        color: #7A7A7A;  /* Mantiene el texto en gris oscuro */
        font-weight: bold;  /* Texto en negrita */
    }


"""
LINEA_COLOR = QColor("#A9A9A9")
FONDO_CICULO_COLOR = QColor("#D3D3D3")
ACLARADO = FONDO_CICULO_COLOR.lighter(150)
LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")