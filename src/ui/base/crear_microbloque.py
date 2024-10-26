from PyQt5.QtWidgets import QMenu,QDialog, QVBoxLayout, QTabWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtWidgets import  QHeaderView, QColorDialog
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor
from PyQt5 import QtGui
import os
from back.json_manager.json_manager import obtener_microbloques_de_una_macro, agregar_microbloque, borrar_micro_bloque, recrear_datos
from .modificar_configuracion import ModificarConfiguracion
from ..base.vista_json import VistaJson
from vcolorpicker import getColor
from PyQt5.QtGui import QColor

LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")

class CrearMicroBloque(QDialog):
    def __init__(self, micro_bloque, tipo, parent=None,tab=0):
        super().__init__(parent)
        self.tipo = tipo
        self.new_microbloque = micro_bloque
        self.padre = parent
        self.setWindowTitle("Nuevo Micro Bloque")
        self.setStyleSheet(ESTILO)
        self.create_new_microbloque(tab)


    def create_new_microbloque(self,tab):
        """
        Función principal para crear un nuevo microbloque o seleccionar un preset.
        """

        layout = QVBoxLayout()
        
        # Agregar botón de ayuda en la parte superior
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)  # Hacer el botón circular
        help_button.setToolTip("Ayuda sobre la configuración del microbloque")
        help_button.clicked.connect(self.mostrar_ayuda)
        layout.addWidget(help_button, alignment=Qt.AlignRight)

        # Crear el tab principal para "Nuevo Microbloque" y "Presets"
        main_tab = QTabWidget()
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
        presets_layout.addWidget(preset_label)

        # Crear QTreeWidget para mostrar los presets en forma de diccionario jerárquico
        presets_tree = QTreeWidget()
        presets_tree.setHeaderLabels(["Preset", "Seleccionar"])

        try:

            # Añadir elementos del diccionario al QTreeWidget
            self.populate_presets_tree(presets_tree)

            presets_layout.addWidget(presets_tree)
        except Exception as e:

            error_layout = QHBoxLayout()
            error_label = QLabel("El archivo de presets falló.")
            recreate_button = QPushButton("Recrear Archivo de Presets")
            recreate_button.clicked.connect(self.recreate_presets_file)
            error_layout.addWidget(error_label)
            error_layout.addWidget(recreate_button)
            error_layout.addStretch()  # Añadir un estiramiento para empujar los widgets a la izquierda
            presets_layout.addLayout(error_layout)
        
        # Botón "Crear Microbloque"
        create_button = QPushButton("Crear Microbloque Desde 0")
        create_button.clicked.connect(self.go_to_create_microbloque_tab)  # Conectar el botón a la función que cambia la pestaña
        presets_layout.addWidget(create_button)
        
        return presets_tab
    
    def recreate_presets_file(self):

        recrear_datos()        

        # Crear una nueva pestaña de presets
        new_presets_tab = self.create_presets_tab()
        
        # Eliminar la pestaña antigua
        self.tabs.removeTab(0)
        
        # Insertar la nueva pestaña en el mismo índice
        self.tabs.insertTab(0, new_presets_tab, "Presets")
        
        # Establecer la pestaña actualizada como la actual
        self.tabs.setCurrentIndex(0)


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
        self.descripcion_input.setText(self.new_microbloque.descripcion)

        self.go_to_create_microbloque_tab()

    def create_new_microbloque_tab(self):

        """
        Crea la pestaña para la creación de un nuevo microbloque.
        """
        new_microbloque_tab = QWidget()
        new_microbloque_layout = QVBoxLayout(new_microbloque_tab)

        # Nombre del microbloque
        nombre_label = QLabel("Nombre:")
        name_input = QLineEdit(self.new_microbloque.nombre)
        name_input.setPlaceholderText("Nombre del microbloque")
        new_microbloque_layout.addWidget(nombre_label)
        new_microbloque_layout.addWidget(name_input)
        self.name_input = name_input

        # Nombre del microbloque
        desc_label = QLabel("Descripcion:")
        descripcion_input = QLineEdit(self.new_microbloque.descripcion)
        descripcion_input.setPlaceholderText("Descripcion:")
        new_microbloque_layout.addWidget(desc_label)
        new_microbloque_layout.addWidget(descripcion_input)
        self.descripcion_input = descripcion_input

        # Botón para seleccionar color
        self.color_button = QPushButton("Seleccionar Color")
        self.color_button.setProperty("selected_color", self.new_microbloque.color)
        self.color_button.clicked.connect(lambda: self.select_color(self.color_button))
        new_microbloque_layout.addWidget(self.color_button)

        # Función de transferencia
        transfer_label = QLabel("Función de Transferencia:")
        latex_editor = LatexEditor(self.new_microbloque.funcion_transferencia)
        new_microbloque_layout.addWidget(transfer_label)
        new_microbloque_layout.addWidget(latex_editor)
        self.latex_editor = latex_editor

        # Pestaña de configuraciones
        config_tab = self.create_config_tab()
        new_microbloque_layout.addWidget(config_tab)

        guardar_preset = QPushButton("Guardar Preset")
        guardar_preset.clicked.connect(self.guardar_preset)  # Conectar el botón a la función que cambia la pestaña
        new_microbloque_layout.addWidget(guardar_preset)

        create_button = QPushButton("Aplicar")
        create_button.clicked.connect(self.crear_microbloque_nuevo)  # Conectar el botón a la función que cambia la pestaña
        new_microbloque_layout.addWidget(create_button)

        edit_json_button = QPushButton("Editar JSON")
        edit_json_button.clicked.connect(self.editar_json)  # Conectar el botón al método editar_json
        new_microbloque_layout.addWidget(edit_json_button)
        
        return new_microbloque_tab

    def mostrar_ayuda(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración del Microbloque")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(600)
        layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Guía de Configuración del Microbloque")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)

        # Contenido organizado en secciones
        contenido = [
            ("<b>¿Qué es un Microbloque?</b>",
            "Un microbloque es un componente fundamental que representa una función de transferencia específica en un sistema de control. "
            "Permite modelar el comportamiento de diferentes partes del sistema."),
            
            ("<b>Elementos principales:</b>",
            "<ul>"
            "<li><b>Nombre:</b> Identificador único del microbloque</li>"
            "<li><b>Descripción:</b> Breve explicación del propósito o funcionamiento</li>"
            "<li><b>Color:</b> Identificador visual para el microbloque en el diagrama</li>"
            "<li><b>Función de transferencia:</b> Expresión matemática que, a través de un cociente, relaciona la respuesta de un sistema (modelada o señal de salida) con una señal de entrada o excitación (también modelada). Se usa para caracterizar las relaciones de entrada y salida de componentes o de sistemas que se describen mediante ecuaciones diferenciales lineales e invariantes en el tiempo</li>"
            "</ul>"),
            
            ("<b>Presets:</b>",
            "Los presets son configuraciones predefinidas que pueden reutilizarse:"
            "<ul>"
            "<li><b>Dominio:</b> Categoría principal del microbloque (ej: Mecánico, Eléctrico)</li>"
            "<li><b>Tipo:</b> Subcategoría específica dentro del dominio</li>"
            "<li><b>Guardar preset:</b> Permite almacenar la configuración actual como plantilla</li>"
            "</ul>"),
            
            ("<b>Funcionalidades adicionales:</b>",
            "<ul>"
            "<li><b>Editor JSON:</b> Permite modificar la configuración en formato JSON</li>"
            "<li><b>Editor LaTeX:</b> Interface para escribir funciones matemáticas con notación LaTeX</li>"
            "<li><b>Vista previa:</b> Muestra cómo se verá el microbloque en el sistema</li>"
            "</ul>")
        ]

        for titulo, texto in contenido:
            seccion = QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 10px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)

        # Botón de cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()
    
    def actualizar_campos(self):
        """
        Actualiza todos los campos del formulario con los valores actuales del microbloque.
        """
        self.name_input.setText(self.new_microbloque.nombre)
        self.descripcion_input.setText(self.new_microbloque.descripcion)
        self.color_button.setProperty("selected_color", self.new_microbloque.color)
        self.color_button.setStyleSheet(f"background-color: {self.new_microbloque.color.name()};")
        self.latex_editor.set_latex(self.new_microbloque.funcion_transferencia)
        self.entrada_name_input.setText(self.new_microbloque.configuracion_entrada.nombre)
        self.entrada_unidad_input.setText(self.new_microbloque.configuracion_entrada.unidad)
        self.salida_name_input.setText(self.new_microbloque.configuracion_salida.nombre)
        self.salida_unidad_input.setText(self.new_microbloque.configuracion_salida.unidad)

    def editar_json(self):
        """
        Abre un diálogo para editar el JSON del microbloque.
        """
        vista = VistaJson(self.new_microbloque, self)
        vista.exec_()
        if vista.result():
            self.actualizar_campos()
            if self.padre.__class__.__name__ == 'Microbloque':
                self.padre.actualizar()


    def select_color(self, button):

        r, g, b, _ = self.new_microbloque.color.getRgb()
        rgb_tuple = getColor((r, g, b))
        rgb_int_tuple = tuple(int(x) for x in rgb_tuple)
        color = QColor(*rgb_int_tuple)

        if color.isValid():
            self.color = color
            self.color_button.setProperty("selected_color", color)
            self.color_button.setStyleSheet(f"background-color: {color.name()}; color: {self.calcular_color(color).name()};")

    
    def guardar_preset(self):

        presets = obtener_microbloques_de_una_macro(self.tipo)

        dialog = QDialog()
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowTitle(f"Guardar preset de {self.new_microbloque.nombre}")
        layout = QVBoxLayout()
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))

         # Primer desplegable: Dominio
        dominio_combo = QComboBox()
        dominio_combo.addItems(list(map(lambda x: x.nombre, presets)))  # Añadir los dominios existentes
        dominio_combo.setEditable(True)  # Permitir escribir uno nuevo

        
        layout.addWidget(QLabel("Dominio"))
        layout.addWidget(dominio_combo)

        # Segundo desplegable: Tipo
        tipo_combo = QComboBox()
        tipo_combo.setEditable(True)  # Permitir escribir uno nuevo
        layout.addWidget(QLabel("Tipo"))
        layout.addWidget(tipo_combo)

        dominio_combo.currentTextChanged.connect(lambda:self.update_tipo_combo(tipo_combo,dominio_combo.currentText(),presets))  # Conectar cambio de texto

        # Botón para guardar el preset
        save_button = QPushButton("Guardar Preset")
        save_button.clicked.connect(lambda: self.save_preset(tipo_combo.currentText(),dominio_combo.currentText(),dialog))  # Conectar el botón a la función que cambia la pestaña
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        
        # Llenar el combobox de tipos basado en el primer dominio por defecto
        self.update_tipo_combo(tipo_combo,dominio_combo.currentText(),presets)
        dialog.exec_()
    
    def save_preset(self, tipo, dominio, dialog):
        if not self.latex_editor.es_funcion_valida(self.latex_editor.get_latex()):
            QMessageBox.warning(self, "Función de transferencia inválida", 
                                "La función de transferencia no es válida. Por favor, corríjala antes de guardar el preset.")
            return

        nombre = self.name_input.text()
        color = self.color_button.property("selected_color")
        funcion_transferencia = self.latex_editor.get_latex()
        nombre_entrada = self.entrada_name_input.text()
        nombre_salida = self.salida_name_input.text()
        unidad_entrada = self.entrada_unidad_input.text()
        unidad_salida = self.salida_unidad_input.text()
        descripcion = self.descripcion_input.text()

        self.new_microbloque.descripcion = descripcion
        self.new_microbloque.nombre = nombre
        self.new_microbloque.color = color
        self.new_microbloque.funcion_transferencia = funcion_transferencia
        self.new_microbloque.configuracion_entrada.nombre = nombre_entrada
        self.new_microbloque.configuracion_salida.nombre = nombre_salida
        self.new_microbloque.configuracion_entrada.unidad = unidad_entrada
        self.new_microbloque.configuracion_salida.unidad = unidad_salida   

        agregar_microbloque(self.new_microbloque.get_dto(), tipo, dominio, self.tipo)
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
        if not self.latex_editor.es_funcion_valida(self.latex_editor.get_latex()):
            QMessageBox.warning(self, "Función de transferencia inválida", 
                                "La función de transferencia no es válida. Por favor, corríjala antes de continuar.")
            return

        nombre = self.name_input.text()
        color = self.color_button.property("selected_color")
        funcion_transferencia = self.latex_editor.get_latex()
        nombre_entrada = self.entrada_name_input.text()
        nombre_salida = self.salida_name_input.text()
        unidad_entrada = self.entrada_unidad_input.text()
        unidad_salida = self.salida_unidad_input.text()
        descripcion = self.descripcion_input.text()

        self.new_microbloque.descripcion = descripcion        
        self.new_microbloque.nombre = nombre
        self.new_microbloque.color = color
        self.new_microbloque.funcion_transferencia = funcion_transferencia
        self.new_microbloque.configuracion_entrada.nombre = nombre_entrada
        self.new_microbloque.configuracion_salida.nombre = nombre_salida
        self.new_microbloque.configuracion_entrada.unidad = unidad_entrada
        self.new_microbloque.configuracion_salida.unidad = unidad_salida   
        
        self.accept()
        
    def create_config_tab(self):
        """
        Crea la pestaña interna de configuraciones para entrada y salida.
        """
        config_tab = QTabWidget()

        # Contenido de configuraciones
        config_content = QWidget()
        config_layout = QGridLayout(config_content)

        # Configuración de entrada
        entrada_name_input = QLineEdit(self.new_microbloque.configuracion_entrada.nombre)
        config_layout.addWidget(QLabel("Nombre de la configuración de entrada:"), 0, 0)
        config_layout.addWidget(entrada_name_input, 0, 1)
        self.entrada_name_input = entrada_name_input

        entrada_unidad_input = QLineEdit(self.new_microbloque.configuracion_entrada.unidad)
        config_layout.addWidget(QLabel("Unidad de entrada:"), 0, 2)
        config_layout.addWidget(entrada_unidad_input, 0, 3)
        self.entrada_unidad_input = entrada_unidad_input

        input_button = QPushButton("Configurar Entrada")
        input_button.clicked.connect(lambda: self.edit_configuration(self.new_microbloque.configuracion_entrada, "entrada"))
        config_layout.addWidget(input_button, 0, 4)
        self.input_button = input_button

        # Configuración de salida
        salida_name_input = QLineEdit(self.new_microbloque.configuracion_salida.nombre)
        config_layout.addWidget(QLabel("Nombre de la configuración de salida:"), 1, 0)
        config_layout.addWidget(salida_name_input, 1, 1)
        self.salida_name_input = salida_name_input

        salida_unidad_input = QLineEdit(self.new_microbloque.configuracion_salida.unidad)
        config_layout.addWidget(QLabel("Unidad de salida:"), 1, 2)
        config_layout.addWidget(salida_unidad_input, 1, 3)
        self.salida_unidad_input = salida_unidad_input

        output_button = QPushButton("Configurar Salida")
        output_button.clicked.connect(lambda: self.edit_configuration(self.new_microbloque.configuracion_salida, "salida"))
        config_layout.addWidget(output_button, 1, 4)

        config_tab.addTab(config_content, "Configuraciones")

        return config_tab
    
    def edit_configuration(self, configuracion, tipo):
        """
        Abre un diálogo para editar una configuración.
        """
        ModificarConfiguracion(configuracion= configuracion, tipo=tipo, padre=self)


    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = LETRA_COLOR if es_claro else TEXTO_BLANCO
        return color_texto

ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;  /* Tamaño de botón más grande */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
    }

    QPushButton:hover {
        background-color: #606060;  /* Gris aún más oscuro al pasar el cursor */
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
        background-color: #F1F1F1;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: white;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }
"""