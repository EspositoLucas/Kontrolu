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
        cursor: pointer;
    }

    QLineEdit {
        background-color: #D0D0D0;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
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
        color: #000000;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }
"""


class Graficadora(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # Panel izquierdo para controles y checkboxes
        self.left_panel = QWidget()
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.graph_layout.addWidget(self.left_panel, 1)
        
        # Área de desplazamiento para checkboxes
        self.checkbox_scroll = QScrollArea()
        self.checkbox_scroll.setWidgetResizable(True)
        self.checkbox_widget = QWidget()
        self.checkbox_layout = QVBoxLayout(self.checkbox_widget)
        self.checkbox_scroll.setWidget(self.checkbox_widget)
        self.left_panel_layout.addWidget(self.checkbox_scroll)
        
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
        self.state_indicator.setStyleSheet("border: 1px solid black;")
        self.state_layout.addWidget(self.state_indicator)

        self.state_label = QLabel("Estado: ")
        self.state_layout.addWidget(self.state_label)

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
        
        self.data_table.setStyleSheet("""
        QTableWidget {
            background-color: #D0D0D0;
            border: 2px solid #505050;
            border-radius: 10px;
            color: #2B2D42;
            font-size: 14px;
            font-family: "Segoe UI", "Arial", sans-serif;
        }
        QHeaderView::section {
            background-color: #808080;
            color: white;
            padding: 5px;
            border: 1px solid #505050;
        }
    """)

        # Agregar después de la creación del QListWidget
        self.column_list.setStyleSheet("""
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
        """)

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
        interpretacion = InterpretacionDatos(self.datos)
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
                if clave != 'tiempo':
                    self.checkboxes[clave] = QCheckBox(clave)
                    self.checkboxes[clave].setChecked(True)
                    self.checkboxes[clave].stateChanged.connect(self.actualizar_grafico)
                    self.controls_layout.addWidget(self.checkboxes[clave])
                
                # if clave == 'carga':
                #     self.datos[clave].append(valor)  # Mantener el diccionario para 'carga'
                
                # Agregar clave a la lista de selección de columnas
                self.column_list.addItem(clave)
            
            valor_numerico = self.convertir_a_numerico(valor)
            self.datos[clave].append(valor_numerico)

        
        self.actualizar_grafico()
        self.actualizar_estado_carga(nuevos_datos.get('carga', None))
        self.actualizar_tabla()

    def actualizar_estado_carga(self, estado):
        if estado is not None:
            nombre_estado = estado.get('nombre', 'Desconocido').lower()
            color = self.obtener_color_estado(nombre_estado)
            self.state_indicator.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            self.state_label.setText(f"Estado: {estado.get('nombre', 'Desconocido')}")

    def obtener_color_estado(self, nombre_estado):
        colores_estado = {
            'excelente': QColor(0, 255, 0),  # Verde brillante fuerte
            'bueno': QColor(144, 238, 144),  # Verde claro apenas notorio
            'regular': QColor(255, 255, 0),  # Amarillo
            'malo': QColor(255, 99, 71),  # Rojo claro
            'pésimo': QColor(255, 0, 0)  # Rojo fuerte
        }
        return colores_estado.get(nombre_estado, QColor(255, 255, 255))  # Blanco por defecto

    def actualizar_tabla(self):
        # Obtener las columnas seleccionadas
        columnas_seleccionadas = [item.text() for item in self.column_list.selectedItems()]
        if not columnas_seleccionadas:
            columnas_seleccionadas = list(self.datos.keys())  # Mostrar todas si no hay selección

        self.data_table.setRowCount(len(self.datos['tiempo']))
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
            if clave != 'tiempo':
                if self.checkboxes[clave].isChecked():
                    self.ax.plot(self.datos['tiempo'], self.datos[clave], label=clave)
                    # Añadir esta línea para mostrar el último valor
                    if len(self.datos[clave]) > 0:
                        ultimo_valor = self.datos[clave][-1]
                        self.ax.annotate(f'{ultimo_valor:.2f}', 
                                        (self.datos['tiempo'][-1], ultimo_valor),
                                        textcoords="offset points", 
                                        xytext=(0,10), 
                                        ha='center')

        self.ax.legend()
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Valor')
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
                for i in range(len(self.graficadora.datos['tiempo'])):
                    row = [self.graficadora.datos[key][i] for key in self.graficadora.datos.keys()]
                    writer.writerow(row)


class InterpretacionDatos(QDialog):
    def __init__(self, datos):
        super().__init__()
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

        tiempo_total = datos['tiempo'][-1] - datos['tiempo'][0]
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
            if key != 'tiempo' and key != 'carga':
                interpretacion += self.analizar_variable(key, datos[key])

        self.text_edit.setText(interpretacion)
    def analizar_estabilizacion(self, datos):
        # Implementa lógica para determinar cuándo el sistema se estabiliza
        salida = datos['salida']
        for i in range(len(salida) - 1):
            if abs(salida[i] - salida[i+1]) < 0.01:  # Umbral de estabilización
                return datos['tiempo'][i]
        return datos['tiempo'][-1]  # Si no se estabiliza, retorna el tiempo final

    def analizar_control(self, datos):
        # Implementa lógica para determinar si hubo control efectivo
        # Por ejemplo, comparando el error inicial con el error final
        try:
            error_inicial = abs(datos['error'][0])
            error_final = abs(datos['error'][-1])
        except KeyError:
            error_inicial = abs(datos['error_real'][0])
            error_final = abs(datos['error_real'][-1])
        return error_final < error_inicial / 2  # Control efectivo si el error se reduce a la mitad
    
    def analizar_cambios_bruscos(self, datos):
        cambios_bruscos = []
        if 'carga' not in datos or len(datos['carga']) < 2:
            return cambios_bruscos

        estados_carga = datos['carga']
        tiempos = datos['tiempo']
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
        
        if nombre == 'salida':
            tiempo_en_maximo = sum(1 for v in valores if v > 0.95 * maximo) / len(valores) * 100
            analisis += f"  Tiempo en máximo esplendor (>95% del máximo): {tiempo_en_maximo:.1f}%\n"
        
        return analisis