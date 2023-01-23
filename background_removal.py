import numpy as np
import cv2
from tshirt import Tshirt
from skimage import morphology
import time
import audio as ad
from Segmentation import segmentation
from cvzone.SelfiSegmentationModule import SelfiSegmentation
#import Speech as sp

#bd_addr = "00:11:22:33:44:55"  # Replace with the MAC address of the Bluetooth device you want to check

bluetooth = True

"""
result = bluetooth.lookup_name(bd_addr)
if (result != None):
    print("Bluetooth device found with address ", result)
else:
    print("Bluetooth device not found.")
"""


color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
                  'white': [[180, 18, 255], [0, 0, 231]],
                  'red1': [[180, 255, 255], [159, 50, 70]],
                  'red2': [[9, 255, 255], [0, 50, 70]],
                  'green': [[89, 255, 255], [36, 50, 70]],
                  'blue': [[130, 255, 255], [70, 10, 2]],
                  'yellow': [[35, 255, 255], [25, 50, 70]],
                  'purple': [[158, 255, 255], [129, 50, 70]],
                  'orange': [[50, 255, 255], [5, 50, 70]],
                  'gray': [[180, 18, 230], [0, 0, 40]]}

UP_LIM = 40
LOW_LIM = 10

N_FRAME = 2
FRAME_TOLL_UP = 12
FRAME_TOLL_LOW = 1
WHITE_THRESHOLD = 20

HEARING_TIME = 2
WAIT_TIME = 0
SLEEP_TIME = 8
N_TSHIRTS = 3
# Text print parameters
# font
font = cv2.FONT_HERSHEY_SIMPLEX
# org
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 255, 255)
# Line thickness of 2 px
thickness = 2
flag_first_tshirt = True
flag_new_tshirt_added = False
flag_enough_time_passed = True
time_seconds = 0
list_tshirt_group1 = []
list_tshirt_group2 = []

# Open Camera
cap = cv2.VideoCapture(1) #, cv2.CAP_DSHOW)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))

#size = (frame_width, frame_height)

#result = cv2.VideoWriter('./output_video/camera_video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

segmentor = SelfiSegmentation()

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
color1_percentage = 0
color2_percentage = 0

start = time.time()
# Loop over all frames

colors = ['black', 'white','red', 'green', 'blue', 'yellow', 'purple', 'orange', 'gray']

def inital():

    not_found = True
    ad.first_color()
    color1 = sp.recognise_speech()
    time.sleep(HEARING_TIME)

    while not_found:
        if color1.lower() in colors:
            ad.found_color()
            not_found = False
        else:
            ad.apology()
            color1 = sp.recognise_speech()
            time.sleep(HEARING_TIME)

    color2 = sp.recognise_speech()
    time.sleep(HEARING_TIME)

    while not_found:
        if color2.lower() in colors:
            ad.found_color()
            not_found = False
        else:
            ad.apology()
            color2 = sp.recognise_speech()
            time.sleep(HEARING_TIME)

    return color1, color2

