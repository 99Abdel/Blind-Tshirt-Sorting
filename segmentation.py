import cv2
import numpy as np
import pygame as pg
from tshirt import *

kernel = np.ones((10, 10), np.uint8)

def color_frame_morpho(hsv_frame, frame, low, high, kernel):
    """
    Perform color based segmentation and morphological operations on a video frame.

    :param hsv_frame: a frame in the HSV color space
    :param frame: a frame in the original color space
    :param low: a lower bound for the color range to be selected
    :param high: a higher bound for the color range to be selected
    :param kernel: the morphological operation kernel
    :return: color, color_closed, color_closed_npixel
        color: the original frame masked with the color range specified by 'low' and 'high'
        color_closed: the original frame masked with the result of applying morphological closure on the color range
                    specified by 'low' and 'high'
        color_closed_npixel: the number of non-zero pixels in color_closed
    """

    # mask
    color_mask = cv2.inRange(hsv_frame, low, high)
    color = cv2.bitwise_and(frame, frame, mask=color_mask)

    # mask after morphology
    color_mask_closing = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)
    color_closed = cv2.bitwise_and(frame, frame, mask=color_mask_closing)

    color_closed_npixel = np.count_nonzero(color_mask_closing)

    return color, color_closed, color_closed_npixel


def show_frames(frame, c1_closed, c2_closed, f_name, c1_name, c2_name):
    """
    Show multiple images in a multiple windows.

    :param frame: the original frame to be displayed
    :param c1_closed: the first processed color to be displayed
    :param c2_closed: the second processed color to be displayed
    :param f_name: the window name for the original frame
    :param c1_name: the window name for the first processed color
    :param c2_name: the window name for the second processed color
    :return: None
    """

    cv2.imshow(f_name, frame)
    cv2.imshow(c1_name, c1_closed)
    cv2.imshow(c2_name, c2_closed)


def segmentize(hsv_frame, frame, low_c1, high_c1, low_c2, high_c2):
    """
    Perform color-based segmentation on a video frame and calculate the percentage of pixels in each color.

    :param hsv_frame: a frame in the HSV color space
    :param frame: a frame in the original color space
    :param low_c1: a lower bound for the first color range to be selected
    :param high_c1: a higher bound for the first color range to be selected
    :param low_c2: a lower bound for the second color range to be selected
    :param high_c2: a higher bound for the second color range to be selected
    :return: c1_percentage, c2_percentage
        c1_percentage: the percentage of pixels in the first color range in the original frame
        c2_percentage: the percentage of pixels in the second color range in the original frame
    """

    [c1, c1_closed, c1_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_c1, high_c1, kernel)
    [c2, c2_closed, c2_closed_npixel] = color_frame_morpho(hsv_frame, frame, low_c2, high_c2, kernel)

    # show_frames(frame, c1_closed, c2_closed, "Frame", "COLOR1", "COLOR2")

    c1_percentage = np.sum(c1_closed) / np.size(c1_closed)
    c2_percentage = np.sum(c2_closed) / np.size(c2_closed)

    return c1_percentage, c2_percentage
