import cv2
import numpy as np
import time
import constants as cs
import audio as ad
from tshirt import Tshirt


def white_perc(frame_col, segmentor):
    """
    Calculate the percentage of white pixels in a given frame and return the white percentage and cleaned binary image.

    :param segmentor:
    :param frame_col: The original color frame.
    :param THRESHOLD: The threshold for removing background. (present in the script)
    :param kernel: The kernel used for erosion. (present in the script)
    :return: the percentage of white pixels and the cleaned binary image.
    """

    bw_frame = segmentor.removeBG(frame_col, (0, 0, 0), threshold=cs.THRESHOLD)
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


def background_reset(white_pixel_perc, cap, segmentor):
    """
    Reset the video capture source until white pixel percentage is below the minimum reset threshold or minimum
    reset iterations has been reached.

    :param segmentor:
    :param cap:
    :param white_pixel_perc: float, the current white pixel percentage of the frame
    :return: None
    """
    count = 0
    while white_pixel_perc > cs.MIN_RESET_THRESHOLD or count < cs.MIN_RESET_ITERATIONS:
        _, frame_col = cap.read()
        white_pixel_perc, _ = white_perc(frame_col, segmentor)
        print("BW percentage: ", white_pixel_perc)
        count += 1
    time.sleep(cs.SLEEP_TIME)
    ad.ready()


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
    if c1_perc > cs.UP_LIM and c2_perc < cs.LOW_LIM:
        c1_num += 1
        name = c1 + str(c1_num)
    elif c2_perc > cs.UP_LIM and c1_perc < cs.LOW_LIM:
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
    clean = cv2.putText(clean, ('W/B Perc. : %.2f' % wpp), (900, 50), cs.font, cs.fontScale, cs.color,
                        cs.thickness, cv2.LINE_AA)
    clean = cv2.putText(clean, (c1 + ': %.2f      ' % c1_percentage + c2 + ': %.2f' % c2_percentage),
                        (900, 110), cs.font, cs.fontScale, cs.color, cs.thickness, cv2.LINE_AA)
    clean = cv2.putText(clean, sst, (1600, 110), cs.font, 4, cs.color, 3, cv2.LINE_AA)
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
        clean = cv2.putText(clean, text_to_print, org, cs.font, cs.fontScale, cs.color, cs.thickness, cv2.LINE_AA)

        y_pos2 = 80 + 60 * index
        org = (50, y_pos2)
        text_to_print = 'Brightness: ' + ('%.2f' % original_t_d[x])
        clean = cv2.putText(clean, text_to_print, org, cs.font, cs.fontScale, cs.color, cs.thickness, cv2.LINE_AA)

    return clean
