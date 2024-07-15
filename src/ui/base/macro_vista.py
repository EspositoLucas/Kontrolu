# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar
# from .drawing_area import DrawingArea

# class MacroVista(QPushButton):
#     def __init__(self, elementoBack, geometria):
#         super().__init__()
#         self.modelo = elementoBack
#         self.setText(self.modelo.nombre)
#         self.setGeometry(geometria)
#         self.clicked.connect(self.click)
    
#     def click(self):
#         self.ventana = QMainWindow()
#         self.ventana.setWindowTitle(self.modelo.nombre)
#         self.ventana.setGeometry(0, 0, 600, 600)
        
#         self.drawing_area = DrawingArea(self, self.ventana)
#         self.ventana.setCentralWidget(self.drawing_area)
        
#         self.init_tool_bar()
#         self.ventana.show()
        
#         self.drawing_area.load_microbloques()
    
#     def init_tool_bar(self):
#         toolbar = QToolBar("Herramientas", self.ventana)
#         self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
#         delete_button = QPushButton('Borrar todo', self)
#         delete_button.clicked.connect(self.drawing_area.clear_all)
#         toolbar.addWidget(delete_button)

#     def configure_microbloque(self):
#         self.drawing_area.create_new_microbloque()


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QAction
from .drawing_area import DrawingArea

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
        self.ventana.setGeometry(0, 0, 600, 600)
        
        self.drawing_area = DrawingArea(self, self.ventana)
        self.ventana.setCentralWidget(self.drawing_area)
        
        self.init_tool_bar()
        self.ventana.show()
        
        self.drawing_area.content.load_microbloques()
    
        
    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        delete_button = QPushButton('Borrar todo', self)
        delete_button.clicked.connect(self.drawing_area.content.clear_all)
        toolbar.addWidget(delete_button)

        self.seleccion_multiple = QPushButton('Seleccionar varios', self)
        self.seleccion_multiple.setCheckable(True)
        self.seleccion_multiple.toggled.connect(self.drawing_area.content.set_seleccion_multiple)
        toolbar.addWidget(self.seleccion_multiple)

    def activar_seleccion_multiple(self, checked):
        self.drawing_area.content.set_seleccion_multiple(checked)

    def configure_microbloque(self):
        self.drawing_area.content.create_new_microbloque()
        

    







