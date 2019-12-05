from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QImage


class StructuralElement():
    def __init__(self, width, height):
        """
        shape: QImage
        anchor: QPoint
        """
        self.image = QImage(width, height, QImage.Format_Mono)
        self.anchor = QPointF(0, 0)

    def pixel(self, x, y):
        return self.image.pixel(x, y)
