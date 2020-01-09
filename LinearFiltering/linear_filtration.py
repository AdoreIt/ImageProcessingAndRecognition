import numpy as np
from math import pi, exp
from enum import Enum

from PyQt5.Qt import qRed, qRgb
from PyQt5.QtGui import QImage


class EFilter(Enum):
    No_change = "No change"
    Blur_box = "Blur box"
    Gaussian_blur = "Gaussian blur"
    Sharpening = "Sharpening"
    Smoothing = "Smoothing"
    Contrast = "Contrast enchantment"
    Cross = "Cross 5x5"
    Prewitt_x = "Prewitt x"
    Prewitt_y = "Prewitt y"
    Prewitt = "Prewitt"
    Sobel_x = "Sobel x"
    Sobel_y = "Sobel y"
    Sobel = "Sobel"
    Roberts_x = "Roberts x"
    Roberts_y = "Roberts y"
    Roberts = "Roberts"
    Laplace = "Laplace"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, EFilter))


def no_change_f():
    return [[[0, 0, 0], [0, 1, 0], [0, 0, 0]]]


def blur_box_f():
    return [[[0.11111, 0.11111, 0.11111], [0.11111, 0.11111, 0.11111],
             [0.11111, 0.11111, 0.11111]]]


def gaussian_blur(sigma, h, w):
    ''' size = tuple(i,j) '''
    filter = list([list(0 for _ in range(int(h))) for _ in range(int(w))])
    for i in range(int(w)):
        for j in range(int(h)):
            x = i - int(w / 2)
            y = j - int(h / 2)
            filter[i][j] = 1 / (2 * pi * sigma**2) * exp(-(
                (x**2 + y**2) / 2 / sigma**2))
    filter = filter / np.sum(filter)
    return [filter]


def sharpening():
    filter = [[-0.88888, -0.88888, -0.88888], [-0.88888, 0.894736, -0.88888],
              [-0.88888, -0.88888, -0.88888]]
    filter = filter / np.sum(filter)
    return [filter]


def smoothing(radius):
    val = 1 / (2 * int(radius) + 1)**2
    filter = [[val, val, val], [val, val, val], [val, val, val]]
    filter = filter / np.sum(filter)
    return [filter]


