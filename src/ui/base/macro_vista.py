# import os
# from PyQt5 import QtGui
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QWidget
# from PyQt5.QtGui import QIcon
# from .drawing_area import DrawingArea

# class MacroVista(QPushButton):
#     def __init__(self, elementoBack, geometria):
#         super().__init__()
#         self.modelo = elementoBack
#         self.setText(self.modelo.nombre)
#         self.setGeometry(geometria)
#         self.clicked.connect(self.click)
#         self.setStyleSheet("""
#             background-color: #0072BB;;  /* Color de fondo azul /
#             font-weight: bold;          /* Texto en negrita */
#             font-weight: bold;          /* Texto en negrita */
#             color: white;               /* Color de texto blanco */
#             font-size: 15px;            /* Tamaño de fuente */
#             font-family: Arial;  
#         """)
    
#     def click(self):
#         self.ventana = QMainWindow()
#         self.ventana.setWindowTitle(self.modelo.nombre)
        
#         screen = QtGui.QGuiApplication.primaryScreen().geometry()
#         self.ventana.setGeometry(screen)
#         self.ventana.showMaximized()
#         self.ventana.setFixedSize(screen.width(), screen.height())
#         self.ventana.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
#         self.drawing_area = DrawingArea(self, self.ventana)
#         self.ventana.setCentralWidget(self.drawing_area)
        
#         self.init_tool_bar()
#         self.ventana.show()
#         self.ventana.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
#         # Ruta de la imagen del logo
#         path =  os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.ventana.setWindowIcon(icon)
        
#         QTimer.singleShot(100, self.drawing_area.content.load_microbloques)
        
#     def init_tool_bar(self):
#         toolbar = QToolBar("Herramientas", self.ventana)
#         self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)

#         button_style = """
#             QPushButton {
#                 background-color: #808080; /* Color gris */
#                 color: white;
#                 font-size: 14px;
#                 padding: 5px;
#                 border-radius: 3px;
#             }

#             QPushButton:hover {
#                 background-color: #696969; /* Un gris más oscuro para el hover */
#             }
#             """
        
#         # Botón de borrar todo
#         delete_button = QPushButton('Borrar todo', self)
#         delete_button.clicked.connect(self.drawing_area.content.clear_all)
#         delete_button.setStyleSheet(button_style)
#         toolbar.addWidget(delete_button)

#         # Espaciador
#         spacer = QWidget()
#         spacer.setFixedSize(50, 5)  # Ajusta el tamaño del espaciador (ancho x alto)
#         spacer.setStyleSheet("background-color: #333;")  # Establece el color de fondo
#         toolbar.addWidget(spacer)

#         # Botón de seleccionar varios
#         self.seleccion_multiple = QPushButton('Seleccionar varios', self)
#         self.seleccion_multiple.setCheckable(True)
#         self.seleccion_multiple.toggled.connect(self.drawing_area.content.set_seleccion_multiple)
#         self.seleccion_multiple.setStyleSheet(button_style + """
#         QPushButton:checked {
#             background-color: #505050; /* Color gris más oscuro cuando está seleccionado */
#         }
#         """)
#         toolbar.addWidget(self.seleccion_multiple)

#         toolbar.setStyleSheet("QToolBar { background-color: #333; }")  # Establece el color de fondo de la barra de herramientas

#     def activar_seleccion_multiple(self, checked):
#         self.drawing_area.content.set_seleccion_multiple(checked)

#     def configure_microbloque(self):
#         self.drawing_area.content.create_new_microbloque()

import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QWidget
from PyQt5.QtGui import QIcon
from .drawing_area import DrawingArea 
from .scrollable_widget import ScrollableWidget

class MacroVista(QPushButton):
    def __init__(self, elementoBack, geometria):
        super().__init__()
        self.modelo = elementoBack
        self.setText(self.modelo.nombre)
        self.setGeometry(geometria)
        self.clicked.connect(self.click)
        self.setStyleSheet("""
            background-color: #0072BB;;  /* Color de fondo azul /
            font-weight: bold;          /* Texto en negrita */
            font-weight: bold;          /* Texto en negrita */
            color: white;               /* Color de texto blanco */
            font-size: 15px;            /* Tamaño de fuente */
            font-family: Arial;  
        """)
    
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.ventana.setGeometry(screen)
        self.ventana.showMaximized()
        self.ventana.setFixedSize(screen.width(), screen.height())
        self.ventana.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        self.drawing_area = DrawingArea(self, self.ventana)
        self.scrollable_widget = ScrollableWidget(self.drawing_area)
        self.ventana.setCentralWidget(self.scrollable_widget)
        
        # Asegurarse de que el tamaño inicial sea suficientemente grande
        self.drawing_area.ajustar_tamanio_widget()
        
        self.init_tool_bar()
        self.ventana.show()
        self.ventana.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
        
        # Ruta de la imagen del logo
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ventana.setWindowIcon(icon)
        
        QTimer.singleShot(100, self.drawing_area.content.load_microbloques)
        
    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)

        button_style = """
            QPushButton {
                background-color: #808080; /* Color gris */
                color: white;
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: #696969; /* Un gris más oscuro para el hover */
            }
            """
        
        # Botón de borrar todo
        delete_button = QPushButton('Borrar todo', self)
        delete_button.clicked.connect(self.drawing_area.content.clear_all)
        delete_button.setStyleSheet(button_style)
        toolbar.addWidget(delete_button)

        # Espaciador
        spacer = QWidget()
        spacer.setFixedSize(50, 5)  # Ajusta el tamaño del espaciador (ancho x alto)
        spacer.setStyleSheet("background-color: #333;")  # Establece el color de fondo
        toolbar.addWidget(spacer)

        # Botón de seleccionar varios
        self.seleccion_multiple = QPushButton('Seleccionar varios', self)
        self.seleccion_multiple.setCheckable(True)
        self.seleccion_multiple.toggled.connect(self.drawing_area.content.set_seleccion_multiple)
        self.seleccion_multiple.setStyleSheet(button_style + """
        QPushButton:checked {
            background-color: #505050; /* Color gris más oscuro cuando está seleccionado */
        }
        """)
        toolbar.addWidget(self.seleccion_multiple)

        toolbar.setStyleSheet("QToolBar { background-color: #333; }")  # Establece el color de fondo de la barra de herramientas

    def activar_seleccion_multiple(self, checked):
        self.drawing_area.content.set_seleccion_multiple(checked)

    def configure_microbloque(self):
        self.drawing_area.content.create_new_microbloque()