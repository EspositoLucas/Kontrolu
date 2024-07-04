# # 

# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar
# from .drawing_area import DrawingArea

# class MacroVista(QPushButton):
#     def __init__(self, elementoBack, geometria):
#         super().__init__()
#         self.modelo = elementoBack
#         self.setText(self.modelo.nombre)
#         self.setGeometry(geometria)
#         self.setCheckable(True)
#         self.clicked.connect(self.click)
    
#     def click(self):
#         self.ventana = QMainWindow()
#         self.ventana.setWindowTitle(self.modelo.nombre)
#         self.ventana.setGeometry(0, 0, 600, 600)
        
#         self.drawing_area = DrawingArea(self.ventana, self.modelo)
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


# 

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar
from .drawing_area import DrawingArea

class MacroVista(QPushButton):
    def __init__(self, elementoBack, geometria):
        super().__init__()
        self.modelo = elementoBack
        self.setText(self.modelo.nombre)
        self.setGeometry(geometria)
        self.setCheckable(True)
        self.clicked.connect(self.click)
    
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        self.ventana.setGeometry(0, 0, 600, 600)
        
        self.drawing_area = DrawingArea(self.ventana, self.modelo)
        self.ventana.setCentralWidget(self.drawing_area)
        
        self.init_tool_bar()
        self.ventana.show()
        
        self.drawing_area.canvas.load_microbloques()
    
    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        delete_button = QPushButton('Borrar todo', self)
        delete_button.clicked.connect(self.drawing_area.canvas.clear_all)
        toolbar.addWidget(delete_button)

    def configure_microbloque(self):
        self.drawing_area.canvas.create_new_microbloque()