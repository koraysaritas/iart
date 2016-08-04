# Korora 22 Selina
# https://github.com/kororaproject/kp-korora-backgrounds/blob/a91c0960a4d9266b9e6393fefd4337f5a48d64ca/upstream/default/wide/korora.png
import numpy as np
import cv2
import math
from scipy.spatial import Delaunay

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
MAX_POINTS = 100
LINE_THICKNESS = 1
COLOR_BLACK_BGR = (0, 0, 0)
COLOR_WHITE_BGR = (255, 255, 255)
BGR_B = (237, 184, 20)
BGR_Y = (116, 213, 251)
BGR_R = (24, 27, 195)


def create_canvas(h, w, c):
    img = np.zeros((h, w, 3), np.uint8)
    img.fill(c)
    return img


def rand_pts(upper_bound, size):
    return np.random.choice(upper_bound, size=size)


def gen_color(num, colors):
    seq_num = math.ceil(num / len(colors))
    colors.append(colors[0])
    for f, t in zip(colors[:-1], colors[1:]):
        arr_b = np.linspace(f[0], t[0], seq_num)
        arr_g = np.linspace(f[1], t[1], seq_num)
        arr_r = np.linspace(f[2], t[2], seq_num)
        for b, g, r in zip(arr_b, arr_g, arr_r):
            yield (b, g, r)


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 0)
    range = max(CANVAS_HEIGHT, CANVAS_WIDTH)
    rand_pts_h = rand_pts(range, 100)
    rand_pts_w = rand_pts(range, 100)

    pts = np.stack((rand_pts_h, rand_pts_w), axis=1)
    edge_pts = [[0, 0], [0, CANVAS_HEIGHT], [CANVAS_WIDTH, 0], [CANVAS_HEIGHT, CANVAS_WIDTH]]
    pts = np.append(pts, edge_pts)
    pts = np.reshape(pts, (MAX_POINTS + len(edge_pts), 2))

    tri = Delaunay(pts)

    gen_c = gen_color(len(tri.simplices), [BGR_B, BGR_Y, BGR_R])
    ix = 0
    visited = {}
    queue = [(ix, tri.simplices[ix])]
    while len(queue) > 0:
        ix, simplex = queue.pop(0)
        if ix not in visited:
            visited[ix] = True
            ix1, ix2, ix3 = simplex
            pt1, pt2, pt3 = tuple(pts[ix1]), tuple(pts[ix2]), tuple(pts[ix3])
            triangle = np.array([pt1, pt2, pt3])
            cv2.fillConvexPoly(img, triangle, next(gen_c))
            cv2.line(img, pt1, pt2, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)
            cv2.line(img, pt2, pt3, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)
            cv2.line(img, pt1, pt3, COLOR_WHITE_BGR, 2, lineType=cv2.LINE_AA)
            ns = tri.neighbors[ix]
            for n in ns:
                if n != -1:
                    queue.append((n, tri.simplices[n]))

    cv2.imshow('korora_selina', img)
    cv2.imwrite('korora_selina.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
