from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtGui import QFont

from .archivo import Archivo
from  ..base.vista_json import VistaJson
from PyQt5.QtWidgets import (QPushButton, QWidget,QMenu,QHBoxLayout)
from PyQt5.QtCore import Qt


class Menu(QMenuBar):
    def __init__(self,main_window,sesion):
        super().__init__(main_window)
        self.sesion = sesion
        self.main_window = main_window
        self.setup(main_window)
    
    def setup(self, main_window):
        
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
        
        # Creamos los botones personalizados
        archivo_button = QPushButton("Archivo", self)
        archivo_button.setFixedSize(120, 40)  # Tamaño fijo para el botón
        archivo_button.setStyleSheet("""
            QPushButton {
                background-color: #4682B4;
                color: #FFFDF5;
                border: 2px solid #2B2D42;
                border-radius: 20px;
                font-weight: bold;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5793C5;
                cursor: pointer;
            }
        """)
        
        editar_json_button = QPushButton("Editar JSON", self)
        editar_json_button.setFixedSize(120, 40)
        editar_json_button.setStyleSheet("""
            QPushButton {
                background-color: #4682B4;
                color: #FFFDF5;
                border: 2px solid #2B2D42;
                border-radius: 20px;
                font-weight: bold;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5793C5;
                cursor: pointer;
            }
        """)
        
        # Creamos un widget contenedor para los botones
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(10, 0, 0, 0)  # Margen izquierdo de 10px
        button_layout.setSpacing(10)  # Espacio entre botones
        button_layout.addWidget(archivo_button)
        button_layout.addWidget(editar_json_button)
        button_layout.addStretch()
        
        # Conectamos las acciones
        archivo_button.clicked.connect(self.show_archivo_menu)
        editar_json_button.clicked.connect(self.open_json_editor)
        
        # Establecemos el widget como el widget principal del menú
        self.setCornerWidget(button_widget, Qt.TopLeftCorner)  # Aquí

    def open_json_editor(self):
        vista = VistaJson(self.sesion, self.main_window)
        vista.exec_()
        if vista.result():
            self.main_window.actualizar_sesion()
            
    
    def show_archivo_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #444;
                color: white;
                border: 1px solid #2B2D42;
                border-radius: 10px;
            }
            QMenu::item {
                background-color: #666;
                padding: 5px 20px;
                border-radius: 5px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #777;
            }
        """)
        
        # Agregamos las acciones del archivo original
        archivo = Archivo(self.main_window, self.sesion)
        for action in archivo.actions():
            menu.addAction(action)
        
        # Mostramos el menú debajo del botón
        button = self.sender()
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec_(pos)