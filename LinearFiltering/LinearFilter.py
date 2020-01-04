from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtGui import QImage

DEFAULT_H = 10
DEFAULT_W = 10


class LinearFilterEdit(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.lin_filt_edit = QPlainTextEdit("0,0,0\r\n0,0,0\r\n0,0,0")
        font = self.lin_filt_edit.font()
        font.setPointSize(16)
        self.lin_filt_edit.setFont(font)

        self.setMouseTracking(True)
        return self.lin_filt_edit
