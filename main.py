from View import View
from Controller import Controller
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizeGrip
from PyQt5.QtCore import Qt
import sys
from qtmodern import styles, windows


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # styles.dark(app)
    app.setStyle('Fusion')
    a = View()

    # mw = windows.ModernWindow(a)
    # mw.show()


    b = Controller(a)
    a.set_control(b)
    sys.exit(app.exec_())