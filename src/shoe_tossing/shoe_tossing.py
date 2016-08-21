# Shoe Tossing
# https://en.wikipedia.org/wiki/Shoe_tossing
import numpy as np
import cv2
import math

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LINE_THICKNESS = 1
COLOR_BLACK_BGR = (0, 0, 0)
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


def draw_base(img):
    h_canvas, w_canvas, _ = img.shape

    gen_c = gen_color(h_canvas, [BGR_BACK_TOP, BGR_BACK_BOTTOM])
    for ix in range(h_canvas):
        img[ix, 0:w_canvas] = next(gen_c)


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    draw_base(img)

    cv2.imshow('shoe_tossing', img)
    cv2.imwrite('shoe_tossing.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
