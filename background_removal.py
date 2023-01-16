import numpy as np
import cv2
from tshirt import Tshirt
from skimage import morphology
import time
from audio import make_sentence


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

# Text print parameters
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
# fontScale
fontScale = 1
# Blue color in BGR
color = (0, 0, 0)
# Line thickness of 2 px
thickness = 2
flag_first_tshirt = True
flag_new_tshirt_added = False
flag_enough_time_passed = True
time_seconds = 0
list_tshirt_group1 = []
list_tshirt_group2 = []

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
count_similar_frames = 0  # number of equal consecutive frames
old_white_pixel_percentage = 0
frame_list = []

blue_tshirt_number = 0
orange_tshirt_number = 0
original_tshirt_dictionary = dict()
new_tshirt_dictionary = dict()
start_segmentation_text = ''
isBackgroudRemovalFineshed = False

start = time.time()
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
        # Calculate absolute difference of current frame and
        # the median frame


        dframe = cv2.absdiff(frame, grayMedianFrame)
        # Treshold to binarize
        th, dframe = cv2.threshold(dframe, 60, 255, cv2.THRESH_BINARY)
        kernel = np.ones((10, 10), "uint8")
        erosion = cv2.erode(dframe, kernel, iterations=1)
        cleaned = morphology.remove_small_objects(erosion, min_size=150, connectivity=150)
        white_pixel_percentage = np.sum(cleaned) / np.size(cleaned)

        if white_pixel_percentage > WHITE_THRESHOLD:
            frame_list.append(white_pixel_percentage)
            if len(frame_list) >= N_FRAME:

                if abs(max(frame_list)-min(frame_list)) < FRAME_TOLL:
                    start_segmentation_text = 'F'
                    # time.sleep(0.5)
                    start = time.time()
                    # Red color
                    low_orange = np.array([5, 50, 70])
                    high_orange = np.array([50, 255, 255])

                    # Blue color
                    low_blue = np.array([94, 80, 2])
                    high_blue = np.array([126, 255, 255])

                    [red, red_closed, red_closed_npixel] = color_frame_morpho(hsv_frame, frame_color, low_orange, high_orange, kernel)
                    [blue, blue_closed, blue_closed_npixel] = color_frame_morpho(hsv_frame, frame_color, low_blue, high_blue, kernel)
                    # uncomment to see the different color in a window
                    # show_frames(frame, red_closed, blue_closed, "Frame", "Orange", "Blue")

                    if (red_closed_npixel > UP_LIM and blue_closed_npixel < LOW_LIM):
                        orange_tshirt_number += 1
                        color_name = 'ORANGE' + str(orange_tshirt_number)
                    elif (blue_closed_npixel > UP_LIM and red_closed_npixel < LOW_LIM):
                        blue_tshirt_number += 1
                        color_name = 'BLUE' + str(blue_tshirt_number)
                    else:
                        color_name = 'None'

                    if color_name != 'None':
                        # DO A MEAN OF THE HSV_FRAME COLUMNS BEFORE CREATING A TSHIRT CLASS.
                        if 'BLUE' in color_name:
                            tshirt_temp = Tshirt(hsv_frame[0, -1, 0], hsv_frame[0, -1, 1], hsv_frame[0, -1, 2], color_name,0)
                        elif 'ORANGE' in color_name:
                            tshirt_temp = Tshirt(hsv_frame[0, -1, 0], hsv_frame[0, -1, 1], hsv_frame[0, -1, 2], color_name,1)

                        if color_name not in original_tshirt_dictionary.keys():
                            original_tshirt_dictionary[color_name] = tshirt_temp.brightness

                    frame_list = []
                else:
                    frame_list = []
        else:
            frame_list = []

        end = time.time()


        original_keys = set(original_tshirt_dictionary.keys())
        new_keys = set(new_tshirt_dictionary.keys())


        if (len(original_keys) - len(new_keys)) == 1:
            if time_seconds < 8 and len(original_keys) != 1:
                original_tshirt_dictionary.popitem()
                if 'BLUE' in color_name:
                    blue_tshirt_number -= 1
                elif 'ORANGE' in color_name:
                    orange_tshirt_number -= 1
            elif time_seconds > 8 and len(original_keys) != 1:
                tshirt = tshirt_temp
                if 'BLUE' in color_name:
                    list_tshirt_group1.append(tshirt)
                    list_tshirt_group1 = sorted(list_tshirt_group1, key=lambda x: x.brightness)
                    index = list_tshirt_group1.index(tshirt)

                    
                elif 'ORANGE' in color_name:
                    list_tshirt_group2.append(tshirt)
                    list_tshirt_group2 = sorted(list_tshirt_group2, key=lambda x: x.brightness)
                    index = list_tshirt_group2.index(tshirt)
            time_seconds = 0

        if len(original_keys) == 1 and flag_first_tshirt:
            flag_first_tshirt = False
            tshirt = tshirt_temp
            if 'BLUE' in color_name:
                list_tshirt_group1.append(tshirt)
                list_tshirt_group1 = sorted(list_tshirt_group1,key=lambda x: x.brightness)
                index = list_tshirt_group1.index(tshirt)
                frase = make_sentence("BLUE", index, tshirt.colour_group, len(list_tshirt_group1))
            elif 'ORANGE' in color_name:
                list_tshirt_group2.append(tshirt)
                list_tshirt_group2 = sorted(list_tshirt_group2, key=lambda x: x.brightness)
                index = list_tshirt_group2.index(tshirt)
                frase = make_sentence("ORANGE", index, tshirt.colour_group, len(list_tshirt_group2))
            time_seconds = 0


        time_seconds = end - start
        frame_color = cv2.putText(frame_color, ('W/B Perc. : %.2f' % white_pixel_percentage), (900, 50), font, fontScale,color, thickness, cv2.LINE_AA)
        frame_color = cv2.putText(frame_color, ('Time: %.2f' % time_seconds), (900, 80), font, fontScale, color,thickness, cv2.LINE_AA)
        frame_color = cv2.putText(frame_color, start_segmentation_text, (1600, 110), font, 4, color, 3 ,cv2.LINE_AA)
        new_tshirt_dictionary = original_tshirt_dictionary.copy()

        if time_seconds > 0.5:
            start_segmentation_text = ''

        index = -1
        for x in original_tshirt_dictionary.keys():
            index += 1
            y_pos1 = 50 + 60*index
            org = (50, y_pos1)
            text_to_print = 'Color Recognized: ' + x
            # Using cv2.putText() method
            frame_color = cv2.putText(frame_color, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

            y_pos2 = 80 + 60*index
            org = (50, y_pos2)
            text_to_print = 'Brightness: ' + ('%.2f' % original_tshirt_dictionary[x])
            frame_color = cv2.putText(frame_color, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

        # Display image
        cv2.imshow('frame2', frame_color)
        n_pixel = 0
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    else:
        break

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
