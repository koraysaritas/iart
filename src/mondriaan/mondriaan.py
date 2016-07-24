# Piet Mondriaan
import numpy as np
import cv2
import random

CANVAS_WIDTH = 512
CANVAS_HEIGHT = 512
LINE_THICKNESS = 5
END_DIST_THRESH = int(CANVAS_WIDTH * 0.1)
COLOR_BLACK_BGR = (0, 0, 0)
H_STEP_MIN = int(CANVAS_HEIGHT * 0.1)
H_STEP_MAX = int(CANVAS_HEIGHT * 0.4)
V_STEP_MIN = int(CANVAS_WIDTH * 0.1)
V_STEP_MAX = int(CANVAS_WIDTH * 0.2)
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


def draw_v_lines(img, h_step_min, h_step_max, end_dist_thresh, color, thickness):
    h_canvas, w_canvas, _ = img.shape
    h_step_start, h_step_end = 0, 0  # (x, y)
    to_end = w_canvas - h_step_end
    v_lines = []

    while to_end > 0 and to_end > end_dist_thresh:
        h_step = random.randint(h_step_min, h_step_max)
        h_step_end = h_step_start + h_step
        to_end = w_canvas - h_step_end

        if h_step_end > w_canvas or to_end <= end_dist_thresh:
            break

        v_lines.append(h_step_end)

        img = cv2.line(img,
                       (h_step_end, 0), (h_step_end, h_canvas),
                       color,
                       thickness)

        h_step_start = h_step_end

    v_lines.append(h_canvas)

    return v_lines


def draw_h_lines(img, v_lines, v_step_min, v_step_max, end_dist_thresh, color, thickness):
    h_canvas, w_canvas, _ = img.shape
    v_step_start, v_step_end = 0, 0  # (x, y)
    to_end = h_canvas - v_step_end
    h_lines = []
    draw_choice = [0, 1]

    while to_end > 0 and to_end > end_dist_thresh:
        v_step = random.randint(v_step_min, v_step_max)
        v_step_end = v_step_start + v_step
        to_end = h_canvas - v_step_end

        if v_step_end > h_canvas or to_end <= end_dist_thresh:
            break

        last_v = 0
        v_step_h_lines = []
        for v_line in v_lines:
            if random.choice(draw_choice) > 0:
                img = cv2.line(img,
                               (last_v, v_step_end), (v_line, v_step_end),
                               color,
                               thickness)
                v_step_h_lines.append((last_v, v_line))

            last_v = v_line

        h_lines.append([v_step_h_lines, v_step_end])
        v_step_start = v_step_end

    return h_lines


def roi_top_left(img, v_lines, h_lines, thickness):
    pt1 = (0, 0)
    pt2 = None

    v_line_first = v_lines[0]
    for h_lines_at_v_step in h_lines:
        lines, h = h_lines_at_v_step[0], h_lines_at_v_step[1]
        for h_line_at_v_step in lines:
            if h_line_at_v_step[1] == v_line_first:
                pt2 = (int(h - thickness / 2), int(v_line_first - thickness / 2))
                break
        if pt2:
            break
    return (pt1, pt2) if pt1 and pt2 else None


def roi_center_right(img, v_lines, h_lines, thickness):
    h_canvas, w_canvas, _ = img.shape
    pt1, pt2 = None, None
    c_canvas = int(h_canvas / 2)

    for h_lines_at_v_step in h_lines:
        lines, h = h_lines_at_v_step[0], h_lines_at_v_step[1]
        for h_line_at_v_step in lines[::-1]:
            h_line_start, h_line_end = h_line_at_v_step[0], h_line_at_v_step[1]
            if h_line_end == w_canvas and h < c_canvas:
                pt1 = ((h + thickness - 1), int(h_line_start + thickness - 1))
            if h_line_end == w_canvas and h > c_canvas:
                pt2 = (int(h - thickness / 2), int(w_canvas))
                break
        if pt2:
            break

    return (pt1, pt2) if pt1 and pt2 else None


def roi_bottom_right(img, v_lines, h_lines, thickness):
    h_canvas, w_canvas, _ = img.shape
    pt1 = None
    pt2 = None
    v_line_end = v_lines[-2]
    for h_lines_at_v_step in h_lines[::-1]:
        lines, h = h_lines_at_v_step[0], h_lines_at_v_step[1]
        for h_line_at_v_step in lines:
            if h_line_at_v_step[1] == v_line_end:
                pt1 = (h + thickness, h_line_at_v_step[0] + thickness)
                pt2 = (int(h_canvas), int(v_line_end - thickness / 2))
                break
        if pt2:
            break
    return (pt1, pt2) if pt1 and pt2 else None


if __name__ == '__main__':
    img = create_canvas(CANVAS_HEIGHT, CANVAS_WIDTH, 255)

    v_lines = draw_v_lines(img, H_STEP_MIN, H_STEP_MAX, END_DIST_THRESH, COLOR_BLACK_BGR, LINE_THICKNESS)
    h_lines = draw_h_lines(img, v_lines, V_STEP_MIN, V_STEP_MAX, END_DIST_THRESH, COLOR_BLACK_BGR, LINE_THICKNESS)

    roi = roi_top_left(img, v_lines, h_lines, LINE_THICKNESS)
    color = random_color(BGR_B_LOWER, BGR_B_UPPER, 0)
    roi_fill_color(img, roi, color)

    roi = roi_bottom_right(img, v_lines, h_lines, LINE_THICKNESS)
    color = random_color(BGR_Y_LOWER, BGR_Y_UPPER, 0)
    roi_fill_color(img, roi, color)

    roi = roi_center_right(img, v_lines, h_lines, LINE_THICKNESS)
    color = random_color(BGR_R_LOWER, BGR_R_UPPER, 2)
    roi_fill_color(img, roi, color)

    cv2.imshow('mondriaan', img)
    cv2.imwrite('mondriaan.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
