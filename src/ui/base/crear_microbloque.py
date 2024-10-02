from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QColor
from .latex_editor import LatexEditor
from back.topologia.configuraciones import Configuracion, TipoError
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

class CrearMicroBloque(QDialog):
    def __init__(self, parent, pos, relation, reference_structure,numero):
        super().__init__(parent)
        self.new_microbloque = MicroBloque(nombre=f"Microbloque {numero}", color=QColor(255, 255, 255))
        self.numero = numero
        self.parent = parent
        self.pos = pos
        self.relation = relation
        self.reference_structure = reference_structure
        self.setWindowTitle("Nuevo Micro Bloque")
        self.setStyleSheet("background-color: #333; color: white;")
        self.create_new_microbloque()


    def create_new_microbloque(self):
        """
        Función principal para crear un nuevo microbloque o seleccionar un preset.
        """
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Microbloque o Seleccionar Preset")
        dialog.setStyleSheet("background-color: #333; color: white;")
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

        # Añadir el tab principal al layout
        layout.addWidget(main_tab)

        dialog.setLayout(layout)
        dialog.exec_()



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

        # Ejemplo de diccionario de presets
        presets = {
            "Preset 1": {
                "Subnivel 1": {
                    "Opción 1.1": "Info 1.1",
                    "Opción 1.2": "Info 1.2"
                },
                "Subnivel 2": {
                    "Opción 2.1": "Info 2.1"
                }
            },
            "Preset 2": {
                "Subnivel 1": {
                    "Opción 1.1": "Info 1.1"
                }
            }
        }

        # Añadir elementos del diccionario al QTreeWidget
        self.populate_presets_tree(presets_tree, presets)

        presets_layout.addWidget(presets_tree)
        
        # Botón "Crear Microbloque"
        create_button = QPushButton("Crear Microbloque")
        create_button.setStyleSheet("background-color: #444; color: white;")
        create_button.clicked.connect(self.go_to_create_microbloque_tab)  # Conectar el botón a la función que cambia la pestaña
        presets_layout.addWidget(create_button)
        
        return presets_tab

    def go_to_create_microbloque_tab(self):
        """
        Cambia a la pestaña 'Nuevo Microbloque' en el QTabWidget.
        """
        self.tabs.setCurrentIndex(1)


    def populate_presets_tree(self, tree_widget, presets):
        """
        Función para agregar los elementos del diccionario de presets a un QTreeWidget.
        """
        for key, sub_presets in presets.items():
            parent_item = QTreeWidgetItem([key])
            tree_widget.addTopLevelItem(parent_item)
            parent_item.setExpanded(True)
            
            for subkey, options in sub_presets.items():
                sub_item = QTreeWidgetItem([subkey])
                parent_item.addChild(sub_item)
                sub_item.setExpanded(True)
                
                for option_key, option_value in options.items():
                    option_item = QTreeWidgetItem([option_key])
                    sub_item.addChild(option_item)
                    
                    # Botón "Seleccionar" al final de cada opción
                    select_button = QPushButton("+")
                    select_button.clicked.connect(lambda _, k=option_key: self.select_preset(k))
                    tree_widget.setItemWidget(option_item, 1, select_button)


    def select_preset(self, preset_name):
        """
        Función que se ejecuta al seleccionar un preset.
        """
        print(f"Preset seleccionado: {preset_name}")

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

        create_button = QPushButton("Crear Microbloque")
        create_button.setStyleSheet("background-color: #444; color: white;")
        create_button.clicked.connect(self.crear_microbloque_nuevo)  # Conectar el botón a la función que cambia la pestaña
        new_microbloque_layout.addWidget(create_button)
        
        return new_microbloque_tab
    
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
        
        if isinstance(self.reference_structure, MicroBloque):
            self.parent.agregar_respecto_microbloque(self.new_microbloque, self.relation, self.reference_structure)
        elif isinstance(self.reference_structure, TopologiaSerie):
            self.parent.agregar_respecto_serie(self.new_microbloque, self.relation, self.reference_structure)
        elif isinstance(self.reference_structure, TopologiaParalelo):
            self.parent.agregar_respecto_paralelo(self.new_microbloque, self.relation, self.reference_structure)
        else:
            self.parent.macrobloque.modelo.topologia.agregar_elemento(self.new_microbloque) # sería el primer microbloque

        self.parent.load_microbloques()  # recargo todos los microbloques
        self.parent.update()
        self.parent.hide_add_buttons() # ocultamos los botones "+" por si quedaron visibles
        
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