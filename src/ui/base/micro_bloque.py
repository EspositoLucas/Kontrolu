from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog,QComboBox,QHBoxLayout, QMessageBox, QGraphicsItem,QTabWidget,QGridLayout
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
        self.configuracion_entrada = microbloque_back.configuracion_entrada or Configuracion(f"{self.nombre}_entrada")
        self.configuracion_salida = microbloque_back.configuracion_salida or Configuracion(f"{self.nombre}_salida")
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


    def edit_configuration(self, configuracion, tipo):
        dialog = QDialog(self.scene().views()[0].window())
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
        save_button.clicked.connect(lambda: self.save_configuration(dialog, configuracion, input_fields, tipo_error_combo, tipo))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_configuration(self, dialog, configuracion, input_fields, tipo_error_combo, tipo):
        # Creamos una nueva instancia de Configuracion para guardar los cambios
        new_config = Configuracion(configuracion.nombre)

        for attr, input_field in input_fields.items():
            value = input_field.text()
            try:
                if value.lower() == "inf":
                    setattr(new_config, attr, float('inf'))
                elif value.lower() == "-inf":
                    setattr(new_config, attr, float('-inf'))
                else:
                    setattr(new_config, attr, float(value))
            except ValueError:
                QMessageBox.warning(dialog, "Error", f"Valor inválido para {attr}")
                return

        new_config.tipo = TipoError(tipo_error_combo.currentText())
        
        if tipo == "entrada":
            self.configuracion_entrada = new_config
        else:
            self.configuracion_salida = new_config
        
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
        dialog = QDialog(self.scene().views()[0].window())
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
        
        config_content = QWidget()
        config_layout = QGridLayout(config_content)

        # Configuración de entrada
        entrada_name_input = QLineEdit(self.configuracion_entrada.nombre)
        entrada_name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Nombre de la configuración de entrada:"), 0, 0)
        config_layout.addWidget(entrada_name_input, 0, 1)

        input_button = QPushButton("Configurar Entrada")
        input_button.setStyleSheet("background-color: #444; color: white;")
        input_button.clicked.connect(lambda: self.edit_configuration(self.configuracion_entrada, "entrada"))
        config_layout.addWidget(input_button, 0, 2)

        # Configuración de salida
        salida_name_input = QLineEdit(self.configuracion_salida.nombre)
        salida_name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        config_layout.addWidget(QLabel("Nombre de la configuración de salida:"), 1, 0)
        config_layout.addWidget(salida_name_input, 1, 1)

        output_button = QPushButton("Configurar Salida")
        output_button.setStyleSheet("background-color: #444; color: white;")
        output_button.clicked.connect(lambda: self.edit_configuration(self.configuracion_salida, "salida"))
        config_layout.addWidget(output_button, 1, 2)

        config_tab.addTab(config_content, "Configuraciones")
        layout.addWidget(config_tab)


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

            # Actualizar los nombres de las configuraciones
            self.configuracion_entrada.nombre = entrada_name_input.text()
            self.configuracion_salida.nombre = salida_name_input.text()

            # Actualizar las configuraciones en el elemento_back
            self.elemento_back.configuracion_entrada = self.configuracion_entrada
            self.elemento_back.configuracion_salida = self.configuracion_salida
            
            self.update()
    
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
