import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import InitialMenuWindow
from back.sesion import Sesion

def launch_application(sesion):
    initial_menu = InitialMenuWindow()
    initial_menu.sesion = sesion
    initial_menu.show()
    return initial_menu

def main():
    app = QApplication(sys.argv) 
    sesion = Sesion()
    main_window = launch_application(sesion)
    # main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()