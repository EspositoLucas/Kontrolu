from PyQt5.QtWidgets import QGraphicsTextItem,QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QTabWidget, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QWidget, QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from back.estabilidad import Estabilidad
from tbcontrol.symbolic import routh
import numpy as np
import os
from PyQt5 import QtGui
from sympy import latex
from PyQt5 import QtWidgets


VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFD700")  # Un amarillo brillante
NEGRO = QColor("#2B2D42")


# Colores aclarados al 150%
VERDE_ACLARADO = VERDE.lighter(150)
ROJO_ACLARADO = ROJO.lighter(150)
AMARILLO_ACLARADO = AMARILLO.lighter(150)
NEGRO_ACLARADO = NEGRO.lighter(150)

class EstabilidadTexto(QGraphicsTextItem):

    def __init__(self, sesion, estabilidad, parent=None):

        super().__init__(parent)

        self.polinomio = estabilidad

        self.estabilidad = Estabilidad(sesion)

        self.sesion = sesion

        self.default_color = AMARILLO

        self.hoover_color = AMARILLO_ACLARADO

        self.update_text(estabilidad)

        font = QFont("Arial", 30, QFont.Bold)

        self.setFont(font)

        self.setAcceptHoverEvents(True)
    
    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            EstabilidadDialog(self.sesion,self.estabilidad).exec_()
            self.update_text()


        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)


    def update_text(self,estabilidad):

        self.polinomio = estabilidad

        _ , estado =  self.estabilidad.calcular_routh_con_libreria(estabilidad[0])

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
        elif estado == "CRITICAMENTE_ESTABLE":
            self.setPlainText("Criticamente Estable")
            self.setDefaultTextColor(AMARILLO)
            self.default_color = AMARILLO
            self.hoover_color = AMARILLO_ACLARADO
        else:
            self.setPlainText("Indeterminable")
            self.setDefaultTextColor(NEGRO)
            self.default_color = NEGRO
            self.hoover_color = NEGRO_ACLARADO

        self.update()
    
    def hoverEnterEvent(self, event):
        self.setDefaultTextColor(self.hoover_color)
        self.setCursor(Qt.PointingHandCursor)
        self.update()

    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(self.default_color)
        self.unsetCursor()
        self.update()



