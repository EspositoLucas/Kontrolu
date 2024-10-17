from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout, QToolButton
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from sympy import sympify, Symbol, SympifyError,Expr
import re

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