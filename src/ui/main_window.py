# src/ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .drawing_area import DrawingArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Diagramador')
        self.setGeometry(100, 100, 800, 600)
        
        # Menú de archivo
        new_action = QAction(QIcon('new.png'), 'Nuevo', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_project)
        
        open_action = QAction(QIcon('open.png'), 'Abrir', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_project)
        
        save_action = QAction(QIcon('save.png'), 'Guardar', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_project)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Archivo')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        
        self.statusBar().showMessage('Listo')
        
        # Área de dibujo
        self.drawing_area = DrawingArea()
        self.setCentralWidget(self.drawing_area)
        
        # Panel de herramientas
        self.initToolBar()
    
    def initToolBar(self):
        toolbar = QToolBar("Herramientas", self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        
        square_btn = QPushButton("Cuadrado", self)
        square_btn.clicked.connect(lambda: self.drawing_area.set_shape('square'))
        toolbar.addWidget(square_btn)
        
        rect_btn = QPushButton("Rectángulo", self)
        rect_btn.clicked.connect(lambda: self.drawing_area.set_shape('rectangle'))
        toolbar.addWidget(rect_btn)
        
        circle_btn = QPushButton("Círculo", self)
        circle_btn.clicked.connect(lambda: self.drawing_area.set_shape('circle'))
        toolbar.addWidget(circle_btn)
        
        arrow_btn = QPushButton("Flecha", self)
        arrow_btn.clicked.connect(lambda: self.drawing_area.set_shape('arrow'))
        toolbar.addWidget(arrow_btn)

    def new_project(self):
        self.statusBar().showMessage('Nuevo proyecto creado')
        self.drawing_area.clear()

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