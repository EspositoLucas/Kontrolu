from PyQt5.QtWidgets import  QAction, QFileDialog, QMessageBox, QMenu, QAction
from PyQt5.QtGui import QIcon
import json 

class Archivo(QMenu):
    def __init__(self,main_window,sesion):
        super().__init__('Archivo',main_window)
        self.main_window = main_window
        self.sesion = sesion
        self.setup()
        self.setStyleSheet("""
            QMenu {
                background-color: #444;
                color: white;
            }
            QMenu::item {
                background-color: #666;
                border-radius: 3px;
                padding-right: 40px;  
                margin-top: 5px;  
            }
            QMenu::item:selected {
                background-color: #777;
            }
        """)
        

        
    
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