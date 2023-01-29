import numpy as np
import cv2
from tshirt import Tshirt
import time
import audio as ad
from segmentation import segmentize
from cvzone.SelfiSegmentationModule import SelfiSegmentation


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

UP_LIM = 30
LOW_LIM = 10

N_FRAME = 5
FRAME_TOLL_UP = 12
FRAME_TOLL_LOW = 2
WHITE_THRESHOLD = 20
THRESHOLD = 0.6
MIN_RESET_THRESHOLD = 2.5
MIN_RESET_ITERATIONS = 15

HEARING_TIME = 2
WAIT_TIME = 0
SLEEP_TIME = 5
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
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

segmentor = SelfiSegmentation()

white_pixel_percentage = 0
count_first_frame_above_threshold = 0  # number of consecutive frames above the 20% threshold
count_similar_frames = 0  # number of equal consecutive frames
old_white_pixel_percentage = 0
frame_list = []

c1_tshirt_number = 0
c2_tshirt_number = 0
original_tshirt_dictionary = dict()
new_tshirt_dictionary = dict()
start_segmentation_text = ''
isBackgroudRemovalFineshed = False
color1_percentage = 0
color2_percentage = 0

start = time.time()
# Loop over all frames

colors = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'gray']


def white_perc(frame_col):
    bw_frame = segmentor.removeBG(frame_col, (0, 0, 0), threshold=THRESHOLD)
    kernel = np.ones((2, 2), "uint8")
    clean = cv2.erode(bw_frame, kernel, iterations=1)
    # morphology.remove_small_objects(erosion, min_size=150, connectivity=150)
    white_pixel_perc = np.sum(clean) / np.size(clean)

    return white_pixel_perc, clean


def sorting_instruction(tshirt_group, t_shirt):
    tshirt_group.append(t_shirt)
    tshirt_group = sorted(tshirt_group, key=lambda x: x.brightness)
    index = tshirt_group.index(t_shirt)
    frase = ad.make_sentence(t_shirt.main_colour[:-1], index, t_shirt.colour_group, len(tshirt_group) - 1)
    return frase


def background_reset(white_pixel_perc):
    count = 0
    while white_pixel_perc > MIN_RESET_THRESHOLD or count < MIN_RESET_ITERATIONS:
        _, frame_col = cap.read()
        white_pixel_perc, _ = white_perc(frame_col)
        print("BW percentage: ", white_pixel_perc)
        count += 1
    time.sleep(SLEEP_TIME)
    ad.ready()


def print_info(clean, sst, c1, c2, c1_percentage, c2_percentage, wpp, original_t_d):
    clean = cv2.putText(clean, ('W/B Perc. : %.2f' % wpp), (900, 50), font, fontScale, color,
                        thickness, cv2.LINE_AA)
    clean = cv2.putText(clean, (c1 + ': %.2f      ' % c1_percentage + c2 + ': %.2f' % c2_percentage),
                        (900, 110), font, fontScale, color, thickness, cv2.LINE_AA)
    clean = cv2.putText(clean, sst, (1600, 110), font, 4, color, 3, cv2.LINE_AA)
    new_t_d = original_t_d.copy()
    print('W/B Perc.: %.2f   ' % wpp + c1 + ': %.2f   ' % c1_percentage + c2 +
          ': %.2f' % c2_percentage)
    return new_t_d, clean


