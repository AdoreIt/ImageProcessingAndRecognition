from io import StringIO
import csv
import numpy

from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPainter, QPixmap, QIntValidator
from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout,
                             QApplication, QWidget, QPushButton, QFileDialog,
                             QLineEdit, QPlainTextEdit, QComboBox, QSizePolicy,
                             QDialog)

from linear_filtration import *


def read_image(file_name):
    return QImage(file_name)


class FunctionParamsDialog(QDialog):
    def __init__(self, parent=None):
        super(FunctionParamsDialog, self).__init__(parent)
        self.everything_is_fine = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Q:
            self.everything_is_fine = True
            self.close()


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

        result_image_layout.addStretch(1)

        # structural element layout
        structural_element_layout = self.filterLayout()

        # add layouts
        g_layout.addLayout(input_image_layout, 2)
        g_layout.addLayout(structural_element_layout, 1)
        g_layout.addLayout(result_image_layout, 2)

        # Add layouts to CentralWidget
        w.setLayout(g_layout)
        self.setCentralWidget(w)

        self.__setInputImage("Images/input_image.jpg")
        self.resize(1200, 500)
        self.setWindowTitle("LinearFiltering")

    def __createParamsEdits(self, names):
        dialog = FunctionParamsDialog()
        d_h_l = QHBoxLayout()

        line_edits = []

        for name in names:
            l_e = QLineEdit()
            l_e.setPlaceholderText(name)
            l_e.setValidator(QIntValidator())
            d_h_l.addWidget(l_e)
            line_edits.append(l_e)

        dialog.setLayout(d_h_l)
        dialog.exec()
        if dialog.everything_is_fine:
            return [float(line.text()) for line in line_edits]
        else:
            return None

    def __onFilterSelected(self, filter):
        filter_info = FILTERS_DICT[EFilter(filter)]
        args = []
        if filter_info[1]:
            args = self.__createParamsEdits(filter_info[1])
        if args or not filter_info[1]:
            self.lin_filt_edit.appendPlainText(
                self.__filters_arr_to_string(filter_info[0](*args)))

    def __filters_arr_to_string(self, filters_arr):
        filters_str = ""
        for filter in filters_arr:
            for row in filter:
                filters_str += ','.join(map(str, row)) + '\r\n'
            filters_str += ';\r\n'

        return filters_str

    def __createButton(self, name, function, max_w=60):
        button = QPushButton(name)
        button.setMaximumWidth(max_w)
        button.clicked.connect(function)
        return button

    def __selectButton(self):
        fname = QFileDialog.getOpenFileName(caption='Open image',
                                            filter="Image files (*.jpg *.png)")
        if fname[0]:
            self.__setInputImage(fname[0])

    def __sumImagesButton(self):
        self.w_res_image.setImage(sum_images(self.w_in_image.image,
                                             self.w_res_image.image))

    def __substractImagesButton(self):
        self.w_res_image.setImage(
            substract_images(self.w_in_image.image, self.w_res_image.image))

    def __setInputImage(self, image_path):
        img = self.__openImage(image_path)
        self.w_in_image.setImage(img)

    def __createImageLayout(self):
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        w_image = WImage()
        v_layout.addWidget(w_image, 5)
        return v_layout, w_image

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q:
            self.close()

    def filterLayout(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        v_layout.addStretch()
        self.lin_filt_edit = QPlainTextEdit()
        font = self.lin_filt_edit.font()
        font.setPointSize(12)
        self.lin_filt_edit.setFont(font)
        v_layout.addWidget(self.lin_filt_edit)

        self.lin_filt_edit.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding)
        self.lin_filt_edit.setMinimumSize(200, 200)

        h_btns_layout = QHBoxLayout()
        self.c_se_box = QComboBox()
        self.c_se_box.addItems(EFilter.list())
        self.c_se_box.activated[str].connect(self.__onFilterSelected)
        self.apply_filt_btn = self.__createButton("Apply",
                                                  self.__onApplyFilterBtn, 60)
        h_btns_layout.addWidget(self.c_se_box)
        h_btns_layout.addWidget(self.apply_filt_btn)

        h_op_btns_layout = QHBoxLayout()
        self.sum_btn = self.__createButton("Sum images",
                                           self.__sumImagesButton, 120)
        h_op_btns_layout.addWidget(self.sum_btn)
        self.subtract_btn = self.__createButton("Subtract images",
                                                self.__substractImagesButton,
                                                120)
        h_op_btns_layout.addWidget(self.subtract_btn)

        v_layout.addLayout(h_layout)
        v_layout.addLayout(h_btns_layout)
        v_layout.addLayout(h_op_btns_layout)
        v_layout.addStretch()
        return v_layout

    def __openImage(self, image_path):
        image = QImage(image_path)
        image.convertTo(QImage.Format_Grayscale8)
        return image

    def __onApplyFilterBtn(self):
        filter_str_list = self.lin_filt_edit.toPlainText().split(';')

        self.w_res_image.setImage(
            linear_filter(self.w_in_image.image,
                          self.__QStringToNp(filter_str_list)))

    def __QStringToNp(self, array_of_qstrings):
        filters = []
        for array in array_of_qstrings:
            f = StringIO(array)
            reader = csv.reader(f, delimiter=",")
            x = list(filter(bool, reader))
            filters.append(numpy.array(x).astype("float"))
        return filters


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
