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
        
        self.setStyleSheet(ESTILO)
        
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
        menu.setStyleSheet(ESTILO)
        
        # Agregamos las acciones del archivo original
        archivo = Archivo(self.main_window, self.sesion)
        for action in archivo.actions():
            menu.addAction(action)
        
        # Mostramos el menú debajo del botón
        button = self.sender()
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec_(pos)

ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #707070;  /* Un gris más oscuro para mayor contraste */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;  /* Texto en negrita */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
    }

    QLineEdit {
        background-color: #FAF8F6;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }
    
    QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
    }

    QLabel {
        color: #2B2D42;  /* Texto gris oscuro */
        background-color: transparent;
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox {
        background-color: #D0D0D0;  /* Fondo gris claro */
        color: #2B2D42;  /* Texto gris oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 5px;
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox QAbstractItemView {
        background-color: #D0D0D0;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: #2B2D42;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }

    QTabWidget::pane {
        border: 2px solid #505050;
        border-radius: 10px;
        background-color: #FAF8F6;
        padding: 10px;
    }

    QTabBar::tab {
        background-color: #D0D0D0;
        color: #2B2D42;
        border: 2px solid #505050;
        border-radius: 5px;
        padding: 12px 30px;  /* Aumentar el padding para más espacio */
        min-width: 140px;   /* Tamaño mínimo para evitar solapamiento */
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-weight: bold;  /* Texto en negrita */
    }

    QTabBar::tab:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco en la pestaña seleccionada */
    }

    QTabBar::tab:hover {
        background-color: #606060;  /* Fondo gris más oscuro al pasar el cursor */
        color: white;  /* Texto en blanco al pasar el cursor */
    }

    QTableWidget {
        background-color: #FAF8F6;  /* Color de fondo del área sin celdas */
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        gridline-color: #505050;  /* Color de las líneas de la cuadrícula */
    }

    QTableWidget::item {
        background-color: #D0D0D0;  /* Color de fondo de las celdas */
        border: none;
    }

    QHeaderView::section {
        background-color: #808080;
        color: white;
        padding: 5px;
        border: 1px solid #505050;
    }

    QTableCornerButton::section {
        background-color: #808080;  /* Color del botón de esquina */
        border: 1px solid #505050;
    }

    QListWidget {
        background-color: #D0D0D0;
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QListWidget::item:selected {
        background-color: #808080;
        color: white;
    }

    QMenu {
        background-color: #D0D0D0;  /* Fondo gris claro para el menú */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-family: "Segoe UI", "Arial", sans-serif;
        font-size: 14px;
    }

    QMenu::item {
        background-color: transparent;  /* Fondo transparente para los items */
        padding: 8px 20px;  /* Espaciado para los items */
        color: #2B2D42;
    }

    QMenu::item:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco al seleccionar */
    }

    QMenuBar {
        background-color: #B0B0B0;  /* Fondo gris pastel oscuro para la barra de menú */
        border: 1px solid #505050;  /* Borde gris oscuro */
    }

    QMenuBar::item {
        background-color: transparent;  /* Fondo transparente para los items de la barra de menú */
        padding: 8px 16px;  /* Espaciado para los items */
        color: #2B2D42;
    }

    QMenuBar::item:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco al seleccionar */
    }

    QMenuBar::item:pressed {
        background-color: #606060;  /* Fondo más oscuro al hacer clic */
        color: white;  /* Texto en blanco al hacer clic */
    }

"""
