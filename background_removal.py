import numpy as np
import cv2
from tshirt import Tshirt
import time
import audio as ad
from segmentation import segmentize
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# dictionary with all the limits for the colors in HSV with upper boundaries and lower boundaries
# most of them require still an accurate tuning, currently only orange and blue are checked to be good.
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

# ALL THE FOLLOWING CONSTANTS ARE CHOSEN EMPIRICALLY FROM OUR TEST EXPERIENCE AND SEEM TO BE THE BEST ONES
# AND GIVE A ROBUST SYSTEM THAT IS NOT AFFECTED BY ENVIROMENTAL NOISES.
# BUT THEY STILL remain EMPIRICAL

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

colors = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'gray']


# ------------------------------------------- Open Camera --------------------------------------------------
#  ------------------------------  UNCOMMENT WHEN USING RAPBERRY -------------------------------------------
#  ------------------------------  UNCOMMENT WHEN USING RAPBERRY -------------------------------------------
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


# ------------------------------------------- Open Camera --------------------------------------
#  ------------------------------  COMMENT WHEN USING RAPBERRY -------------------------------------------
#  ------------------------------  COMMENT WHEN USING RAPBERRY -------------------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# ---------------- IF USING LAPTOP BOTH CAP THEY WORK JUST CHOOSE ONE. --------------------------

segmentor = SelfiSegmentation()
start = time.time()


def white_perc(frame_col):
    """
    Calculate the percentage of white pixels in a given frame and return the white percentage and cleaned binary image.

    :param frame_col: The original color frame.
    :param THRESHOLD: The threshold for removing background. (present in the script)
    :param kernel: The kernel used for erosion. (present in the script)
    :return: the percentage of white pixels and the cleaned binary image.
    """

    bw_frame = segmentor.removeBG(frame_col, (0, 0, 0), threshold=THRESHOLD)
    kernel = np.ones((2, 2), "uint8")
    clean = cv2.erode(bw_frame, kernel, iterations=1)
    # morphology.remove_small_objects(erosion, min_size=150, connectivity=150)
    white_pixel_perc = np.sum(clean) / np.size(clean)

    return white_pixel_perc, clean


def sorting_instruction(tshirt_group, t_shirt):
    """
    adds the tshirt to the group indicated and sorts it by brightness ascending order. and spells the instructions
    to the user.

    :param tshirt_group: List of t-shirt objects to be sorted of one color
    :param t_shirt: A single t-shirt object to be inserted and sorted into the tshirt_group
    :return: A string containing sorting instructions
    """
    tshirt_group.append(t_shirt)
    tshirt_group = sorted(tshirt_group, key=lambda x: x.brightness)
    index = tshirt_group.index(t_shirt)
    frase = ad.make_sentence(t_shirt.main_colour[:-1], index, t_shirt.colour_group, len(tshirt_group) - 1)
    return frase


def background_reset(white_pixel_perc):
    """
    Reset the video capture source until white pixel percentage is below the minimum reset threshold or minimum
    reset iterations has been reached.

    :param white_pixel_perc: float, the current white pixel percentage of the frame
    :return: None
    """
    count = 0
    while white_pixel_perc > MIN_RESET_THRESHOLD or count < MIN_RESET_ITERATIONS:
        _, frame_col = cap.read()
        white_pixel_perc, _ = white_perc(frame_col)
        print("BW percentage: ", white_pixel_perc)
        count += 1
    time.sleep(SLEEP_TIME)
    ad.ready()


def print_info(clean, sst, c1, c2, c1_percentage, c2_percentage, wpp, original_t_d):
    """
   Adds information to the image and prints it to the console.

   :param clean: Cleaned binary image
   :param sst: start segmentation text " " or "F"
   :param c1: First color name
   :param c2: Second color name
   :param c1_percentage: Percentage of the first color
   :param c2_percentage: Percentage of the second color
   :param wpp: White pixel percentage
   :param original_t_d: Original T-Shirt dictionary
   :return: The updated T-Shirt dictionary and the image with added information
   """
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
    """
    This function takes as input the original_t_d (dictionary containing colors and their brightness)
    and clean (the processed image) and outputs the same image with additional information added to it.

    :param original_t_d: dictionary containing colors and their brightness
    :param clean: processed image
    :return: processed image with additional information added to it
    """
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
    """
    Decides the color which covers more the screen according to the set limits UP_LIM and LOW_LIM
    :param c1: string, first color name
    :param c2: string, second color name
    :param c1_perc: float, percentage of the first color
    :param c2_perc: float, percentage of the second color
    :param c1_num: int, count of the first color
    :param c2_num: int, count of the second color
    :return: tuple (string, int, int), name of the color recognized, count of the first color and count of the second color
    """
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
    """
       Creates a Tshirt instance, initializing its attributes with the hue, saturation, and brightness values
       extracted from the input image and a unique name that differentiates it from other tshirts.
       and adds it to the dictionary 'original_t_d',

       :param hsv: 3D numpy array of hue, saturation and value of the t-shirt in the image.
       :param name: The name of the t-shirt.
       :param c1: The name of the first color.
       :param c2: The name of the second color.
       :param original_t_d: A dictionary containing the Tshirt instances and their brightness values.
       :return: The Tshirt instance and the updated 'original_t_d' dictionary.
    """
    if c1 in name:
        t_shirt_temp = Tshirt(hsv[0, -1, 0], hsv[0, -1, 1], hsv[0, -1, 2], name, 0)
    elif c2 in name:
        t_shirt_temp = Tshirt(hsv[0, -1, 0], hsv[0, -1, 1], hsv[0, -1, 2], name, 1)

    if name not in original_t_d.keys():
        original_t_d[name] = t_shirt_temp.brightness

    return t_shirt_temp, original_t_d


