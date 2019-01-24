from View import View
from Controller import Controller
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizeGrip
from PyQt5.QtCore import Qt
import sys

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    a = View()

    b = Controller(a)
    a.set_control(b)

    sys.exit(app.exec_())