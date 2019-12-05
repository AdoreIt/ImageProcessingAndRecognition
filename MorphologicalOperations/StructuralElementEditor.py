from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QWidget

from enum import Enum

from StructuralElement import StructuralElement


class EPreset(Enum):
    FILL = 0
    SQUARE = 1
    CIRCLE = 2
    TRIANGLE = 3


DEFAULT_W = 300
DEFAULT_H = 300


class  WStructuralElementEditor(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.str_elem = StructuralElement(DEFAULT_W, DEFAULT_H)

    on_image_changed = pyqtSignal(StructuralElement, name="onImageChanged")

    def setPreset(self,preset):
        self.clear()

    def clear(self):
        print("clear called")
        self.__send()

    def setSize(self, w, h):
        self.str_elem = StructuralElement(w, h)
        self.__send()

    ### events

    def mousePressEvent(self, e):
        print("mousePressEvent")

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.lightGray)
        p.drawImage(0, 0, self.str_elem.image)

    ### private methods

    def __send(self):
        self.on_image_changed.emit(self.str_elem)
