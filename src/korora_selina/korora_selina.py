# Korora 22 Selina
# https://github.com/kororaproject/kp-korora-backgrounds/blob/a91c0960a4d9266b9e6393fefd4337f5a48d64ca/upstream/default/wide/korora.png
import numpy as np
import cv2
import random
from scipy.spatial import Delaunay
import pylab

CANVAS_WIDTH = 512
CANVAS_HEIGHT = 512
LINE_THICKNESS = 1
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_WHITE_BGR = (255, 255, 255)
BGR_B_LOWER = (125, 112, 66)
BGR_B_UPPER = (210, 112, 66)
BGR_Y_LOWER = (0, 255, 254)
BGR_Y_UPPER = (40, 255, 254)
BGR_R_LOWER = (2, 15, 215)
BGR_R_UPPER = (2, 15, 250)


def create_canvas(h, w, c):
    img = np.zeros((h, w, 3), np.uint8)  # h-w-d
    img.fill(c)
    return img


def random_color(bgr_lower, bgr_upper, index):
    c = np.array([0, 0, 0])
    for i, (l, u) in enumerate(zip(bgr_lower, bgr_upper)):
        if i == index:
            c[i] = random.randint(bgr_lower[index], bgr_upper[index])
        else:
            c[i] = u
    return c


def roi_fill_color(img, roi, color):
    if roi:
        img[roi[0][0]:roi[1][0], roi[0][1]:roi[1][1]] = color


def rand_pts(upper_bound, size):
    return np.random.choice(upper_bound, size=size)


def gen_color(bgr_lower, bgr_upper, num):
    arr_b = np.linspace(bgr_lower[0], bgr_upper[0], num)
    arr_g = np.linspace(bgr_lower[1], bgr_upper[1], num)
    arr_r = np.linspace(bgr_lower[2], bgr_upper[2], num)
    for b, g, r in zip(arr_b, arr_g, arr_r):
        yield (b, g, r)


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)

    rand_pts_h = rand_pts(CANVAS_HEIGHT, 50)
    rand_pts_w = rand_pts(CANVAS_WIDTH, 50)

    pts = np.stack((rand_pts_h, rand_pts_w), axis=1)
    edge_pts = [[0, 0], [CANVAS_HEIGHT, 0], [0, CANVAS_WIDTH], [CANVAS_HEIGHT, CANVAS_WIDTH]]
    pts = np.append(pts, edge_pts)
    pts = np.reshape(pts, (54, 2))

    tri = Delaunay(pts)

    gen_c = gen_color(BGR_R_LOWER, BGR_B_UPPER, CANVAS_WIDTH)
    for ix in range(CANVAS_WIDTH):
        cv2.line(img, (ix, 0), (ix, CANVAS_HEIGHT), next(gen_c), 1, lineType=cv2.LINE_AA)

    for simplex in tri.simplices:
        ix1, ix2, ix3 = simplex
        pt1, pt2, pt3 = tuple(pts[ix1]), tuple(pts[ix2]), tuple(pts[ix3])
        # triangle = np.array([pt1, pt2, pt3], np.int32)
        # cv2.fillConvexPoly(img, triangle, BGR_B_UPPER)
        cv2.line(img, pt1, pt2, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)
        cv2.line(img, pt2, pt3, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)
        cv2.line(img, pt1, pt3, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)

    cv2.imshow('korora_selina', img)
    cv2.imwrite('korora_selina.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
