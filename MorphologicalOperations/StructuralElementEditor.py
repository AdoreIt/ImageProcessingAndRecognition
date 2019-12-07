from PyQt5.Qt import Qt, qRgb
from PyQt5.QtCore import pyqtSignal, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QWidget

from enum import Enum

from StructuralElement import StructuralElement

BLACK = qRgb(0, 0, 0)
WHITE = qRgb(255, 255, 255)


class EPreset(Enum):
    EMPTY = 0
    FILLED = 1
    SQUARE = 2
    CIRCLE = 3
    TRIANGLE = 4


DEFAULT_W = 10
DEFAULT_H = 10


class  WStructuralElementEditor(QWidget):
    ### signals

    on_image_changed = pyqtSignal(StructuralElement, name="onImageChanged")

    ### methods

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.setMouseTracking(True)

        self.str_elem = StructuralElement(DEFAULT_W, DEFAULT_H)
        self.last_pos = None

    def setPreset(self, preset):
        self.clear()

    def clear(self):
        self.__send()

    def setSize(self, w, h):
        self.str_elem = StructuralElement(w, h)
        self.__send()

    ### events

    def mousePressEvent(self, e):
        self.draw_color = BLACK if self.str_elem.image.pixel(self.last_pos) != BLACK else WHITE

        pos = self.__window_to_image(e.pos())
        if self.last_pos is not None and pos is not None and e.buttons() == Qt.LeftButton:
            self.__draw_line(self.last_pos, pos, self.draw_color)
        self.last_pos = pos

        self.update()

    def mouseMoveEvent(self, e):
        pos = self.__window_to_image(e.pos())
        if self.last_pos is not None and pos is not None and e.buttons() == Qt.LeftButton:
            self.__draw_line(self.last_pos, pos, self.draw_color)
        self.last_pos = pos

        self.update()

    def leaveEvent(self, e):
        self.last_pos = None

        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.lightGray)

        pixmap = QPixmap.fromImage(self.str_elem.image)

        if self.last_pos is not None and self.str_elem.image.pixel(self.last_pos) != BLACK:
            with QPainter(pixmap) as pix_painter:
                pix_painter.setPen(QPen(QColor(200, 200, 200)))
                pix_painter.drawPoint(self.last_pos)

        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)

    ### private methods

    def __send(self):
        self.update()
        self.on_image_changed.emit(self.str_elem)

    def __window_to_image(self, point):
        image = self.str_elem.image

        window_aspect = self.width() / self.height()
        image_aspect = image.width() / image.height()

        if window_aspect > image_aspect:
            factor = self.height() / image.height()
            offset = QPointF(self.width() - image.width() * factor, 0) / 2
        else:
            factor = self.width() / image.width()
            offset = QPointF(0, self.height() - image.height() * factor) / 2

        res = (point - offset) / factor
        res = QPoint(int(res.x()), int(res.y()))

        return res if image.rect().contains(res) else None

    def __draw_line(self, a, b, color):
        p = QPainter(self.str_elem.image)
        p.setPen(QColor.fromRgb(color))
        p.drawLine(a, b)

        self.__send()
