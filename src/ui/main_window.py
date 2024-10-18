# from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QDialog, 
#                              QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, 
#                              QToolBar, QAction, 
#                              QTableWidgetItem, QTableWidget, QFrame)
# from PyQt5 import QtGui
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon
# import os
# from .menu.menu_bar import Menu
# from .macro_diagrama import MacroDiagrama
# from .menu.archivo import Archivo
# from back.simulacion import Simulacion
# from back.simulacion import Simulacion
# from back.estabilidad import Estabilidad
# from ui.base.grafico_simulacion import Graficadora
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWidgets import QApplication,QMessageBox
# import sympy as sp
# import sys
# class MainWindow(QMainWindow):
    
#     def __init__(self,sesion):
#         super().__init__()
#         self.sesion = sesion
#         self.estabilidad = Estabilidad(sesion)
#         self.archivo = Archivo(self, self.sesion)  # Crea una instancia de Archivo
        
#         # Mostrar el menú inicial
#         self.show_initial_menu()

#     def show_initial_menu(self):
#         self.initial_menu = self.create_initial_menu()
#         self.initial_menu.show()

#     def create_initial_menu(self):
#         initial_menu = QDialog(self)
#         initial_menu.setWindowTitle('Menú Inicial - Kontrolu')
#         initial_menu.setStyleSheet("background-color: #333; color: white;")
#         initial_menu.resize(400, 150)
#         layout = QVBoxLayout()
        
#         # Configurar el icono de la ventana
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path,'base','imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(QtGui.QIcon(icon))

#         new_project_btn = QPushButton('Crear proyecto nuevo')
#         new_project_btn.clicked.connect(self.new_project_from_menu)
#         layout.addWidget(new_project_btn)

#         open_project_btn = QPushButton('Abrir proyecto existente')
#         open_project_btn.clicked.connect(self.open_project_from_menu)
#         layout.addWidget(open_project_btn)

#         initial_menu.setLayout(layout)
#         return initial_menu
    
#     def new_project_from_menu(self):
#         self.sesion.nueva_sesion()
#         self.close_initial_menu_and_show_main()

#     def open_project_from_menu(self):
#         self.archivo.open_project()
#         self.close_initial_menu_and_show_main()

#     def close_initial_menu_and_show_main(self):
#         if self.initial_menu:
#             self.initial_menu.close()
#             self.initial_menu = None
#         self.initUI()
#         self.show()
            
    
#     def initUI(self):
#         self.setWindowTitle('Kontrolu')
#         self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
#         # Ruta de la imagen del logo
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base/imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(QIcon(icon))

#         menuBar = Menu(self,self.sesion)
#         self.setMenuBar(menuBar)

#         # Barra de herramientas
#         toolbar = QToolBar("Barra de Herramientas")
#         self.addToolBar(toolbar)

#         # Botón de simulación
#         boton_simulacion = QAction("Iniciar Simulación", self)
#         boton_simulacion.triggered.connect(self.iniciar_simulacion)
#         toolbar.addAction(boton_simulacion)

#         toolbar.addSeparator()

#         # Botón de análisis de estabilidad
#         boton_estabilidad = QAction("Análisis de Estabilidad", self)
#         boton_estabilidad.triggered.connect(self.mostrar_analisis_estabilidad)
#         toolbar.addAction(boton_estabilidad)
#         toolbar.setStyleSheet("background-color: #444; color: white;")

#         # Obtener los botones de la barra de herramientas y aplicarles estilos personalizados
#         simulacion_button = toolbar.widgetForAction(boton_simulacion)
#         if simulacion_button:
#             simulacion_button.setStyleSheet("""
#                 QToolButton {
#                     background-color: #666;  
#                     color: white;               /* Color del texto */
#                     font-weight: bold;          /* Texto en negrita */
#                     border: none;               /* Sin borde */
#                     padding: 5px;               /* Espaciado interno */
#                     border-radius: 3px;
#                 }
#                 QToolButton:hover {
#                     background-color: #4cae4c;  /* Color de fondo cuando se pasa el mouse */
#                 }
#             """)

