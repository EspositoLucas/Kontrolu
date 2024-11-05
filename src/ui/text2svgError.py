from PyQt5.QtWidgets import  QApplication
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QTransform
from io import BytesIO
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import ( QApplication, 
                              QDialog, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import os
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify,DiracDelta,N,latex
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTabWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from io import BytesIO
import pyperclip
import os

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

class SVGViewError(QGraphicsSvgItem):
    def __init__(self, macro, padre, pos_x,pos_y, errores, parent=None):
        super().__init__(parent)
        self.padre = padre
        self.macro = macro

        self.pos_x = pos_x
        self.pos_y = pos_y

        plt.rc('mathtext', fontset='cm')

        self.renders =[]
        self.graficos = []

        self.calculo, self.calculo_simpy, self.error_estado_estable = errores


        if self.error_estado_estable.is_real:
            #limitar cantidad de decimales
            self.error_estado_estable = N(self.error_estado_estable, 2)
        self.error_estado_estable_texto = 'e_{ss} = ' + latex(self.error_estado_estable)
        bytess_error_estado_estable = self.tex2svg(self.error_estado_estable_texto)
        self.renderer_error_estado_estable = QSvgRenderer(bytess_error_estado_estable)

        self.renders.append(self.renderer_error_estado_estable)


        self.calculo_texto = 'lim_{s \\to 0} ' + self.calculo + ' = ' + latex(self.error_estado_estable)
        bytess_calculo = self.tex2svg(self.calculo_texto)
        self.renderer_calculo = QSvgRenderer(bytess_calculo)
        self.renders.append(self.renderer_calculo)
        self.graficos.append((self.calculo_simpy,True,'Error','e_{ss} = lim_{s \\to 0}'))




        if len(self.renders) > 0:
            self.setSharedRenderer(self.renders[0])
            self.elegir = 0
            self.setAcceptHoverEvents(True)
            self.setSize()
        

    
    def setSize(self):

        max_x = 560
        max_y = 250

        render = self.renders[self.elegir]

        rect = render.viewBoxF()

        # Calcular la escala necesaria para ajustar el SVG al tamaño máximo
        scale_x = max_x / rect.width()
        scale_y = max_y / rect.height()
        scale = min(scale_x, scale_y,1)
        
        # Aplicar la escala al QGraphicsSvgItem
        self.setTransform(QTransform().scale(scale, scale))

        # Calcular la nueva posición para centrar el SVG
        # Obtener el tamaño escalado
        scaled_width = rect.width() * scale
        scaled_height = rect.height() * scale

        pos_x = self.pos_x -(scaled_width/2)
        pos_y = self.pos_y -(scaled_height/2)

        # Establecer la nueva posición
        self.setPos(pos_x, pos_y)




    def tex2svg(self, formula, fontsize=50, dpi=300):
        """Render TeX formula to SVG."""
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                    bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)

        output.seek(0)
        return output.read()

    def mousePressEvent(self, event):
        # Obtener la posición del clic
        pos = event.pos()
        
        # Verificar si el clic fue con el botón izquierdo
        if event.button() == Qt.RightButton:
            self.elegir += 1
            if self.elegir >= len(self.renders):
                self.elegir = 0
            self.setSharedRenderer(self.renders[self.elegir])
            self.setSize()
            #self.padre.error_update_pos()




        if event.button() == Qt.LeftButton:
            self.open_graph_window(self.elegir)
        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)

    def open_graph_window(self, cual):
        dialog = GraphWindow()
        for fdt, is_laplace, title, output in self.graficos:
            dialog.add_plot(fdt, is_laplace, title, output, cual)
        dialog.exec_()        

        
    
    def hoverEnterEvent(self, event):
        # Cambiar el cursor al formato de clic
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Restaurar el cursor al estado predeterminado
        QApplication.restoreOverrideCursor()
        super().hoverLeaveEvent(event)



class GraphWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Dominio de Laplace")
        self.setStyleSheet(ESTILO)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Diccionarios para almacenar las figuras y latex por pestaña
        self.figures = {}
        self.latex_expressions = {}
        
        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QIcon()
        icon.addPixmap(QPixmap(image_path), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Botón de ayuda
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.clicked.connect(self.mostrar_ayuda)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignRight)

        # TabWidget para los gráficos
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Contenedor para los botones
        button_layout = QHBoxLayout()
        
        # Botón para copiar LaTeX
        copy_latex_btn = QPushButton("Copiar LaTeX")
        copy_latex_btn.clicked.connect(self.copy_latex)
        button_layout.addWidget(copy_latex_btn)
        
        # Botón para guardar gráfico
        save_graph_btn = QPushButton("Guardar Gráfico")
        save_graph_btn.clicked.connect(self.save_graph)
        button_layout.addWidget(save_graph_btn)
        
        # Botón para guardar LaTeX como imagen
        save_latex_btn = QPushButton("Guardar LaTeX")
        save_latex_btn.clicked.connect(self.save_latex)
        button_layout.addWidget(save_latex_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_plot(self, fdt, is_laplace, title, output, index):
        """Añade un nuevo plot al tab widget"""
        plot_label = QLabel()
        if is_laplace:
            fig = self.plot_laplace(fdt, title, output)
            pixmap = self.get_plot_pixmap(fig)
            
            # Guardar la información para esta pestaña específica
            self.latex_expressions[title] = f"{output} {latex(sympify(fdt))}"
            self.figures[title] = fig
            
        plot_label.setPixmap(pixmap)
        self.tab_widget.addTab(plot_label, title)
        self.tab_widget.setCurrentIndex(index)

    def get_current_title(self):
        """Obtiene el título de la pestaña actual"""
        return self.tab_widget.tabText(self.tab_widget.currentIndex())

    def copy_latex(self):
        """Copia la expresión LaTeX al portapapeles"""
        current_title = self.get_current_title()
        latex_expr = self.latex_expressions.get(current_title)
        if latex_expr:
            pyperclip.copy(latex_expr)

    def save_graph(self):
        """Guarda el gráfico actual como imagen"""
        current_title = self.get_current_title()
        current_fig = self.figures.get(current_title)
        
        if current_fig:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Guardar Gráfico",
                self.get_current_title()+"_grafico.png", "PNG Files (*.png);;All Files (*)"
            )
            if file_name:
                current_fig.savefig(file_name, bbox_inches='tight', dpi=300)

    def save_latex(self):
        """Guarda la ecuación LaTeX como imagen"""
        current_title = self.get_current_title()
        latex_expr = self.latex_expressions.get(current_title)
        
        if latex_expr:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Guardar LaTeX",
                self.get_current_title()+"_latex.png", "PNG Files (*.png);;All Files (*)"
            )
            if file_name:
                # Crear una figura solo con la ecuación
                fig = plt.figure(figsize=(10, 1))
                plt.axis('off')
                plt.text(0.5, 0.5, f"${latex_expr}$",
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=30)
                plt.savefig(file_name, bbox_inches='tight', dpi=300,
                          transparent=True)
                plt.close(fig)

    def plot_laplace(self, fdt, title, output):
        """Generar y mostrar el gráfico del dominio de Laplace con la ecuación en LaTeX."""
        s = symbols('s')
        f_laplace = sympify(fdt)
        F_laplace = lambdify(s, f_laplace, 'numpy')

        fig = plt.figure(figsize=(10, 6))
        ax = plt.subplot2grid((1,1), (0,0))
        
        s_vals = np.linspace(0, 10, 100)
        F_s = F_laplace(s_vals)
        
        if np.isscalar(F_s):
            F_s = np.full_like(s_vals, F_s)

        plt.plot(s_vals, F_s)
        plt.title(title)
        plt.xlabel("S")
        plt.ylabel(f"${output}$")
        plt.grid(True)
        
        latex_expr = f"{output} {latex(f_laplace)}"
        fig.text(0.5, 0.08, f"${latex_expr}$", 
                horizontalalignment='center', 
                fontsize=30)
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25)
        
        return fig
        


    def get_plot_pixmap(self, figure):
        """Convierte una figura de matplotlib en un QPixmap."""
        buf = BytesIO()
        figure.savefig(buf, format="png")
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        buf.close()
        return pixmap
    
    def mostrar_ayuda(self):
        help_dialog = QtWidgets.QDialog()
        help_dialog.setWindowTitle("Ayuda - Visualización del Sistema")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base','imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        help_dialog.setWindowIcon(icon)
        
        layout = QtWidgets.QVBoxLayout()
        
        titulo = QtWidgets.QLabel("Guía de Visualización del Sistema de Control")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        contenido = [
            ("<b>Visualización del Error en Estado Estable:</b>",
         "Esta ventana permite analizar el error en estado estable del sistema de control en el dominio de Laplace."),
        
        ("<b>Interpretación de Gráficos:</b>",
         "<ul>"
         "<li><b>Dominio de Laplace:</b> Muestra el valor del error en estado estable y su cálculo algebraico</li>"
         "</ul>"),
        
        ("<b>Navegación e Interacción:</b>",
         "<ul>"
         "<li><b>Clic Derecho:</b> Alterna entre las diferentes representaciones del error en estado estable</li>"
         "<li><b>Clic Izquierdo:</b> Abre una ventana con gráficos detallados de las representaciones</li>"
         "<li><b>Pestañas:</b> Permiten cambiar entre las diferentes vistas de la visualización</li>"
         "</ul>"),
        
        ("<b>Análisis del Error en Estado Estable:</b>",
         "<ul>"
         "<li><b>Valor Numérico:</b> Consultar el valor exacto del error en estado estable</li>"
         "<li><b>Cálculo Algebraico:</b> Examinar la expresión matemática que define el error</li>"
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
        
        cerrar_btn = QtWidgets.QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()