# Goncu
import numpy as np
import cv2
import random

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
RECT_BASE_WIDTH = 10
RECT_WIDTH = 40
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_WHITE_BGR = (255, 255, 255)


def create_canvas(h, w, c):
    img = np.zeros((h, w, 3), np.uint8)  # h-w-d
    img.fill(c)
    return img


def draw_base(img, rect_base_width):
    h_canvas, w_canvas, _ = img.shape
    pts_h = np.arange(0, h_canvas, step=rect_base_width)
    pts_w = np.arange(0, w_canvas, step=rect_base_width)
    cycle = 0
    for pt_h in pts_h:
        cycle += 1
        for pt_w in pts_w:
            cycle += 1
            pt1 = (pt_h, pt_w)
            pt2 = (pt_h + rect_base_width, pt_w + rect_base_width)
            clr = COLOR_WHITE_BGR
            if cycle % 2 == 0:
                clr = COLOR_BLACK_BGR
            roi_fill_color(img, (pt1, pt2), clr)


def draw_rects(img, rect_width):
    pass


def roi_fill_color(img, roi, color):
    if roi:
        img[roi[0][0]:roi[1][0], roi[0][1]:roi[1][1]] = color


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    draw_base(img, RECT_BASE_WIDTH)
    draw_rects(img, RECT_WIDTH)

    cv2.imshow('goncu', img)
    cv2.imwrite('goncu.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