class EstabilidadDialog(QDialog):

    def __init__(self, sistema, estabilidad, parent=None):

        super().__init__(parent)

        self.estabilidad = estabilidad


        self.matriz_routh_obtenida,self.nombre_estabilidad = self.estabilidad.calcular_routh_con_libreria()
        self.polinomio = latex(self.estabilidad.polinomio_caracteristico())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        

        
        self.sistema = sistema
        self.setWindowTitle("Análisis de Estabilidad")
        self.resize(800, 600)
        self.setStyleSheet(ESTILO)
        
        # Crear el layout principal
        layout = QVBoxLayout()
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))
        
        # Crear label para mostrar el estado de estabilidad
        self.estado_label = QLabel()
        self.estado_label.setAlignment(Qt.AlignCenter)
        self.estado_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        self.actualizar_estado_label()
        layout.addWidget(self.estado_label)
        
        # Crear el canvas para la ecuación LaTeX
        self.eq_canvas = self.crear_canvas_ecuacion()
        layout.addWidget(self.eq_canvas)
        
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
        
        # Agregar el botón de ayuda
        self.agregar_boton_ayuda()
        
        # Llenar los datos
        self.actualizar_datos()
    
    def agregar_boton_ayuda(self):
        """Agrega el botón de ayuda a la ventana"""
        help_button = QtWidgets.QPushButton("?", self)
        help_button.setFixedSize(30, 30)
        help_button.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #808080;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        help_button.clicked.connect(self.mostrar_ayuda)
        # Posicionar el botón en la esquina superior derecha
        help_button.move(self.width() - 40, 10)

    def mostrar_ayuda(self):
        """Muestra el diálogo de ayuda con explicaciones sobre el análisis de estabilidad"""
        help_dialog = QtWidgets.QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Análisis de Estabilidad")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(600)
        layout = QtWidgets.QVBoxLayout()
        
        # Título principal
        titulo = QtWidgets.QLabel("Guía de Análisis de Estabilidad")
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
            ("<b>¿Qué es la estabilidad de un sistema?</b>", 
            "La estabilidad es una característica fundamental que determina si un sistema de control "
            "mantendrá un comportamiento acotado ante entradas acotadas. Un sistema estable retornará "
            "a su estado de equilibrio después de una perturbación."),
            
            ("<b>Tabla de Routh:</b>",
            "<ul>"
            "<li><b>¿Qué es?</b> Es un método matemático para determinar la estabilidad sin calcular las raíces del sistema</li>"
            "<li><b>Interpretación:</b> Si no hay cambios de signo en la primera columna, el sistema es estable</li>"
            "<li><b>Coeficientes:</b> Cada fila representa los coeficientes del polinomio característico</li>"
            "<li><b>Grados:</b> Los grados 's' en la columna izquierda indican el orden de cada fila</li>"
            "</ul>"),
            
            ("<b>Diagrama de Polos y Ceros:</b>",
            "<ul>"
            "<li><b>Polos (X):</b> Raíces del denominador de la función de transferencia</li>"
            "<li><b>Ceros (O):</b> Raíces del numerador de la función de transferencia</li>"
            "<li><b>Región Estable:</b> Lado izquierdo del plano complejo (parte real negativa)</li>"
            "<li><b>Región Inestable:</b> Lado derecho del plano complejo (parte real positiva)</li>"
            "</ul>"),
            
            ("<b>Interpretación de Resultados:</b>",
            "<ul>"
            "<li><b>Sistema Estable:</b> Todos los polos están en el lado izquierdo del plano</li>"
            "<li><b>Sistema Inestable:</b> Uno o más polos están en el lado derecho del plano</li>"
            "<li><b>Sistema Críticamente Estable:</b> Uno o más polos están sobre el eje imaginario</li>"
            "</ul>")
        ]
        
        for titulo, texto in contenido:
            seccion = QtWidgets.QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 5px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)
        
        # Botón de cerrar
        cerrar_btn = QtWidgets.QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()

    def actualizar_estado_label(self):
        """Actualiza el estilo y texto del label según el estado de estabilidad"""
        if self.nombre_estabilidad == "ESTABLE":
            color = VERDE
        elif self.nombre_estabilidad == "INESTABLE":
            color = ROJO
        elif self.nombre_estabilidad == "CRITICAMENTE_ESTABLE":
            color = AMARILLO
        else:
            color = NEGRO
            
        self.estado_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
                color: white;
                background-color: {color};
            }}
        """)
        self.estado_label.setText(f"Sistema {self.nombre_estabilidad}")

    def crear_canvas_ecuacion(self):
        """Crea un canvas de matplotlib para mostrar la ecuación en LaTeX"""
        fig = Figure(figsize=(8, 1))
        canvas = FigureCanvas(fig)
        
        # Configurar el subplot
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Si hay un polinomio, mostrarlo
        if self.polinomio:
            ax.text(0.5, 0.5, f"${self.polinomio}$", 
                    fontsize=12, 
                    horizontalalignment='center',
                    verticalalignment='center')
        
        fig.tight_layout()
        return canvas

    def actualizar_ecuacion(self):
        """Actualiza la ecuación mostrada en el canvas"""
        if self.polinomio:
            self.eq_canvas.figure.clear()
            ax = self.eq_canvas.figure.add_subplot(111)
            ax.axis('off')
            ax.text(0.5, 0.5, f"${self.polinomio}$", 
                    fontsize=12, 
                    horizontalalignment='center',
                    verticalalignment='center')
            self.eq_canvas.figure.tight_layout()
            self.eq_canvas.draw()

    def actualizar_datos(self):
        """Actualiza todos los elementos de la interfaz"""
        try:
            self.actualizar_estado_label()
            self.actualizar_ecuacion()
            self.actualizar_tabla_routh()
            self.actualizar_grafico_polos()
        except Exception as e:
            self.mostrar_error(f"Error al actualizar los datos: {str(e)}")
    
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

    def actualizar_tabla_routh(self):
        """
        Actualiza la tabla de Routh con los datos del sistema
        """
        try:
            # Obtener la matriz de Routh (asumiendo que tienes un método que la calcula)
            matriz_routh = self.matriz_routh_obtenida # Este método debe devolver una sympy Matrix
            
            # Obtener dimensiones de la matriz
            filas, columnas = matriz_routh.shape
            
            # Configurar la tabla
            self.tabla_routh.setRowCount(filas)
            self.tabla_routh.setColumnCount(columnas)
            
            # Llenar la tabla
            for i in range(filas):
                for j in range(columnas):
                    valor = matriz_routh[i, j]
                    
                    # Convertir el valor sympy a string para mejor visualización
                    if valor == 0:
                        texto = "0"
                    else:
                        # Usar pretty para una mejor representación de fracciones
                        texto = str(valor)
                    
                    # Crear el item de la tabla
                    item = QTableWidgetItem(texto)
                    
                    # Centrar el texto
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Si el valor es 0 o None, cambiar el color de fondo
                    if valor == 0 or valor is None:
                        item.setBackground(QColor(240, 240, 240))
                    
                    self.tabla_routh.setItem(i, j, item)
            
            # Ajustar el tamaño de las columnas y filas
            self.tabla_routh.resizeColumnsToContents()
            self.tabla_routh.resizeRowsToContents()
            
            # Agregar headers (s⁴, s³, s², s¹, s⁰)
            headers_horizontales = []
            for i in range(columnas):
                if i == 0:
                    headers_horizontales.append("Coef.")
                else:
                    headers_horizontales.append(f"c{i}")
            
            self.tabla_routh.setHorizontalHeaderLabels(headers_horizontales)
            
            # Headers verticales para mostrar el grado de s
            headers_verticales = []
            grado_actual = filas - 1
            for i in range(filas):
                if grado_actual >= 0:
                    headers_verticales.append(f"s{grado_actual}")
                    grado_actual -= 1
                else:
                    headers_verticales.append("")
            
            self.tabla_routh.setVerticalHeaderLabels(headers_verticales)
            

            
        except Exception as e:
            self.mostrar_error(f"Error al actualizar la tabla de Routh: {str(e)}")
    def mostrar_error(self, mensaje):
        """
        Muestra un diálogo de error
        """
        QMessageBox.critical(self, "Error", mensaje)

    def actualizar_grafico_polos(self):
        """
        Actualiza el gráfico de polos y ceros en el plano complejo
        """
        try:
            # Obtener polos y ceros del sistema
            polos_dict, ceros_dict = self.estabilidad.calcular_polos_y_ceros()
            
            # Convertir los diccionarios de sympy a listas de números complejos
            polos_complex = []
            if polos_dict:  # Si hay polos
                for polo, multiplicidad in polos_dict.items():
                    polo_complex = complex(polo.evalf())
                    polos_complex.extend([polo_complex] * multiplicidad)
            
            ceros_complex = []
            if ceros_dict:  # Si hay ceros
                for cero, multiplicidad in ceros_dict.items():
                    cero_complex = complex(cero.evalf())
                    ceros_complex.extend([cero_complex] * multiplicidad)
            
            # Convertir a arrays de numpy
            polos_complex = np.array(polos_complex)
            ceros_complex = np.array(ceros_complex)
            
            # Limpiar la figura anterior
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            
            # Determinar los límites del gráfico
            if len(polos_complex) > 0 or len(ceros_complex) > 0:
                # Si hay al menos polos o ceros, usar sus valores para los límites
                if len(polos_complex) > 0 and len(ceros_complex) > 0:
                    all_points = np.concatenate([polos_complex, ceros_complex])
                elif len(polos_complex) > 0:
                    all_points = polos_complex
                else:
                    all_points = ceros_complex
                    
                max_abs = max(abs(np.max(all_points)), abs(np.min(all_points)))
                limit = max_abs * 1.2
            else:
                # Si no hay ni polos ni ceros, usar límites predeterminados
                limit = 5
            
            # Graficar polos (x)
            if len(polos_complex) > 0:
                ax.plot(polos_complex.real, polos_complex.imag, 'rx', 
                    markersize=10, label='Polos', markeredgewidth=2)
            
            # Graficar ceros (o)
            if len(ceros_complex) > 0:
                ax.plot(ceros_complex.real, ceros_complex.imag, 'bo', 
                    markersize=10, label='Ceros', fillstyle='none', markeredgewidth=2)
            
            # Configurar el aspecto del gráfico
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
            
            # Establecer límites y aspecto
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.set_aspect('equal')
            
            # Etiquetas y título
            ax.set_xlabel('Eje Real')
            ax.set_ylabel('Eje Imaginario')
            ax.set_title('Diagrama de Polos y Ceros')
            
            # Agregar leyenda solo si hay elementos para mostrar
            if len(polos_complex) > 0 or len(ceros_complex) > 0:
                ax.legend()
            
            # Determinar si el sistema es estable
            if polos_dict:
                sistema_estable = all(complex(polo.evalf()).real < 0 for polo in polos_dict.keys())
                estabilidad_texto = "Sistema Estable" if sistema_estable else "Sistema Inestable"
            else:
                estabilidad_texto = "Sistema sin polos"
                sistema_estable = True
            
            # Agregar una región sombreada para la parte inestable del plano
            ax.axvline(x=0, color='r', linestyle='--', alpha=0.2)
            ax.fill_betweenx([-limit, limit], 0, limit, alpha=0.1, color='red', 
                            label='Región Inestable')
            
            # Agregar texto indicando la estabilidad
            color_texto = "green" if sistema_estable else "red"
            ax.text(0.02, 0.98, estabilidad_texto,
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                    color=color_texto)
            
            # Ajustar el layout para que no se corten las etiquetas
            self.canvas.figure.tight_layout()
            
            # Actualizar el canvas
            self.canvas.draw()
            
        except Exception as e:
            self.mostrar_error(f"Error al actualizar el gráfico de polos y ceros: {str(e)}")
    

ESTILO = """
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
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);  /* Sombra de texto para resaltar */
        cursor: pointer;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
        cursor: pointer;
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