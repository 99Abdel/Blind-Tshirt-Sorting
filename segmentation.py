import cv2
import numpy as np
import pygame as pg
from tshirt import *

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


def show_frames(frame, c1_closed, c2_closed, f_name, c1_name, c2_name):
    cv2.imshow(f_name, frame)
    cv2.imshow(c1_name, c1_closed)
    cv2.imshow(c2_name, c2_closed)


def segmentize(hsv_frame, frame, low_c1, high_c1, low_c2, high_c2):

    [c1, c1_closed, c1_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_c1, high_c1, kernel)
    [c2, c2_closed, c2_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_c2, high_c2, kernel)

    # show_frames(frame, c1_closed, c2_closed, "Frame", "COLOR1", "COLOR2")

    c1_percentage = np.sum(c1_closed) / np.size(c1_closed)
    c2_percentage = np.sum(c2_closed) / np.size(c2_closed)

    return c1_percentage, c2_percentage
