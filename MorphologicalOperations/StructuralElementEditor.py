from PyQt5.Qt import Qt, qRgb
from PyQt5.QtCore import pyqtSignal, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QWidget

from enum import Enum
import math

from StructuralElement import StructuralElement

BLACK = qRgb(0, 0, 0)
WHITE = qRgb(255, 255, 255)


class EPreset(Enum):
    EMPTY = 0
    FILLED = 1
    SQUARE = 2
    CIRCLE = 3
    TRIANGLE = 4


DEFAULT_W = 3
DEFAULT_H = 3


class WStructuralElementEditor(QWidget):
    # signals

    on_structural_element_changed = pyqtSignal(StructuralElement, name="onStructuralElementChanged")

    # methods

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

    # events

    def mousePressEvent(self, e):
        pos = self.__window_to_image(e.pos())

        if e.buttons() == Qt.LeftButton:
            self.draw_color = BLACK if self.last_pos is None or self.str_elem.image.pixel(
                self.last_pos) != BLACK else WHITE

            if self.last_pos is not None and pos is not None and e.buttons() == Qt.LeftButton:
                self.__draw_line(self.last_pos, pos, self.draw_color)
            self.last_pos = pos
        elif e.buttons() == Qt.RightButton:
            if self.last_pos is not None:
                self.__set_anchor(pos)

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

        if self.last_pos is not None:
            with QPainter(pixmap) as pix_painter:
                color = QColor(200, 200, 200) if self.str_elem.image.pixel(self.last_pos) != BLACK else QColor(80, 80, 80)
                pix_painter.setPen(QPen(color))
                pix_painter.drawPoint(self.last_pos)

        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)

        win_pos, factor = self.__image_to_window(self.str_elem.anchor)
        anchor_color = QColor(Qt.white) if self.str_elem.image.pixel(self.str_elem.anchor) == BLACK else QColor(Qt.black)
        p.setPen(QPen(anchor_color, 2))
        cross_side = factor / 2 / 2
        p.translate(factor / 2, factor / 2)
        p.drawLine(win_pos - QPoint(cross_side, cross_side), win_pos + QPoint(cross_side, cross_side))
        p.drawLine(win_pos - QPoint(cross_side, -cross_side), win_pos + QPoint(cross_side, -cross_side))

    # private methods

    def __send(self):
        self.update()
        self.on_structural_element_changed.emit(self.str_elem)

    def __calc_factor_and_offset(self):
        image = self.str_elem.image

        window_aspect = self.width() / self.height()
        image_aspect = image.width() / image.height()

        if window_aspect > image_aspect:
            factor = self.height() / image.height()
            offset = QPointF(self.width() - image.width() * factor, 0) / 2
        else:
            factor = self.width() / image.width()
            offset = QPointF(0, self.height() - image.height() * factor) / 2

        return factor, offset

    def __image_to_window(self, point):
        factor, offset = self.__calc_factor_and_offset()
        return factor * point + offset, factor

    def __window_to_image(self, point):
        image = self.str_elem.image

        factor, offset = self.__calc_factor_and_offset()

        res = (point - offset) / factor
        res = QPoint(math.floor(res.x()), math.floor(res.y()))

        return res if image.rect().contains(res) else None

    def __set_anchor(self, pos):
        self.str_elem.anchor = pos

        self.__send()

    def __draw_line(self, a, b, color):
        p = QPainter(self.str_elem.image)
        p.setPen(QColor.fromRgb(color))
        p.drawLine(a, b)

        self.__send()
