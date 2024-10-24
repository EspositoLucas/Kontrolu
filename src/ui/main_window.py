from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QDialog, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, 
                             QToolBar, QAction,QTableWidgetItem, QTableWidget, QFrame,QGraphicsView,QWidget)
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtGui import QIcon
import os
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
from .menu.archivo import Archivo
from .base.floating_buttons_main import FloatingButtonsMainView
from back.simulacion import Simulacion
from back.simulacion import Simulacion
from back.estabilidad import Estabilidad
from ui.base.grafico_simulacion import Graficadora
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from .base.vista_json import VistaJson
import sympy as sp
import sys
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

        # Agregar mensaje de bienvenida
        welcome_label = QLabel('¡Bienvenido a Kontrolu!')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 30px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(welcome_label)

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
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        # Campos de configuración
        campos = {
            'tiempo_total': ('Tiempo total (s):', str(self.sesion.tiempo_total)),
            'salida_inicial': ('Variable a controlar en tiempo 0:', str(self.sesion.salida_inicial)),
            'delta_t': ('Intervalo de tiempo (dt):', str(self.sesion.delta_t)),
            'velocidad': ('Duración de simulación de cada ciclo (Milisegundos):', str(self.sesion.velocidad))
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


            self.sesion.delta_t = delta_t
            self.sesion.tiempo_total = tiempo_total
            self.sesion.salida_inicial = salida_inicial
            self.sesion.velocidad = velocidad


    # Modificar el método iniciar_simulacion existente
    def iniciar_simulacion(self):
        self.graficadora = Graficadora()
        self.graficadora.show()
        
        self.simulacion = Simulacion(
            controlador=self.sesion.controlador, 
            actuador=self.sesion.actuador,
            proceso=self.sesion.proceso,
            medidor=self.sesion.medidor,
            delta=self.sesion.delta_t,
            ciclos=int(self.sesion.tiempo_total/self.sesion.delta_t),
            entrada=self.sesion.entrada,
            salida_cero=self.sesion.salida_inicial,
            carga=self.sesion.carga,
            graficadora=self.graficadora,
            window= self.floating_ellipses_view
        )
        
        self.simulacion.ejecutar_simulacion(self.sesion.velocidad)
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


    def mostrar_analisis_estabilidad(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Análisis de Estabilidad")
        dialog.setStyleSheet(ESTILO)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
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
            resultado = f"La función de transferencia es una constante: {matriz_routh[0][0]}. "
            resultado += "El sistema es estable." if es_estable else "El sistema es inestable."
        else:
            resultado = "El sistema es estable." if es_estable else "El sistema es inestable."
        
        self.resultado_label.setText(resultado)
        self.resultado_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;" if es_estable else "font-weight: bold; font-size: 14px; color: red;")
    
    def calcular_y_mostrar_error_estado_estable(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Error en Estado Estable")
        dialog.setStyleSheet(ESTILO)
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        tipo_entrada = QComboBox()
        tipo_entrada.addItems(["escalon", "rampa", "parabola"])
        layout.addWidget(QLabel("Seleccione el tipo de entrada:"))
        layout.addWidget(tipo_entrada)

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
            tipo = tipo_entrada.currentText()
            error = self.estabilidad.calcular_error_estado_estable(tipo)
            resultado_label.setText(f"Error en estado estable para entrada {tipo}:\n{error}")
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
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;  /* Tamaño de botón más grande */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
    }

    QPushButton:hover {
        background-color: #606060;  /* Gris aún más oscuro al pasar el cursor */
    }

    QLineEdit {
        background-color: #D0D0D0;  /* Fondo gris claro */
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
        background-color: #F1F1F1;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: white;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }

    QMessageBox {
        background-color: #B0B0B0;  /* Fondo gris pastel oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
    }

    QMessageBox QLabel {
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QMessageBox QPushButton {
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QMessageBox QPushButton:hover {
        background-color: #606060;  /* Botón más oscuro al pasar el cursor */
    }
"""