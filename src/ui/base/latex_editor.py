from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, QToolButton
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from sympy import sympify, Symbol, SympifyError,Expr
import re
from latex2sympy2 import latex2sympy

class LatexEditor(QWidget):
    latex_changed = pyqtSignal(str)

    def __init__(self, initial_latex="", parent=None):
        super().__init__(parent)
        self.initial_latex = initial_latex  # Guardamos el valor inicial
        self.page_loaded = False  # Nueva bandera para controlar el estado de carga
        self.init_ui(initial_latex)
        self.connect_web_signals()
        self.validation_timer = QTimer(self)
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.delayed_validation)

    def init_ui(self, initial_latex):
        self.setStyleSheet(ESTILO)

        layout = QVBoxLayout()

        self.preview_label = QLabel("Vista previa:")
        layout.addWidget(self.preview_label)

        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(75)
        channel = QWebChannel()
        self.web_view.page().setWebChannel(channel)
        channel.registerObject("latex_editor", self)
        
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
    
        // Definimos updateLatex inmediatamente
        window.updateLatex = function(latex) {
            var content = document.getElementById('latex-content');
            if (content) {
                content.innerHTML = '$$' + latex + '$$';
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, content]);
            }
        };
        var latex_editor;

        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$','$'], ['\\(','\\)']],
                processEscapes: true
            },
            TeX: {
                equationNumbers: { autoNumber: "AMS" },
                extensions: ["AMSmath.js", "AMSsymbols.js"]
            },
            messageStyle: "none"
        });

        function updateLatex(latex) {
            console.log("updateLatex called with:", latex);
            var content = document.getElementById('latex-content');
            if (content) {
                content.innerHTML = '$$' + latex + '$$';
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, content]);
            } else {
                console.error("Element 'latex-content' not found");
            }
        }

        function initWebChannel() {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                latex_editor = channel.objects.latex_editor;
                if (latex_editor && typeof latex_editor.get_latex === 'function') {
                    latex_editor.get_latex(function(initialLatex) {
                        updateLatex(initialLatex);
                    });
                }
            });
        }

        document.addEventListener("DOMContentLoaded", initWebChannel);

        window.updateLatex = updateLatex;
    </script>
</head>
<body>
    <div id="latex-content" style="font-size: 16px;"></div>
