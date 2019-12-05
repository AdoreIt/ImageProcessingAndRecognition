from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QApplication, QWidget)


def read_image(file_name):
    return QImage(file_name)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        grid_layout = QGridLayout()
        # grid_layout.add

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("MorphologicalOperations")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