#         estabilidad_button = toolbar.widgetForAction(boton_estabilidad)
#         if estabilidad_button:
#             estabilidad_button.setStyleSheet("""
#                 QToolButton {
#                     background-color: #666;  
#                     color: white;               /* Color del texto */
#                     font-weight: bold;          /* Texto en negrita */
#                     border: none;               /* Sin borde */
#                     padding: 5px;               /* Espaciado interno */
#                     border-radius: 3px;
#                 }
#                 QToolButton:hover {
#                     background-color: #c9302c;  /* Color de fondo cuando se pasa el mouse */
#                 }
#             """)

#         self.statusBar().showMessage('Listo')
        
#         # # Modificar la conexión del botón "Nuevo proyecto" en la barra de herramientas
#         # new_project_action = QAction("Nuevo proyecto", self)
#         # new_project_action.triggered.connect(self.new_project_from_main)
#         # toolbar.addAction(new_project_action)

#         self.init_macrobloques() 

#         self.showMaximized()
    
#     def new_project_from_main(self):
#         if self.archivo.new_project(from_menu=False):
#             self.actualizar_sesion()
    
        
#     def init_macrobloques(self):
#         self.diagrama = MacroDiagrama()
#         self.diagrama.setupUi(self)
#         self.setCentralWidget(self.diagrama)
#         self.diagrama.mostrarElementos()
#         self.diagrama.zoom_in()

#     def new_project(self):
#         self.statusBar().showMessage('Nuevo proyecto creado')

#     def open_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto {file_name} abierto')
#             # Lógica para abrir un proyecto
    
#     def save_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto guardado en {file_name}')
#             # Lógica para guardar un proyecto

#     def iniciar_simulacion(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Parámetros de Simulación")
#         dialog.setStyleSheet("background-color: #333; color: white;")
#         layout = QVBoxLayout()

#         # Configurar el icono de la ventana
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         dialog.setWindowIcon(QtGui.QIcon(icon))

#         # Tiempo total
#         tiempo_layout = QHBoxLayout()
#         tiempo_layout.addWidget(QLabel("Tiempo total (s):"))
#         tiempo_edit = QLineEdit()
#         tiempo_edit.setText("10")
#         tiempo_edit.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
#         tiempo_layout.addWidget(tiempo_edit)
#         layout.addLayout(tiempo_layout)
#         # Salida
#         salida_layout = QHBoxLayout()
#         salida_layout.addWidget(QLabel("Variable a controlar en tiempo 0:"))
#         salida_edit = QLineEdit()
#         salida_edit.setText("10")
#         salida_edit.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
#         salida_layout.addWidget(salida_edit)
#         layout.addLayout(salida_layout)

#         # Delta t
#         dt_layout = QHBoxLayout()
#         dt_layout.addWidget(QLabel("Intervalo de tiempo (dt):"))
#         dt_edit = QLineEdit()
#         dt_edit.setText("0.01")
#         dt_edit.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
#         dt_layout.addWidget(dt_edit)
#         layout.addLayout(dt_layout)

#         # Velocidad de simulacion
#         velocidad_layout = QHBoxLayout()
#         velocidad_layout.addWidget(QLabel("Duracion de simulacion de cada ciclo (segundos reales):"))
#         velocidad_edit = QLineEdit()
#         velocidad_edit.setText("2")
#         velocidad_edit.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
#         velocidad_layout.addWidget(velocidad_edit)
#         layout.addLayout(velocidad_layout)

#         # Botones OK y Cancelar
#         button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         button_box.accepted.connect(dialog.accept)
#         button_box.rejected.connect(dialog.reject)
#         layout.addWidget(button_box)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             t_total = float(tiempo_edit.text())
#             dt = float(dt_edit.text())
#             velocidad = float(velocidad_edit.text())
#             y_salida = float(salida_edit.text())
            
