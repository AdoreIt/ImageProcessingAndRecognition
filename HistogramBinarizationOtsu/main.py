import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import time


def rgb2grayscale(image):
    r_coeff = 0.36
    g_coeff = 0.53
    b_coeff = 0.11

    if len(image.shape) > 2:
        return np.dot(image[..., :3], [r_coeff, g_coeff, b_coeff]).round().astype(int)
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


def otsu(histogram):
    def pixels_intensity_probabilities(histogram):
        probabilities = np.zeros(256)
        for intensity in range(256):
            probabilities[intensity] = histogram[intensity] / \
                sum(histogram)
        return probabilities

    def sum_group_probabilities(pixels_intensity_probabilities):
        sum_group_probs = np.zeros(256)
        sum_group_probs[0] = pixels_intensity_probabilities[0]

        for threshold in range(1, 256):
            sum_group_probs[threshold] = sum_group_probs[threshold - 1] + \
                pixels_intensity_probabilities[threshold]

        return sum_group_probs

    def mean_group_values(pixels_intensity_probabilities, sum_group_probabilities):
        mu_1, mu_2 = np.zeros(256), np.zeros(256)

        for threshold in range(256):
            for intensity in range(threshold + 1):
                mu_1[threshold] += (intensity * pixels_intensity_probabilities[intensity]
                                    ) / sum_group_probabilities[threshold]
            for intensity in range(threshold + 1, 256):
                mu_2[threshold] += (intensity * pixels_intensity_probabilities[intensity]
                                    ) / (1 - sum_group_probabilities[threshold])

        return mu_1, mu_2

    def equivalent_maximization(sum_group_probabilities, mu_1, mu_2):
        equivalent_max_values = np.zeros(256)

        for threshold in range(256):
            equivalent_max_values[threshold] = sum_group_probabilities[threshold] * \
                (1 - sum_group_probabilities[threshold]) * \
                ((mu_1[threshold] - mu_2[threshold]) ** 2)

        return equivalent_max_values

    pixels_intensity_probs = pixels_intensity_probabilities(histogram)
    sum_group_probs = sum_group_probabilities(
        pixels_intensity_probs)
    mu_1, mu_2 = mean_group_values(
        pixels_intensity_probs, sum_group_probs)
    equivalent_max_values = equivalent_maximization(
        sum_group_probs, mu_1, mu_2)

    return np.argmax(equivalent_max_values)


def add_image_figure(figure, name, location, image):
    fig_image = figure.add_subplot(location)
    fig_image.set_title(name)
    fig_image.imshow(image, cmap=plt.get_cmap('gray'))
    fig_image.axis('off')
    return fig_image


class ThresholdSelector(object):
    def __init__(self, ax):
        self.ax = ax
        self.select_line = ax.axvline(color='lightskyblue')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.95, 0.9, '', transform=ax.transAxes)
        self.ani = animation.FuncAnimation(
            self.ax.figure, self.update_lines, interval=50)
        self.x = 0

    def mouse_move(self, event):
        if not event.inaxes:
            return
        self.x = int(event.xdata)

    def update_lines(self, i):
        self.select_line.set_xdata(self.x)
        self.txt.set_text('{}'.format(self.x))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description='Histogram creator')
    argparser.add_argument(
        '-i', '--input_image_path',
        type=str,
        help="path to input image",
        default="input_image.jpg")

    args = argparser.parse_args()

    image = mpimg.imread(args.input_image_path)
    gray_image = rgb2grayscale(image)
    im_histogram = histogram(gray_image)
    otsu = otsu(im_histogram)

    figure = plt.figure(constrained_layout=True)
    specs = gridspec.GridSpec(ncols=3, nrows=2, figure=figure)

    fig_input_image = add_image_figure(
        figure, "Original image", specs[0, 0], gray_image)
    fig_binary_image = add_image_figure(figure, "Binarized image", specs[
        0, 1], binarizate(gray_image, 100))
    fig_otsu_image = add_image_figure(figure, "Otsu image", specs[
        0, 2], binarizate(gray_image, otsu))

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
            print(selected_threshold)
            binary_line.set_xdata(selected_threshold)
            fig_binary_image.imshow(binarizate(
                gray_image, selected_threshold), plt.get_cmap('gray'))
            print(event.xdata, event.ydata)
            plt.draw()

    figure.canvas.mpl_connect('button_press_event', onclick)
    cursor = ThresholdSelector(fig_histogram)
    figure.canvas.mpl_connect('motion_notify_event', cursor.mouse_move)

    plt.legend()
    plt.show()
