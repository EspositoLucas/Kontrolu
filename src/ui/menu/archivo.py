from PyQt5.QtWidgets import  QAction, QFileDialog, QMessageBox, QMenu, QAction
from PyQt5.QtGui import QIcon
import json 

class Archivo(QMenu):
    def __init__(self,main_window,sesion):
        super().__init__('Archivo',main_window)
        self.main_window = main_window
        self.sesion = sesion
        self.setup()
        self.setStyleSheet(ESTILO)
        

        
    
    def setup(self):
        # Menú de archivo
        
        # Modificar la acción "Nuevo" para usar el parámetro from_menu
        new_action = QAction(QIcon('new.png'), 'Nuevo', self.main_window)
        new_action.triggered.connect(lambda: self.new_project(from_menu=False))
        
        open_action = QAction(QIcon('open.png'), 'Abrir', self.main_window)
        open_action.triggered.connect(self.open_project)
        
        save_action = QAction(QIcon('save.png'), 'Guardar', self.main_window)
        save_action.triggered.connect(self.save_project)

        self.addAction(new_action)
        self.addAction(open_action)
        self.addAction(save_action)
    
    def new_project(self, from_menu=False):
        if not from_menu:
            msgBox = QMessageBox(self.main_window)
            msgBox.setWindowTitle('Confirmar Nuevo Proyecto')
            msgBox.setText('¿Seguro que quieres crear un nuevo proyecto? Se perderán los cambios no guardados.')
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            
            # Cambiar el texto del botón "Yes" a "Si"
            yesButton = msgBox.button(QMessageBox.Yes)
            yesButton.setText('Si')
            
            # Aplicar el nuevo estilo
            msgBox.setStyleSheet("""
                QMessageBox {
                    background-color: #B0B0B0;
                    border: 2px solid #505050;
                    border-radius: 15px;
                    padding: 20px;
                }
                
                QTextEdit {
                    background-color: #FAF8F6;  /* Fondo blanco pastel */
    }

                QMessageBox QLabel {
                    color: #2B2D42;
                    font-size: 16px;
                    font-family: "Segoe UI", "Arial", sans-serif;
                    background-color: transparent;
                }

                QMessageBox QPushButton {
                    background-color: #808080;
                    color: white;
                    border: 2px solid #505050;
                    border-radius: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-family: "Segoe UI", "Arial", sans-serif;
                    min-width: 80px;
                    min-height: 30px;
                }

                QMessageBox QPushButton:hover {
                    background-color: #606060;
                }
            """)
            
            reply = msgBox.exec_()
            
            if reply == QMessageBox.Yes:
                self.sesion.nueva_sesion()
                self.main_window.actualizar_sesion()
                self.main_window.statusBar().showMessage('Nuevo proyecto creado')
                return True
            return False
        else:
            self.sesion.nueva_sesion()
            return True

    def open_project(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, 'Abrir Proyecto', '', 'Archivos JSON (*.json);;Todos los archivos (*)', options=options)
        
        if file_name:
            with open(file_name, 'r') as file:
                json_text = file.read()
                try:
                    json_data = json.loads(json_text)
                    self.sesion.validar_dict(json_data)
                    self.sesion.from_json(json_data)
                    self.main_window.actualizar_sesion()
                    self.main_window.statusBar().showMessage(f'Proyecto {file_name} abierto')
                    return True
                except json.JSONDecodeError as e:
                    QMessageBox.critical(self.main_window, "JSON Error", f"La estructura del JSON es incorrecta: {str(e)}")
                except Exception as e:
                    QMessageBox.critical(self.main_window, "Error", f"Error al cargar el JSON: {str(e)}")
        return False
    
    def save_project(self):
        options = QFileDialog.Options()
        file_name = ""
        default_name = self.sesion.nombre + ".json"
        file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', default_name, 'Archivos JSON (*.json)', options=options)
        
        if file_name:

            json_data = self.sesion.to_json()

            with open(file_name, 'w') as file:
                file.write(json.dumps(json_data))

            self.main_window.statusBar().showMessage(f'Proyecto guardado en {file_name}')
            # Lógica para guardar un proyecto

ESTILO = ESTILO = """
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
