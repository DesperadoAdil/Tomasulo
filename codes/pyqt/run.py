# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Tomasulo(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Tomasulo')
        self.setWindowIcon(QIcon('static/icon.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Tomasulo()

    sys.exit(app.exec_())
