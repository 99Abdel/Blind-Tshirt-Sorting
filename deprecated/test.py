import cvzone
import numpy as np
import cv2
from tshirt import Tshirt
from skimage import data, filters
from skimage import morphology
import time
import pygame as pg
from segmentation import segmentize
from cvzone.SelfiSegmentationModule import SelfiSegmentation

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

RESOLUTION = 1920 * 1080
UP_LIM = RESOLUTION * 0.3
LOW_LIM = RESOLUTION * 0.01

N_FRAME = 10
FRAME_TOLL = 2
WHITE_THRESHOLD = 20


# Open Camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

segmentor = SelfiSegmentation()
# Loop over all frames
while (cap.isOpened()):
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    ret, frame_color = cap.read()
    if ret == True:
        # Convert frame to hsv
        hsv_frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2HSV)
        # Convert current frame to grayscale
        frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

        BW_frame = segmentor.removeBG(frame_color, (0, 0, 0), threshold=0.7)
        kernel = np.ones((10, 10), "uint8")
        erosion = cv2.erode(BW_frame, kernel, iterations=1)
        cleaned = morphology.remove_small_objects(erosion, min_size=150, connectivity=150)
        white_pixel_percentage = np.sum(cleaned) / np.size(cleaned)

        [red_closed_npixel, blue_closed_npixel] = segmentize(hsv_frame, cleaned,,
        print('Orange : %.2f' %red_closed_npixel + 'Blue : %.2f' %blue_closed_npixel)
        n_pixel = 0
        key = cv2.waitKey(150)
        if key == ord('q'):
            break
    else:
        break

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