def choose_color_and_sort(tshirt_t, name, c1, c2, g1, g2):
    """
     Choose the color of the T-shirt based on the color name recognition results and sort it into the correct group
     based on the sorting instructions.

     :param tshirt_t: An instance of the Tshirt class that stores information about the T-shirt.
     :param name: The name of the color recognized for the T-shirt.
     :param c1: The name of the first color.
     :param c2: The name of the second color.
     :param g1: First color group.
     :param g2: Second color group.
     :return: None
    """
    t_shirt = tshirt_t
    if c1 in name:
        sorting_instruction(g1, t_shirt)
    elif c2 in name:
        sorting_instruction(g2, t_shirt)


# Check if the video capture is open
if cap.isOpened():

    # Start the message "power on"
    ad.startMessage()

    # Initialize colors and their respective HSV values in an array format
    color1, color2 = "blue", "orange"
    high_c1, low_c1 = np.array(color_dict_HSV[color1][0]), np.array(color_dict_HSV[color1][1])
    high_c2, low_c2 = np.array(color_dict_HSV[color2][0]), np.array(color_dict_HSV[color2][1])

    # Keep looping until the video capture is open
    while cap.isOpened():
        # Read the current frame from the video capture
        # vid_capture.read() methods returns a tuple, first element is a bool
        # and the second is framed
        ret, frame_color = cap.read()

        # If the frame is read successfully
        if ret == True:
            # Initialize an empty list of frames if there is no white pixel in the frame
            if white_pixel_percentage == 0:
                frame_list = []
            # Convert frame to hsv
            hsv_frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2HSV)
            # Convert current frame to grayscale
            frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

            # Calculate the percentage of white pixels in the current frame
            white_pixel_percentage, cleaned = white_perc(frame_color)

            if white_pixel_percentage > WHITE_THRESHOLD:
                frame_list.append(white_pixel_percentage) # Add the white pixel percentage to the frame list

                # N_FRAME (minimum to assure stability, so that the tshirt is in fron of us and not just passing by)
                if len(frame_list) >= N_FRAME:
                    # Check if the difference between the maximum and minimum values in the frame list is within the
                    # specified tolerance range (minimum to assure stability, so that the tshirt is in fron of us and
                    # not just passing by)
                    if abs(max(frame_list) - min(frame_list)) < FRAME_TOLL_UP and abs(
                            max(frame_list) - min(frame_list)) > FRAME_TOLL_LOW:

                        start_segmentation_text = 'F'
                        print("Start Segmentation")
                        # time.sleep(0.5)
                        start = time.time()

                        # Segmentize the current frame into two color regions
                        [color1_percentage, color2_percentage] = segmentize(hsv_frame, cleaned, low_c1, high_c1, low_c2,
                                                                            high_c2)
                        # Recognize the color in the current frame
                        color_name, c1_tshirt_number, c2_tshirt_number = recognise_color(color1, color2,
                                                                                         color1_percentage,
                                                                                         color2_percentage,
                                                                                         c1_tshirt_number,
                                                                                         c2_tshirt_number)
                        # Create a t-shirt based on the recognized color
                        if color_name != 'None':
                            tshirt_temp, original_tshirt_dictionary = create_tshirt(hsv_frame, color_name, color1,
                                                                                    color2, original_tshirt_dictionary)

                        frame_list = [] # empty it for the next cases

                    else:
                        frame_list = [] # empty it for the next cases
            else:
                frame_list = [] # empty it for the next cases

            end = time.time()

            # Store the keys of the dictionaries in sets to compare their length later
            original_keys = set(original_tshirt_dictionary.keys())
            new_keys = set(new_tshirt_dictionary.keys())

            if (len(original_keys) - len(new_keys)) == 1:

                # If the time elapsed is less than or equal to the wait time and the original keys set is not of length1
                # (the last condition means that we are not in the first tshirt case)
                if time_seconds <= WAIT_TIME and len(original_keys) != 1:
                    original_tshirt_dictionary.popitem() # we do not save the tshirt so remove it from dictionary
                    if color1 in color_name:
                        c1_tshirt_number -= 1 # decrement the number of this tshirts bcs we incremented it earlier
                    elif color2 in color_name:
                        c2_tshirt_number -= 1 # decrement the number of this tshirts bcs we incremented it earlier

                # If the time elapsed is greater than the wait time and the original keys set is not of length 1
                # (the last condition means that we are not in the first tshirt case)
                elif time_seconds > WAIT_TIME and len(original_keys) != 1:
                    choose_color_and_sort(tshirt_temp, color_name, color1, color2, list_tshirt_group1,
                                          list_tshirt_group2)
                    background_reset(white_pixel_percentage)
                    frame_list = []

            # We are in the first tshirt case so we dont have to wait for a time period, as soon as we see it we acquire
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

            # The program finishes if q key is pressed or the sorting is finished so all the tshirts for each group are
            # put in the sorting hanger
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
