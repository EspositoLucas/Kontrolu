from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog,QComboBox,QHBoxLayout, QMessageBox, QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF
from .latex_editor import LatexEditor
from back.topologia.configuraciones import Configuracion,TipoError
class Microbloque(QGraphicsItem):
    def __init__(self, microbloque_back=None):
        super().__init__()
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.color = microbloque_back.color or QColor(255, 255, 0)
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.configuracion = microbloque_back.configuracion or Configuracion(self.nombre)
        self.esta_selecionado = False

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(1)
    
    def boundingRect(self):
        return QRectF(0, 0, self.elemento_back.ancho(), self.elemento_back.alto())

    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = "black" if es_claro else "white"
        return color_texto

    def setPos(self, pos):
        super().setPos(pos)

    def height(self):
        return self.boundingRect().height()
    
    def width(self):
        return self.boundingRect().width()

    def setSeleccionado(self, seleccionado):
        self.esta_selecionado = seleccionado
        self.update()

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.esta_selecionado:
            painter.setPen(QPen(Qt.red, 3))
        else:
            painter.setPen(QPen(Qt.black, 2))
        
        painter.setBrush(self.color)
        painter.drawRect(self.boundingRect())
        
        font = QFont("Arial", max(1, round(10)), QFont.Bold)
        painter.setFont(font)
        
        color_texto = self.calcular_color(self.color)
        painter.setPen(QPen(QColor(color_texto)))
        
        text_rect = self.boundingRect().adjusted(5, 5, -5, -5)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.nombre)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.edit_properties()


    def edit_configuration(self, configuracion, layout):
        dialog = QDialog(self.scene().views()[0].window())
        dialog.setWindowTitle(f"Editar Configuración: {configuracion.nombre}")
        dialog.setStyleSheet("background-color: #333; color: white;")
        edit_config_layout = QVBoxLayout()

        name_input = QLineEdit(configuracion.nombre)
        name_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        edit_config_layout.addWidget(name_input)

        fields = [
            ("Límite inferior", "limite_inferior", self.format_limit(configuracion.limite_inferior)),
            ("Límite superior", "limite_superior", self.format_limit(configuracion.limite_superior)),
            ("Límite por ciclo", "limite_por_ciclo", self.format_limit(configuracion.limite_por_ciclo)),
            ("Error máximo", "error_maximo", self.format_error(configuracion.error_maximo)),
            ("Proporción", "proporcion", str(configuracion.proporcion)),
            ("Último valor", "ultimo_valor", str(configuracion.ultimo_valor)),
            ("Probabilidad", "probabilidad", str(configuracion.probabilidad))
        ]

        for label, attr, value in fields:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: white;")
            input_field = QLineEdit(value)
            input_field.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
            row.addWidget(lbl)
            row.addWidget(input_field)
            edit_config_layout.addLayout(row)

        tipo_error_combo = QComboBox()
        tipo_error_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        for error_type in TipoError:
            tipo_error_combo.addItem(error_type.value)
        tipo_error_combo.setCurrentText(configuracion.tipo.value)
        edit_config_layout.addWidget(QLabel("Tipo de error"))
        edit_config_layout.addWidget(tipo_error_combo)

        save_button = QPushButton("Guardar cambios")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(lambda: self.save_edited_configuration(dialog, configuracion, name_input, edit_config_layout, tipo_error_combo))
        edit_config_layout.addWidget(save_button)

        dialog.setLayout(edit_config_layout)
        dialog.exec_()

    def format_limit(self, value):
        return "Sin límite" if value in [float('inf'), float('-inf')] else str(value)

    def format_error(self, value):
        return "Sin error" if value == float('inf') else str(value)

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

    def save_edited_configuration(self, dialog, configuracion, name_input, layout, tipo_error_combo):
        new_name = name_input.text()
        new_tipo = TipoError(tipo_error_combo.currentText())

        for i in range(1, layout.count() - 2):  # Ignorar el nombre y el botón de guardar
            row = layout.itemAt(i)
            if isinstance(row, QHBoxLayout):
                label = row.itemAt(0).widget().text()
                value = row.itemAt(1).widget().text()
                attr = self.get_attr_from_label(label)
                if attr:
                    try:
                        if value.lower() == "inf":
                            setattr(configuracion, attr, float('inf'))
                        elif value.lower() == "-inf":
                            setattr(configuracion, attr, float('-inf'))
                        else:
                            setattr(configuracion, attr, float(value))
                    except ValueError:
                        QMessageBox.warning(dialog, "Error", f"Valor inválido para {label}")
                        return

        configuracion.nombre = new_name
        configuracion.tipo = new_tipo

        # Actualizamos directamente la configuración del microbloque
        self.configuracion = configuracion
        self.elemento_back.configuracion = configuracion

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

    def edit_properties(self):
        # Obtener la ventana principal como el padre del diálogo
        parent = None
        if self.scene():
            views = self.scene().views()
            if views:
                parent = views[0].window()

        dialog = QDialog(parent)
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
        
        config_label = QLabel("Configuraciones:")
        config_label.setStyleSheet("color: white;")
        layout.addWidget(config_label)

        config_button = QPushButton(self.configuracion.nombre)
        config_button.setStyleSheet("background-color: #444; color: white;")
        config_button.clicked.connect(lambda: self.edit_configuration(self.configuracion, layout))
        layout.addWidget(config_button)

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

    def add_configuration(self, layout):
        dialog = QDialog(self.scene().views()[0].window())
        dialog.setWindowTitle("Agregar Configuración")
        dialog.setStyleSheet("background-color: #333; color: white;")
        config_layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre de la configuración")
        name_input.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
        config_layout.addWidget(name_input)

        fields = [
            ("Límite inferior", "-inf"),
            ("Límite superior", "inf"),
            ("Límite por ciclo", "inf"),
            ("Error máximo", "inf"),
            ("Proporción", "0"),
            ("Último valor", "0"),
            ("Probabilidad", "0")
        ]

        for label, default_value in fields:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet("color: white;")
            input_field = QLineEdit(default_value)
            input_field.setStyleSheet("background-color: white; color: black; border: 1px solid #555;")
            row.addWidget(lbl)
            row.addWidget(input_field)
            config_layout.addLayout(row)

        tipo_error_combo = QComboBox()
        tipo_error_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        for error_type in TipoError:
            tipo_error_combo.addItem(error_type.value)
        config_layout.addWidget(QLabel("Tipo de error"))
        config_layout.addWidget(tipo_error_combo)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(lambda: self.save_new_configuration(dialog, name_input, config_layout, tipo_error_combo, layout))
        save_button.setStyleSheet("background-color: #444; color: white;")
        config_layout.addWidget(save_button)

        dialog.setLayout(config_layout)
        dialog.exec_()
    
    def save_new_configuration(self, dialog, name_input, config_layout, tipo_error_combo, main_layout):
        nombre = name_input.text()
        if not nombre:
            QMessageBox.warning(dialog, "Error", "Por favor, ingrese un nombre para la configuración.")
            return

        new_config = Configuracion(nombre)
        new_config.tipo = TipoError(tipo_error_combo.currentText())

        for i in range(1, config_layout.count() - 2):
            row = config_layout.itemAt(i)
            if isinstance(row, QHBoxLayout):
                label = row.itemAt(0).widget().text()
                value = row.itemAt(1).widget().text()
                attr = self.get_attr_from_label(label)
                if attr:
                    try:
                        if value.lower() == "inf":
                            setattr(new_config, attr, float('inf'))
                        elif value.lower() == "-inf":
                            setattr(new_config, attr, float('-inf'))
                        else:
                            setattr(new_config, attr, float(value))
                    except ValueError:
                        QMessageBox.warning(dialog, "Error", f"Valor inválido para {label}")
                        return

        self.configuracion = new_config
        self.elemento_back.configuracion = new_config
        
        config_button = QPushButton(nombre)
        config_button.setStyleSheet("background-color: #444; color: white;")
        config_button.clicked.connect(lambda checked, c=new_config: self.edit_configuration(c, main_layout))
        main_layout.insertWidget(main_layout.count() - 2, config_button)

        dialog.accept()

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
