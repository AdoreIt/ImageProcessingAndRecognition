from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import (
    QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit)

from morphological_operations import *
from StructuralElementEditor import WStructuralElementEditor


def read_image(file_name):
    return QImage(file_name)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        w = QWidget()

        g_layout = QGridLayout()
        # input image layout
        input_image_layout, w_in_image = self.createImageLayout()
        self.w_in_image = w_in_image

        # -- buttons
        select_button = self.createButton("Select", self.selectButton, 60)
        input_image_layout.addWidget(select_button)

        # result image layout
        result_image_layout, w_res_image = self.createImageLayout()
        self.w_res_image = w_res_image

        # -- buttons
        dilation_btn = self.createButton("Dilation", self.selectButton, 60)
        result_image_layout.addWidget(dilation_btn)

        # structural element layout
        structural_element_layout = self.structuralElementLayout()

        # add layouts
        g_layout.addLayout(input_image_layout, 0, 0, 3, 1, Qt.AlignCenter)
        g_layout.addLayout(structural_element_layout, 1, 1)
        g_layout.addLayout(result_image_layout, 0, 2, 3, 1, Qt.AlignCenter)

        # grid_layout.add

        w.setLayout(g_layout)
        self.setCentralWidget(w)

        self.w_in_image.setImage("input.png")
        self.resize(1200, 500)
        self.setWindowTitle("MorphologicalOperations")

    def createButton(self, name, function, max_w=60):
        button = QPushButton(name)
        button.setMaximumWidth(max_w)
        button.clicked.connect(function)
        return button

    def selectButton(self):
        fname = QFileDialog.getOpenFileName(caption='Open image',
                                            filter="Image files (*.jpg *.png)")
        self.w_in_image.setImage(fname[0])

    def structuralElementLayout(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        # width
        label_w = QLabel("width")
        label_w.setMaximumWidth(40)
        h_layout.addWidget(label_w)

        self.width_edit = QLineEdit()
        self.width_edit.setMaximumWidth(50)
        h_layout.addWidget(self.width_edit)

        # height
        label_w = QLabel("height")
        label_w.setMaximumWidth(45)
        h_layout.addWidget(label_w)

        self.height_edit = QLineEdit()
        self.height_edit.setMaximumWidth(50)
        h_layout.addWidget(self.height_edit)

        v_layout.addWidget(WStructuralElementEditor())

        v_layout.addLayout(h_layout)
        return v_layout

    def createStructuralElementLayout(self):
        v_layout = QVBoxLayout()
        w_image = WImage()

    def createImageLayout(self):
        v_layout = QVBoxLayout()
        # v_layout.insertStretch(0)
        w_image = WImage()
        w_image.setMinimumSize(400, 400)
        v_layout.addWidget(w_image)
        # v_layout.insertStretch(1)
        return v_layout, w_image


class WImage(QWidget):
    def __init__(self, parent=None):
        super(WImage, self).__init__(parent)

        self.image = None

    def setImage(self, image_fname):
        self.image = QImage(image_fname, "mono")
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)

        p.fillRect(self.rect(), Qt.lightGray)
        if self.image is not None:
            p.drawImage(0, 0, self.image)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
