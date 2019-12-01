import numpy as np
import argparse
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

from Otsu import Otsu
from ThresholdSelector import ThresholdSelector


def rgb2grayscale(image):
    r_coeff = 0.36
    g_coeff = 0.53
    b_coeff = 0.11

    if len(image.shape) > 2:
        return np.dot(image[..., :3],
                      [r_coeff, g_coeff, b_coeff]).round().astype(int)
    else:
        return image


def histogram(image):
    histogram = np.zeros(256)

    for h_pixel in range(image.shape[0]):
        for w_pixel in range(image.shape[1]):
            histogram[image[h_pixel, w_pixel]] += 1
    return histogram


def binarizate(image, threshold):
    binarized_image = image.copy()

    for h_pixel in range(binarized_image.shape[0]):
        for w_pixel in range(binarized_image.shape[1]):
            if binarized_image[h_pixel, w_pixel] >= threshold:
                binarized_image[h_pixel, w_pixel] = 1
            else:
                binarized_image[h_pixel, w_pixel] = 0

    return binarized_image


def add_image_figure(figure, name, location, image):
    fig_image = figure.add_subplot(location)
    fig_image.set_title(name)
    fig_image.imshow(image, cmap=plt.get_cmap('gray'))
    fig_image.axis('off')
    return fig_image


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description='Histogram creator. Image binarizator')
    argparser.add_argument(
        '-i',
        '--input_image_path',
        type=str,
        help="path to input image",
        default="input_image.jpg")

    args = argparser.parse_args()

    image = mpimg.imread(args.input_image_path)

    gray_image = rgb2grayscale(image)
    im_histogram = histogram(gray_image)
    otsu = Otsu(im_histogram)
    otsu = otsu.otsu()

    matplotlib.rcParams['toolbar'] = 'None'
    figure = plt.figure()
    figure.canvas.set_window_title('Histogram creator. Image binarizator')
    specs = gridspec.GridSpec(ncols=3, nrows=2, figure=figure)

    fig_input_image = add_image_figure(figure, "Original image", specs[0, 0],
                                       gray_image)
    fig_binary_image = add_image_figure(figure, "Binarized image", specs[0, 1],
                                        binarizate(gray_image, 100))
    fig_otsu_image = add_image_figure(figure, "Otsu image", specs[0, 2],
                                      binarizate(gray_image, otsu))

    fig_histogram = figure.add_subplot(specs[1, :])
    fig_histogram.set_title("Histogram")
    fig_histogram.set_xlim([0, 255])
    plt.bar(np.arange(256), im_histogram, color="black")

    otsu_line = plt.axvline(x=otsu, color='red', label="Otsu threshold")
    binary_line = plt.axvline(
        color='deepskyblue', label="Binarization threshold")

    def onclick(event):
        if event.inaxes in [fig_histogram]:
            selected_threshold = int(event.xdata)
            binary_line.set_xdata(selected_threshold)
            fig_binary_image.imshow(
                binarizate(gray_image, selected_threshold),
                plt.get_cmap('gray'))
            plt.draw()

    figure.canvas.mpl_connect('button_press_event', onclick)
    cursor = ThresholdSelector(fig_histogram)
    figure.canvas.mpl_connect('motion_notify_event', cursor.mouse_move)

    plt.legend()
    plt.show()
