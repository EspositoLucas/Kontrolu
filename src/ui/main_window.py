from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QDialog, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, 
                             QWidget, QStackedWidget, QTextEdit, QToolBar, QAction, 
                             QTableWidgetItem, QTableWidget, QFrame)
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import os
from .menu.archivo import Archivo
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
from back.simulacion import Simulacion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ctypes
from back.simulacion import Simulacion
from back.estabilidad import Estabilidad
from ui.base.latex_editor import LatexEditor
from ui.base.grafico_simulacion import Graficadora
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication,QMessageBox
import sympy as sp
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('company.app.1')

class MainWindow(QMainWindow):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.estabilidad = Estabilidad(sesion)
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
        # Ruta de la imagen del logo
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base/imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QIcon(icon))

        menuBar = Menu(self,self.sesion)
        self.setMenuBar(menuBar)

        # Barra de herramientas
        toolbar = QToolBar("Barra de Herramientas")
        self.addToolBar(toolbar)

        # Botón de simulación
        boton_simulacion = QAction("Iniciar Simulación", self)
        boton_simulacion.triggered.connect(self.iniciar_simulacion)
        toolbar.addAction(boton_simulacion)

        # Botón de análisis de estabilidad
        boton_estabilidad = QAction("Análisis de Estabilidad", self)
        boton_estabilidad.triggered.connect(self.mostrar_analisis_estabilidad)
        toolbar.addAction(boton_estabilidad)
        toolbar.setStyleSheet("background-color: #333; color: white;")
        self.statusBar().showMessage('Listo')

        self.init_macrobloques() 

        self.showMaximized()
    
        
    def init_macrobloques(self):
        self.diagrama = MacroDiagrama()
        self.diagrama.setupUi(self)
        self.setCentralWidget(self.diagrama)
        self.diagrama.mostrarElementos()
        self.diagrama.zoom_in()

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

    def iniciar_simulacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Parámetros de Simulación")
        layout = QVBoxLayout()


        # Tiempo total
        tiempo_layout = QHBoxLayout()
        tiempo_layout.addWidget(QLabel("Tiempo total (s):"))
        tiempo_edit = QLineEdit()
        tiempo_edit.setText("10")
        tiempo_layout.addWidget(tiempo_edit)
        layout.addLayout(tiempo_layout)

        # Salida
        salida_layout = QHBoxLayout()
        salida_layout.addWidget(QLabel("Variable a controlar en tiempo 0:"))
        salida_edit = QLineEdit()
        salida_edit.setText("10")
        salida_layout.addWidget(salida_edit)
        layout.addLayout(salida_layout)

        # Delta t
        dt_layout = QHBoxLayout()
        dt_layout.addWidget(QLabel("Intervalo de tiempo (dt):"))
        dt_edit = QLineEdit()
        dt_edit.setText("0.01")
        dt_layout.addWidget(dt_edit)
        layout.addLayout(dt_layout)

        # Velocidad de simulacion
        velocidad_layout = QHBoxLayout()
        velocidad_layout.addWidget(QLabel("Duracion de simulacion de cada ciclo (segundos reales):"))
        velocidad_edit = QLineEdit()
        velocidad_edit.setText("2")
        velocidad_layout.addWidget(velocidad_edit)
        layout.addLayout(velocidad_layout)

        # Botones OK y Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_():
            t_total = float(tiempo_edit.text())
            dt = float(dt_edit.text())
            velocidad = float(velocidad_edit.text())
            y_salida = float(salida_edit.text())
            
            graficadora = Graficadora() # se instancia la clase Graficadora
            graficadora.show()
            
            simulacion = Simulacion(controlador=self.sesion.controlador, 
                                    actuador=self.sesion.actuador,
                                    proceso=self.sesion.proceso,
                                    medidor=self.sesion.medidor,
                                    delta=dt,
                                    ciclos=int(t_total/dt),
                                    entrada=self.sesion.entrada,
                                    salida_cero=y_salida,
                                    carga=self.sesion.carga,
                                    graficadora=graficadora) # se la pasa como parametro a la clase Simulacion
            simulacion.ejecutar_simulacion(velocidad)
            
            self.statusBar().showMessage('Simulación completada')
            
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
        layout = QVBoxLayout()

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
                self.matrix_table.setItem(i, j, item)

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
        layout = QVBoxLayout()

        tipo_entrada = QComboBox()
        tipo_entrada.addItems(["escalon", "rampa", "parabola"])
        layout.addWidget(QLabel("Seleccione el tipo de entrada:"))
        layout.addWidget(tipo_entrada)

        calcular_button = QPushButton("Calcular")
        layout.addWidget(calcular_button)

        resultado_frame = QFrame()
        resultado_frame.setFrameShape(QFrame.StyledPanel)
        resultado_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        resultado_layout = QVBoxLayout(resultado_frame)
        
        resultado_label = QLabel()
        resultado_label.setAlignment(Qt.AlignCenter)
        resultado_label.setStyleSheet("font-weight: bold; font-size: 16px;")
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
        reply = QMessageBox.question(self, 'Confirmar salida',
                                     '¿Está seguro de que desea salir?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()

    def actualizar_sesion(self):
        self.estabilidad = Estabilidad(self.sesion)
        
        # Actualizar el menú
        menuBar = Menu(self, self.sesion)
        self.setMenuBar(menuBar)
        
        # Actualizar la barra de herramientas
        self.initUI()
        
        # Actualizar el diagrama de macrobloques
        self.init_macrobloques()
        
        self.statusBar().showMessage('Sesión actualizada')