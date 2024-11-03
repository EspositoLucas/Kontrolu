from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel,QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, 
                             QPushButton, QFileDialog, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QLabel,QListWidget,QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
from PyQt5 import QtGui
import numpy as np
import csv
import os

ESTILO = """
    QCheckBox {
        spacing: 5px;  /* Espaciado entre el cuadro y el texto */
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tamaño de fuente */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía */
        font-weight: bold;  /* Texto en negrita */
    }

    QCheckBox::indicator {
        width: 20px;  /* Ancho del cuadro de verificación */
        height: 20px;  /* Alto del cuadro de verificación */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 5px;  /* Bordes redondeados */
        background-color: #FAF8F6;  /* Color de fondo del cuadro */
    }

    QCheckBox::indicator:checked {
        background-color: #808080;  /* Fondo gris oscuro cuando está marcado */
        border: 2px solid #505050;  /* Borde gris oscuro */
    }

    QCheckBox::indicator:unchecked {
        background-color: #FAF8F6;  /* Fondo claro cuando no está marcado */
    }



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
"""

class Graficadora(QMainWindow):
    def __init__(self,carga_nombre):
        super().__init__()

        self.carga_nombre = carga_nombre

        # Aplicar el estilo global
        self.setStyleSheet(ESTILO)
        
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setWindowTitle("Gráfico y Datos de Simulación en Tiempo Real")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))

        # Crear pestañas
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Pestaña del gráfico
        self.graph_widget = QWidget()
        self.graph_layout = QHBoxLayout(self.graph_widget)  # Cambiado a QHBoxLayout
        self.tabs.addTab(self.graph_widget, "Gráfico")
        

        
        # Área de desplazamiento para checkboxes
        self.checkbox_scroll = QScrollArea()
        self.checkbox_scroll.setWidgetResizable(True)
        self.checkbox_widget = QWidget()
        self.checkbox_layout = QVBoxLayout(self.checkbox_widget)
        self.checkbox_scroll.setWidget(self.checkbox_widget)
        
        # Panel derecho para el gráfico
        self.right_panel = QWidget()
        self.right_panel_layout = QVBoxLayout(self.right_panel)
        self.graph_layout.addWidget(self.right_panel, 3)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.right_panel_layout.addWidget(self.toolbar)
        self.right_panel_layout.addWidget(self.canvas)

        # Controles y estado de carga
        controls_and_state = QHBoxLayout()
        self.graph_layout.addLayout(controls_and_state)

        self.controls_layout = QVBoxLayout()
        controls_and_state.addLayout(self.controls_layout, 1)

        self.state_layout = QVBoxLayout()
        controls_and_state.addLayout(self.state_layout)

        # Indicador de estado de carga
        self.state_layout = QHBoxLayout()
        self.right_panel_layout.addLayout(self.state_layout)
        self.state_indicator = QLabel()
        self.state_indicator.setFixedSize(50, 50)
        self.state_indicator.setStyleSheet("border: 3px solid black; border-radius: 25px;")
        self.state_layout.addWidget(self.state_indicator)

        self.state_indicator.setStyleSheet(
                f"background-color: {QColor(200, 200, 200).name()};"
                f"border: 3px solid {QColor(200, 200, 200).darker().name()};"
                f"border-radius: 25px;"
                f"color: {QColor(200, 200, 200).darker().name()};"
                f"font-weight: bold;")
            # Establece el texto de `state_indicator` con la prioridad en formato 'prioridad/5'
        self.state_indicator.setText(f" 0/5")
        


        self.state_label = QLabel("Rendimiento del sistema desconocido.")
        self.state_layout.addWidget(self.state_label)

        # Actualiza el label de estado en negrita y centrado
        self.state_label.setStyleSheet(
            "font-weight: bold;"
            "text-align: center;"
            "vertical-align: middle;"
            "line-height: 1.5em;"  # Ajusta esta altura para centrar verticalmente
        )

        # Pestaña de la tabla
        self.table_widget = QWidget()
        self.table_layout = QHBoxLayout(self.table_widget)
        self.tabs.addTab(self.table_widget, "Datos")

        # Lista de selección de columnas
        self.column_list = QListWidget()
        self.column_list.setSelectionMode(QListWidget.MultiSelection)
        self.column_list.itemSelectionChanged.connect(self.actualizar_tabla)
        self.table_layout.addWidget(self.column_list, 1)
        
        # Tabla de datos
        self.data_table = QTableWidget()
        self.table_layout.addWidget(self.data_table, 3)

        self.datos = {}
        self.lineas = {}
        self.checkboxes = {}
        self.colores = plt.cm.get_cmap('Set1')(np.linspace(0, 1, 10))
        


        self.export_manager = ExportManager(self)

        self.setup_controls()

    def add_simulacion(self, simulacion):
        self.simulacion = simulacion
    
    def setup_controls(self):
        export_button = QPushButton("Exportar Datos")
        export_button.clicked.connect(self.export_manager.export_data)
        export_button.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor al pasar por encima
        self.controls_layout.addWidget(export_button)
        
        interpret_button = QPushButton("Interpretar Datos")
        interpret_button.clicked.connect(self.mostrar_interpretacion)
        interpret_button.setCursor(Qt.PointingHandCursor)
        self.controls_layout.addWidget(interpret_button)
        
        self.pause_button = QPushButton("Pausar Simulación")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setCursor(Qt.PointingHandCursor)
        self.controls_layout.addWidget(self.pause_button)
    
    def toggle_pause(self):
        if self.pause_button.text() == "Pausar Simulación":
            self.pause_button.setText("Reanudar Simulación")
            self.simulacion.parar()
        else:
            self.pause_button.setText("Pausar Simulación")
            self.simulacion.reanudar()


    def pause_button_change(self):
        self.pause_button.setText("Pausar Simulación")
    
    def resume_button_change(self):
        self.pause_button.setText("Reanudar Simulación")


    def mostrar_interpretacion(self):
        interpretacion = InterpretacionDatos(self.datos,self.carga_nombre)
        interpretacion.exec_()

    def export_to_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "", "PDF Files (*.pdf)")
        if filename:
            with PdfPages(filename) as pdf:
                pdf.savefig(self.fig)

    def agregar_datos(self, nuevos_datos):
        for clave, valor in nuevos_datos.items():
            if clave not in self.datos:
                self.datos[clave] = []
                color = self.colores[len(self.lineas) % len(self.colores)]
                self.lineas[clave], = self.ax.plot([], [], label=clave, color=color)
                if clave != 'Tiempo':
                    self.checkboxes[clave] = QCheckBox(clave)
                    self.checkboxes[clave].setChecked(True)
                    self.checkboxes[clave].stateChanged.connect(self.actualizar_grafico)
                    self.controls_layout.addWidget(self.checkboxes[clave])
                
                # if clave == self.carga_nombre:
                #     self.datos[clave].append(valor)  # Mantener el diccionario para self.carga_nombre
                
                # Agregar clave a la lista de selección de columnas
                self.column_list.addItem(clave)
            
            valor_numerico = self.convertir_a_numerico(valor)
            self.datos[clave].append(valor_numerico)

        
        self.actualizar_grafico()
        self.actualizar_estado_carga(nuevos_datos.get(self.carga_nombre, None))
        self.actualizar_tabla()

    def actualizar_estado_carga(self, estado):
        if estado is not None:
            nombre_estado = estado.get('nombre', 'desconocido').lower()
            prioridad_estado = estado.get('prioridad', 0)
            
            # Obtén el color base y un color más oscuro para el borde
            color = self.obtener_color_estado(prioridad_estado)
            borde_color = color.darker(120)  # Un 20% más oscuro que el color base
            
            # Actualiza el indicador de estado con el color de fondo y el borde
            self.state_indicator.setStyleSheet(
                f"background-color: {color.name()};"
                f"border: 3px solid {borde_color.name()};"
                f"border-radius: 25px;"
                f"color: {borde_color.name()};"
                f"font-weight: bold;"
            )
            # Establece el texto de `state_indicator` con la prioridad en formato 'prioridad/5'
            self.state_indicator.setText(f" {prioridad_estado}/5")
            
            # Actualiza el label de estado en negrita y centrado
            self.state_label.setStyleSheet(
                "font-weight: bold;"
                "text-align: center;"
                "vertical-align: middle;"
                "line-height: 1.5em;"  # Ajusta esta altura para centrar verticalmente
            )
            self.state_label.setText(f"{self.carga_nombre} del sistema {nombre_estado}.")


    def obtener_color_estado(self, nombre_estado):
        colores_estado = {
            5: QColor(153, 255, 153),  # Verde pastel suave
            4: QColor(204, 255, 204),      # Verde más claro pastel
            3: QColor(255, 255, 153),    # Amarillo pastel
            2: QColor(255, 178, 178),       # Rojo claro pastel
            1: QColor(255, 153, 153),      # Rojo pastel más fuerte
            0: QColor(200, 200, 200)      # Blanco
        }
        return colores_estado.get(nombre_estado, QColor(255, 255, 255))  # Blanco por defecto

    def actualizar_tabla(self):
        # Obtener las columnas seleccionadas
        columnas_seleccionadas = [item.text() for item in self.column_list.selectedItems()]
        if not columnas_seleccionadas:
            columnas_seleccionadas = list(self.datos.keys())  # Mostrar todas si no hay selección

        self.data_table.setRowCount(len(self.datos['Tiempo']))
        self.data_table.setColumnCount(len(columnas_seleccionadas))

        # Establecer encabezados
        self.data_table.setHorizontalHeaderLabels(columnas_seleccionadas)

        # Llenar la tabla con datos
        for col, key in enumerate(columnas_seleccionadas):
            for row, value in enumerate(self.datos[key]):
                item = QTableWidgetItem(str(value))
                self.data_table.setItem(row, col, item)

        # Ajustar tamaño de columnas
        self.data_table.resizeColumnsToContents()
    
    def convertir_a_numerico(self, valor):
        if isinstance(valor, (int, float)):
            return valor
        elif isinstance(valor, dict):
            for key in ['valor', 'prioridad', 'minimo']:
                if key in valor and isinstance(valor[key], (int, float)):
                    return valor[key]
            return 0
        else:
            try:
                return float(str(valor))
            except ValueError:
                return 0

    def actualizar_grafico(self):
        self.ax.clear()
        for clave, linea in self.lineas.items():
            if clave != 'Tiempo':
                if self.checkboxes[clave].isChecked():
                    self.ax.plot(self.datos['Tiempo'], self.datos[clave], label=clave)
                    # Añadir esta línea para mostrar el último valor
                    if len(self.datos[clave]) > 0:
                        ultimo_valor = self.datos[clave][-1]
                        self.ax.annotate(f'{ultimo_valor:.2f}', 
                                        (self.datos['Tiempo'][-1], ultimo_valor),
                                        textcoords="offset points", 
                                        xytext=(0,10), 
                                        ha='center')

        self.ax.legend()
        self.ax.set_xlabel('Segundos')
        self.ax.set_ylabel('Salidas')
        self.canvas.draw()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def procesar_eventos(self):
        QApplication.processEvents()


