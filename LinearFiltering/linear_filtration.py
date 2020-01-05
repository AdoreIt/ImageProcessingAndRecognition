from PyQt5.Qt import Qt, qRed, qRgb
from PyQt5.QtGui import QImage
import numpy as np


def linear_filter(image, filter):
    # shape(h,w)
    # filtered_img = np.zeros(image.height,image.width)
    padded_img = np.pad(QImageToNp(image),
                        pad_width=int((filter.shape[1] - 1) / 2),
                        mode='constant',
                        constant_values=0)
    filtered_img = np.zeros((image.height(), image.width()), int)
    for h in range(image.height()):
        for w in range(image.width()):
            filtered_img[h, w] = np.sum(
                padded_img[h:h + filter.shape[0], w:w + filter.shape[1]] *
                filter)

    return NpToQImage(filtered_img)


def QImageToNp(img):
    '''  Converts a grascale QImage into np arr'''

    width = img.width()
    height = img.height()

    buf = []
    for y in range(height):
        for x in range(width):
            buf.append(qRed(img.pixel(x, y)))
    arr = np.array(buf).reshape((height, width))
    return arr


def NpToQImage(arr):
    height, width = arr.shape[:2]
    img = QImage(width, height, QImage.Format_Grayscale8)
    for y in range(height):
        for x in range(width):
            c = arr[y, x]
            img.setPixel(x, y, qRgb(c, c, c))
    return img