#             graficadora = Graficadora() # se instancia la clase Graficadora
#             graficadora.show()
            
#             simulacion = Simulacion(controlador=self.sesion.controlador, 
#                                     actuador=self.sesion.actuador,
#                                     proceso=self.sesion.proceso,
#                                     medidor=self.sesion.medidor,
#                                     delta=dt,
#                                     ciclos=int(t_total/dt),
#                                     entrada=self.sesion.entrada,
#                                     salida_cero=y_salida,
#                                     carga=self.sesion.carga,
#                                     graficadora=graficadora) # se la pasa como parametro a la clase Simulacion
#             simulacion.ejecutar_simulacion(velocidad)
            
#             self.statusBar().showMessage('Simulación completada')
            
#     def toggle_input_method(self, index):
#         if self.entrada_combo.currentText() == "Personalizada":
#             self.input_stack.setCurrentIndex(1)
#         else:
#             self.input_stack.setCurrentIndex(0)

#     def parse_latex_function(self, latex_func):
#         # This is a placeholder. You'll need to implement proper LaTeX parsing.
#         # For now, we'll assume the LaTeX is a valid Python expression
#         return lambda t: eval(latex_func.replace('t', 'math.t'))


#     def mostrar_analisis_estabilidad(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Análisis de Estabilidad")
#         dialog.setStyleSheet("background-color: #333; color: white;")
#         layout = QVBoxLayout()

#         # Configurar el icono de la ventana
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         dialog.setWindowIcon(QtGui.QIcon(icon))
        
#             # Función de transferencia
#         ft_label = QLabel("Función de Transferencia de Lazo Cerrado:")
#         layout.addWidget(ft_label)
        
#         # Usar QWebEngineView para renderizar LaTeX
#         web_view = QWebEngineView()
#         web_view.setFixedHeight(100)  # Ajustamos la altura para que sea más compacta
#         layout.addWidget(web_view)

#         # Obtener la función de transferencia
#         ft_latex = self.estabilidad.obtener_funcion_transferencia()

#         # HTML con MathJax para renderizar LaTeX
#         html_content = f"""
#         <html>
#         <head>
#             <script type="text/javascript" async
#                 src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
#             </script>
#         </head>
#         <body>
#             <p>$$%s$$</p>
#         </body>
#         </html>
#         """ % ft_latex

#         web_view.setHtml(html_content)

#         # Matriz de Routh-Hurwitz
#         matrix_label = QLabel("Matriz de Routh-Hurwitz:")
#         layout.addWidget(matrix_label)
#         self.matrix_table = QTableWidget()
#         layout.addWidget(self.matrix_table)

#         # Botón para calcular estabilidad
#         calcular_button = QPushButton("Calcular Estabilidad")
#         calcular_button.clicked.connect(self.calcular_y_mostrar_estabilidad)
#         layout.addWidget(calcular_button)

#         # Botón para calcular error en estado estable
#         error_button = QPushButton("Calcular Error en Estado Estable")
#         error_button.clicked.connect(self.calcular_y_mostrar_error_estado_estable)
#         layout.addWidget(error_button)

#         # Etiqueta para mostrar el resultado
#         self.resultado_label = QLabel()
#         layout.addWidget(self.resultado_label)

#         dialog.setLayout(layout)
#         dialog.exec_()

#     def calcular_y_mostrar_estabilidad(self):
#         matriz_routh, es_estable = self.estabilidad.calcular_estabilidad()
        
#         # Configurar la tabla
#         rows = len(matriz_routh)
#         cols = len(matriz_routh[0])
#         self.matrix_table.setRowCount(rows)
#         self.matrix_table.setColumnCount(cols)

