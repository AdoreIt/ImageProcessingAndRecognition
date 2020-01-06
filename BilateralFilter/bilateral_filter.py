import numpy as np
from math import pi, exp

from PyQt5.Qt import qRed, qRgb
from PyQt5.QtGui import QImage


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


class BilateralFilter:
    def __init__(self, image):
        self.image = QImageToNp(image)

    def apply(self, sigma, height, width, threshold):
        filter = self.gaussian_distribution(sigma, height, width)
        image = self.bilateral_filtering(filter, threshold)
        return NpToQImage(image)

    def gaussian_distribution(self, sigma, h, w):
        filter = list([list(0 for _ in range(int(h))) for _ in range(int(w))])
        for i in range(int(w)):
            for j in range(int(h)):
                x = i - int(w / 2)
                y = j - int(h / 2)
                filter[i][j] = 1 / (2 * pi * sigma**2) * exp(-(
                    (x**2 + y**2) / 2 / sigma**2))
        return filter

    def bilateral_filtering(self, filter, threshold):
        filtered_img = self.image.copy()

        padded_img = np.pad(self.image,
                            pad_width=int((filter.shape[1] - 1) / 2),
                            mode='constant',
                            constant_values=0)

        for h in range(self.image.height()):
            for w in range(self.image.width()):
                image_region = padded_img[h:h + filter.shape[0],
                                          w:w + filter.shape[1]]

                changed_filter = self.change_filter(image_region, filter,
                                                    threshold)

                filtered_img[h, w] = np.sum(
                    image_region[h:h + filter.shape[0],
                                 w:w + filter.shape[1]] * changed_filter)

        return filtered_img

    def change_filter(self, image_region, filter, threshold):
        changed_filter = filter.copy()
        f_centr = filter[(filter.size[0] - 1) / 2, (filter.size[1] - 1) / 2]

        for h in range(image_region.size[0]):
            for w in range(image_region.size[1]):
                if abs(image_region[h, w], f_centr) >= threshold:
                    changed_filter[h, w] = 0

        return changed_filter / np.sum(changed_filter)
