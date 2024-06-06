from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QGridLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .macro_diagrama import MacroDiagrama

class MainWindow(QMainWindow):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.showMaximized()
        
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
        
        # Panel de herramientas
        self.init_tool_bar()


        diagrama = MacroDiagrama(self.sesion)
        diagrama.show()
        self.setCentralWidget(diagrama)
    

    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        delete_button = QPushButton('Borrar', self)
        # delete_button.clicked.connect(lambda: self.drawing_area.clear())
        toolbar.addWidget(delete_button)
        pass

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