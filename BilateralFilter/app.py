from io import StringIO
import csv
import numpy

from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPainter, QPixmap, QIntValidator
from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout,
                             QApplication, QWidget, QPushButton, QFileDialog,
                             QLineEdit, QPlainTextEdit, QComboBox, QSizePolicy,
                             QDialog, QLabel, QSlider)

from bilateral_filter import *


def read_image(file_name):
    return QImage(file_name)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filter = None

        self.setMinimumSize(1000, 500)

        w = QWidget()

        h_box_layout = QVBoxLayout()
        h_box_layout.setContentsMargins(15, 15, 15, 15)

        self.w_image = WImage()
        h_box_layout.addWidget(self.w_image)

        inputs_layout = QHBoxLayout()

        select_button = QPushButton("Select")
        select_button.setMaximumWidth(50)
        select_button.clicked.connect(self.__onSelect)
        inputs_layout.addWidget(select_button)

        w_label = QLabel("w")
        font = w_label.font()
        font.setPointSize(16)
        w_label.setFont(font)
        inputs_layout.addWidget(w_label)

        self.width_edit = QLineEdit("3")
        self.width_edit.setMinimumWidth(50)
        self.width_edit.textEdited.connect(self.__update)
        self.width_edit.setValidator(QIntValidator())
        inputs_layout.addWidget(self.width_edit, 1)

        h_label = QLabel("h")
        font = h_label.font()
        font.setPointSize(16)
        h_label.setFont(font)
        inputs_layout.addWidget(h_label)

        self.height_edit = QLineEdit("3")
        self.height_edit.setMinimumWidth(50)
        self.height_edit.textEdited.connect(self.__update)
        self.height_edit.setValidator(QIntValidator())
        inputs_layout.addWidget(self.height_edit, 1)

        inputs_layout.addStretch(20)

        h_box_layout.addLayout(inputs_layout)

        sigma_layout = QHBoxLayout()

        sigma_label = QLabel("σ")
        font = sigma_label.font()
        font.setPointSize(16)
        sigma_label.setFont(font)
        sigma_layout.addWidget(sigma_label)

        self.sigma_slider = QSlider(Qt.Horizontal)
        self.sigma_slider.setRange(0, 100)
        self.sigma_slider.setTickInterval(5)
        self.sigma_slider.setTickPosition(QSlider.TicksBelow)
        self.sigma_slider.valueChanged.connect(self.__update)
        sigma_layout.addWidget(self.sigma_slider, 20)

        h_box_layout.addLayout(sigma_layout)

        threshold_layout = QHBoxLayout()

        threshold_label = QLabel("threshold")
        font = threshold_label.font()
        font.setPointSize(16)
        threshold_label.setFont(font)
        threshold_layout.addWidget(threshold_label)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setTickInterval(5)
        self.threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.threshold_slider.valueChanged.connect(self.__update)
        threshold_layout.addWidget(self.threshold_slider, 20)

        h_box_layout.addLayout(threshold_layout)


        w.setLayout(h_box_layout)
        self.setCentralWidget(w)


    def __onSelect(self):
        fname = QFileDialog.getOpenFileName(caption='Open image',
                                            filter="Image files (*.jpg *.png)")
        if fname[0]:
            self.original_image = self.__openImage(fname[0])
            self.w_image.setImage(self.original_image)
            self.filter = BilateralFilter(self.original_image)


    def __update(self):
        if self.filter:
            if not self.width_edit.text() or not self.height_edit.text():
                return
            sigma = self.sigma_slider.value()
            width = int(self.width_edit.text())
            height = int(self.height_edit.text())
            threshold = self.threshold_slider.value()
            self.w_image.setImage(self.filter.apply(sigma, height, width, threshold))


    def __openImage(self, image_path):
        image = QImage(image_path)
        image.convertTo(QImage.Format_Grayscale8)
        return image


class WImage(QWidget):
    def __init__(self, parent=None):
        super(WImage, self).__init__(parent)

        self.image = None

    def setImage(self, image):
        self.image = image
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.lightGray)

        if self.image is not None:
            pixmap = QPixmap.fromImage(self.image)
            pixmap = pixmap.scaled(self.width(), self.height(),
                                   Qt.KeepAspectRatio)
            p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
