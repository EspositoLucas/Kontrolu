from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar
from .drawing_area import DrawingArea

class MacroVista(QPushButton):
    def __init__(self, elementoBack, geometria):
        super().__init__()
        self.modelo = elementoBack
        self.setText(self.modelo.nombre)
        self.setGeometry(geometria)
        self.setCheckable(True)
        self.clicked.connect(self.click) # Conecta el evento click con el método click
    
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        self.ventana.setGeometry(0, 0, 600, 600)
        
        self.init_tool_bar()
        self.drawing_area = DrawingArea(self.ventana, self.modelo)
        self.ventana.setCentralWidget(self.drawing_area)
        self.ventana.show()
    
    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        delete_button = QPushButton('Borrar todo', self)
        delete_button.clicked.connect(self.clear_all)
        toolbar.addWidget(delete_button)

        microbloque_button = QPushButton('Microbloque', self)
        microbloque_button.clicked.connect(self.add_microbloque)
        toolbar.addWidget(microbloque_button)

        delete_microbloque_button = QPushButton('Borrar Microbloque', self)
        delete_microbloque_button.clicked.connect(self.delete_microbloque)
        toolbar.addWidget(delete_microbloque_button)

        flecha_button = QPushButton('Flecha', self)
        flecha_button.clicked.connect(self.add_flecha)
        toolbar.addWidget(flecha_button)

        delete_flecha_button = QPushButton('Borrar Flecha', self)
        delete_flecha_button.clicked.connect(self.delete_flecha)
        toolbar.addWidget(delete_flecha_button)

    def add_microbloque(self):
        nombre = f"Microbloque {len(self.drawing_area.microbloques) + 1}"
        self.drawing_area.add_microbloque(nombre)

    def delete_microbloque(self):
        self.drawing_area.delete_microbloque()

    def add_flecha(self):
        # This is a placeholder. You would implement logic to add arrows between microbloques.
        if len(self.drawing_area.microbloques) >= 2:
            start = self.drawing_area.microbloques[0].pos() + QPoint(50, 25)
            end = self.drawing_area.microbloques[1].pos() + QPoint(50, 25)
            self.drawing_area.add_arrow(start, end)

    def delete_flecha(self):
        self.drawing_area.delete_arrow()

    def clear_all(self):
        self.drawing_area.microbloques.clear()
        self.drawing_area.arrows.clear()
        self.drawing_area.update()