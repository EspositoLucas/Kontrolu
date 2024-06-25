# from PyQt5.QtCore import Qt, QPoint
# from PyQt5.QtWidgets import (QPushButton, QMainWindow, QToolBar, QInputDialog, QColorDialog, 
#                              QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QDialog)
# from PyQt5.QtGui import QColor
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
        
#         self.init_tool_bar()
#         self.drawing_area = DrawingArea(self.ventana, self.modelo)
#         self.ventana.setCentralWidget(self.drawing_area)
#         self.ventana.show()
    
#     def init_tool_bar(self):
#         toolbar = QToolBar("Herramientas", self.ventana)
#         self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
#         delete_button = QPushButton('Borrar todo', self)
#         delete_button.clicked.connect(self.clear_all)
#         toolbar.addWidget(delete_button)

#         microbloque_button = QPushButton('Microbloque', self)
#         microbloque_button.clicked.connect(self.configure_microbloque)
#         toolbar.addWidget(microbloque_button)

#         delete_microbloque_button = QPushButton('Borrar Microbloque', self)
#         delete_microbloque_button.clicked.connect(self.delete_microbloque)
#         toolbar.addWidget(delete_microbloque_button)

#         flecha_button = QPushButton('Flecha', self)
#         flecha_button.clicked.connect(self.add_flecha)
#         toolbar.addWidget(flecha_button)

#         delete_flecha_button = QPushButton('Borrar Flecha', self)
#         delete_flecha_button.clicked.connect(self.delete_flecha)
#         toolbar.addWidget(delete_flecha_button)

#     def configure_microbloque(self):
#         dialog = QDialog(self.ventana)
#         dialog.setWindowTitle("Configurar Microbloque")
        
#         layout = QVBoxLayout()
        
#         name_layout = QHBoxLayout()
#         name_label = QLabel("Nombre (opcional):")
#         name_input = QLineEdit()
#         name_input.setPlaceholderText(f"Microbloque {len(self.drawing_area.microbloques) + 1}")
#         name_layout.addWidget(name_label)
#         name_layout.addWidget(name_input)
        
#         color_button = QPushButton("Seleccionar Color (opcional)")
#         color_button.clicked.connect(lambda: self.select_color(color_button))
        
#         save_button = QPushButton("Guardar")
#         save_button.clicked.connect(dialog.accept)
        
#         layout.addLayout(name_layout)
#         layout.addWidget(color_button)
#         layout.addWidget(save_button)
        
#         dialog.setLayout(layout)
        
#         if dialog.exec_():
#             nombre = name_input.text() if name_input.text() else None
#             color = color_button.property("selected_color") if color_button.property("selected_color") else None
#             self.drawing_area.start_creating_microbloque({"nombre": nombre, "color": color})

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)

#     def delete_microbloque(self):
#         self.drawing_area.delete_microbloque()

#     def add_flecha(self):
#         if len(self.drawing_area.microbloques) >= 2:
#             start = self.drawing_area.microbloques[0].pos() + QPoint(50, 25)
#             end = self.drawing_area.microbloques[1].pos() + QPoint(50, 25)
#             self.drawing_area.add_arrow(start, end)

#     def delete_flecha(self):
#         self.drawing_area.delete_arrow()

#     def clear_all(self):
#         self.drawing_area.microbloques.clear()
#         self.drawing_area.arrows.clear()
#         self.drawing_area.update()



# from PyQt5.QtCore import Qt, QPoint
# from PyQt5.QtWidgets import (QPushButton, QMainWindow, QToolBar, QInputDialog, QColorDialog, 
#                              QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QDialog)
# from PyQt5.QtGui import QColor
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
        
#         self.init_tool_bar()
#         self.drawing_area = DrawingArea(self.ventana, self.modelo)
#         self.ventana.setCentralWidget(self.drawing_area)
#         self.ventana.show()
    
