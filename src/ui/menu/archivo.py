from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QHBoxLayout, QWidget, QPushButton, QMenu, QAction
from PyQt5.QtGui import QIcon

class Archivo(QMenu):
    def __init__(self,main_window):
        super().__init__('Archivo',main_window)
        self.main_window = main_window
        self.setup()
    
    def setup(self):
        # Menú de archivo
        new_action = QAction(QIcon('new.png'), 'Nuevo', self.main_window)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_project)
        
        open_action = QAction(QIcon('open.png'), 'Abrir', self.main_window)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_project)
        
        save_action = QAction(QIcon('save.png'), 'Guardar', self.main_window)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_project)

        self.addAction(new_action)
        self.addAction(open_action)
        self.addAction(save_action)
    
    # Estilo para el menú Archivo
        self.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
            }
            
            QMenu::item {
                padding: 8px 20px;
                background-color: transparent; /* Fondo transparente */
            }
            
            QMenu::item:selected {
                background-color: #666; /* Color de fondo seleccionado */
                color: white; /* Color de texto seleccionado */
            }
        """)

    def new_project(self):
        print('Nuevo proyecto creado')
        self.main_window.statusBar().showMessage('Nuevo proyecto creado')

    def open_project(self):
        print('Proyecto abierto')
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.main_window.statusBar().showMessage(f'Proyecto {file_name} abierto')
            # Lógica para abrir un proyecto
    
    def save_project(self):
        print('Proyecto guardado')
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.main_window.statusBar().showMessage(f'Proyecto guardado en {file_name}')
            # Lógica para guardar un proyecto