</body>
</html>
        """
        self.web_view.setHtml(html_content)
        layout.addWidget(self.web_view)

        self.editor = QTextEdit()
        self.editor.setFixedHeight(35)
        self.editor.setText(initial_latex)
        self.editor.textChanged.connect(self.update_preview)
        layout.addWidget(self.editor)
        
        self.editor.textChanged.connect(self.start_validation_timer)
        
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.validation_label)

        # Add symbol selector
        symbol_layout = QHBoxLayout()
        symbols = ["s", "\\frac{}{}", "^2", "^3", "\sqrt[n]{x}", "\log","\ln", "e", "\pi"]
        for symbol in symbols:
            button = QToolButton()
            if symbol == "\\frac{}{}":
                button.setText("a/b")
            elif symbol == "\\sqrt[n]{x}":
                button.setText("√ₙ(x)")
            elif symbol == "\ln":
                button.setText("ln")
            elif symbol == "\log":
                button.setText("log")
            elif symbol == "\pi":
                button.setText("π")
            else:
                button.setText(symbol)
            button.clicked.connect(lambda checked, s=symbol: self.insert_symbol(s))
            symbol_layout.addWidget(button)
            
        layout.addLayout(symbol_layout)

        self.setLayout(layout)

    def insert_symbol(self, symbol):
        cursor = self.editor.textCursor()
        if symbol == "\\frac{}{}":
            cursor.insertText("\\frac{numerador}{denominador}")
            # Seleccionar "numerador" para que el usuario pueda reemplazarlo fácilmente
            cursor.movePosition(cursor.Left, cursor.KeepAnchor, 9)
        elif symbol == "\log":
            cursor.insertText("\\log()")
            cursor.movePosition(cursor.Left, cursor.MoveMode.MoveAnchor, 1)
        elif symbol == "\ln":
            cursor.insertText("\\ln()")
            cursor.movePosition(cursor.Left, cursor.MoveMode.MoveAnchor, 1)
        else:
            cursor.insertText(symbol)
        self.editor.setFocus()
        
    def start_validation_timer(self):
        self.validation_timer.start(1000)  # 1000 ms = 1 segundo de delay

    def delayed_validation(self):
        latex = self.editor.toPlainText()
        if self.es_funcion_valida(latex):
            self.validation_label.setText("Función válida")
            self.validation_label.setStyleSheet("color: green; font-weight: bold;")
            self.update_preview()
            self.latex_changed.emit(latex)
        else:
            self.validation_label.setText("Función inválida")
            self.validation_label.setStyleSheet("color: red; font-weight: bold;")

    def update_preview(self):
        if not self.page_loaded:  # Si la página no está cargada, no hacemos nada
            return
        
        latex = self.editor.toPlainText()
        escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
        js_code = f"if(window.updateLatex) {{ window.updateLatex('{escaped_latex}'); }} else {{ console.error('updateLatex not available'); }}"
        self.web_view.page().runJavaScript(js_code)
        self.latex_changed.emit(latex)
        
    def connect_web_signals(self):
        self.web_view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            print("Web page loaded successfully")
            self.page_loaded = True  # Marcamos la página como cargada
            if self.initial_latex:  # Si hay un valor inicial, lo actualizamos
                self.update_preview()
        else:
            print("Failed to load web page")

    def get_latex(self):
        return self.editor.toPlainText()

    def set_latex(self, latex):
        self.editor.setText(latex)
        if self.page_loaded:  # Solo actualizamos si la página está cargada
            self.update_preview()
            
    def es_funcion_valida(self, latex):
        """
        Valida si una expresión LaTeX es válida según los siguientes criterios:
        1. Puede ser convertida a sympy usando latex2sympy
        2. Solo contiene la variable 's' como símbolo
        
        Args:
            latex (str): La expresión LaTeX a validar
            
        Returns:
            bool: True si la expresión es válida, False en caso contrario
        """
        try:
            # Intentamos convertir la expresión LaTeX a sympy
            expr = latex2sympy(latex)
            
            # Obtenemos todos los símbolos (variables) en la expresión
            simbolos = expr.free_symbols

            print(simbolos)
            
            # Verificamos que solo haya un símbolo y sea 's'
            if len(simbolos) == 0:
                return True
            return len(simbolos) == 1 and 's' in [str(sym) for sym in simbolos]
            
        except Exception as e:
            # Si hay cualquier error en la conversión, la función no es válida
            return False


        latex = latex.replace(' ', '').lower()
        
        if not latex or latex.count('{') != latex.count('}'):
            return False
        
        if latex.replace('.', '').isdigit():
            return True
        
        # Permitir expresiones LaTeX específicas
        valid_latex_expressions = ["\\frac", "\\log", "\\ln", "e", "\\pi", "\\sqrt"]
        if any(expr in latex for expr in valid_latex_expressions):
            pass  # Permitir estas expresiones y continuar con la validación
        elif re.search(r'([a-z\d])\s*([a-z\d])', latex):
            # Verificar si hay términos adyacentes sin operador, excluyendo comandos LaTeX
            return False
        
        # Tratar símbolos especiales
        latex = re.sub(r'\\sqrt\[([^]]+)\]\{([^}]+)\}', r'(\2)**(1/(\1))', latex)  # raíz n-ésima
        # Tratar fracciones
        latex = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'((\1)/(\2))', latex)
        latex = latex.replace('\\log', 'log')
        latex = latex.replace('\\ln', 'ln')
        latex = latex.replace('e', 'E')  # 'E' es reconocido como la constante e en sympy
        latex = latex.replace('\\pi', 'pi')
        
        s = Symbol('s')
        try:
            expr = sympify(latex, locals={'s': s})
            
            if isinstance(expr, (dict, list, tuple)):
                return False
            
            if not isinstance(expr, Expr):
                return False
            
            if 's' not in latex and not expr.is_constant():
                return False
            
            return True
        except (SympifyError, TypeError, ValueError):
            return False
        
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
        background-color: #D0D0D0;  /* Fondo gris claro */
        color: #2B2D42;  /* Texto gris oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;  /* Bordes redondeados */
        padding: 12px;  /* Aumento del espaciado interior para más altura */
        font-size: 14px;  /* Tipografía */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
        min-height: 30px;  /* Altura mínima para que sea más alto */
    }

    QToolButton {
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;  /* Bordes redondeados */
        padding: 10px 20px;  /* Tamaño de botón más grande */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
        font-weight: bold;  /* Texto en negrita */
    }

    QToolButton:hover {
        background-color: #606060;  /* Gris aún más oscuro al pasar el cursor */
        cursor: pointer;  /* Cambia el cursor al pasar sobre el botón */
    }

    QToolButton:pressed {
        background-color: #505050;  /* Color de fondo al presionar el botón */
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