from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from PyQt5.Qt import Qt


class StructuralElement():
    def __init__(self, width, height):
        """
        shape: QImage
        anchor: QPoint
        """
        self.image = QImage(width, height, QImage.Format_Mono)
        self.anchor = QPoint(0, 0)

        self.image.fill(Qt.black)

    def pixel(self, x, y):
        return self.image.pixel(x, y)

    def width(self):
        return self.image.width()

    def height(self):
        return self.image.height()
