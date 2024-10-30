from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QTabWidget, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFD700")  # Un amarillo brillante


# Colores aclarados al 150%
VERDE_ACLARADO = VERDE.lighter(150)
ROJO_ACLARADO = ROJO.lighter(150)
AMARILLO_ACLARADO = AMARILLO.lighter(150)

class EstabilidadTexto(QGraphicsTextItem):

    def __init__(self, sesion, parent=None):

        super().__init__(parent)

        self.sesion = sesion

        self.default_color = AMARILLO

        self.hoover_color = AMARILLO_ACLARADO

        self.update_text()

        font = QFont("Arial", 30, QFont.Bold)

        self.setFont(font)

        self.setAcceptHoverEvents(True)

    
    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            EstabilidadDialog(self.sesion).exec_()
            self.update_text()


        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)
        


    def update_text(self):

        estado =  self.sesion.calcular_estabilidad()        

        if estado == "ESTABLE":
            self.setPlainText("Estable")
            self.setDefaultTextColor(VERDE)
            self.default_color = VERDE
            self.hoover_color = VERDE_ACLARADO
        elif estado == "INESTABLE":
            self.setPlainText("Inestable")
            self.setDefaultTextColor(ROJO)
            self.default_color = ROJO
            self.hoover_color = ROJO_ACLARADO
        else:
            self.setPlainText("Criticamente Estable")
            self.setDefaultTextColor(AMARILLO)
            self.default_color = AMARILLO
            self.hoover_color = AMARILLO_ACLARADO

        self.update()
    
    def hoverEnterEvent(self, event):
        self.setDefaultTextColor(self.hoover_color)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(self.default_color)
        self.update()



class EstabilidadDialog(QDialog):
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.setWindowTitle("Análisis de Estabilidad")
        self.resize(800, 600)
        self.setStyleSheet(ESTILO)
        
        # Crear el layout principal
        layout = QVBoxLayout()
        
        # Crear el widget de pestañas
        tab_widget = QTabWidget()
        
        # Primera pestaña: Tabla de Routh
        tab_routh = QWidget()
        tab_routh_layout = QVBoxLayout()
        self.tabla_routh = QTableWidget()
        tab_routh_layout.addWidget(self.tabla_routh)
        tab_routh.setLayout(tab_routh_layout)
        
        # Segunda pestaña: Gráfico de polos y ceros
        tab_polos = QWidget()
        tab_polos_layout = QVBoxLayout()
        self.canvas = self.crear_canvas_matplotlib()
        tab_polos_layout.addWidget(self.canvas)
        tab_polos.setLayout(tab_polos_layout)
        
        # Agregar pestañas al widget
        tab_widget.addTab(tab_routh, "Tabla de Routh")
        tab_widget.addTab(tab_polos, "Polos y Ceros")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
        
        # Llenar los datos
        self.actualizar_datos()
    
    def crear_canvas_matplotlib(self):
        """Crea el canvas de matplotlib para el gráfico de polos y ceros"""
        fig = Figure(figsize=(8, 8))
        canvas = FigureCanvas(fig)
        return canvas
    
    def actualizar_datos(self):
        """Actualiza tanto la tabla como el gráfico"""
        try:
            self.actualizar_tabla_routh()
            self.actualizar_grafico_polos()
        except Exception as e:
            self.mostrar_error(f"Error al actualizar los datos: {str(e)}")
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error en la tabla"""
        self.tabla_routh.setRowCount(1)
        self.tabla_routh.setColumnCount(1)
        self.tabla_routh.setItem(0, 0, QTableWidgetItem(mensaje))
        self.tabla_routh.resizeColumnsToContents()
    
    def actualizar_tabla_routh(self):
        """Actualiza la tabla de Routh con los datos calculados"""
        try:
            tabla, diagnostico = self.sistema.calcular_tabla_routh()
            
            if tabla is None or len(tabla) == 0:
                raise ValueError("La tabla de Routh está vacía")
            
            # Configurar la tabla
            filas, columnas = tabla.shape
            self.tabla_routh.setRowCount(filas)
            self.tabla_routh.setColumnCount(columnas + 1)  # +1 para la columna de diagnóstico
            
            # Establecer encabezados
            headers = ['s^' + str(filas-i-1) for i in range(filas)]
            self.tabla_routh.setVerticalHeaderLabels(headers)
            
            # Establecer encabezados horizontales
            headers_h = ['Coef ' + str(i) for i in range(columnas)] + ['Diagnóstico']
            self.tabla_routh.setHorizontalHeaderLabels(headers_h)
            
            # Llenar la tabla
            for i in range(filas):
                for j in range(columnas):
                    if j < tabla.shape[1]:  # Verificar que el índice está dentro de los límites
                        valor = tabla[i, j]
                        # Formatear el valor para mostrar solo 4 decimales si es necesario
                        if abs(valor) < 1e-10:
                            valor = 0
                        item = QTableWidgetItem(f"{valor:.4f}")
                        self.tabla_routh.setItem(i, j, item)
            
            # Agregar el diagnóstico
            diagnostico_texto = f"Estado: {diagnostico['estabilidad']}\n{diagnostico['mensaje']}"
            for i in range(filas):
                if i == 0:
                    item_diagnostico = QTableWidgetItem(diagnostico_texto)
                else:
                    item_diagnostico = QTableWidgetItem("")
                self.tabla_routh.setItem(i, columnas, item_diagnostico)
            
        except Exception as e:
            self.mostrar_error(f"Error al crear la tabla de Routh: {str(e)}")
        
        # Ajustar el tamaño de las columnas
        self.tabla_routh.resizeColumnsToContents()
    
    def actualizar_grafico_polos(self):
        """Actualiza el gráfico de polos y ceros"""
        try:
            polos, ceros = self.sistema.obtener_polos_ceros()
            
            # Limpiar la figura anterior
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            
            # Graficar ejes
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            
            # Graficar polos
            for polo in polos:
                ax.plot(complex(polo).real, complex(polo).imag, 'rx', 
                       markersize=10, label='Polos')
            
            # Graficar ceros
            for cero in ceros:
                ax.plot(complex(cero).real, complex(cero).imag, 'bo', 
                       markersize=10, label='Ceros')
            
            # Configurar gráfico
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Eje Real')
            ax.set_ylabel('Eje Imaginario')
            ax.set_title('Diagrama de Polos y Ceros')
            
            # Eliminar etiquetas duplicadas en la leyenda
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            if by_label:  # Solo mostrar leyenda si hay elementos
                ax.legend(by_label.values(), by_label.keys())
            
            # Hacer el gráfico cuadrado y establecer límites
            ax.axis('equal')
            
            # Si no hay polos ni ceros, establecer límites predeterminados
            if not polos and not ceros:
                ax.set_xlim(-1, 1)
                ax.set_ylim(-1, 1)
            
            # Actualizar el canvas
            self.canvas.draw()
            
        except Exception as e:
            # En caso de error, mostrar un gráfico vacío con mensaje de error
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, f"Error al graficar:\n{str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()




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
        background-color: #D0D0D0;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: #2B2D42;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }
"""