import cv2
import numpy as np

def remove_background(frames):

    # Calculate the median along the time axis
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

    # Convert background to grayscale
    grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
    return grayMedianFrame