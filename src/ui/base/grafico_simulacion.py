from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
import numpy as np
import csv


class Graficadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setWindowTitle("Gráfico de Simulación en Tiempo Real")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        self.layout.addLayout(graph_layout, 3)

        self.controls_layout = QVBoxLayout()
        self.layout.addLayout(self.controls_layout, 1)

        self.datos = {}
        self.lineas = {}
        self.checkboxes = {}
        self.colores = plt.cm.get_cmap('Set1')(np.linspace(0, 1, 10))

        self.export_manager = ExportManager(self)

        self.setup_controls()

    def setup_controls(self):
        export_button = QPushButton("Exportar Datos")
        export_button.clicked.connect(self.export_manager.export_data)
        self.controls_layout.addWidget(export_button)

        export_pdf_button = QPushButton("Exportar a PDF")
        export_pdf_button.clicked.connect(self.export_to_pdf)
        self.controls_layout.addWidget(export_pdf_button)
        interpret_button = QPushButton("Interpretar Datos")
        interpret_button.clicked.connect(self.mostrar_interpretacion)
        self.controls_layout.addWidget(interpret_button)

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
            
            valor_numerico = self.convertir_a_numerico(valor)
            self.datos[clave].append(valor_numerico)

        self.actualizar_grafico()

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