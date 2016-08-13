# Charlie Brown
import numpy as np
import cv2
import random

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
ZIGZAG_HEIGHT = int(CANVAS_HEIGHT / 4)
ZIGZAG_WIDTH = ZIGZAG_HEIGHT
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


def _fill_z_base(img, z_h_start, z_w_start, z_height, z_width):
    z_part = img[z_h_start:z_h_start + z_height, z_w_start:z_w_start + z_width]
    roi = np.tril_indices(z_height)
    z_part[roi] = COLOR_BLACK_BGR
    return img, z_part


def _draw_even_tril_up(img, z_h_start, z_w_start, z_height, z_width):
    img, z_part = _fill_z_base(img, z_h_start, z_w_start, z_height, z_width)
    return img


def _draw_even_tril_down(img, z_h_start, z_w_start, z_height, z_width):
    img, z_part = _fill_z_base(img, z_h_start, z_w_start, z_height, z_width)
    img[z_h_start:z_h_start + z_height, z_w_start:z_w_start + z_width] = np.rot90(z_part, 2)
    return img


def _draw_odd_tril_up(img, z_h_start, z_w_start, z_height, z_width):
    img, z_part = _fill_z_base(img, z_h_start, z_w_start, z_height, z_width)
    img[z_h_start:z_h_start + z_height, z_w_start:z_w_start + z_width] = np.rot90(z_part)
    return img


def _draw_odd_tril_down(img, z_h_start, z_w_start, z_height, z_width):
    img, z_part = _fill_z_base(img, z_h_start, z_w_start, z_height, z_width)
    img[z_h_start:z_h_start + z_height, z_w_start:z_w_start + z_width] = np.rot90(z_part, 3)
    return img


def draw_zigzag(img, z_h_start_base, z_w_start, z_height, z_width):
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.tril_indices.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.fliplr.html#numpy.fliplr
    h_canvas, w_canvas, _ = img.shape
    num_iter = int(w_canvas / z_width)
    z_h_start = z_h_start_base

    for i in range(num_iter):
        if i % 2 == 0:
            img = _draw_even_tril_up(img, z_h_start, z_w_start, z_height, z_width)
            z_h_start = z_h_start_base + z_height
            img = _draw_even_tril_down(img, z_h_start, z_w_start, z_height, z_width)
        else:
            img = _draw_odd_tril_up(img, z_h_start, z_w_start, z_height, z_width)
            z_h_start = z_h_start_base + z_height
            img = _draw_odd_tril_down(img, z_h_start, z_w_start, z_height, z_width)

        z_w_start = z_w_start + z_width
        z_h_start = z_h_start_base
        
    return img


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    fill_base(img)

    z_h_start = random.randint(CANVAS_HEIGHT / 3, CANVAS_HEIGHT - ZIGZAG_HEIGHT * 2)
    z_w_start = 0
    z_height = ZIGZAG_HEIGHT
    z_width = ZIGZAG_WIDTH
    img = draw_zigzag(img, z_h_start, z_w_start, z_height, z_width)

    cv2.imshow('charlie_brown', img)
    cv2.imwrite('charlie_brown.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