#     def init_tool_bar(self):
#         toolbar = QToolBar("Herramientas", self.ventana)
#         self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
#         delete_button = QPushButton('Borrar todo', self)
#         delete_button.clicked.connect(self.clear_all)
#         toolbar.addWidget(delete_button)

#         microbloque_button = QPushButton('Microbloque', self)
#         microbloque_button.clicked.connect(self.configure_microbloque)
#         toolbar.addWidget(microbloque_button)

#         delete_microbloque_button = QPushButton('Borrar Microbloque', self)
#         delete_microbloque_button.clicked.connect(self.delete_microbloque)
#         toolbar.addWidget(delete_microbloque_button)

#         flecha_button = QPushButton('Flecha', self)
#         flecha_button.clicked.connect(self.start_creating_arrow)
#         toolbar.addWidget(flecha_button)

#         delete_flecha_button = QPushButton('Borrar Flecha', self)
#         delete_flecha_button.clicked.connect(self.delete_flecha)
#         toolbar.addWidget(delete_flecha_button)

#     def configure_microbloque(self):
#         dialog = QDialog(self.ventana)
#         dialog.setWindowTitle("Configurar Microbloque")
        
#         layout = QVBoxLayout()
        
#         name_layout = QHBoxLayout()
#         name_label = QLabel("Nombre:")
#         name_input = QLineEdit()
#         name_input.setPlaceholderText(f"Microbloque {len(self.drawing_area.microbloques) + 1}")
#         name_layout.addWidget(name_label)
#         name_layout.addWidget(name_input)
        
#         color_button = QPushButton("Seleccionar Color")
#         color_button.clicked.connect(lambda: self.select_color(color_button))
        
#         transfer_function_layout = QHBoxLayout()
#         transfer_function_label = QLabel("Función de Transferencia:")
#         transfer_function_input = QLineEdit()
#         transfer_function_layout.addWidget(transfer_function_label)
#         transfer_function_layout.addWidget(transfer_function_input)
        
#         save_button = QPushButton("Guardar")
#         save_button.clicked.connect(dialog.accept)
        
#         layout.addLayout(name_layout)
#         layout.addWidget(color_button)
#         layout.addLayout(transfer_function_layout)
#         layout.addWidget(save_button)
        
#         dialog.setLayout(layout)
        
#         if dialog.exec_():
#             nombre = name_input.text() if name_input.text() else None
#             color = color_button.property("selected_color") if color_button.property("selected_color") else None
#             funcion_transferencia = transfer_function_input.text() if transfer_function_input.text() else None
#             self.drawing_area.start_creating_microbloque({
#                 "nombre": nombre,
#                 "color": color,
#                 "funcion_transferencia": funcion_transferencia
#             })

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)

#     def delete_microbloque(self):
#         self.drawing_area.delete_microbloque()

#     def start_creating_arrow(self):
#         self.drawing_area.start_creating_arrow()
        
#     def add_flecha(self):
#         if len(self.drawing_area.microbloques) >= 2:
#             start = self.drawing_area.microbloques[0].pos() + QPoint(50, 25)
#             end = self.drawing_area.microbloques[1].pos() + QPoint(50, 25)
#             self.drawing_area.add_arrow(start, end)


#     def delete_flecha(self):
#         self.drawing_area.delete_arrow()

#     def clear_all(self):
#         self.drawing_area.microbloques.clear()
#         self.drawing_area.arrows.clear()
#         self.drawing_area.update()


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
    
    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        delete_button = QPushButton('Borrar todo', self)
        delete_button.clicked.connect(self.drawing_area.clear_all)
        toolbar.addWidget(delete_button)

        # delete_microbloque_button = QPushButton('Borrar Microbloque', self)
        # delete_microbloque_button.clicked.connect(self.drawing_area.delete_microbloque)
        # toolbar.addWidget(delete_microbloque_button)

    def configure_microbloque(self):
        self.drawing_area.create_new_microbloque()