if bluetooth and cap.isOpened():

    ad.startMessage()

    # color1,color2 = inital()
    color1, color2 = "blue", "orange"

    while (cap.isOpened()):
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is frame
        ret, frame_color = cap.read()

        if ret == True:
            if white_pixel_percentage == 0:
               frame_list = []
            # Convert frame to hsv
            hsv_frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2HSV)
            # Convert current frame to grayscale
            frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

            BW_frame = segmentor.removeBG(frame_color, (0, 0, 0), threshold=0.7)
            kernel = np.ones((2, 2), "uint8")
            erosion = cv2.erode(BW_frame, kernel, iterations=1)
            cleaned = erosion
            # morphology.remove_small_objects(erosion, min_size=150, connectivity=150)
            white_pixel_percentage = np.sum(cleaned) / np.size(cleaned)

            if white_pixel_percentage > WHITE_THRESHOLD:
                frame_list.append(white_pixel_percentage)
                if len(frame_list) >= N_FRAME:
                    if abs(max(frame_list) - min(frame_list)) < FRAME_TOLL_UP and abs(max(frame_list)-min(frame_list)) > FRAME_TOLL_LOW:
                        start_segmentation_text = 'F'
                        print("Start Segmentation")
                        # time.sleep(0.5)
                        start = time.time()
                        high_c1, low_c1 = np.array(color_dict_HSV[color1][0]), np.array(color_dict_HSV[color1][1])
                        high_c2, low_c2 = np.array(color_dict_HSV[color2][0]), np.array(color_dict_HSV[color2][1])
                        [color1_percentage, color2_percentage] = segmentation(hsv_frame, cleaned, low_c1, high_c1, low_c2, high_c2)

                        if color1_percentage > UP_LIM and color2_percentage < LOW_LIM:
                            orange_tshirt_number += 1
                            color_name = color1 + str(orange_tshirt_number)
                        elif color2_percentage > UP_LIM and color1_percentage < LOW_LIM:
                            blue_tshirt_number += 1
                            color_name = color2 + str(blue_tshirt_number)
                        else:
                            color_name = 'None'

                        if color_name != 'None':
                            # DO A MEAN OF THE HSV_FRAME COLUMNS BEFORE CREATING A TSHIRT CLASS.
                            if color1 in color_name:
                                tshirt_temp = Tshirt(hsv_frame[0, -1, 0], hsv_frame[0, -1, 1], hsv_frame[0, -1, 2],
                                                     color_name, 0)
                            elif color2 in color_name:
                                tshirt_temp = Tshirt(hsv_frame[0, -1, 0], hsv_frame[0, -1, 1], hsv_frame[0, -1, 2],
                                                     color_name, 1)

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
                if time_seconds <= WAIT_TIME and len(original_keys) != 1:
                    original_tshirt_dictionary.popitem()
                    if color1 in color_name:
                        blue_tshirt_number -= 1
                    elif color2 in color_name:
                        orange_tshirt_number -= 1
                elif time_seconds > WAIT_TIME and len(original_keys) != 1:
                    tshirt = tshirt_temp
                    if color1 in color_name:
                        list_tshirt_group1.append(tshirt)
                        list_tshirt_group1 = sorted(list_tshirt_group1, key=lambda x: x.brightness)
                        index = list_tshirt_group1.index(tshirt)
                        frase = ad.make_sentence(color1, index, tshirt.colour_group, len(list_tshirt_group1) - 1)
                    elif color2 in color_name:
                        list_tshirt_group2.append(tshirt)
                        list_tshirt_group2 = sorted(list_tshirt_group2, key=lambda x: x.brightness)
                        index = list_tshirt_group2.index(tshirt)
                        frase = ad.make_sentence(color2, index, tshirt.colour_group, len(list_tshirt_group2) - 1)
                    white_pixel_percentage = 0
                    frame_list = []
                    time.sleep(SLEEP_TIME)
                    ad.ready()
                    time_seconds = 0


            if len(original_keys) == 1 and flag_first_tshirt:
                flag_first_tshirt = False
                tshirt = tshirt_temp
                if color1 in color_name:
                    list_tshirt_group1.append(tshirt)
                    list_tshirt_group1 = sorted(list_tshirt_group1, key=lambda x: x.brightness)
                    index = list_tshirt_group1.index(tshirt)
                    frase = ad.make_sentence(color1, index, tshirt.colour_group, len(list_tshirt_group1) - 1)
                elif color2 in color_name:
                    list_tshirt_group2.append(tshirt)
                    list_tshirt_group2 = sorted(list_tshirt_group2, key=lambda x: x.brightness)
                    index = list_tshirt_group2.index(tshirt)
                    frase = ad.make_sentence(color2, index, tshirt.colour_group, len(list_tshirt_group2) - 1)
                frame_list = []
                white_pixel_percentage = 0
                time.sleep(SLEEP_TIME)
                ad.ready()
                time_seconds = 0

            time_seconds = end - start
            cleaned = cv2.putText(cleaned, ('W/B Perc. : %.2f' % white_pixel_percentage), (900, 50), font,
                                  fontScale, color, thickness, cv2.LINE_AA)
            cleaned = cv2.putText(cleaned, ('Time: %.2f' % time_seconds), (900, 80), font, fontScale, color,
                                  thickness, cv2.LINE_AA)
            cleaned = cv2.putText(cleaned, (color1 + ': %.2f' % color1_percentage + color2 + ': %.2f' % color2_percentage),
                                  (900, 110), font, fontScale, color,
                                  thickness, cv2.LINE_AA)
            cleaned = cv2.putText(cleaned, start_segmentation_text, (1600, 110), font, 4, color, 3, cv2.LINE_AA)
            new_tshirt_dictionary = original_tshirt_dictionary.copy()
            print('W/B Perc.: %.2f' % white_pixel_percentage + '   Time: %.2f  ' % time_seconds + color1 + ': %.2f  ' % color1_percentage + color2 + ': %.2f  ' % color2_percentage)

            if time_seconds > 0.5:
                start_segmentation_text = ''
            #if time_seconds > 8 and time_seconds < 8.2:
                #ad.ready()
            index = -1
            for x in original_tshirt_dictionary.keys():
                index += 1
                y_pos1 = 50 + 60 * index
                org = (50, y_pos1)
                text_to_print = 'Color Recognized: ' + x
                # Using cv2.putText() method
                cleaned = cv2.putText(cleaned, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

                y_pos2 = 80 + 60 * index
                org = (50, y_pos2)
                text_to_print = 'Brightness: ' + ('%.2f' % original_tshirt_dictionary[x])
                cleaned = cv2.putText(cleaned, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

            # result.write(cleaned)
            # Display image
            # cv2.imshow('frame2', cleaned)
            n_pixel = 0
            key = cv2.waitKey(40)
            if  key == ord('q') or (len(list_tshirt_group1) >= N_TSHIRTS and len(list_tshirt_group2) >= N_TSHIRTS):
                ad.task_finished()
                break
        else:
            break

    # Release video object
    cap.release()
    # result.release()
    # Destroy all windows
    cv2.destroyAllWindows()
