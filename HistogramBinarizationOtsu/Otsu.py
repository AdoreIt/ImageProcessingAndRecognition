import numpy as np


class Otsu:
    def __init__(self, histogram):
        self.histogram = histogram

    def pixels_intensity_probabilities(self, histogram):
        probabilities = np.zeros(256)
        for intensity in range(256):
            probabilities[intensity] = histogram[intensity] / \
                sum(histogram)
        return probabilities

    def sum_group_probabilities(self, pixels_intensity_probabilities):
        sum_group_probs = np.zeros(256)
        sum_group_probs[0] = pixels_intensity_probabilities[0]

        for threshold in range(1, 256):
            sum_group_probs[threshold] = sum_group_probs[threshold - 1] + \
                pixels_intensity_probabilities[threshold]

        return sum_group_probs

    def mean_group_values(self, pixels_intensity_probabilities,
                          sum_group_probabilities):
        mu_1, mu_2 = np.zeros(256), np.zeros(256)

        for threshold in range(256):
            for intensity in range(threshold + 1):
                mu_1[threshold] += (intensity *
                                    pixels_intensity_probabilities[intensity]
                                    ) / sum_group_probabilities[threshold]
            for intensity in range(threshold + 1, 256):
                mu_2[threshold] += (
                    intensity * pixels_intensity_probabilities[intensity]) / (
                        1 - sum_group_probabilities[threshold])

        return mu_1, mu_2

    def equivalent_maximization(self, sum_group_probabilities, mu_1, mu_2):
        equivalent_max_values = np.zeros(256)

        for threshold in range(256):
            equivalent_max_values[threshold] = sum_group_probabilities[threshold] * \
                (1 - sum_group_probabilities[threshold]) * \
                ((mu_1[threshold] - mu_2[threshold]) ** 2)

        return equivalent_max_values

    def otsu(self, histogram=None):
        if histogram is not None:
            self.histogram = histogram

        pixels_intensity_probs = self.pixels_intensity_probabilities(
            self.histogram)
        sum_group_probs = self.sum_group_probabilities(pixels_intensity_probs)
        mu_1, mu_2 = self.mean_group_values(pixels_intensity_probs,
                                            sum_group_probs)
        equivalent_max_values = self.equivalent_maximization(
            sum_group_probs, mu_1, mu_2)

        return np.argmax(equivalent_max_values)
