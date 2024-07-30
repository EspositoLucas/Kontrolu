from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog,QComboBox,QHBoxLayout
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

        for config in self.configuracion_mb.configuraciones.items():
            config_layout = QHBoxLayout()
            
            valor_formateado = ""
            if config.tipo == TipoConfiguracion.NUMERICA:
                valor_formateado = config.valor
            elif config.tipo == TipoConfiguracion.BOOLEANA:
                valor_formateado = "Bool"
            elif config.tipo == TipoConfiguracion.NUMERADA:
                for v in config.valores_posibles:
                    valor_formateado += f" {v}"
            else:
                valor_formateado = config.valor

            config_layout.addWidget(QLabel(f"Nombre: {config.nombre} - Valor: {valor_formateado}"))
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
            
            # Guardar configuraciones
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QHBoxLayout):
                    nombre = item.itemAt(0).widget().text().rstrip(':')
                    value_widget = item.itemAt(1).widget()
                    if isinstance(value_widget, QLineEdit):
                        valor = value_widget.text()
                    elif isinstance(value_widget, QComboBox):
                        valor = value_widget.currentText()
                    
                    if nombre in self.configuracion_mb.configuraciones:
                        config = self.configuracion_mb.configuraciones[nombre]
                        if config.tipo == TipoConfiguracion.NUMERICA:
                            config.set_valor(float(valor))
                        elif config.tipo == TipoConfiguracion.BOOLEANA:
                            config.set_valor(valor == "True")
                        elif config.tipo == TipoConfiguracion.ENUMERADA:
                            config.set_valor(valor)
                        else:  # FUNCION
                            config.set_funcion_efecto(valor)
            
            self.update()
    
    def seleccion_tipo_configuracion(self):
        if self.input_widget:
            self.config_layout.removeWidget(self.input_widget)
            self.input_widget.deleteLater()
            self.input_widget = None

        valor_seleccionado = self.type_combo.currentText()
        if valor_seleccionado == TipoConfiguracion.BOOLEANA:
            return
        elif valor_seleccionado == TipoConfiguracion.NUMERICA:
            self.input_widget = QLineEdit()
            self.input_widget.setPlaceholderText("Ingrese un valor de tipo numérico")
        elif valor_seleccionado == TipoConfiguracion.FUNCION:
            self.input_widget = QLineEdit()
            self.input_widget.setPlaceholderText("Ingrese una función")
        elif valor_seleccionado == TipoConfiguracion.ENUMERADA:
            self.input_widget = QLineEdit()
            self.input_widget.setPlaceholderText("Ingrese valores separados por comas")

        if self.input_widget:
            self.input_widget.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: white;
                    border: 1px solid #555;
                }
                QLineEdit::placeholder {
                    color: white;
                }
            """)
            self.config_layout.addWidget(self.input_widget)


    def add_configuration(self, layout):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Configuración")
        dialog.setStyleSheet("background-color: #333; color: white;")
        config_layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre de la configuración")
        name_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: white;
                border: 1px solid #555;
            }
            QLineEdit::placeholder {
                color: white;
            }
        """)
        config_layout.addWidget(name_input)

        self.type_combo = QComboBox()
        self.type_combo.addItems([t.name for t in TipoConfiguracion])
        self.type_combo.setStyleSheet("""
            QComboBox {
                background-color: #444;
                color: white;
                border: 1px solid #555;
            }
            QComboBox QAbstractItemView {
                background-color: #444;
                color: white;
                selection-background-color: #666;
            }
        """)
        config_layout.addWidget(self.type_combo)
        self.type_combo.currentIndexChanged.connect(self.seleccion_tipo_configuracion)


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
