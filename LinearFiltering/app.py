from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPainter, QPixmap, QIntValidator
from PyQt5.QtWidgets import (
    QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QPlainTextEdit, QComboBox, QSizePolicy)

from io import StringIO
import csv
import numpy

# from morphological_operations import *
from LinearFilter import *

def read_image(file_name):
    return QImage(file_name)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setMinimumSize(1000, 500)

        w = QWidget()

        g_layout = QHBoxLayout()
        g_layout.setContentsMargins(50, 0, 50, 0)
        # input image layout
        input_image_layout, w_in_image = self.__createImageLayout()
        w_in_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        w_in_image.setMinimumSize(200, 200)
        self.w_in_image = w_in_image

        # -- buttons
        select_button = self.__createButton("Select", self.__selectButton, 60)
        input_image_layout.addWidget(select_button)
        input_image_layout.addStretch(1)

        # result image layout
        result_image_layout, w_res_image = self.__createImageLayout()
        w_res_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        w_res_image.setMinimumSize(200, 200)
        self.w_res_image = w_res_image

        # -- Drop Down menu
        c_box = QComboBox()
        c_box.addItems(
            ["Dilation", "Erosion", "Border", "Opening", "Closure"])
        # c_box.activated[str].connect(self.onMorfOperationChanged)
        self.operation = "Dilation"
        result_image_layout.addWidget(c_box)
        result_image_layout.addStretch(1)

        # structural element layout
        structural_element_layout = self.structuralElementLayout()

        # add layouts
        g_layout.addLayout(input_image_layout, 2)
        g_layout.addLayout(structural_element_layout, 1)
        g_layout.addLayout(result_image_layout, 2)

        # grid_layout.add

        w.setLayout(g_layout)
        self.setCentralWidget(w)

        self.w_in_image.setImage(self.__openImage("input_image.jpg"))
        self.resize(1200, 500)
        self.setWindowTitle("LinearFiltration")

        # self.truct_el.clear()

    def __createButton(self, name, function, max_w=60):
        button = QPushButton(name)
        button.setMaximumWidth(max_w)
        button.clicked.connect(function)
        return button

    def __selectButton(self):
        fname = QFileDialog.getOpenFileName(caption='Open image',
                                            filter="Image files (*.jpg *.png)")
        if fname[0]:
            self.w_in_image.setImage(self.__openImage(fname[0]))

    def __createImageLayout(self):
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        w_image = WImage()
        v_layout.addWidget(w_image, 5)
        return v_layout, w_image

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def structuralElementLayout(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        # width
        label_w = QLabel("width")
        label_w.setMaximumWidth(40)
        h_layout.addWidget(label_w)

        self.width_edit = QLineEdit(str(0))
        self.width_edit.setValidator(QIntValidator(1, 99))
        # self.width_edit.returnPressed.connect(self.structuralElementSetSize)
        self.width_edit.setMaximumWidth(50)
        h_layout.addWidget(self.width_edit)

        # height
        label_w = QLabel("height")
        label_w.setMaximumWidth(45)
        h_layout.addWidget(label_w)

        self.height_edit = QLineEdit(str(0))
        self.height_edit.setValidator(QIntValidator(1, 99))
        # self.height_edit.returnPressed.connect(self.structuralElementSetSize)
        self.height_edit.setMaximumWidth(50)
        h_layout.addWidget(self.height_edit)

        v_layout.addStretch()
        self.lin_filt_edit = QPlainTextEdit("0,0,0\r\n0,0,0\r\n0,0,0")
        font = self.lin_filt_edit.font()
        font.setPointSize(16)
        self.lin_filt_edit.setFont(font)
        # self.lin_filt_edit.onStructuralElementChanged.connect(
        #     self.onStructuralElementChanged)
        v_layout.addWidget(self.lin_filt_edit)
        self.lin_filt_edit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lin_filt_edit.setMinimumSize(200, 200)

        h_btns_layout = QHBoxLayout()
        self.c_se_box = QComboBox()
        self.c_se_box.addItems(["Select preset", "Filled",
                                "Square", "Circle", "Triangle"])
        # self.c_se_box.activated[str].connect(self.applyPreset)
        self.apply_filt_btn = self.__createButton(
                "Apply", self.__onApplyFilterBtn, 60)
        h_btns_layout.addWidget(self.c_se_box)
        h_btns_layout.addWidget(self.apply_filt_btn)

        v_layout.addLayout(h_layout)
        v_layout.addLayout(h_btns_layout)
        v_layout.addStretch()
        return v_layout

    def __openImage(self, image_path):
        image = QImage(image_path)
        image.convertTo(QImage.Format_Grayscale8)
        # print(len(image))
        return image

    def __onApplyFilterBtn(self):
        mat_str = self.lin_filt_edit.text()
        f = StringIO(mat_str)
        reader = csv.reader(f, delimiter=",")
        x = list(reader)
        result = numpy.array(x).astype("float")
        print(result)

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
            pixmap = pixmap.scaled(
                self.width(), self.height(), Qt.KeepAspectRatio)
            p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
