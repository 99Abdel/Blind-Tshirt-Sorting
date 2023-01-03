import cv2
import numpy as np
import pygame as pg
from tshirt import *

# image constant utilities
RESOLUTION = 640 * 480
UP_LIM = RESOLUTION * 0.3
LOW_LIM = RESOLUTION * 0.01

# initialization of clock to measure time
SETTLING_TIME = 2000
pg.init()
clk = pg.time.Clock()
time = 0

# open cv initialization
cap = cv2.VideoCapture(0)
kernel = np.ones((10, 10), np.uint8)


def color_frame_morpho(hsv_frame, frame, low, high, kernel):
    # mask
    color_mask = cv2.inRange(hsv_frame, low, high)
    color = cv2.bitwise_and(frame, frame, mask=color_mask)

    # mask after morphology
    color_mask_closing = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)
    color_closed = cv2.bitwise_and(frame, frame, mask=color_mask_closing)

    color_closed_npixel = np.count_nonzero(color_mask_closing)

    return color, color_closed, color_closed_npixel


def show_frames(frame, color1_closed, color2_closed, f_name, c1_name, c2_name):
    cv2.imshow(f_name, frame)
    cv2.imshow(c1_name, red_closed)
    cv2.imshow(c2_name, blue_closed)


while True:
    clk.tick()
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
                      'white': [[180, 18, 255], [0, 0, 231]],
                      'red1': [[180, 255, 255], [159, 50, 70]],
                      'red2': [[9, 255, 255], [0, 50, 70]],
                      'green': [[89, 255, 255], [36, 50, 70]],
                      'blue': [[128, 255, 255], [90, 50, 70]],
                      'yellow': [[35, 255, 255], [25, 50, 70]],
                      'purple': [[158, 255, 255], [129, 50, 70]],
                      'orange': [[24, 255, 255], [10, 50, 70]],
                      'gray': [[180, 18, 230], [0, 0, 40]]}

    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])

    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])

    [red, red_closed, red_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_red, high_red, kernel)
    [blue, blue_closed, blue_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_blue, high_blue, kernel)

    show_frames(frame, red_closed, blue_closed, "Frame", "Red", "Blue")

    if (red_closed_npixel > UP_LIM and blue_closed_npixel < LOW_LIM):
        time += clk.get_time()
        c = "RED"
    elif (blue_closed_npixel > UP_LIM and red_closed_npixel < LOW_LIM):
        time += clk.get_time()
        c = "BLUE"
    else:
        time = 0
        c = ""

    # print(time)

    if c != "" and time >= SETTLING_TIME:
        # DO A MEAN OF THE HSV_FRAME COLUMNS BEFORE CREATING A TSHIRT CLASS.
        tshirt = Tshirt(hsv_frame[0, -1, 0], hsv_frame[0, -1, 1], hsv_frame[0, -1, 2], c)
        print(c)

    key = cv2.waitKey(1)

    if key == 27:
        break
