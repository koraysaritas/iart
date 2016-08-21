# Shoe Tossing
# https://en.wikipedia.org/wiki/Shoe_tossing
import numpy as np
import cv2
from scipy.misc import comb
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LINE_THICKNESS = 1
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_BLACK_WIRE = (33, 33, 33)
COLOR_WHITE_BGR = (255, 255, 255)
BGR_BACK_TOP = (254, 190, 125)
BGR_BACK_BOTTOM = (207, 106, 38)


def create_canvas(h, w, c):
    img = np.zeros((h, w, 3), np.uint8)
    img.fill(c)
    return img


def gen_color(num, colors):
    for f, t in zip(colors[:-1], colors[1:]):
        arr_b = np.linspace(f[0], t[0], num)
        arr_g = np.linspace(f[1], t[1], num)
        arr_r = np.linspace(f[2], t[2], num)
        for b, g, r in zip(arr_b, arr_g, arr_r):
            yield (b, g, r)


def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals


def draw_base(img):
    h_canvas, w_canvas, _ = img.shape

    gen_c = gen_color(h_canvas, [BGR_BACK_TOP, BGR_BACK_BOTTOM])
    for ix in range(h_canvas):
        img[ix, 0:w_canvas] = next(gen_c)


def draw_wire(img):
    h_canvas, w_canvas, _ = img.shape

    w_h_start = random.randint(h_canvas / 3, h_canvas / 2)
    w_h_end = random.randint(w_h_start, w_h_start + 50)
    pt1 = (0, w_h_start)
    pt2 = (w_canvas, w_h_end)

    cv2.line(img, pt1, pt2, COLOR_BLACK_WIRE, 2, lineType=cv2.LINE_AA)


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    draw_base(img)
    draw_wire(img)

    cv2.imshow('shoe_tossing', img)
    cv2.imwrite('shoe_tossing.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
