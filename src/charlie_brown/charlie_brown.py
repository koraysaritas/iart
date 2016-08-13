# Charlie Brown
import numpy as np
import cv2
import random

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_BASE_BGR = (59, 230, 251)


def create_canvas(h, w, c):
    img = np.zeros((h, w, 3), np.uint8)
    img.fill(c)
    return img


def roi_fill_color(img, roi, color):
    if roi:
        img[int(roi[0][0]):int(roi[1][0]), int(roi[0][1]):int(roi[1][1])] = color


def fill_base(img):
    h_canvas, w_canvas, _ = img.shape
    roi = ((0, 0), (h_canvas, w_canvas))
    roi_fill_color(img, roi, COLOR_BASE_BGR)


def draw_zigzag(img):
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.tril_indices.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.fliplr.html#numpy.fliplr
    pass


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    fill_base(img)
    draw_zigzag(img)

    cv2.imshow('charlie_brown', img)
    cv2.imwrite('charlie_brown.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
