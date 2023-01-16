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


def show_frames(frame, color1_closed, color2_closed, f_name, c1_name, c2_name):
    cv2.imshow(f_name, frame)
    cv2.imshow(c1_name, color1_closed)
    cv2.imshow(c2_name, color2_closed)


def segmentation(hsv_frame, frame):

    # Red color
    low_red = np.array([5, 50, 70])
    high_red = np.array([50, 255, 255])

    # Blue color
    low_blue = np.array([70, 10, 2])
    high_blue = np.array([130, 255, 255])

    [red, red_closed, red_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_red, high_red, kernel)
    [blue, blue_closed, blue_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_blue, high_blue, kernel)

    # show_frames(frame, red_closed, blue_closed, "Frame", "Red", "Blue")

    orange_percentage = np.sum(red_closed) / np.size(red_closed)
    blue_percentage = np.sum(blue_closed) / np.size(blue_closed)

    return orange_percentage, blue_percentage

