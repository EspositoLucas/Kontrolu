from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QPushButton
from PyQt5.QtCore import Qt

from .menu.archivo import Archivo
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama

class MainWindow(QMainWindow):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.showMaximized()

        menuBar = Menu(self)
        self.setMenuBar(menuBar)

        self.statusBar().showMessage('Listo')
        
        # Panel de herramientas lateral
        self.init_tool_bar()
        
        # Diagrama inicial de lazo cerrado
        self.init_macrobloques()
    

    def init_tool_bar(self):
        toolbar = QToolBar("Herramientas", self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        delete_button = QPushButton('Borrar', self)
        # delete_button.clicked.connect(lambda: self.drawing_area.clear())
        toolbar.addWidget(delete_button)
        pass

    def init_macrobloques(self):
        a = MacroDiagrama()
        a.setupUi(self)
        a.mostrarElementos()

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