class ExportManager:
    def __init__(self, graficadora):
        self.graficadora = graficadora

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self.graficadora, "Guardar datos", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.graficadora.datos.keys())
                for i in range(len(self.graficadora.datos['Tiempo'])):
                    row = [self.graficadora.datos[key][i] for key in self.graficadora.datos.keys()]
                    writer.writerow(row)


class InterpretacionDatos(QDialog):
    def __init__(self, datos,carga_nombre):
        super().__init__()
        self.carga_nombre = carga_nombre
        self.setStyleSheet(ESTILO)  # Aplicar el estilo
        self.setWindowTitle("Interpretación de Datos")
        self.setGeometry(200, 200, 800, 600)
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))
        
        # Configuración del layout
        layout = QVBoxLayout()
        
        # Personalizar el QTextEdit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #D0D0D0;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 10px;
                color: #2B2D42;
                font-size: 14px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
        """)
        layout.addWidget(self.text_edit)
        
        # Botón para descargar el archivo
        self.btn_descargar = QPushButton("Descargar como TXT")
        self.btn_descargar.clicked.connect(self.descargar_archivo)
        layout.addWidget(self.btn_descargar)
        
        # Botón para copiar el texto
        self.btn_copiar = QPushButton("Copiar al portapapeles")
        self.btn_copiar.clicked.connect(self.copiar_al_portapapeles)
        layout.addWidget(self.btn_copiar)
        
        self.setLayout(layout)
        
        self.interpretar_datos(datos)

    def descargar_archivo(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Interpretación como", "", "Archivos de Texto (*.txt)", options=options)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def copiar_al_portapapeles(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
    
    def obtener_nombre_estado(self, prioridad):
        estados = {
            5: "Excelente",
            4: "Bueno",
            3: "Regular",
            2: "Malo",
            1: "Pésimo"
        }
        return estados.get(prioridad, "Desconocido")

    def interpretar_datos(self, datos):
        interpretacion = "Interpretación detallada de los datos de la simulación:\n\n"

        tiempo_total = datos['Tiempo'][-1] - datos['Tiempo'][0]
        interpretacion += f"Tiempo total de simulación: {tiempo_total:.2f} unidades\n\n"

        # Análisis de estabilización
        tiempo_estabilizacion = self.analizar_estabilizacion(datos)
        interpretacion += f"El sistema se estabilizó aproximadamente a las {tiempo_estabilizacion:.2f} unidades de tiempo.\n\n"

        # Análisis de control
        hubo_control = self.analizar_control(datos)
        interpretacion += f"{'Hubo' if hubo_control else 'No hubo'} un control efectivo del sistema.\n\n"

        # Análisis de cambios bruscos
        cambios_bruscos = self.analizar_cambios_bruscos(datos)
        if cambios_bruscos:
            interpretacion += "Se detectaron los siguientes cambios bruscos en el estado de la carga:\n"
            for cambio in cambios_bruscos:
                estado_anterior = self.obtener_nombre_estado(cambio[1])
                estado_nuevo = self.obtener_nombre_estado(cambio[2])
                interpretacion += f"  - En el tiempo {cambio[0]:.2f}: cambio de '{estado_anterior}' a '{estado_nuevo}'\n"
        else:
            interpretacion += "No se detectaron cambios bruscos significativos en el estado de la carga.\n"

        # Análisis por variable
        for key in datos:
            if key != 'Tiempo' and key != self.carga_nombre:
                interpretacion += self.analizar_variable(key, datos[key])

        self.text_edit.setText(interpretacion)
    def analizar_estabilizacion(self, datos):
        # Implementa lógica para determinar cuándo el sistema se estabiliza
        salida = datos['Salida']
        for i in range(len(salida) - 1):
            if abs(salida[i] - salida[i+1]) < 0.01:  # Umbral de estabilización
                return datos['Tiempo'][i]
        return datos['Tiempo'][-1]  # Si no se estabiliza, retorna el tiempo final

    def analizar_control(self, datos):
        # Implementa lógica para determinar si hubo control efectivo
        # Por ejemplo, comparando el error inicial con el error final
 
        error_inicial = abs(datos['Error Real'][0])
        error_final = abs(datos['Error Real'][-1])
        return error_final < error_inicial / 2  # Control efectivo si el error se reduce a la mitad
    
    def analizar_cambios_bruscos(self, datos):
        cambios_bruscos = []
        if self.carga_nombre not in datos or len(datos[self.carga_nombre]) < 2:
            return cambios_bruscos

        estados_carga = datos[self.carga_nombre]
        tiempos = datos['Tiempo']
        def calificar_estado(estado):
            if estado is not None:
                if estado== 5:
                    return 4
                elif estado == 4:
                    return 3
                elif estado == 3:
                    return 2
                elif estado == 2:
                    return 1
                elif estado == 1:
                    return 0
            return -1  # Estado desconocido

        estado_anterior = calificar_estado(estados_carga[0])
        for i in range(1, len(estados_carga)):
            estado_actual = calificar_estado(estados_carga[i])
            if estado_actual != -1 and estado_anterior != -1:
                if abs(estado_actual - estado_anterior) > 0:  # Cambio brusco
                    cambios_bruscos.append((tiempos[i], estados_carga[i-1], estados_carga[i]))
                estado_anterior = estado_actual

        return cambios_bruscos

    def analizar_variable(self, nombre, valores):
        promedio = sum(valores) / len(valores)
        maximo = max(valores)
        minimo = min(valores)
        tiempo_max = (valores.index(maximo) / len(valores)) * 100
        
        analisis = f"\n{nombre.capitalize()}:\n"
        analisis += f"  Promedio: {promedio:.2f}\n"
        analisis += f"  Máximo: {maximo:.2f} (alcanzado al {tiempo_max:.1f}% del tiempo total)\n"
        analisis += f"  Mínimo: {minimo:.2f}\n"
        
        if nombre == 'Salida':
            tiempo_en_maximo = sum(1 for v in valores if v > 0.95 * maximo) / len(valores) * 100
            analisis += f"  Tiempo en máximo esplendor (>95% del máximo): {tiempo_en_maximo:.1f}%\n"
        
        return analisis