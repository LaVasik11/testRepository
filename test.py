from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Управление задачами")
        self.setGeometry(300, 250, 350, 200)

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText('это текст :)')
        self.main_text.move(100, 50)

def application():
    app = QApplication(sys.argv)
    window = Window()


    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