#         # Rellenar la tabla con los valores de la matriz
#         for i in range(rows):
#             for j in range(cols):
#                 valor = matriz_routh[i][j]
#                 if isinstance(valor, sp.Expr):
#                     valor = sp.simplify(valor)
#                 item = QTableWidgetItem(str(valor))
#                 item.setTextAlignment(Qt.AlignCenter)
#                 self.matrix_table.setItem(i, j, item)

#         # Ajustar el estilo de la tabla
#         self.matrix_table.setStyleSheet("""
#             QTableWidget {
#                 background-color: #333;
#                 gridline-color: black;
#             }
#             QTableWidget::item {
#                 color: white;
#                 background-color: #444;
#             }
#             QHeaderView::section {
#                 background-color: #333;
#                 color: white;
#                 font-weight: bold;
#             }
#         """)
#         self.matrix_table.horizontalHeader().setVisible(True)
#         self.matrix_table.verticalHeader().setVisible(True)

#         # Ajustar el tamaño de las celdas
#         self.matrix_table.resizeColumnsToContents()
#         self.matrix_table.resizeRowsToContents()

#         # Interpretar el resultado
#         if rows == 1 and cols == 1:
#             resultado = f"La función de transferencia es una constante: {matriz_routh[0][0]}. "
#             resultado += "El sistema es estable." if es_estable else "El sistema es inestable."
#         else:
#             resultado = "El sistema es estable." if es_estable else "El sistema es inestable."
        
#         self.resultado_label.setText(resultado)
#         self.resultado_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;" if es_estable else "font-weight: bold; font-size: 14px; color: red;")
    
#     def calcular_y_mostrar_error_estado_estable(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Error en Estado Estable")
#         dialog.setStyleSheet("background-color: #333; color: white;")
#         layout = QVBoxLayout()

#         # Configurar el icono de la ventana
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         dialog.setWindowIcon(QtGui.QIcon(icon))

#         tipo_entrada = QComboBox()
#         tipo_entrada.addItems(["escalon", "rampa", "parabola"])
#         tipo_entrada.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
#         layout.addWidget(QLabel("Seleccione el tipo de entrada:"))
#         layout.addWidget(tipo_entrada)

#         calcular_button = QPushButton("Calcular")
#         layout.addWidget(calcular_button)

#         resultado_frame = QFrame()
#         resultado_frame.setFrameShape(QFrame.StyledPanel)
#         resultado_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
#         resultado_layout = QVBoxLayout(resultado_frame)
        
#         resultado_label = QLabel()
#         resultado_label.setAlignment(Qt.AlignCenter)
#         resultado_label.setStyleSheet("font-weight: bold; font-size: 16px;")
#         resultado_layout.addWidget(resultado_label)
        
#         layout.addWidget(resultado_frame)

#         def calcular():
#             tipo = tipo_entrada.currentText()
#             error = self.estabilidad.calcular_error_estado_estable(tipo)
#             resultado_label.setText(f"Error en estado estable para entrada {tipo}:\n{error}")
#             if error == 0:
#                 resultado_frame.setStyleSheet("background-color: #d4edda; padding: 2px; border-radius: 2px;")
#                 resultado_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #155724;")
#             else:
#                 resultado_frame.setStyleSheet("background-color: #f8d7da; padding: 2px; border-radius: 2px;")
#                 resultado_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #721c24;")

#         calcular_button.clicked.connect(calcular)

#         dialog.setLayout(layout)
#         dialog.exec_()
    

#     def closeEvent(self, event):
#         dialog = QMessageBox(self)
#         dialog.setWindowTitle('Confirmar salida')
#         dialog.setText('¿Está seguro de que desea salir?')
#         dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         dialog.setDefaultButton(QMessageBox.No)
        
#         # Configurar el icono de la ventana
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         dialog.setWindowIcon(QtGui.QIcon(icon))
        
#         # Establecer el estilo de la ventana
#         dialog.setStyleSheet("""
#             QMessageBox {
#                 background-color: #333;
#                 color: white;
#             }
            
#             QMessageBox QLabel {
#             color: white;
#             background-color: black;
#             padding: 10px;
#         }
        
