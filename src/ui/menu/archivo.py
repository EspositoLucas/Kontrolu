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
                background-color: white;
                border: 1px solid #777;
            }
            
            QMenu::item:selected {
                background-color: #ADD8E6;
                color: black;
            }
        """)
    
    def setup(self):
        # Menú de archivo
        
        # Modificar la acción "Nuevo" para usar el parámetro from_menu
        new_action = QAction(QIcon('new.png'), 'Nuevo', self.main_window)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(lambda: self.new_project(from_menu=False))
        
        open_action = QAction(QIcon('open.png'), 'Abrir', self.main_window)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_project)
        
        save_action = QAction(QIcon('save.png'), 'Guardar', self.main_window)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_project)

        self.addAction(new_action)
        self.addAction(open_action)
        self.addAction(save_action)
    
    def new_project(self, from_menu=False):
            if not from_menu:
                reply = QMessageBox.question(self.main_window, 'Confirmar Nuevo Proyecto', 
                            '¿Seguro que quieres crear un nuevo proyecto? Se perderán los cambios no guardados.', 
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.sesion.nueva_sesion()
                    self.main_window.actualizar_sesion()
                    self.main_window.statusBar().showMessage('Nuevo proyecto creado')
                    return True
                return False
            else:
                # Si se llama desde el menú inicial, no mostrar confirmación
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