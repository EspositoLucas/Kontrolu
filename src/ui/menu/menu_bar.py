from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtGui import QFont

from .archivo import Archivo
from  ..base.vista_json import VistaJson

class Menu(QMenuBar):
    def __init__(self,main_window,sesion):
        super().__init__(main_window)
        self.sesion = sesion
        self.main_window = main_window
        self.setup(main_window)
    
    def setup(self,main_window):
        archivo = Archivo(main_window,self.sesion)
        self.addMenu(archivo)

        self.setStyleSheet("""
            QMenuBar {
                background-color: #333;
                color: white;
                font-size: 14px;
                padding: 5px 5px;  /* Ajustar el relleno para cambiar el ancho */
            }
            
            QMenuBar::item {
                padding: 5px;
                background-color: #555;
                border-radius: 3px;
                margin-right: 10px;
            }      
        """)
        
        font = QFont("Arial", 12)
        self.setFont(font)
        
        editar_json = self.addMenu("Editar JSON")
        editar_json.setStyleSheet("""
            QMenu {
            background-color: #444;
            color: white;
            }
            QMenu::item {
            background-color: #666;
            padding: 5px;
            border-radius: 3px;
            }
            QMenu::item:selected {
            background-color: #777;
            }
        """)

        # Add actions to the "Editar JSON" menu
        editar_json_action = editar_json.addAction("Open JSON Editor")
        editar_json_action.triggered.connect(self.open_json_editor)

    def open_json_editor(self):
        vista = VistaJson(self.sesion, self.main_window)
        vista.exec_()
        if vista.result():
            self.main_window.actualizar_sesion()