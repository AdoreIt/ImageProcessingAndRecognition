import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
# import matplotlib.gridspec as gridspec

# 1. create circle
# 2. noise it
# 3. show it

# def create_circle(r, x0, y0):


def create_circle(center=None, radius=None):
    '''
    theta is a parametric value in range 0 to 2π, interpreted geometrically as
    the angle that the ray from (a, b) to (x, y) makes with the positive x-axis
    '''
    theta = np.linspace(0, 2 * np.pi, 100)

    if radius is None:
        radius = np.random.rand() + 0.5

    xc = np.random.rand() if center is None else center[0]
    yc = np.random.rand() if center is None else center[1]

    # print("({0}, {1}) = {2}".format(xc, yc, radius))

    x = xc + radius * np.cos(theta)
    y = yc + radius * np.sin(theta)

    return x, y, theta


def add_noise(theta, x, y, variance=0.02, mean=0, sigma=None):
    if sigma is None:
        sigma = variance**0.5
    n_x = x + sigma * np.random.randn(len(theta)) + mean
    n_y = y + sigma * np.random.randn(len(theta)) + mean
    return n_x, n_y


def get_points_from_set(x, y):
    indices = np.random.randint(0, len(x), 3)
    points = [(x[index], y[index]) for index in indices]
    return points  # [(x1, y1), (x2, y2), (x3, y3)]


def get_centre_radius(three_points):
    p1 = three_points[0]
    p2 = three_points[1]
    p3 = three_points[2]

    if p3 == p2 or p3 == p1 or p1 == p2:
        return None, None
    # print(p1)
    # print(p2)
    # print(p3)
    A = np.array([[1, ((p1[1] - p2[1]) / (p1[0] - p2[0]))],
                  [(p1[0] - p3[0]) / (p1[1] - p3[1]), 1]])
    # print(A)
    A_inv = np.linalg.inv(A)
    B = np.array([
        ((p1[0]**2 - p2[0]**2 + p1[1]**2 - p2[1]**2) / 2 / (p1[0] - p2[0])),
        ((p1[1]**2 - p3[1]**2 + p1[0]**2 - p3[0]**2) / 2 / (p1[1] - p3[1]))
    ])

    center_point = np.dot(A_inv, B)
    # print(center_point)
    radius = math.sqrt((p1[0] - center_point[0])**2 +
                       (p1[1] - center_point[1])**2)
    # print(radius)
    return center_point, radius


def distance_to_circle(point, center, radius):
    p_x, p_y, c_x, c_y = point[0], point[1], center[0], center[1]

    return abs(math.sqrt((p_x - c_x)**2 + (p_y - c_y)**2) - radius)


def RANSAC_cirle_iteration(x, y, threshold=0.5):
    inliners = 0
    three_points = get_points_from_set(x, y)
    center, radius = get_centre_radius(three_points)
    if center is None:
        return None

    for point in zip(x, y):
        # print(point)
        if distance_to_circle(point, center, radius) < threshold:
            inliners += 1

    return (inliners, center, radius)


def RANSAC(x_set, y_set, iterations=1000):
    best_circle = (0, 0, 0)
    for _ in range(iterations):
        circle = RANSAC_cirle_iteration(x_set, y_set)
        if circle is None:
            continue
        if circle[0] > best_circle[0]:
            best_circle = circle
    return best_circle[1], best_circle[2]  # center, radius


if __name__ == "__main__":
    original_x, original_y, theta = create_circle()
    noised_x, noised_y = add_noise(theta, original_x, original_y)
    # points = get_points_from_set(x, y)
    # print(points)
    # RANSAC_cirle_iteration(x, y)
    # get_centre_radius(points)

    estimated_cirle = RANSAC(noised_x, noised_y)
    estimated_x, estimated_y, _ = create_circle(tuple(estimated_cirle[0]),
                                                estimated_cirle[1])

    mpl.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(1)
    fig.canvas.set_window_title("RANSAC circle estimator")

    # ax.plot(original_x, original_y, color="lime", alpha=.8)
    ax.plot(noised_x, noised_y, 'o', color="red")
    ax.plot(estimated_x, estimated_y, color="blue")
    ax.set_aspect(1)

    # plt.title("RANSAC")

    # plt.xlim(-1.25, 1.25)
    # plt.ylim(-1.25, 1.25)

    plt.grid(linestyle='--')
    # plt.legend()
    plt.show()
