from PyQt5.QtGui import QImage


class StructuralElement():
    def __init__(self, width, height, anchor):
        """
        shape: QImage
        anchor: QPoint
        """
        self.shape = QImage(width, height, QImage.Format_Mono)
        self.anchor = anchor
        self.width = width
        self.height = height

    def pixel(self, x, y):
        return self.shape.pixel(x, y)
