from PyQt5.Qt import qRgb
from PyQt5.QtGui import QImage

BLACK = qRgb(0, 0, 0) # 0
WHITE = qRgb(255, 255, 255) # 1


def getImagePosition(im_x, im_y, structural_element, x_shift, y_shift):
    x = im_x - structural_element.anchor.x + x_shift
    y = im_y - structural_element.anchor.y + y_shift
    return x, y


def isSame(image, im_x, im_y, structural_element):
    for w in range(structural_element.width):
        for h in range(structural_element.height):
            x, y = getImagePosition(im_x, im_y, structural_element, w, h)
            if image.pixel(x, y) != structural_element.pixel(w, h):
                return False

    return True


def dilate(image, im_x, im_y, structural_element, out_image):
    """
    image: QImage
    structural_element: StructuralElement
    out_image (copy of image): QImage
    """
    for w in range(structural_element.width):
        for h in range(structural_element.height):
            if structural_element.pixel(w, h) == BLACK:
                x, y = getImagePosition(im_x, im_y, structural_element, w, h)
                out_image.setPixel(x, y, 1)


def dilation(image, structural_element):
    """
    image: QImage
    structural_element: QImage
    """
    image_dilation = image.copy()
    for w in range(image.size().width()):
        for h in range(image.size().height()):
            if image.pixel(w, h) == BLACK:
                dilate(image, w, h, structural_element, image_dilation)

    return image_dilation


def erosion(image, structural_element):
    """
    image: QImage
    structural_element: QImage
    """
    image_erosion = image.copy()
    for w in range(image.size().width()):
        for h in range(image.size().height()):
            if not isSame(image, w, h, structural_element):
                image_erosion.setPixel(w, h, 1)

    return image_erosion


def difference(image_l, image_r):
    """ """
    image_difference = QImage(image_l.size(), QImage.Format_Mono)
    for w in range(image_l.size().width()):
        for h in range(image_l.size().height()):
            if image_l.pixel(w, h) == BLACK and image_r.pixel(w, h) == WHITE:
                image_difference.setPixel(w, h, 0)
            else:
                image_difference.setPixel(w, h, 1)
    return image_difference


def border(image, structural_element):
    image_erosion = erosion(image, structural_element)
    return difference(image, image_erosion)


def closing(image, structural_element):
    return erosion(dilation(image, structural_element), structural_element)


def opening(image, structural_element):
    return dilation(erosion(image, structural_element), structural_element)
