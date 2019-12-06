from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, QPointF
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtWidgets import QWidget

from enum import Enum

from StructuralElement import StructuralElement


class EPreset(Enum):
    EMPTY = 0
    FILLED = 1
    SQUARE = 2
    CIRCLE = 3
    TRIANGLE = 4


DEFAULT_W = 20
DEFAULT_H = 10


class  WStructuralElementEditor(QWidget):
    ### signals

    on_image_changed = pyqtSignal(StructuralElement, name="onImageChanged")

    ### methods

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.str_elem = StructuralElement(DEFAULT_W, DEFAULT_H)

    def setPreset(self, preset):
        print("WStructuralElementEditor.setPreset(preset=%i)" % (preset))

        self.clear()

    def clear(self):
        print("WStructuralElementEditor.clear()")

        self.__send()

    def setSize(self, w, h):
        print("WStructuralElementEditor.mousePressEvent(w=%i, h=%i)" % (w, h))

        self.str_elem = StructuralElement(w, h)
        self.__send()

    ### events

    def mousePressEvent(self, e):
        print("WStructuralElementEditor.mousePressEvent(x=%i, y=%i)" % (e.x(), e.y()))

    def mouseMoveEvent(self, e):
        print("WStructuralElementEditor.mouseMoveEvent(x=%i, y=%i)" % (e.x(), e.y()))

        point = self.__window_to_image(e.pos())
        if point:
            self.__set_pixel(point, 0)

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.lightGray)

        pixmap = QPixmap.fromImage(self.str_elem.image)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)

    ### private methods

    def __send(self):
        print("WStructuralElementEditor.__send()")

        self.update()
        self.on_image_changed.emit(self.str_elem)

    def __window_to_image(self, point):
        image = self.str_elem.image

        max_image_side = max(image.width(), image.height())
        # min_image_side = min(image.width(), image.height())

        min_window_side = min(self.width(), self.height())
        # max_window_side = max(self.width(), self.height())

        factor = min_window_side / max_image_side
        # other_factor = max_window_side / min_image_side

        window_aspect = self.width() / self.height()
        image_aspect = image.width() / image.height()

        if window_aspect > image_aspect:
            print("window is wider")
            offset = QPointF(self.width() - image.width() * factor, 0) / 2
        else:
            print("window is taller")
            offset = QPointF(0, self.height() - image.height() * factor) / 2

        return (point - offset) / factor

    def __set_pixel(self, point, value):
        print("WStructuralElementEditor.__set_pixel(x=%i, y=%i, v=%i)" % (point.x(), point.y(), value))

        self.str_elem.image.setPixel(point.x(), point.y(), value)
        self.__send()
