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
import numpy as np
import csv


class Graficadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setWindowTitle("Gráfico y Datos de Simulación en Tiempo Real")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

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

        self.export_manager = ExportManager(self)

        self.setup_controls()

        # Temporizador para actualizar la tabla
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_tabla)
        self.timer.start(1000)  # Actualizar cada segundo


    def setup_controls(self):
        export_button = QPushButton("Exportar Datos")
        export_button.clicked.connect(self.export_manager.export_data)
        self.controls_layout.addWidget(export_button)
        
        interpret_button = QPushButton("Interpretar Datos")
        interpret_button.clicked.connect(self.mostrar_interpretacion)
        self.controls_layout.addWidget(interpret_button)
        
        self.pause_button = QPushButton("Pausar Simulacion")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.controls_layout.addWidget(self.pause_button)

        self.is_paused = False
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.setText("Reanudar" if self.is_paused else "Pausar")
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.actualizar_tabla()  # Actualizar la tabla inmediatamente al pausar/reanudar


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
                
                # Agregar clave a la lista de selección de columnas
                self.column_list.addItem(clave)
            
            valor_numerico = self.convertir_a_numerico(valor)
            self.datos[clave].append(valor_numerico)

        if not self.is_paused:
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
            'Excelente': QColor(0, 255, 0),  # Verde brillante fuerte
            'Bueno': QColor(144, 238, 144),  # Verde claro apenas notorio
            'Regular': QColor(255, 255, 0),  # Amarillo
            'Mal': QColor(255, 99, 71),  # Rojo claro
            'Pesimo': QColor(255, 0, 0)  # Rojo fuerte
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
        self.setWindowTitle("Interpretación de Datos")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.interpretar_datos(datos)

    def interpretar_datos(self, datos):
        interpretacion = "Interpretación de los datos de la simulación:\n\n"

        # Ejemplo de interpretación básica
        tiempo_total = datos['tiempo'][-1] - datos['tiempo'][0]
        interpretacion += f"Tiempo total de simulación: {tiempo_total:.2f} unidades\n"

        for key in datos:
            if key != 'tiempo':
                promedio = sum(datos[key]) / len(datos[key])
                maximo = max(datos[key])
                minimo = min(datos[key])
                interpretacion += f"\n{key.capitalize()}:\n"
                interpretacion += f"  Promedio: {promedio:.2f}\n"
                interpretacion += f"  Máximo: {maximo:.2f}\n"
                interpretacion += f"  Mínimo: {minimo:.2f}\n"

        self.text_edit.setText(interpretacion)