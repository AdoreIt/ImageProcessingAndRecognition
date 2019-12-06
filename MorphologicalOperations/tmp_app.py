from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QMainWindow, QGridLayout, QApplication, QWidget)
from StructuralElementEditor import WStructuralElementEditor


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.w = WStructuralElementEditor()
        self.w.onImageChanged.connect(self.onImageChanged)

        self.setCentralWidget(self.w)

        self.resize(1280, 720)
        self.setWindowTitle("MorphologicalOperations")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Space:
            self.w.clear()

    def onImageChanged(self, str_elem):
        pass


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
