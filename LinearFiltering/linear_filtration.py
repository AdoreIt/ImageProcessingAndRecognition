import numpy as np
from math import pi, exp
from enum import Enum

from PyQt5.Qt import Qt, qRed, qRgb
from PyQt5.QtGui import QImage


class EFilter(Enum):
    No_change = "No change"
    Blur_box = "Blur box"
    Gaussian_blur = "Gaussian blur"
    Sharpening = "Sharpening"
    Smoothing = "Smoothing"
    Roberts_x = "Roberts x"
    Roberts_y = "Roberts y"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, EFilter))


def no_change_f():
    return '0,0,0\r\n0,1,0\r\n0,0,0'


def blur_box_f():
    return '0.11111,0.11111,0.11111\r\n0.11111,0.11111,0.11111\r\n0.11111,0.11111,0.11111'


def gaussian_blur(sigma, h, w):
    ''' size = tuple(i,j) '''
    filter = list([list(0 for _ in range(int(h))) for _ in range(int(w))])
    for i in range(int(w)):
        for j in range(int(h)):
            filter[i][j] = 1 / (2 * pi * sigma**2) * exp(-(
                (i**2 + j**2) / 2 / sigma**2))
    return filter_arr_to_string(filter)


def sharpening():
    return '-0.88888,-0.88888,-0.88888\r\n-0.88888,1.88888,-0.88888\r\n-0.88888,-0.88888,-0.88888'


def smoothing(radius):
    value = 1 / (2 * int(radius) + 1)**2
    return '{st},{st},{st}\r\n{st},{st},{st}\r\n{st},{st},{st}'.format(
        st=str(value))


def roberts_x(size):
    size = int(size)
    if size == 2:
        return filter_arr_to_string([[-1, 0], [0, 1]])
    elif size == 3:
        return filter_arr_to_string([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])


def roberts_y(size):
    size = int(size)
    if size == 2:
        return filter_arr_to_string([[0, -1], [1, 0]])
    elif size == 3:
        return filter_arr_to_string([[0, -1, -1], [1, 0, -1], [
            1,
            1,
            0,
        ]])


def filter_arr_to_string(filter_arr):
    filter_str = ""
    print(filter_arr)
    for row in filter_arr:
        filter_str += ','.join(map(str, row)) + '\r\n'

    return filter_str


FILTERS_DICT = {
    EFilter.No_change: (no_change_f, []),
    EFilter.Blur_box: (blur_box_f, []),
    EFilter.Gaussian_blur:
    (gaussian_blur, ["sigma", "filter height", "filter width"]),
    EFilter.Sharpening: (sharpening, []),
    EFilter.Smoothing: (smoothing, ["radius"]),
    EFilter.Roberts_x: (roberts_x, ["size: 2 or 3"]),
    EFilter.Roberts_y: (roberts_y, ["size: 2 or 3"])
}


def linear_filter(image, filters):
    # shape(h,w)
    # filtered_img = np.zeros(image.height,image.width)
    np_img = QImageToNp(image)
    filtered_img = np.zeros((image.height(), image.width()), int)

    for filter in filters:
        padded_img = np.pad(np_img,
                            pad_width=int((filter.shape[1] - 1) / 2),
                            mode='constant',
                            constant_values=0)
        for h in range(image.height()):
            for w in range(image.width()):
                filtered_img[h, w] = np.sum(
                    padded_img[h:h + filter.shape[0], w:w + filter.shape[1]] *
                    filter)
        np_img = filtered_img

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
