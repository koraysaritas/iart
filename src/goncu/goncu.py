# Goncu
import numpy as np
import cv2
import random

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
RECT_BASE_WIDTH = 20
RECT_TILE_WIDTH = 100
STEP_IN_TILE = 20
STEP_TILE = 50
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_WHITE_BGR = (255, 255, 255)
COLOR_BROWN_BGR = (79, 61, 144)


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


def gen_tile(pts_h, pts_w, rect_tile_width, step_tile, step_in_tile):
    for pt_h in pts_h:
        for pt_w in pts_w:
            roi_outer = [(pt_h, pt_w), (pt_h + rect_tile_width, pt_w + rect_tile_width)]
            roi_mid = [(pt_h + 9, pt_w + 9), (pt_h + rect_tile_width - 9, pt_w + rect_tile_width - 9)]
            roi_inner = [(pt_h + 9 + step_in_tile, pt_w + 9 + step_in_tile),
                         (pt_h + rect_tile_width - 9 - step_in_tile, pt_w + rect_tile_width - 9 - step_in_tile)]
            yield [roi_outer, roi_mid, roi_inner]


def draw_tiles(img, rect_tile_width, step_tile, step_in_tile):
    h_canvas, w_canvas, _ = img.shape
    pts_h = np.arange(int(step_tile * 1 / 2), h_canvas + step_tile * 2, step=rect_tile_width + 5 / 2 * step_tile)
    pts_w = np.arange(int(step_tile * 1 / 2), w_canvas + step_tile * 2, step=rect_tile_width + 5 / 2 * step_tile)
    num_tiles = len(pts_h) * len(pts_w)
    gen_t = gen_tile(pts_h, pts_w, rect_tile_width, step_tile, step_in_tile)
    for i in range(num_tiles):
        roi_outer, roi_mid, roi_inner = next(gen_t)
        roi_fill_color(img, roi_outer, COLOR_BLACK_BGR)
        roi_fill_color(img, roi_mid, COLOR_BROWN_BGR)
        roi_fill_color(img, roi_inner, COLOR_BLACK_BGR)


def roi_fill_color(img, roi, color):
    if roi:
        img[roi[0][0]:roi[1][0], roi[0][1]:roi[1][1]] = color


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    draw_base(img, RECT_BASE_WIDTH)
    draw_tiles(img, RECT_TILE_WIDTH, STEP_TILE, STEP_IN_TILE)

    cv2.imshow('goncu', img)
    cv2.imwrite('goncu.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
