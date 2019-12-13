from PyQt5.Qt import qRgb
from PyQt5.QtGui import QImage

BLACK = qRgb(0, 0, 0)  # 0
WHITE = qRgb(255, 255, 255)  # 1


def __setPixel(image, x, y, color):
    if x >= 0 and x < image.width() and y >= 0 and y < image.height():
        image.setPixel(x, y, color)


def __getPixel(image, x, y):
    if x >= 0 and x < image.width() and y >= 0 and y < image.height():
        return image.pixel(x, y)
    return BLACK


def getImagePosition(im_x, im_y, structural_element, x_shift, y_shift):
    x = im_x - structural_element.anchor.x() + x_shift
    y = im_y - structural_element.anchor.y() + y_shift
    return x, y


def isSame(image, im_x, im_y, structural_element):
    for w in range(structural_element.width()):
        for h in range(structural_element.height()):
            x, y = getImagePosition(im_x, im_y, structural_element, w, h)
            if __getPixel(image, x, y) != __getPixel(structural_element, w, h):
                return False

    return True


def dilate(image, im_x, im_y, structural_element, out_image):
    """
    image: QImage
    structural_element: StructuralElement
    out_image (copy of image): QImage
    """
    for w in range(structural_element.width()):
        for h in range(structural_element.height()):
            if __getPixel(structural_element, w, h) == BLACK:
                x, y = getImagePosition(im_x, im_y, structural_element, w, h)
                __setPixel(out_image, x, y, 1)


def dilation(image, structural_element):
    """
    image: QImage
    structural_element: QImage
    """
    image_dilation = image.copy()
    for w in range(image.width()):
        for h in range(image.height()):
            if __getPixel(image, w, h) == BLACK:
                dilate(image, w, h, structural_element, image_dilation)

    return image_dilation


def erosion(image, structural_element):
    """
    image: QImage
    structural_element: QImage
    """
    image_erosion = image.copy()
    for w in range(image.width()):
        for h in range(image.height()):
            if not isSame(image, w, h, structural_element):
                __setPixel(image_erosion, w, h, 0)

    return image_erosion


def __difference(image_l, image_r):
    """ """
    image_difference = QImage(image_l.size(), QImage.Format_Mono)
    for w in range(image_l.width()):
        for h in range(image_l.height()):
            if __getPixel(image_l, w, h) == BLACK and __getPixel(image_r, w, h) == WHITE:
                __setPixel(image_difference, w, h, 0)
            else:
                __setPixel(image_difference, w, h, 1)
    return image_difference


def border(image, structural_element):
    image_erosion = erosion(image, structural_element)
    return __difference(image, image_erosion)


def closure(image, structural_element):
    return erosion(dilation(image, structural_element), structural_element)


def opening(image, structural_element):
    return dilation(erosion(image, structural_element), structural_element)
