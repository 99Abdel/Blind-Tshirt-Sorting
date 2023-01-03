import numpy as np
import cv2
from skimage import data, filters
from skimage import morphology

# Open Video
cap = cv2.VideoCapture('video_test/unsorted.mp4')

# Randomly select 25 frames
frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

# Store selected frames in an array
frames = []
for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frames.append(frame)

# Calculate the median along the time axis
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
white_pixel_percentage = 0
count_first_frame_above_threshold = 0  # number of consecutive frames above the 20% threshold
count_equal_frame = 0  # number of equal consecutive frames
old_white_pixel_percentage = 0
frame_list = []

# Loop over all frames
while (cap.isOpened()):
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    ret, frame = cap.read()
    if ret == True:
        # Read frame
        # Convert current frame to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate absolute difference of current frame and
        # the median frame
        dframe = cv2.absdiff(frame, grayMedianFrame)
        # Treshold to binarize
        th, dframe = cv2.threshold(dframe, 60, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), "uint8")
        erosion = cv2.erode(dframe, kernel, iterations=1)
        cleaned = morphology.remove_small_objects(erosion, min_size=150, connectivity=150)

        white_pixel_percentage = np.sum(cleaned) / np.size(cleaned)
        print(white_pixel_percentage)

        if white_pixel_percentage > 20:
            count_first_frame_above_threshold += 1
            frame_list.append(white_pixel_percentage)
            if count_first_frame_above_threshold == 5 and abs(max(frame_list)-min(frame_list)) < 4:
                print("Start segmentation")
                frame_list = []
                count_first_frame_above_threshold = 0
            else:
                count_first_frame_above_threshold = 0
                frame_list = []
        else:
            frame_list = []
            count_first_frame_above_threshold = 0

        # Display image
        cv2.imshow('frame2', cleaned)
        n_pixel = 0
        key = cv2.waitKey(20)
        if key == ord('q'):
            break
    else:
        break

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
