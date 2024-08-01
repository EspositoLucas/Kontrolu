from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog,QComboBox,QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPointF
from .latex_editor import LatexEditor
from back.configuracion.configuracion import Configuracion, TipoConfiguracion,EfectoConfiguracion
from back.configuracion.configuracion_microbloque import ConfiguracionMicrobloque
class Microbloque(QWidget):
    def __init__(self, parent=None, microbloque_back=None):
        super().__init__(parent)
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.color = microbloque_back.color or QColor(255, 255, 0)
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.configuracion_mb = microbloque_back.configuracion
        self.esta_selecionado = False
        self.setFixedSize(microbloque_back.ancho(), microbloque_back.alto())
        self.setAttribute(Qt.WA_StyledBackground, True)
        color_texto = self.calcular_color(self.color)
        self.setStyleSheet(f"""
            font-weight: bold;
            color: {color_texto};
            font-family: Arial;  
            background-color: {self.color.name()};
        """)
    
    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = "black" if es_claro else "white"
        return color_texto

    def setPos(self, pos):
        self.move(pos.toPoint())

    def setSeleccionado(self, seleccionado):
        self.esta_selecionado = seleccionado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dibuja el rectángulo
        if self.esta_selecionado:
            painter.setPen(QPen(Qt.red, 3))  # Borde rojo y más grueso para seleccionados
        else:
            painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(self.color)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        # Configura la fuente
        font = QFont("Arial", max(1, round(10)), QFont.Bold)
        painter.setFont(font)

        # Configura el color del texto
        color_texto = self.calcular_color(self.color)
        painter.setPen(QPen(QColor(color_texto)))
        
        # Dibuja el texto
        text_rect = self.rect().adjusted(5, 5, -5, -5)  # Margen para el texto
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.nombre)

    def mouseDoubleClickEvent(self, event):
        self.edit_properties()

    def seleccion_tipo_configuracion_edit(self, edit_config_layout, type_combo):
        # paso 1: eliminar el input de valor (si existe en el edit_config_layout) --> seria el segundo QLineEdit del layout
        
        # Identificar y eliminar el segundo QLineEdit
        qlineedit_counter = 0
        for i in range(edit_config_layout.count()):
            item = edit_config_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QLineEdit):
                qlineedit_counter += 1
                if qlineedit_counter == 2:
                    edit_config_layout.removeWidget(widget)
                    widget.deleteLater()
                    break
    
        # paso 2: eliminar el combo de efecto (si exite en el edit_config_layout) --> sería el segundo QComboBox del layout 

        qcombobox_counter = 0
        for i in range(edit_config_layout.count()):
            item = edit_config_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QComboBox):
                qcombobox_counter += 1
                if qcombobox_counter == 2:
                    edit_config_layout.removeWidget(widget)
                    widget.deleteLater()
                    break

        # Obtener el tipo de configuración seleccionado
        tipo_seleccionado = type_combo.currentData()
        if tipo_seleccionado is None:
            return  # Si no hay tipo seleccionado, no hacemos nada

        # Crear los widgets específicos según el tipo de configuración seleccionado
        input_widget = None
        efecto_combo = None
        if tipo_seleccionado == TipoConfiguracion.NUMERICA:
            # Para configuración numérica, se crea un campo de entrada de texto
            input_widget = QLineEdit()
            input_widget.setPlaceholderText("Ingrese un valor de tipo numérico")
        elif tipo_seleccionado == TipoConfiguracion.FUNCION:
            # Para configuración de función, se crea un campo de entrada y un combo box para el efecto
            input_widget = LatexEditor()
            efecto_combo = QComboBox()
            efecto_combo.addItem("Seleccione tipo de efecto", None)  # Opción por defecto
            efecto_combo.addItem(EfectoConfiguracion.DIRECTO.name, EfectoConfiguracion.DIRECTO)
            efecto_combo.addItem(EfectoConfiguracion.INDIRECTO.name, EfectoConfiguracion.INDIRECTO)
            efecto_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        elif tipo_seleccionado == TipoConfiguracion.ENUMERADA:
            # Para configuración enumerada, se crea un campo de entrada de texto
            input_widget = QLineEdit()
            input_widget.setPlaceholderText("Ingrese valores separados por comas")

        if input_widget != None:
            input_widget.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
            edit_config_layout.insertWidget(2, input_widget)
        if efecto_combo:
            edit_config_layout.insertWidget(3, efecto_combo)

        # Actualizar la interfaz para reflejar los cambios
        self.update()

    def edit_configuration(self, configuracion, layout):
        if configuracion is None: # esto sería raro que pase
            QMessageBox.warning(self, "Error", f"No se encontró la configuración")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar Configuración: {configuracion.nombre}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        edit_config_layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setText(configuracion.nombre)
        name_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        edit_config_layout.addWidget(name_input)

        type_combo = QComboBox()
        for t in TipoConfiguracion:
            type_combo.addItem(t.name, t)
        type_combo.setCurrentIndex(type_combo.findData(configuracion.tipo)) # esto selecciona el tipo de la configuracion en el combo
        type_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        type_combo.currentIndexChanged.connect(lambda: self.seleccion_tipo_configuracion_edit(edit_config_layout, type_combo))
        edit_config_layout.addWidget(type_combo)
        
        if configuracion.tipo != TipoConfiguracion.BOOLEANA: # si no es booleana
            if configuracion.tipo == TipoConfiguracion.FUNCION: # si es de tipo funcion
                funcion, efecto = configuracion.get_valor() # capturamos tanto la funcion como el efecto
                value_input = LatexEditor(initial_latex=funcion) # creamos un input para la funcion
                value_input.update_preview()
                edit_config_layout.addWidget(value_input) # agrega el input a la ventana
                efecto_combo = QComboBox() # creamos el combo del efecto y le agregamos las opciones
                efecto_combo.addItem(EfectoConfiguracion.DIRECTO.name, EfectoConfiguracion.DIRECTO)
                efecto_combo.addItem(EfectoConfiguracion.INDIRECTO.name, EfectoConfiguracion.INDIRECTO)
                efecto_combo.setCurrentIndex(efecto_combo.findData(efecto)) # seleccionamos la opcion segun el tipo de efecto que tenia la configuracion
                efecto_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
                edit_config_layout.addWidget(efecto_combo)
            else: # si entra por acá, entonces es de tipo ENUMERADA O NUMERICA
                valor = configuracion.get_valor() 
                value_input = QLineEdit(valor)
                value_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
                edit_config_layout.addWidget(value_input)

        save_button = QPushButton("Guardar cambios")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(lambda: self.save_edited_configuration(
            dialog,
            configuracion.nombre, 
            name_input, 
            type_combo, 
            self.find_input_widget(edit_config_layout, QLineEdit, 2) if (type_combo.currentData() != TipoConfiguracion.FUNCION) else self.find_input_widget(edit_config_layout, LatexEditor, 1), #El numero es la ocurrencia del widget en el layout, no el numero de widget
            self.find_input_widget(edit_config_layout, QComboBox, 2).currentData() if (type_combo.currentData() == TipoConfiguracion.FUNCION and self.find_input_widget(edit_config_layout, QComboBox, 2)) else None
        ))
        edit_config_layout.addWidget(save_button)

        dialog.setLayout(edit_config_layout)
        dialog.exec_()

    def find_input_widget(self, layout, widget_type, occurrence=2):
        counter = 0
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, widget_type):
                counter += 1
                if counter == occurrence:
                    return widget
        return None

    def save_edited_configuration(self, dialog, old_name, name_input, type_combo, value_input, efecto_combo=None):
        new_name = name_input.text()
        new_type = type_combo.currentData()
        if new_type == TipoConfiguracion.BOOLEANA:
            new_value = True
        else:
            if new_type == TipoConfiguracion.FUNCION:
                new_value = value_input.get_latex()
            else:
                new_value = value_input.text()  
        new_efecto = efecto_combo if efecto_combo else None

        self.elemento_back.actualizar_configuracion(old_name, new_name, new_type, new_value, new_efecto)

        # Actualizar el texto del botón si el nombre ha cambiado
        if old_name != new_name:
            for i in range(self.layout().count()):
                widget = self.layout().itemAt(i).widget()
                if isinstance(widget, QPushButton) and widget.text() == old_name: # busca los botones del dialog por el nombre
                    widget.setText(new_name) # le cambia el nombre
                    widget.clicked.disconnect() # le desasocia la accion vieja para el evento clicked
                    widget.clicked.connect(lambda: self.edit_configuracion(new_name)) # le configura la nueva accion de edicion
                    break

        dialog.accept()

    def edit_properties(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Microbloque")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        name_input = QLineEdit(self.nombre)
        name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(name_input)

        color_button = QPushButton("Cambiar Color")
        color_button.setStyleSheet(f"background-color: {self.color.name()};")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        transfer_label.setStyleSheet("color: white;")
        latex_editor = LatexEditor(initial_latex=self.funcion_transferencia)
        latex_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)
        
        # Agregar sección para configuraciones
        config_label = QLabel("Configuraciones:")
        config_label.setStyleSheet("color: white;")
        layout.addWidget(config_label)

        config_layout = QHBoxLayout()
        for config in self.configuracion_mb.get_configuraciones().items(): # items devuelve una lista de tuplas [(clave, valor), ...]
            config_boton = QPushButton(config[0]) # i=0 es la clave, i=1 es el valor asociado a la clave en el diccionario
            config_boton.setStyleSheet("background-color: #444; color: white;")
            config_boton.clicked.connect(lambda: self.edit_configuration(config[1], layout))
            config_layout.addWidget(config_boton)
            layout.addLayout(config_layout)

        add_config_button = QPushButton("Agregar Configuración")
        add_config_button.setStyleSheet("background-color: #444; color: white;")
        add_config_button.clicked.connect(lambda: self.add_configuration(layout))
        layout.addWidget(add_config_button)
       
        save_button = QPushButton("Guardar")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)
        
        dialog.setLayout(layout)

        if dialog.exec_():
            self.elemento_back.nombre = name_input.text()
            self.elemento_back.color = self.color
            self.nombre = name_input.text()
            nueva_funcion = latex_editor.get_latex()
            self.elemento_back.funcion_transferencia = nueva_funcion
            self.funcion_transferencia = nueva_funcion      
            self.update()
    
    def seleccion_tipo_configuracion(self, layout, type_combo):
        # Este método se llama cuando el usuario selecciona un tipo de configuración en el combo box

        # buscar y eliminar el input de valor (si existe en el layout) --> sería el segundo QLineEdit del layout
        input_widget = self.find_input_widget(layout, QLineEdit, 2)
        efecto_combo = self.find_input_widget(layout, QComboBox, 2)

        # Limpiar los widgets anteriores para evitar conflictos
        if input_widget != None:
            layout.removeWidget(input_widget)
            input_widget.deleteLater()
            input_widget = None
        
        if efecto_combo != None:
            layout.removeWidget(self.efecto_combo)
            efecto_combo.deleteLater()
            efecto_combo = None
            
        # Obtener el tipo de configuración seleccionado
        tipo_seleccionado = type_combo.currentData()
        if tipo_seleccionado is None:
            return  # Si no hay tipo seleccionado, no hacemos nada

        # Crear los widgets específicos según el tipo de configuración seleccionado
        if tipo_seleccionado == TipoConfiguracion.NUMERICA:
            # Para configuración numérica, se crea un campo de entrada de texto
            input_widget = QLineEdit()
            input_widget.setPlaceholderText("Ingrese un valor de tipo numérico")
        elif tipo_seleccionado == TipoConfiguracion.FUNCION:
            # Para configuración de función, se crea un campo de entrada y un combo box para el efecto
            input_widget = LatexEditor() # se crea el editor y la vista previa de latex
            efecto_combo = QComboBox()
            efecto_combo.addItem("Seleccione tipo de efecto", None)  # Opción por defecto
            efecto_combo.addItem("DIRECTO", EfectoConfiguracion.DIRECTO)
            efecto_combo.addItem("INDIRECTO", EfectoConfiguracion.INDIRECTO)
            efecto_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        elif tipo_seleccionado == TipoConfiguracion.ENUMERADA:
            # Para configuración enumerada, se crea un campo de entrada de texto
            input_widget = QLineEdit()
            input_widget.setPlaceholderText("Ingrese valores separados por comas")

        # Aplicar estilo y agregar los widgets al layout
        
        input_widget.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        layout.insertWidget(2, input_widget)
        layout.insertWidget(3, efecto_combo)

        # Actualizar la interfaz para reflejar los cambios
        self.update()

    def edit_configuracion(self, configuracion):
        if configuracion is None: # esto sería raro que pase
            QMessageBox.warning(self, "Error", f"No se encontró la configuración")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar Configuración: {configuracion.nombre}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        edit_config_layout = QHBoxLayout()

        name_input = QLineEdit()
        name_input.setText(configuracion.nombre)
        name_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        edit_config_layout.addWidget(name_input)

        type_combo = QComboBox()
        for t in TipoConfiguracion:
            type_combo.addItem(t.name, t)
        type_combo.setCurrentIndex(type_combo.findData(configuracion.tipo)) # esto selecciona el tipo de la configuracion en el combo
        type_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        type_combo.currentIndexChanged.connect(lambda: self.seleccion_tipo_configuracion_edit(edit_config_layout, type_combo))
        edit_config_layout.addWidget(type_combo)
        
        if configuracion.tipo != TipoConfiguracion.BOOLEANA: # si no es booleana
            if configuracion.tipo == TipoConfiguracion.FUNCION: # si es de tipo funcion
                funcion, efecto = configuracion.get_valor() # capturamos tanto la funcion como el efecto
                value_input = LatexEditor(initial_latex=funcion) # creamos un input para la funcion
                value_input.update_preview()
                edit_config_layout.addWidget(value_input) # agrega el input a la ventana
                efecto_combo = QComboBox() # creamos el combo del efecto y le agregamos las opciones
                efecto_combo.addItem(EfectoConfiguracion.DIRECTO.name, EfectoConfiguracion.DIRECTO)
                efecto_combo.addItem(EfectoConfiguracion.INDIRECTO.name, EfectoConfiguracion.INDIRECTO)
                efecto_combo.setCurrentIndex(efecto_combo.findData(efecto)) # seleccionamos la opcion segun el tipo de efecto que tenia la configuracion
                efecto_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
                edit_config_layout.addWidget(efecto_combo)
            else: # si entra por acá, entonces es de tipo ENUMERADA O NUMERICA
                valor = configuracion.get_valor() 
                value_input = QLineEdit(valor)
                value_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
                edit_config_layout.addWidget(value_input)

        save_button = QPushButton("Guardar cambios")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(lambda: self.save_edited_configuration(
            dialog,
            configuracion.nombre, 
            name_input, 
            type_combo, 
            self.find_input_widget(edit_config_layout, QLineEdit, 2), #El numero es la ocurrencia del widget en el layout, no el numero de widget
            self.find_input_widget(edit_config_layout, QComboBox, 2).currentData() if (configuracion.tipo == TipoConfiguracion.FUNCION and self.find_input_widget(edit_config_layout, QComboBox, 2)) else None
        ))
        edit_config_layout.addWidget(save_button)

        dialog.setLayout(edit_config_layout)
        dialog.exec_()

    def guardar_configuracion(self, dialog, name_input, layout_del_dialog_principal, type_combo, config_layout):
        # Este método se llama cuando el usuario intenta guardar una configuración

        # Obtener el nombre y tipo de la configuración
        nombre = name_input.text()
        tipo_seleccionado = type_combo.currentData()

        # Validar que se hayan completado los campos básicos
        if not nombre or tipo_seleccionado is None:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return
        
        # buscar input_widget
        input_widget = self.find_input_widget(config_layout, QLineEdit, 2)

        # Manejar configuraciones no booleanas
        efecto = None
        if tipo_seleccionado != TipoConfiguracion.BOOLEANA:
            # Verificar que se haya ingresado un valor
            if not input_widget:
                input_widget = self.find_input_widget(config_layout, LatexEditor, 1)
                if not input_widget.get_latex():
                    QMessageBox.warning(self, "Error", "Por favor, ingrese un valor para la configuración.")
                    return
            
            # Obtener el valor ingresado (texto para QLineEdit, LaTeX para LatexEditor)
            if isinstance(input_widget, QLineEdit):
                valor = input_widget.text()
            else:
                input_widget = self.find_input_widget(config_layout, LatexEditor, 1)
                valor = input_widget.get_latex()
            
            # Validación específica para cada tipo de configuración
            if tipo_seleccionado == TipoConfiguracion.NUMERICA:
                # Asegurar que el valor sea numérico
                if not valor or not valor.replace('.', '').isdigit():
                    QMessageBox.warning(self, "Error", "Por favor, ingrese un valor numérico válido.")
                    return
            elif tipo_seleccionado == TipoConfiguracion.ENUMERADA:
                # Asegurar que haya al menos dos valores separados por comas
                valores = [v.strip() for v in valor.split(',') if v.strip()]
                if len(valores) < 2:
                    QMessageBox.warning(self, "Error", "Por favor, ingrese al menos dos valores separados por comas.")
                    return
                valor = ','.join(valores)  # Reformatear el valor
            elif tipo_seleccionado == TipoConfiguracion.FUNCION:
                # Asegurar que se haya ingresado una función LaTeX no vacía
                if not valor.strip():
                    QMessageBox.warning(self, "Error", "Por favor, ingrese una función válida en LaTeX.")
                    return
                
                # Buscar el combo de efecto:
                efecto_combo = self.find_input_widget(config_layout, QComboBox, 2)

                # Verificar que se haya seleccionado un efecto para la función
                if efecto_combo.currentData() is None:
                    QMessageBox.warning(self, "Error", "Por favor, seleccione un efecto para la función.")
                    return
                efecto = efecto_combo.currentData()
        else:
            # Para configuraciones booleanas, usar True como valor por defecto
            valor = True
        
        
        # if tipo_seleccionado == TipoConfiguracion.FUNCION:
        #     if not hasattr(self, 'efecto_combo') or self.efecto_combo.currentData() is None:
        #         QMessageBox.warning(self, "Error", "Por favor, seleccione un efecto para la función.")
        #         return
        #     efecto = self.efecto_combo.currentData()

        self.elemento_back.agregar_configuracion(nombre, tipo_seleccionado, valor, efecto)
        boton_de_la_configuracion = QPushButton(nombre)
        boton_de_la_configuracion.setStyleSheet("background-color: #444; color: white;")
        boton_de_la_configuracion.clicked.connect(lambda: self.edit_configuracion(self.elemento_back.get_configuracion(nombre)))
        layout_del_dialog_principal.insertWidget(layout_del_dialog_principal.count() - 2, boton_de_la_configuracion)
        # Cerrar el diálogo de configuración
        dialog.accept()

    def add_configuration(self, layout_del_dialog_principal):
        # Este método crea y muestra el diálogo para agregar una nueva configuración

        # Crear el diálogo
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Configuración")
        dialog.setStyleSheet("background-color: #333; color: white;")
        config_layout = QVBoxLayout()

        # Crear el campo de entrada para el nombre de la configuración
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre de la configuración")
        name_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        config_layout.addWidget(name_input)

        # Crear el combo box para seleccionar el tipo de configuración
        type_combo = QComboBox()
        type_combo.addItem("Seleccione un tipo", None)
        for t in TipoConfiguracion:
            type_combo.addItem(t.name, t)
        type_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(type_combo)

        # Conectar el cambio de selección del tipo con el método que actualiza la interfaz
        type_combo.currentIndexChanged.connect(lambda: self.seleccion_tipo_configuracion(config_layout, type_combo))

        # Crear el botón para guardar la configuración
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(lambda: self.guardar_configuracion(dialog, name_input, layout_del_dialog_principal, type_combo, config_layout))
        save_button.setStyleSheet("background-color: #444; color: white;")
        config_layout.addWidget(save_button)

        # Configurar y mostrar el diálogo
        dialog.setLayout(config_layout)
        dialog.exec_()
        

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            button.setStyleSheet(f"background-color: {color.name()};")

    def get_center(self):
        return self.pos() + QPointF(self.width() / 2, self.height() / 2)

    def set_center(self, point):
        new_pos = point - QPointF(self.width() / 2, self.height() / 2)
        self.move(new_pos.toPoint())

    def __str__(self):
        return f"Microbloque(nombre={self.nombre}, color={self.color.name()}, funcion_transferencia={self.funcion_transferencia})"

    def __repr__(self):
        return self.__str__()
