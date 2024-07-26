from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

class LatexEditor(QWidget):
    latex_changed = pyqtSignal(str)

    def __init__(self, initial_latex="", parent=None):
        super().__init__(parent)
        self.init_ui(initial_latex)
        # self.load_saved_content()
        self.connect_web_signals()

    def init_ui(self, initial_latex):
        layout = QVBoxLayout()

        self.preview_label = QLabel("Vista previa:")
        layout.addWidget(self.preview_label)

        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(50)
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
                window.latex_editor = channel.objects.latex_editor;
                console.log("QWebChannel initialized");
                if (window.latex_editor && typeof window.latex_editor.get_latex === 'function') {
                    window.latex_editor.get_latex(function(initialLatex) {
                        console.log("Initial LaTeX:", initialLatex);
                        updateLatex(initialLatex);
                    });
                } else {
                    console.error("latex_editor or get_latex not available");
                }
            });
        }

        document.addEventListener("DOMContentLoaded", initWebChannel);
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
        self.editor.setFixedHeight(50)
        self.editor.setText(initial_latex)
        self.editor.textChanged.connect(self.update_preview)
        layout.addWidget(self.editor)

        self.setLayout(layout)
        self.update_preview()

    def update_preview(self):
        latex = self.editor.toPlainText()
        escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
        js_code = f"console.log('Updating LaTeX:', '{escaped_latex}'); window.updateLatex('{escaped_latex}');"
        self.web_view.page().runJavaScript(js_code)
        self.latex_changed.emit(latex)
        
    def load_saved_content(self):
        latex = self.get_latex()
        escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
        js_code = f"console.log('Loading saved content:', '{escaped_latex}'); window.updateLatex('{escaped_latex}');"
        self.web_view.page().runJavaScript(js_code)
        
    def connect_web_signals(self):
        self.web_view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            print("Web page loaded successfully")
            self.load_saved_content()
        else:
            print("Failed to load web page")

    def get_latex(self):
        return self.editor.toPlainText()

    def set_latex(self, latex):
        self.editor.setText(latex)
        self.update_preview()
