from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QComboBox, QSizePolicy)

from morphological_operations import *
from StructuralElementEditor import WStructuralElementEditor


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
        input_image_layout, w_in_image = self.createImageLayout()
        w_in_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        w_in_image.setMinimumSize(200, 200)
        self.w_in_image = w_in_image

        # -- buttons
        select_button = self.createButton("Select", self.selectButton, 60)
        input_image_layout.addWidget(select_button)
        input_image_layout.addStretch(1)

        # result image layout
        result_image_layout, w_res_image = self.createImageLayout()
        w_res_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        w_res_image.setMinimumSize(200, 200)
        self.w_res_image = w_res_image

        # -- Drop Down menu
        c_box = QComboBox()
        c_box.addItems(["Dilation", "Erosion", "Difference", "Border", "Opening", "Closing"])
        c_box.currentTextChanged.connect(self.onMorfOperationChanged)
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

        self.w_in_image.setImage(self.openImage("input_image.jpg"))
        self.resize(1200, 500)
        self.setWindowTitle("MorphologicalOperations")

    def applyOperation(self):
        if self.operation == "Dilation":
            self.w_res_image.setImage(dilation(self.w_in_image.image, self.structural_element))
        elif self.operation == "Erosion":
            self.w_res_image.setImage(erosion(self.w_in_image.image, self.structural_element))
        elif self.operation == "Difference":
            self.w_res_image.setImage(difference(self.w_in_image.image, self.structural_element))
        elif self.operation == "Border":
            self.w_res_image.setImage(border(self.w_in_image.image, self.structural_element))
        elif self.operation == "Opening":
            self.w_res_image.setImage(opening(self.w_in_image.image, self.structural_element))
        elif self.operation == "Closing":
            self.w_res_image.setImage(closing(self.w_in_image.image, self.structural_element))

    def onStructuralElementChanged(self, structural_element):
        self.structural_element = structural_element
        self.applyOperation()

    def onMorfOperationChanged(self, operation):
        self.operation = operation
        self.applyOperation()

    def openImage(self, image_path):
        image = QImage(image_path)
        image.convertTo(QImage.Format_Mono)
        #self.applyOperation()
        return image

    def createButton(self, name, function, max_w=60):
        button = QPushButton(name)
        button.setMaximumWidth(max_w)
        button.clicked.connect(function)
        return button

    def selectButton(self):
        fname = QFileDialog.getOpenFileName(caption='Open image',
                                            filter="Image files (*.jpg *.png)")
        self.w_in_image.setImage(self.openImage(fname[0]))

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

        v_layout.addStretch()
        w_struct_el = WStructuralElementEditor()
        w_struct_el.onStructuralElementChanged.connect(self.onStructuralElementChanged)
        v_layout.addWidget(w_struct_el)
        w_struct_el.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        w_struct_el.setMinimumSize(200, 200)

        v_layout.addLayout(h_layout)
        v_layout.addStretch()
        return v_layout

    def createStructuralElementLayout(self):
        v_layout = QVBoxLayout()
        w_image = WImage()

    def createImageLayout(self):
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        w_image = WImage()
        v_layout.addWidget(w_image, 5)
        return v_layout, w_image

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q:
            self.close()
        elif e.key() == Qt.Key_Space:
            self.w.clear()


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
            pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
            p.drawPixmap(self.rect().center() - pixmap.rect().center(), pixmap)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
