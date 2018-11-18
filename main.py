from View import View
from Controller import Controller
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = View()
    b = Controller(a)
    a.set_control(b)
    a.show()
    sys.exit(app.exec_())