def contrast(value):
    value = check_value(int(value), 5, 9)
    if value == 5:
        return [[[0, -1, 0], [-1, 5, -1], [0, -1, 0]]]
    if value == 9:
        return [[[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]]


def cross():
    return [[[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1],
             [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]]


def prewitt_x():
    return [[[-1 / 3, 0, 1 / 3], [-1 / 3, 0, 1 / 3], [-1 / 3, 0, 1 / 3]]]


def prewitt_y():
    return [[[-1 / 3, -1 / 3, -1 / 3], [0, 0, 0], [1 / 3, 1 / 3, 1 / 3]]]


def prewitt():
    return prewitt_x() + prewitt_y()


def sobel_x():
    return [[[-1 / 4, 0, 1 / 4], [-1 / 2, 0, -1], [-1 / 4, 0, 1 / 4]]]


def sobel_y():
    return [[[-1 / 4, -1 / 2, -1 / 4], [0, 0, 0], [1 / 4, 1 / 2, 1 / 4]]]


def sobel():
    return sobel_x() + sobel_y()


def roberts_x(size):
    size = check_value(int(size), 2, 3)
    if size == 2:
        return [[[-1, 0], [0, 1]]]
    elif size == 3:
        return [[[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]]


def roberts_y(size):
    size = check_value(int(size), 2, 3)
    if size == 2:
        return [[[0, -1], [1, 0]]]
    elif size == 3:
        return [[[0, -1, -1], [1, 0, -1], [
            1,
            1,
            0,
        ]]]


def roberts(size):
    return roberts_x(size) + roberts_y(size)


def laplace(value):
    if int(value) == 16:
        return [[[0, 0, 1, 0, 0], [0, 1, 2, 1, 0], [1, 2, -16, 2, 1],
                 [0, 1, 2, 1, 0], [0, 0, 1, 0, 0]]]

    value = check_value(int(value), 4, 8)
    if value == 4:
        return [[[0, -1, 0], [-1, 4, -1], [0, -1, 0]]]
    if value == 8:
        return [[[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]]


def check_value(value, v_1, v_2):
    if value != v_1 and value != v_2:
        value = v_1
    return value


def convolve(np_im, filters, img_w, img_h):
    # shape(h,w)
    np_img = np_im.copy()
    filtered_img = np.zeros((img_h, img_w), int)

    for filter in filters:
        if len(filter) == 0:
            continue
        padded_img = np.pad(np_img,
                            pad_width=int((filter.shape[1] - 1) / 2),
                            mode='constant',
                            constant_values=0)
        for h in range(img_h):
            for w in range(img_w):
                filtered_img[h, w] = np.sum(
                    padded_img[h:h + filter.shape[0], w:w + filter.shape[1]] *
                    filter)
        np_img = filtered_img
    return filtered_img


def linear_filter(image, filters):
    np_img = QImageToNp(image)
    filtered_img = convolve(np_img, filters, image.width(), image.height())
    return NpToQImage(filtered_img)


def sum_images(img_1, img_2):
    return NpToQImage(QImageToNp(img_1) + QImageToNp(img_2))


def substract_images(img_1, img_2):
    return NpToQImage(QImageToNp(img_1) - QImageToNp(img_2))


def LaplacianOfGaussian(image, threshold):
    np_img = QImageToNp(image)
    gaussian_filter = [
        np.array([[1 / 16., 1 / 8., 1 / 16.], [1 / 8., 1 / 4., 1 / 8.],
                  [1 / 16., 1 / 8., 1 / 16.]])
    ]
    img = convolve(np_img, gaussian_filter, image.width(), image.height())

    L_x = convolve(img, [np.array(sobel_x()[0])], image.width(),
                   image.height())
    L_y = convolve(img, [np.array(sobel_y()[0])], image.width(),
                   image.height())
    L = pow((L_x * L_x + L_y * L_y), 0.5)
    L = (L > threshold) * L

    temp_img = convolve(img, [np.array(laplace(16)[0])], image.width(),
                        image.height())

    # detect zero crossing by checking values across 8-neighbors on a 3x3 grid
    (M, N) = temp_img.shape
    temp = np.zeros((M + 2, N + 2))
    temp[1:-1, 1:-1] = temp_img
    img = np.zeros((M, N))
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if temp[i, j] < 0:
                for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                             (1, -1), (1, 0), (1, 1)]:
                    if temp[i + x, j + y] > 0:
                        img[i - 1, j - 1] = 1

    LoG = np.array(np.logical_and(img, L))
    LoG = LoG.astype(float) * 255
    return NpToQImage(LoG)


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
            c = max(0, min(arr[y, x], 255))
            img.setPixel(x, y, qRgb(c, c, c))
    return img


def ImpulseNoise(image):
    np_image = QImageToNp(image)
    row, col = np_image.shape
    s_vs_p = 0.5
    amount = 0.04

    # Salt mode
    num_salt = np.ceil(amount * np_image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in np_image.shape]
    np_image[tuple(coords)] = 255

    # Pepper mode
    num_pepper = np.ceil(amount * np_image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in np_image.shape]
    np_image[tuple(coords)] = 0

    return NpToQImage(np_image)


FILTERS_DICT = {
    EFilter.No_change: (no_change_f, []),
    EFilter.Blur_box: (blur_box_f, []),
    EFilter.Gaussian_blur:
    (gaussian_blur, ["sigma", "filter height", "filter width"]),
    EFilter.Sharpening: (sharpening, []),
    EFilter.Smoothing: (smoothing, ["radius"]),
    EFilter.Contrast: (contrast, ["value: 5 or 9"]),
    EFilter.Cross: (cross, []),
    EFilter.Prewitt_x: (prewitt_x, []),
    EFilter.Prewitt_y: (prewitt_y, []),
    EFilter.Prewitt: (prewitt, []),
    EFilter.Sobel_x: (sobel_x, []),
    EFilter.Sobel_y: (sobel_y, []),
    EFilter.Sobel: (sobel, []),
    EFilter.Roberts_x: (roberts_x, ["size: 2 or 3"]),
    EFilter.Roberts_y: (roberts_y, ["size: 2 or 3"]),
    EFilter.Roberts: (roberts, ["size: 2 or 3"]),
    EFilter.Laplace: (laplace, ["value: 4, 8 or 16"]),
}
