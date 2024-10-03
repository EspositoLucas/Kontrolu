from PyQt5.QtWidgets import QMenu,QDialog, QVBoxLayout, QTabWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QHeaderView
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor
from back.topologia.configuraciones import Configuracion, TipoError
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo
from back.topologia.microbloque import MicroBloque
from back.json_manager.json_manager import obtener_microbloques_de_una_macro, agregar_microbloque, borrar_micro_bloque



class CrearMicroBloque(QDialog):
    def __init__(self, micro_bloque, tipo, parent=None,tab=0):
        super().__init__(parent)
        self.tipo = tipo
        self.new_microbloque = micro_bloque
        self.parent = parent
        self.setWindowTitle("Nuevo Micro Bloque")
        self.setStyleSheet("background-color: #333; color: white;")
        self.create_new_microbloque(tab)


    def create_new_microbloque(self,tab):
        """
        Función principal para crear un nuevo microbloque o seleccionar un preset.
        """
        

        layout = QVBoxLayout()

        # Crear el tab principal para "Nuevo Microbloque" y "Presets"
        main_tab = QTabWidget()
        main_tab.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #555; 
                background-color: #333;
            }
            QTabBar::tab { 
                background-color: #444; 
                color: white; 
                padding: 5px;
            }
            QTabBar::tab:selected { 
                background-color: #555;
            }
        """)
        self.tabs = main_tab

        # Crear la pestaña "Presets"
        presets_tab = self.create_presets_tab()
        main_tab.addTab(presets_tab, "Presets")

        # Crear la pestaña "Nuevo Microbloque"
        new_microbloque_tab = self.create_new_microbloque_tab()
        main_tab.addTab(new_microbloque_tab, "Nuevo Microbloque")
        self.tabs.setCurrentIndex(tab)

        # Añadir el tab principal al layout
        layout.addWidget(main_tab)

        self.setLayout(layout)




    def create_presets_tab(self):
        """
        Crea la pestaña para seleccionar presets. Utiliza un QTreeWidget para mostrar una jerarquía.
        """
        presets_tab = QWidget()
        presets_layout = QVBoxLayout(presets_tab)

        # Label de Presets
        preset_label = QLabel("Seleccionar Preset:")
        preset_label.setStyleSheet("color: white;")
        presets_layout.addWidget(preset_label)

        # Crear QTreeWidget para mostrar los presets en forma de diccionario jerárquico
        presets_tree = QTreeWidget()
        presets_tree.setHeaderLabels(["Preset", "Seleccionar"])
        presets_tree.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")


        # Añadir elementos del diccionario al QTreeWidget
        self.populate_presets_tree(presets_tree)

        presets_layout.addWidget(presets_tree)
        
        # Botón "Crear Microbloque"
        create_button = QPushButton("Crear Microbloque Desde 0")
        create_button.setStyleSheet("background-color: #444; color: white;")
        create_button.clicked.connect(self.go_to_create_microbloque_tab)  # Conectar el botón a la función que cambia la pestaña
        presets_layout.addWidget(create_button)
        
        return presets_tab

    def go_to_create_microbloque_tab(self):
        """
        Cambia a la pestaña 'Nuevo Microbloque' en el QTabWidget.
        """
        self.tabs.setCurrentIndex(1)



    def populate_presets_tree(self, tree_widget):
        """
        Función para agregar los elementos del diccionario de presets a un QTreeWidget.
        """
        # Obtener los microbloques (el método que estás usando)
        tree_widget.setHeaderHidden(True)
        presets = obtener_microbloques_de_una_macro(self.tipo)

        # Asegurarse de que el texto se ajuste a la columna automáticamente
        tree_widget.header().setStretchLastSection(False)
        tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        for dominio in presets:
            parent_item = QTreeWidgetItem([dominio.nombre])
            tree_widget.addTopLevelItem(parent_item)
            parent_item.setExpanded(True)
            
            for tipo in dominio.tipos:
                sub_item = QTreeWidgetItem([tipo.nombre_tipo])
                parent_item.addChild(sub_item)
                sub_item.setExpanded(True)
                
                for microbloque in tipo.micro_bloques:
                    # Crear el texto con el nombre y la descripción
                    button_text = microbloque.nombre
                    if microbloque.descripcion:
                        button_text += f" - {microbloque.descripcion}"
                    
                    # Crear el QTreeWidgetItem relacionado con el sub_item
                    option_item = QTreeWidgetItem([button_text])  
                    sub_item.addChild(option_item)

                    # Conectar el evento de selección de este item a la función select_preset
                    option_item.microbloque = microbloque  # Guardar el microbloque como atributo del item
                    option_item.dominio = dominio
                    option_item.tipo = tipo
                    tree_widget.itemClicked.connect(self.on_item_clicked)

                    tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
                    tree_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.tree_widget = tree_widget

    def show_context_menu(self, pos):
        """
        Muestra un menú contextual al hacer clic derecho en el QTreeWidget.
        """
        item = self.tree_widget.itemAt(pos)
        if item is not None:
            # Crear el menú contextual
            context_menu = QMenu(self)

            # Agregar acciones al menú
            action_delete = context_menu.addAction("Eliminar Preset")

            # Conectar las acciones a los métodos correspondientes
            action_delete.triggered.connect(lambda: self.delete_preset(item))

            # Mostrar el menú en la posición del clic
            context_menu.exec_(self.tree_widget.viewport().mapToGlobal(pos))

    def delete_preset(self, item):
        """
        Método para eliminar el preset y actualizar la pestaña.
        """
        borrar_micro_bloque(item.tipo.nombre_tipo, item.dominio.nombre, self.tipo, item.microbloque)
        
        # Crear una nueva pestaña de presets
        new_presets_tab = self.create_presets_tab()
        
        # Eliminar la pestaña antigua
        self.tabs.removeTab(0)
        
        # Insertar la nueva pestaña en el mismo índice
        self.tabs.insertTab(0, new_presets_tab, "Presets")
        
        # Establecer la pestaña actualizada como la actual
        self.tabs.setCurrentIndex(0)


    def on_item_clicked(self, item, column):
        """
        Método que se ejecuta al hacer clic en un elemento del árbol.
        """
        if hasattr(item, 'microbloque'):
            # Llama al método select_preset pasando el microbloque del item clickeado
            self.select_preset(item.microbloque)



    def select_preset(self, mi_preset):
        """
        Selecciona un preset para crear un nuevo microbloque.
        """
        self.new_microbloque.set_dto(mi_preset)

        self.entrada_name_input.setText(self.new_microbloque.configuracion_entrada.nombre)
        self.entrada_unidad_input.setText(self.new_microbloque.configuracion_entrada.unidad)
        self.salida_name_input.setText(self.new_microbloque.configuracion_salida.nombre)
        self.salida_unidad_input.setText(self.new_microbloque.configuracion_salida.unidad)
        self.latex_editor.set_latex(self.new_microbloque.funcion_transferencia)
        self.name_input.setText(self.new_microbloque.nombre)
        self.color_button.setProperty("selected_color", self.new_microbloque.color)

        self.go_to_create_microbloque_tab()

    def create_new_microbloque_tab(self):

        """
        Crea la pestaña para la creación de un nuevo microbloque.
        """
        new_microbloque_tab = QWidget()
        new_microbloque_layout = QVBoxLayout(new_microbloque_tab)

        # Nombre del microbloque
        name_input = QLineEdit(self.new_microbloque.nombre)
        name_input.setPlaceholderText("Nombre del microbloque")
        name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        new_microbloque_layout.addWidget(name_input)
        self.name_input = name_input

        # Botón para seleccionar color
        color_button = QPushButton("Seleccionar Color")
        color_button.setStyleSheet("background-color: #444; color: white;")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        new_microbloque_layout.addWidget(color_button)
        self.color_button = color_button

        # Función de transferencia
        transfer_label = QLabel("Función de Transferencia:")
        transfer_label.setStyleSheet("color: white;")
        latex_editor = LatexEditor(self.new_microbloque.funcion_transferencia)
        latex_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        new_microbloque_layout.addWidget(transfer_label)
        new_microbloque_layout.addWidget(latex_editor)
        self.latex_editor = latex_editor

        # Pestaña de configuraciones
        config_tab = self.create_config_tab()
        new_microbloque_layout.addWidget(config_tab)

        guardar_preset = QPushButton("Guardar Preset")
        guardar_preset.setStyleSheet("background-color: #444; color: white;")
        guardar_preset.clicked.connect(self.guardar_preset)  # Conectar el botón a la función que cambia la pestaña
        new_microbloque_layout.addWidget(guardar_preset)

        create_button = QPushButton("Aplicar")
        create_button.setStyleSheet("background-color: #444; color: white;")
        create_button.clicked.connect(self.crear_microbloque_nuevo)  # Conectar el botón a la función que cambia la pestaña
        new_microbloque_layout.addWidget(create_button)
        
        return new_microbloque_tab
    
    def guardar_preset(self):

        presets = obtener_microbloques_de_una_macro(self.tipo)

        dialog = QDialog()
        dialog.setWindowTitle(f"Guardar preset de {self.new_microbloque.nombre}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

         # Primer desplegable: Dominio
        dominio_combo = QComboBox()
        dominio_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        dominio_combo.addItems(list(map(lambda x: x.nombre, presets)))  # Añadir los dominios existentes
        dominio_combo.setEditable(True)  # Permitir escribir uno nuevo

        
        layout.addWidget(QLabel("Dominio"))
        layout.addWidget(dominio_combo)

        # Segundo desplegable: Tipo
        tipo_combo = QComboBox()
        tipo_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        tipo_combo.setEditable(True)  # Permitir escribir uno nuevo
        layout.addWidget(QLabel("Tipo"))
        layout.addWidget(tipo_combo)

        dominio_combo.currentTextChanged.connect(lambda:self.update_tipo_combo(tipo_combo,dominio_combo.currentText(),presets))  # Conectar cambio de texto

        # Botón para guardar el preset
        save_button = QPushButton("Guardar Preset")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(lambda: self.save_preset(tipo_combo.currentText(),dominio_combo.currentText(),dialog))  # Conectar el botón a la función que cambia la pestaña
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        
        # Llenar el combobox de tipos basado en el primer dominio por defecto
        self.update_tipo_combo(tipo_combo,dominio_combo.currentText(),presets)
        dialog.exec_()
    
    def save_preset(self,tipo,dominio,dialog):
        agregar_microbloque(self.new_microbloque.get_dto(),tipo,dominio,self.tipo)
        # Crear una nueva pestaña de presets
        new_presets_tab = self.create_presets_tab()
        
        # Eliminar la pestaña antigua
        self.tabs.removeTab(0)
        
        # Insertar la nueva pestaña en el mismo índice
        self.tabs.insertTab(0, new_presets_tab, "Presets")
        dialog.accept()
        

    def update_tipo_combo(self, tipo_combo, dominio, presets):
        tipo_combo.clear()  # Limpiar las opciones actuales

        for preset in presets:
            if preset.nombre == dominio:
                tipo_combo.addItems(list(map(lambda x: x.nombre_tipo, preset.tipos)))



    def crear_microbloque_nuevo(self):
        nombre = self.name_input.text()
        color = self.color_button.property("selected_color")
        funcion_transferencia = self.latex_editor.get_latex()
        nombre_entrada = self.entrada_name_input.text()
        nombre_salida = self.salida_name_input.text()
        unidad_entrada = self.entrada_unidad_input.text()
        unidad_salida = self.salida_unidad_input.text()
        
        self.new_microbloque.nombre = nombre
        self.new_microbloque.color = color
        self.new_microbloque.funcion_transferencia = funcion_transferencia
        self.new_microbloque.configuracion_entrada.nombre = nombre_entrada
        self.new_microbloque.configuracion_salida.nombre = nombre_salida
        self.new_microbloque.configuracion_entrada.unidad = unidad_entrada
        self.new_microbloque.configuracion_salida.unidad = unidad_salida   
        
        print("Microbloque creado")
        self.accept()
        
    def create_config_tab(self):
        """
        Crea la pestaña interna de configuraciones para entrada y salida.
        """
        config_tab = QTabWidget()
        config_tab.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #555; 
                background-color: #333;
            }
            QTabBar::tab { 
                background-color: #444; 
                color: white; 
                padding: 5px;
            }
            QTabBar::tab:selected { 
                background-color: #555;
            }
        """)

        # Contenido de configuraciones
        config_content = QWidget()
        config_layout = QGridLayout(config_content)

        # Configuración de entrada
        entrada_name_input = QLineEdit(self.new_microbloque.configuracion_entrada.nombre)
        entrada_name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Nombre de la configuración de entrada:"), 0, 0)
        config_layout.addWidget(entrada_name_input, 0, 1)
        self.entrada_name_input = entrada_name_input

        entrada_unidad_input = QLineEdit(self.new_microbloque.configuracion_entrada.unidad)
        entrada_unidad_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Unidad de entrada:"), 0, 2)
        config_layout.addWidget(entrada_unidad_input, 0, 3)
        self.entrada_unidad_input = entrada_unidad_input

        input_button = QPushButton("Configurar Entrada")
        input_button.setStyleSheet("background-color: #444; color: white;")
        input_button.clicked.connect(lambda: self.edit_configuration(self.new_microbloque.configuracion_entrada, "entrada"))
        config_layout.addWidget(input_button, 0, 4)
        self.input_button = input_button

        # Configuración de salida
        salida_name_input = QLineEdit(self.new_microbloque.configuracion_salida.nombre)
        salida_name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Nombre de la configuración de salida:"), 1, 0)
        config_layout.addWidget(salida_name_input, 1, 1)
        self.salida_name_input = salida_name_input

        salida_unidad_input = QLineEdit(self.new_microbloque.configuracion_salida.unidad)
        salida_unidad_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Unidad de salida:"), 1, 2)
        config_layout.addWidget(salida_unidad_input, 1, 3)
        self.salida_unidad_input = salida_unidad_input

        output_button = QPushButton("Configurar Salida")
        output_button.setStyleSheet("background-color: #444; color: white;")
        output_button.clicked.connect(lambda: self.edit_configuration(self.new_microbloque.configuracion_salida, "salida"))
        config_layout.addWidget(output_button, 1, 4)

        config_tab.addTab(config_content, "Configuraciones")

        return config_tab



    def edit_configuration(self, configuracion, tipo):
        dialog = QDialog()
        dialog.setWindowTitle(f"Editar Configuración de {tipo.capitalize()}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        fields = [
            ("Límite inferior", "limite_inferior"),
            ("Límite superior", "limite_superior"),
            ("Límite por ciclo", "limite_por_ciclo"),
            ("Error máximo", "error_maximo"),
            ("Proporción", "proporcion"),
            ("Último valor", "ultimo_valor"),
            ("Probabilidad", "probabilidad")
        ]

        input_fields = {}
        for label, attr in fields:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: white;")
            input_field = QLineEdit(str(getattr(configuracion, attr)))
            input_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
            row.addWidget(lbl)
            row.addWidget(input_field)
            layout.addLayout(row)
            input_fields[attr] = input_field

        tipo_error_combo = QComboBox()
        tipo_error_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        for error_type in TipoError:
            tipo_error_combo.addItem(error_type.value)
        tipo_error_combo.setCurrentText(configuracion.tipo.value)
        layout.addWidget(QLabel("Tipo de error"))
        layout.addWidget(tipo_error_combo)

        save_button = QPushButton("Guardar cambios")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(lambda: self.save_configuration(dialog, configuracion, input_fields, tipo_error_combo))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()
    
    def save_configuration(self, dialog, configuracion, input_fields, tipo_error_combo):
        # Creamos una nueva instancia de Configuracion para guardar los cambios

        for attr, input_field in input_fields.items():
            value = input_field.text()
            try:
                if value.lower() == "inf":
                    setattr(configuracion, attr, float('inf'))
                elif value.lower() == "-inf":
                    setattr(configuracion, attr, float('-inf'))
                else:
                    setattr(configuracion, attr, float(value))
            except ValueError:
                QMessageBox.warning(dialog, "Error", f"Valor inválido para {attr}")
                return

        configuracion.tipo = TipoError(tipo_error_combo.currentText())

        
        dialog.accept()
        
    def get_attr_from_label(self, label):
        attr_map = {
            "Límite inferior": "limite_inferior",
            "Límite superior": "limite_superior",
            "Límite por ciclo": "limite_por_ciclo",
            "Error máximo": "error_maximo",
            "Proporción": "proporcion",
            "Último valor": "ultimo_valor",
            "Probabilidad": "probabilidad"
        }
        return attr_map.get(label, "")