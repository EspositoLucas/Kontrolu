from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QDialog, 
                             QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, 
                             QToolBar, QAction,QTableWidgetItem, QTableWidget, QFrame,QWidget,QCheckBox)
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QEvent,QRectF
from PyQt5.QtGui import QIcon, QImage, QPainter
import os
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
from .menu.archivo import Archivo
from .base.floating_buttons_main import FloatingButtonsMainView
from back.simulacion import Simulacion
from back.estabilidad import Estabilidad
from ui.base.grafico_simulacion import Graficadora
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from .base.vista_json import VistaJson
import sympy as sp
import sys
from latex2sympy2 import latex2sympy

class MainWindow(QMainWindow):
    
    def __init__(self, sesion):
        super().__init__()

        self.sesion = sesion
        self.estabilidad = Estabilidad(sesion)
        self.archivo = Archivo(self, self.sesion)
        # Agregar configuración por defecto de simulación
        self.config_simulacion = {
            'tiempo_total': '10',
            'salida_inicial': '0',
            'delta_t': '0.1',
            'velocidad': '100'
        }
        self.show_initial_menu()

    def show_initial_menu(self):
        self.initial_menu = self.create_initial_menu()
        self.initial_menu.show()
        
    def create_initial_menu(self):
        initial_menu = QDialog(self)
        initial_menu.setWindowTitle('Menú Inicial - Kontrolu')
        initial_menu.setStyleSheet(ESTILO)
        initial_menu.resize(400, 400)  # Aumentamos el tamaño para acomodar el logo
        initial_menu.setWindowFlags(initial_menu.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'base','imgs','logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))
        
        # Configurar el icono del menu inicial
        path = os.path.dirname(os.path.abspath(__file__))
        image_path_2 = os.path.join(path,'base','imgs','kontrolu_azul_oscuro.png')
        icon_2 = QtGui.QIcon()
        icon_2.addPixmap(QtGui.QPixmap(image_path_2), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # Agregar logo grande
        logo_label = QLabel()
        pixmap = QtGui.QPixmap(image_path_2)
        scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        # Etiqueta de bienvenida
        welcome_label = QLabel('¡Bienvenido a Kontrolu!')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 30px; font-weight: bold; margin: 20px 0 5px 0;")  # Margen: arriba 20px, abajo 5px
        layout.addWidget(welcome_label)

        # Subtítulo
        subtitle_label = QLabel('El valor deseado de ser controlado')
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2B2D42; margin: 0px 0 20px 0;")  # Margen superior 10px
        layout.addWidget(subtitle_label)


        new_project_btn = QPushButton('Crear proyecto nuevo')
        new_project_btn.clicked.connect(self.new_project_from_menu)
        layout.addWidget(new_project_btn)

        open_project_btn = QPushButton('Abrir proyecto existente')
        open_project_btn.clicked.connect(self.open_project_from_menu)
        layout.addWidget(open_project_btn)

        initial_menu.setLayout(layout)
        return initial_menu
    
    def new_project_from_menu(self):
        self.sesion.nueva_sesion()
        self.close_initial_menu_and_show_main()

    def open_project_from_menu(self):
        self.archivo.open_project()
        self.close_initial_menu_and_show_main()

    def close_initial_menu_and_show_main(self):
        if self.initial_menu:
            self.initial_menu.close()
            self.initial_menu = None
        self.initUI()
        self.show()
            
    
    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.floating_ellipses_view = None
        
        # Debug de información de pantalla
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        print("\n=== PANTALLA DEBUG ===")
        print(f"Resolución de pantalla: {screen.width()}x{screen.height()}")
        print(f"DPI de pantalla: {QtGui.QGuiApplication.primaryScreen().logicalDotsPerInch()}")
        print(f"Factor de escalado: {QtGui.QGuiApplication.primaryScreen().devicePixelRatio()}")
        
        
        # Print tamaño inicial de ventana
        print(f"Tamaño mínimo establecido: 800x600")
        print(f"Geometría inicial: {self.geometry().width()}x{self.geometry().height()}")
        print("=====================\n")
        
        self.showMaximized()
        
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base/imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QIcon(icon))
        self.init_macrobloques()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.WindowStateChange:  # Cambiado de Qt.WindowStateChange a QEvent.WindowStateChange
            print("Estado actual:")
            print(f"- Minimizado: {bool(self.windowState() & Qt.WindowMinimized)}")
            print(f"- Maximizado: {bool(self.windowState() & Qt.WindowMaximized)}")
            print(f"- Pantalla completa: {bool(self.windowState() & Qt.WindowFullScreen)}")
            print("===========================\n")
    
        
    def new_project_from_main(self):
        if self.archivo.new_project(from_menu=False):
            self.actualizar_sesion()
            self.actualizar_sesion()
    
            self.actualizar_sesion() 
        
    def init_macrobloques(self):

        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.central_widget = QWidget(self)
        self.setGeometry(screen)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.diagrama = MacroDiagrama(self)
        layout.addWidget(self.diagrama)
        self.diagrama.setGeometry(self.central_widget.geometry())

        # Crear la segunda QGraphicsView que contendrá los elipses
        self.floating_ellipses_view = FloatingButtonsMainView(self.central_widget,padre=self)
        self.floating_ellipses_view.raise_()

        # Establecer la posición de la vista de elipses flotantes en la esquina inferior izquierda
        height = self.size().height()
        width = self.size().width()
        self.floating_ellipses_view.setGeometry(0, height-200, width, 150)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.floating_ellipses_view:
            # Prints para debugging de dimensiones
            print("\n=== RESIZE EVENT DEBUG ===")
            print(f"Ventana actual - Ancho: {self.size().width()}, Alto: {self.size().height()}")
            print(f"Evento resize - Antiguo tamaño: {event.oldSize().width()}x{event.oldSize().height()}")
            print(f"Evento resize - Nuevo tamaño: {event.size().width()}x{event.size().height()}")
            
            # Calcular dimensiones
            print("resize")
            height = self.size().height()
            width = self.size().width()
            print(height)
            
            self.floating_ellipses_view.setGeometry(0, height-200, width, 150)

    
    def new_project(self):
        self.statusBar().showMessage('Nuevo proyecto creado')

    def open_project(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.statusBar().showMessage(f'Proyecto {file_name} abierto')
            # Lógica para abrir un proyecto
    
    def save_project(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.statusBar().showMessage(f'Proyecto guardado en {file_name}')
            # Lógica para guardar un proyecto
    
    def vista_json(self):
        vista = VistaJson(self.sesion, self)
        vista.exec_()
        if vista.result():
            self.actualizar_sesion()

    # Agregar este nuevo método
    def configurar_simulacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuración de Simulación")
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        

        # Agregar botón de ayuda
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.clicked.connect(self.mostrar_ayuda_simulacion)
        help_button.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #808080;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignRight)

        # Campos de configuración
        campos = {
            'tiempo_total': ('Tiempo total (s):', str(self.sesion.tiempo_total)),
            'salida_inicial': ('Variable a controlar en tiempo 0:', str(self.sesion.salida_inicial)),
            'delta_t': ('Muestreo de datos:', str(self.sesion.delta_t)),
            'velocidad': ('Duración del SCAN (Milisegundos):', str(self.sesion.velocidad))
        }

        inputs = {}
        for key, (label, value) in campos.items():
            layout_h = QHBoxLayout()
            layout_h.addWidget(QLabel(label))
            input_field = QLineEdit()
            input_field.setText(value)
            layout_h.addWidget(input_field)
            inputs[key] = input_field
            layout.addLayout(layout_h)

        #aramem un check item que diga Simulacion Precisa quiero que sea para tildar o no
        self.precisa = QHBoxLayout()
        self.precisa.addWidget(QLabel("Simulacion Precisa"))
        self.check = QCheckBox()
        self.precisa.addWidget(self.check)
        layout.addLayout(self.precisa)
        self.check.setChecked(self.sesion.precisa)

        

        
        # Crear el QDialogButtonBox con los botones estándar
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        # Cambiar el texto de los botones
        button_box.button(QDialogButtonBox.Save).setText("Guardar")
        button_box.button(QDialogButtonBox.Cancel).setText("Cancelar")

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_():

            
            delta_t = float(inputs['delta_t'].text())
            tiempo_total = float(inputs['tiempo_total'].text())
            salida_inicial = float(inputs['salida_inicial'].text())
            velocidad = float(inputs['velocidad'].text())
            precisa = self.check.isChecked()


            self.sesion.delta_t = delta_t
            self.sesion.tiempo_total = tiempo_total
            self.sesion.salida_inicial = salida_inicial
            self.sesion.velocidad = velocidad
            self.sesion.precisa = precisa
            
    def mostrar_ayuda_simulacion(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración de Simulación")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Guía de Configuración de Simulación")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)

        # Contenido organizado en secciones
        contenido = [
            ("<b>¿Qué es la Configuración de Simulación?</b>", 
            "La configuración de simulación permite establecer los parámetros fundamentales que determinan "
            "cómo se ejecutará la simulación del sistema de control. Estos parámetros afectan directamente "
            "la precisión y el comportamiento de la simulación."),
            
            ("<b>Parámetros Principales:</b>",
            "<ul>"
            "<li><b>Tiempo total (s):</b> Duración total de la simulación en segundos. Define cuánto tiempo se "
            "simulará el comportamiento del sistema.</li>"
            "<li><b>Variable a controlar en tiempo 0:</b> Valor inicial de la variable que se desea controlar. "
            "Representa el punto de partida del sistema.</li>"
            "<li><b>Muestreo de datos:</b> Paso de tiempo entre cada cálculo de la simulación. Un valor "
            "más pequeño aumenta la precisión pero requiere más recursos computacionales.</li>"
            "<li><b>Duración del SCAN:</b> Tiempo en milisegundos que tarda cada ciclo de "
            "simulación. Afecta la velocidad de visualización de la simulación.</li>"
            "</ul>"),
            
            ("<b>Recomendaciones:</b>",
            "<ul>"
            "<li>Use intervalos de tiempo pequeños para sistemas rápidos o que requieran alta precisión</li>"
            "<li>Ajuste el tiempo total según la dinámica específica de su sistema</li>"
            "<li>Balance la duración de ciclo entre fluidez visual y capacidad de procesamiento</li>"
            "<li>Configure la variable inicial según las condiciones reales de su sistema</li>"
            "</ul>")
        ]

        for titulo, texto in contenido:
            seccion = QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 5px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)

        # Botón de cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()

    # Modificar el método iniciar_simulacion existente
    def iniciar_simulacion(self):
        self.graficadora = Graficadora()
        self.graficadora.show()
        
        self.simulacion = Simulacion(
            graficadora=self.graficadora,
            window= self.floating_ellipses_view,
            sesion=self.sesion
        )
        
        self.simulacion.simulacion_inicio_real()
        self.statusBar().showMessage('Simulación completada')
    
    def detener_simulacion(self):
        self.simulacion.detener_simulacion()

    def pausar_simulacion(self):
        self.simulacion.pausar_simulacion()

    def reanudar_simulacion(self):
        self.simulacion.reanudar_simulacion()
            
    def toggle_input_method(self, index):
        if self.entrada_combo.currentText() == "Personalizada":
            self.input_stack.setCurrentIndex(1)
        else:
            self.input_stack.setCurrentIndex(0)

    def parse_latex_function(self, latex_func):
        # This is a placeholder. You'll need to implement proper LaTeX parsing.
        # For now, we'll assume the LaTeX is a valid Python expression
        return lambda t: eval(latex_func.replace('t', 'math.t'))
    
    def copy_image(self):

        # Determine the bounding rectangle of the scene
        rect = self.diagrama.scene.itemsBoundingRect()
        
        # Create an image with the same size as the scene
        image = QImage(rect.size().toSize(), QImage.Format_ARGB32)
        image.fill(0)  # Fill with a transparent background

        # Render the scene onto the image
        painter = QPainter(image)
        self.diagrama.scene.render(painter, target=QRectF(image.rect()), source=rect)
        painter.end()

        # Access the system clipboard and set the image
        clipboard = QApplication.clipboard()
        clipboard.setImage(image)

            # Open a file dialog to select the save location
        save_path, _ = QFileDialog.getSaveFileName(None, "Save Image", "", "PNG Files (*.png);;All Files (*)")

        # Save the image if a path is selected
        if save_path:
            image.save(save_path)
            print(f"Image saved to {save_path}")


    def mostrar_analisis_estabilidad(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Análisis de Estabilidad")
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
        # Agregar botón de ayuda
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.clicked.connect(self.mostrar_ayuda_estabilidad)
        help_button.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #808080;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignRight)
        
            # Función de transferencia
        ft_label = QLabel("Función de Transferencia de Lazo Cerrado:")
        layout.addWidget(ft_label)
        
        # Usar QWebEngineView para renderizar LaTeX
        web_view = QWebEngineView()
        web_view.setFixedHeight(100)  # Ajustamos la altura para que sea más compacta
        layout.addWidget(web_view)

        # Obtener la función de transferencia
        ft_latex = self.estabilidad.obtener_funcion_transferencia()

        # HTML con MathJax para renderizar LaTeX
        html_content = f"""
        <html>
        <head>
            <script type="text/javascript" async
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
            </script>
        </head>
        <body>
            <p>$$%s$$</p>
        </body>
        </html>
        """ % ft_latex

        web_view.setHtml(html_content)

        # Matriz de Routh-Hurwitz
        matrix_label = QLabel("Matriz de Routh-Hurwitz:")
        layout.addWidget(matrix_label)
        self.matrix_table = QTableWidget()
        layout.addWidget(self.matrix_table)

        # Botón para calcular estabilidad
        calcular_button = QPushButton("Calcular Estabilidad")
        calcular_button.clicked.connect(self.calcular_y_mostrar_estabilidad)
        layout.addWidget(calcular_button)

        # Botón para calcular error en estado estable
        error_button = QPushButton("Calcular Error en Estado Estable")
        error_button.clicked.connect(self.calcular_y_mostrar_error_estado_estable)
        layout.addWidget(error_button)

        # Etiqueta para mostrar el resultado
        self.resultado_label = QLabel()
        layout.addWidget(self.resultado_label)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def mostrar_ayuda_estabilidad(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Análisis de Estabilidad")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(600)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Guía de Análisis de Estabilidad")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)

        # Contenido organizado en secciones
        contenido = [
            ("<b>¿Qué es el Análisis de Estabilidad?</b>", 
            "El análisis de estabilidad es una herramienta fundamental que permite determinar si un sistema de control "
            "mantendrá un comportamiento controlado y predecible en el tiempo. Un sistema estable eventualmente "
            "alcanzará un estado de equilibrio, mientras que uno inestable puede presentar oscilaciones crecientes "
            "o comportamientos erráticos."),
            
            ("<b>Función de Transferencia de Lazo Cerrado:</b>",
            "Representa matemáticamente el comportamiento completo del sistema, incluyendo todos sus componentes "
            "y sus interacciones. Se muestra en formato LaTeX para una mejor visualización de las expresiones matemáticas."),
            
            ("<b>Matriz de Routh-Hurwitz:</b>",
            "Es una herramienta matemática que permite determinar la estabilidad del sistema sin necesidad de calcular "
            "las raíces del denominador de la función de transferencia. La presencia de cambios de signo en la primera "
            "columna de la matriz indica inestabilidad."),
            
            ("<b>Cálculo de Estabilidad:</b>",
            "<ul>"
            "<li><b>Sistema Estable:</b> Todos los valores en la primera columna de la matriz son positivos</li>"
            "<li><b>Sistema Inestable:</b> Hay cambios de signo en la primera columna de la matriz</li>"
            "<li>El resultado se muestra en verde (estable) o rojo (inestable)</li>"
            "</ul>"),
            
            ("<b>Error en Estado Estable:</b>",
            "Es la diferencia entre el valor deseado y el valor real que alcanza el sistema cuando el tiempo tiende "
            "a infinito. Se puede calcular para diferentes tipos de entrada:"
            "<ul>"
            "<li><b>Escalón:</b> Mide la precisión para alcanzar un valor constante</li>"
            "<li><b>Rampa:</b> Evalúa la capacidad de seguir una señal que aumenta linealmente</li>"
            "<li><b>Parabólica:</b> Analiza el seguimiento de señales con aceleración constante</li>"
            "</ul>"
            "Un error de cero (verde) indica seguimiento perfecto, mientras que un error no nulo (rojo) indica "
            "una desviación permanente del valor deseado.")
        ]

        for titulo, texto in contenido:
            seccion = QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 5px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)

        # Botón de cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()

    def calcular_y_mostrar_estabilidad(self):
        matriz_routh, es_estable = self.estabilidad.calcular_estabilidad()
        
        # Configurar la tabla
        rows = len(matriz_routh)
        cols = len(matriz_routh[0])
        self.matrix_table.setRowCount(rows)
        self.matrix_table.setColumnCount(cols)

        # Rellenar la tabla con los valores de la matriz
        for i in range(rows):
            for j in range(cols):
                valor = matriz_routh[i][j]
                if isinstance(valor, sp.Expr):
                    valor = sp.simplify(valor)
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignCenter)
                self.matrix_table.setItem(i, j, item)

        # Ajustar el estilo de la tabla
        self.matrix_table.setStyleSheet("""
            QTableWidget {
                background-color: #333;
                gridline-color: black;
            }
            QTableWidget::item {
                color: white;
                background-color: #444;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                font-weight: bold;
            }
        """)
        self.matrix_table.horizontalHeader().setVisible(True)
        self.matrix_table.verticalHeader().setVisible(True)

        # Ajustar el tamaño de las celdas
        self.matrix_table.resizeColumnsToContents()
        self.matrix_table.resizeRowsToContents()

        # Interpretar el resultado
        if rows == 1 and cols == 1:
            resultado = f"La función de transferencia de lazo cerrado es una constante. "
            resultado += "El sistema es estable." if es_estable else "El sistema es inestable."
        else:
            resultado = "El sistema es estable." if es_estable else "El sistema es inestable."
        
        self.resultado_label.setText(resultado)
        self.resultado_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;" if es_estable else "font-weight: bold; font-size: 14px; color: red;")
    
    def calcular_y_mostrar_error_estado_estable(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Error en Estado Estable")
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        calcular_button = QPushButton("Calcular")
        layout.addWidget(calcular_button)

        resultado_frame = QFrame()
        resultado_frame.setFrameShape(QFrame.StyledPanel)
        resultado_layout = QVBoxLayout(resultado_frame)
        
        resultado_label = QLabel()
        resultado_label.setAlignment(Qt.AlignCenter)
        resultado_layout.addWidget(resultado_label)
        
        layout.addWidget(resultado_frame)

        def calcular():
            error = self.estabilidad.calcular_error_estado_estable()
            resultado_label.setText(f"Error en estado estable para entrada {latex2sympy(self.sesion.entrada.funcion_transferencia)}:\n{error}")
            if error == 0:
                resultado_frame.setStyleSheet("background-color: #d4edda; padding: 2px; border-radius: 2px;")
                resultado_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #155724;")
            else:
                resultado_frame.setStyleSheet("background-color: #f8d7da; padding: 2px; border-radius: 2px;")
                resultado_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #721c24;")

        calcular_button.clicked.connect(calcular)

        dialog.setLayout(layout)
        dialog.exec_()
    

    def closeEvent(self, event):
        dialog = QDialog(self)
        dialog.setWindowTitle('Confirmar salida')
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        label = QLabel('¿Está seguro de que desea salir?')
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.button(QDialogButtonBox.Yes).setText("Si")
        button_box.button(QDialogButtonBox.No).setText("No")

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        reply = dialog.exec_()

        if reply == QDialog.Accepted:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
            
    def actualizar_sesion(self):
        
        # Actualizar el diagrama de macrobloques
        self.init_macrobloques()
        
        self.statusBar().showMessage('Sesión actualizada')


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
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);  /* Sombra de texto para resaltar */
        cursor: pointer;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
        cursor: pointer;
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
"""