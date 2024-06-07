from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QGridLayout, QWidget, QPushButton,QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .macro_diagrama import MacroDiagrama
from .menu.archivo import Archivo
from .menu.menu_bar import Menu
from .diagramtest import Ui_Form

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
        
        # Panel de herramientas
        self.init_tool_bar()

        a = Ui_Form()
        a.setupUi(self)
        a.pushButton.show()
        a.pushButton_2.show()
        a.pushButton_3.show()
        a.pushButton_4.show()
        a.line.show()
        a.line_2.show()
        a.line_3.show()
        a.line_4.show()
        a.line_5.show()
        a.line_6.show()

        

        # diagrama = MacroDiagrama(self.sesion)
        # diagrama.show()
        # self.setCentralWidget(diagrama)
    

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