#         """)
        
#         # Cambiar el texto del botón "Yes" a "Si"
#         yes_button = dialog.button(QMessageBox.Yes)
#         if yes_button:
#             yes_button.setText("Si")

#             # Aplicar estilo a los botones específicos
#         for button in dialog.buttons():
#             button.setStyleSheet("""
#                 background-color: black;
#                 color: white;
#                 min-width: 80px;
#                 min-height: 30px;
#                 border: none;
#                 border-radius: 3px;
#             """)
#         reply = dialog.exec_()

#         if reply == QMessageBox.Yes:
#             event.accept()
#             QApplication.quit()
#         else:
#             event.ignore()
            
#     def actualizar_sesion(self):
        
#         # Actualizar el diagrama de macrobloques
#         self.init_macrobloques()
        
#         self.statusBar().showMessage('Sesión actualizada')


from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QDialog, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, 
                             QToolBar, QAction, 
                             QTableWidgetItem, QTableWidget, QFrame)
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
from .menu.archivo import Archivo
from back.simulacion import Simulacion
from back.simulacion import Simulacion
from back.estabilidad import Estabilidad
from ui.base.grafico_simulacion import Graficadora
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication,QMessageBox
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
            'tiempo_total': 10,
            'salida_inicial': 10,
            'delta_t': 0.01,
            'velocidad': 2
        }
        self.show_initial_menu()

    def show_initial_menu(self):
        self.initial_menu = self.create_initial_menu()
        self.initial_menu.show()

    def create_initial_menu(self):
        initial_menu = QDialog(self)
        initial_menu.setWindowTitle('Menú Inicial - Kontrolu')
        initial_menu.setStyleSheet("background-color: #333; color: white;")
        initial_menu.resize(400, 150)
        layout = QVBoxLayout()
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'base','imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))

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
        
        # Configurar Simulacion
        boton_config_simulacion = QAction("Configurar Simulación", self)
        boton_config_simulacion.triggered.connect(self.configurar_simulacion)
        toolbar.addAction(boton_config_simulacion)
        
        # Aplicar el mismo estilo que los otros botones
        config_button = toolbar.widgetForAction(boton_config_simulacion)
        if config_button:
            config_button.setStyleSheet("""
                QToolButton {
                    background-color: #666;  
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
                QToolButton:hover {
                    background-color: #4cae4c;
                }
            """)

        # Botón de simulación
        boton_simulacion = QAction("Iniciar Simulación", self)
        boton_simulacion.triggered.connect(self.iniciar_simulacion)
        toolbar.addAction(boton_simulacion)

        toolbar.addSeparator()

        # Botón de análisis de estabilidad
        boton_estabilidad = QAction("Análisis de Estabilidad", self)
        boton_estabilidad.triggered.connect(self.mostrar_analisis_estabilidad)
        toolbar.addAction(boton_estabilidad)
        toolbar.setStyleSheet("background-color: #444; color: white;")

        # Obtener los botones de la barra de herramientas y aplicarles estilos personalizados
        simulacion_button = toolbar.widgetForAction(boton_simulacion)
        if simulacion_button:
            simulacion_button.setStyleSheet("""
                QToolButton {
                    background-color: #666;  
                    color: white;               /* Color del texto */
                    font-weight: bold;          /* Texto en negrita */
                    border: none;               /* Sin borde */
                    padding: 5px;               /* Espaciado interno */
                    border-radius: 3px;
                }
                QToolButton:hover {
                    background-color: #4cae4c;  /* Color de fondo cuando se pasa el mouse */
                }
            """)

        estabilidad_button = toolbar.widgetForAction(boton_estabilidad)
        if estabilidad_button:
            estabilidad_button.setStyleSheet("""
                QToolButton {
                    background-color: #666;  
                    color: white;               /* Color del texto */
                    font-weight: bold;          /* Texto en negrita */
                    border: none;               /* Sin borde */
                    padding: 5px;               /* Espaciado interno */
                    border-radius: 3px;
                }
                QToolButton:hover {
                    background-color: #c9302c;  /* Color de fondo cuando se pasa el mouse */
                }
            """)

        self.statusBar().showMessage('Listo')
        
        # # Modificar la conexión del botón "Nuevo proyecto" en la barra de herramientas
        # new_project_action = QAction("Nuevo proyecto", self)
        # new_project_action.triggered.connect(self.new_project_from_main)
        # toolbar.addAction(new_project_action)

        self.init_macrobloques() 

        self.showMaximized()
    
    def new_project_from_main(self):
        if self.archivo.new_project(from_menu=False):
            self.actualizar_sesion()
    
        
    def init_macrobloques(self):
        self.diagrama = MacroDiagrama()
        self.diagrama.setupUi(self)
        self.setCentralWidget(self.diagrama)
        self.diagrama.mostrarElementos()

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

    # Agregar este nuevo método
    def configurar_simulacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuración de Simulación")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        # Campos de configuración
        campos = {
            'tiempo_total': ('Tiempo total (s):', str(self.config_simulacion['tiempo_total'])),
            'salida_inicial': ('Variable a controlar en tiempo 0:', str(self.config_simulacion['salida_inicial'])),
            'delta_t': ('Intervalo de tiempo (dt):', str(self.config_simulacion['delta_t'])),
            'velocidad': ('Duración de simulación de cada ciclo (Milisegundos):', str(self.config_simulacion['velocidad']))
        }

        inputs = {}
        for key, (label, value) in campos.items():
            layout_h = QHBoxLayout()
            layout_h.addWidget(QLabel(label))
            input_field = QLineEdit()
            input_field.setText(value)
            input_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
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
            for key, input_field in inputs.items():
                self.config_simulacion[key] = float(input_field.text())

    # Modificar el método iniciar_simulacion existente
    def iniciar_simulacion(self):
        graficadora = Graficadora()
        graficadora.show()
        
        simulacion = Simulacion(
            controlador=self.sesion.controlador, 
            actuador=self.sesion.actuador,
            proceso=self.sesion.proceso,
            medidor=self.sesion.medidor,
            delta=self.config_simulacion['delta_t'],
            ciclos=int(self.config_simulacion['tiempo_total']/self.config_simulacion['delta_t']),
            entrada=self.sesion.entrada,
            salida_cero=self.config_simulacion['salida_inicial'],
            carga=self.sesion.carga,
            graficadora=graficadora
        )
        
        simulacion.ejecutar_simulacion(self.config_simulacion['velocidad'])
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
        dialog.setStyleSheet("background-color: #333; color: white;")
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
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

        tipo_entrada = QComboBox()
        tipo_entrada.addItems(["escalon", "rampa", "parabola"])
        tipo_entrada.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
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
        dialog = QMessageBox(self)
        dialog.setWindowTitle('Confirmar salida')
        dialog.setText('¿Está seguro de que desea salir?')
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
        # Establecer el estilo de la ventana
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #333;
                color: white;
            }
            
            QMessageBox QLabel {
            color: white;
            background-color: black;
            padding: 10px;
        }
        
        """)
        
        # Cambiar el texto del botón "Yes" a "Si"
        yes_button = dialog.button(QMessageBox.Yes)
        if yes_button:
            yes_button.setText("Si")

            # Aplicar estilo a los botones específicos
        for button in dialog.buttons():
            button.setStyleSheet("""
                background-color: black;
                color: white;
                min-width: 80px;
                min-height: 30px;
                border: none;
                border-radius: 3px;
            """)
        reply = dialog.exec_()

        if reply == QMessageBox.Yes:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
            
    def actualizar_sesion(self):
        
        # Actualizar el diagrama de macrobloques
        self.init_macrobloques()
        
        self.statusBar().showMessage('Sesión actualizada')