def print_info_on_screen(original_t_d, clean):
    index = 0
    for x in original_t_d.keys():
        index += 1
        y_pos1 = 50 + 60 * index
        org = (50, y_pos1)
        text_to_print = 'Color Recognized: ' + x
        # Using cv2.putText() method
        clean = cv2.putText(clean, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

        y_pos2 = 80 + 60 * index
        org = (50, y_pos2)
        text_to_print = 'Brightness: ' + ('%.2f' % original_t_d[x])
        clean = cv2.putText(clean, text_to_print, org, font, fontScale, color, thickness, cv2.LINE_AA)

    return clean


def recognise_color(c1, c2, c1_perc, c2_perc, c1_num, c2_num):
    if c1_perc > UP_LIM and c2_perc < LOW_LIM:
        c1_num += 1
        name = c1 + str(c1_tshirt_number)
    elif c2_perc > UP_LIM and c1_perc < LOW_LIM:
        c2_num += 1
        name = c2 + str(c2_num)
    else:
        name = 'None'

    return name, c1_num, c2_num


def create_tshirt(hsv, name, c1, c2, original_t_d):
    if c1 in name:
        t_shirt_temp = Tshirt(hsv[0, -1, 0], hsv[0, -1, 1], hsv[0, -1, 2], name, 0)
    elif c2 in name:
        t_shirt_temp = Tshirt(hsv[0, -1, 0], hsv[0, -1, 1], hsv[0, -1, 2], name, 1)

    if name not in original_t_d.keys():
        original_t_d[name] = t_shirt_temp.brightness

    return t_shirt_temp, original_t_d


def choose_color_and_sort(tshirt_t, name, c1, c2, g1, g2):
    t_shirt = tshirt_t
    if c1 in name:
        sorting_instruction(g1, t_shirt)
    elif c2 in name:
        sorting_instruction(g2, t_shirt)


if cap.isOpened():

    ad.startMessage()

    color1, color2 = "blue", "orange"
    high_c1, low_c1 = np.array(color_dict_HSV[color1][0]), np.array(color_dict_HSV[color1][1])
    high_c2, low_c2 = np.array(color_dict_HSV[color2][0]), np.array(color_dict_HSV[color2][1])


    while cap.isOpened():
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is framed
        ret, frame_color = cap.read()

        if ret == True:
            if white_pixel_percentage == 0:
                frame_list = []
            # Convert frame to hsv
            hsv_frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2HSV)
            # Convert current frame to grayscale
            frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

            white_pixel_percentage, cleaned = white_perc(frame_color)

            if white_pixel_percentage > WHITE_THRESHOLD:
                frame_list.append(white_pixel_percentage)

                if len(frame_list) >= N_FRAME:

                    if abs(max(frame_list) - min(frame_list)) < FRAME_TOLL_UP and abs(
                            max(frame_list) - min(frame_list)) > FRAME_TOLL_LOW:

                        start_segmentation_text = 'F'
                        print("Start Segmentation")
                        # time.sleep(0.5)
                        start = time.time()
                        [color1_percentage, color2_percentage] = segmentize(hsv_frame, cleaned, low_c1, high_c1, low_c2,
                                                                            high_c2)
                        color_name, c1_tshirt_number, c2_tshirt_number = recognise_color(color1,color2,color1_percentage,
                                                                                         color2_percentage,c1_tshirt_number,
                                                                                         c2_tshirt_number)
                        if color_name != 'None':
                            tshirt_temp, original_tshirt_dictionary = create_tshirt(hsv_frame, color_name, color1,
                                                                                    color2, original_tshirt_dictionary)

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
                        c1_tshirt_number -= 1
                    elif color2 in color_name:
                        c2_tshirt_number -= 1
                elif time_seconds > WAIT_TIME and len(original_keys) != 1:
                    choose_color_and_sort(tshirt_temp, color_name, color1, color2, list_tshirt_group1, list_tshirt_group2)
                    background_reset(white_pixel_percentage)
                    frame_list = []

            if len(original_keys) == 1 and flag_first_tshirt:
                flag_first_tshirt = False
                choose_color_and_sort(tshirt_temp, color_name, color1, color2, list_tshirt_group1, list_tshirt_group2)
                background_reset(white_pixel_percentage)
                frame_list = []

            time_seconds = end - start
            new_tshirt_dictionary, cleaned = print_info(cleaned, start_segmentation_text, color1, color2,
                                                        color1_percentage, color2_percentage, white_pixel_percentage,
                                                        original_tshirt_dictionary)

            if time_seconds > 0.5:
                start_segmentation_text = ''

            cleaned = print_info_on_screen(original_tshirt_dictionary, cleaned)

            # result.write(cleaned)
            # Display image
            cv2.imshow('frame2', cleaned)
            n_pixel = 0
            key = cv2.waitKey(100)

            if key == ord('q') or (len(list_tshirt_group1) >= N_TSHIRTS and len(list_tshirt_group2) >= N_TSHIRTS):
                ad.task_finished()
                break
        else:
            break

    # Release video object
    cap.release()
    # result.release()
    # Destroy all windows
    cv2.destroyAllWindows()
