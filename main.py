from cvzone.SelfiSegmentationModule import SelfiSegmentation
from segmentation import segmentize
import numpy as np
import cv2
import time
import audio as ad
import constants as cs
import utilities as uts

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

# Check if the video capture is open
if cap.isOpened():

    # Start the message "power on"
    ad.startMessage()

    # Initialize colors and their respective HSV values in an array format
    color1, color2 = "blue", "orange"
    high_c1, low_c1 = np.array(cs.color_dict_HSV[color1][0]), np.array(cs.color_dict_HSV[color1][1])
    high_c2, low_c2 = np.array(cs.color_dict_HSV[color2][0]), np.array(cs.color_dict_HSV[color2][1])

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
            white_pixel_percentage, cleaned = uts.white_perc(frame_color, segmentor)

            if white_pixel_percentage > cs.WHITE_THRESHOLD:
                frame_list.append(white_pixel_percentage)  # Add the white pixel percentage to the frame list

                # N_FRAME (minimum to assure stability, so that the tshirt is in fron of us and not just passing by)
                if len(frame_list) >= cs.N_FRAME:
                    # Check if the difference between the maximum and minimum values in the frame list is within the
                    # specified tolerance range (minimum to assure stability, so that the tshirt is in fron of us and
                    # not just passing by)
                    if abs(max(frame_list) - min(frame_list)) < cs.FRAME_TOLL_UP and abs(
                            max(frame_list) - min(frame_list)) > cs.FRAME_TOLL_LOW:

                        start_segmentation_text = 'F'
                        print("Start Segmentation")
                        # time.sleep(0.5)
                        start = time.time()

                        # Segmentize the current frame into two color regions
                        [color1_percentage, color2_percentage] = segmentize(hsv_frame, cleaned, low_c1, high_c1, low_c2,
                                                                            high_c2)
                        # Recognize the color in the current frame
                        color_name, c1_tshirt_number, c2_tshirt_number = uts.recognise_color(color1, color2,
                                                                                             color1_percentage,
                                                                                             color2_percentage,
                                                                                             c1_tshirt_number,
                                                                                             c2_tshirt_number)
                        # Create a t-shirt based on the recognized color
                        if color_name != 'None':
                            tshirt_temp, original_tshirt_dictionary = uts.create_tshirt(hsv_frame, color_name, color1,
                                                                                        color2,
                                                                                        original_tshirt_dictionary)

                        frame_list = []  # empty it for the next cases

                    else:
                        frame_list = []  # empty it for the next cases
            else:
                frame_list = []  # empty it for the next cases

            end = time.time()

            # Store the keys of the dictionaries in sets to compare their length later
            original_keys = set(original_tshirt_dictionary.keys())
            new_keys = set(new_tshirt_dictionary.keys())

            if (len(original_keys) - len(new_keys)) == 1:

                # If the time elapsed is less than or equal to the wait time and the original keys set is not of length1
                # (the last condition means that we are not in the first tshirt case)
                if time_seconds <= cs.WAIT_TIME and len(original_keys) != 1:
                    original_tshirt_dictionary.popitem()  # we do not save the tshirt so remove it from dictionary
                    if color1 in color_name:
                        c1_tshirt_number -= 1  # decrement the number of this tshirts bcs we incremented it earlier
                    elif color2 in color_name:
                        c2_tshirt_number -= 1  # decrement the number of this tshirts bcs we incremented it earlier

                # If the time elapsed is greater than the wait time and the original keys set is not of length 1
                # (the last condition means that we are not in the first tshirt case)
                elif time_seconds > cs.WAIT_TIME and len(original_keys) != 1:
                    uts.choose_color_and_sort(tshirt_temp, color_name, color1, color2, list_tshirt_group1,
                                              list_tshirt_group2)
                    uts.background_reset(white_pixel_percentage, cap, segmentor)
                    frame_list = []

            # We are in the first tshirt case so we dont have to wait for a time period, as soon as we see it we acquire
            if len(original_keys) == 1 and flag_first_tshirt:
                flag_first_tshirt = False
                uts.choose_color_and_sort(tshirt_temp, color_name, color1, color2, list_tshirt_group1,
                                          list_tshirt_group2)
                uts.background_reset(white_pixel_percentage, cap, segmentor)
                frame_list = []

            time_seconds = end - start
            new_tshirt_dictionary, cleaned = uts.print_info(cleaned, start_segmentation_text, color1, color2,
                                                            color1_percentage, color2_percentage,
                                                            white_pixel_percentage,
                                                            original_tshirt_dictionary)

            if time_seconds > 0.5:
                start_segmentation_text = ''

            cleaned = uts.print_info_on_screen(original_tshirt_dictionary, cleaned)

            # result.write(cleaned)
            # Display image
            cv2.imshow('frame2', cleaned)
            n_pixel = 0
            key = cv2.waitKey(100)

            # The program finishes if q key is pressed or the sorting is finished so all the tshirts for each group are
            # put in the sorting hanger
            if key == ord('q') or (len(list_tshirt_group1) >= cs.N_TSHIRTS and len(list_tshirt_group2) >= cs.N_TSHIRTS):
                ad.task_finished()
                break
        else:
            break

    # Release video object
    cap.release()
    # result.release()
    # Destroy all windows
    cv2.destroyAllWindows()
