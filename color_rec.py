import math

import cv2, numpy as np, pygame as pg

# Capturing video through webcam
webcam = cv2.VideoCapture(0)

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

# attempt to track number of colors in the image
nb_colors = 0


#initialization of clock to measure time 
pg.init()

clk = pg.time.Clock()
time = 0


# color detection

def color_dtct(a):

    # [red,Blue,purple,green,yellow]

    if a[0]:
        return "Red"
    if a[1]:
        return "Blue"
    if a[2]:
        return "Purple"
    if a[3]:
        return "Green"
    if a[4]:
        return "Yellow"

# Start a while loop
while (1):
    clk.tick()
    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    rgbFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)
    brightness = np.sqrt(0.241*pow(rgbFrame[0, :, 0],2) + 0.691*pow(rgbFrame[0, :, 1],2) + 0.068*pow(rgbFrame[0, :, 2],2))

    # Set range for red color 1 and
    # define mask
    red1_lower = np.array(color_dict_HSV['red1'][1], np.uint8)
    red1_upper = np.array(color_dict_HSV['red1'][0], np.uint8)
    red1_mask = cv2.inRange(hsvFrame, red1_lower, red1_upper)

    red2_lower = np.array(color_dict_HSV['red2'][1], np.uint8)
    red2_upper = np.array(color_dict_HSV['red2'][0], np.uint8)
    red2_mask = cv2.inRange(hsvFrame, red2_lower, red2_upper)

    red_mask = red1_mask + red2_mask

    # Set range for green color and
    # define mask
    green_lower = np.array(color_dict_HSV['green'][1], np.uint8)
    green_upper = np.array(color_dict_HSV['green'][0], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array(color_dict_HSV['blue'][1], np.uint8)
    blue_upper = np.array(color_dict_HSV['blue'][0], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Set range for yellow color and
    # define mask
    yellow_lower = np.array(color_dict_HSV['yellow'][1], np.uint8)
    yellow_upper = np.array(color_dict_HSV['yellow'][0], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    # Set range for purple color and
    # define mask
    purple_lower = np.array(color_dict_HSV['purple'][1], np.uint8)
    purple_upper = np.array(color_dict_HSV['purple'][0], np.uint8)
    purple_mask = cv2.inRange(hsvFrame, purple_lower, purple_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask1 = cv2.dilate(red1_mask, kernal)
    res_red1 = cv2.bitwise_and(imageFrame, imageFrame,
                              mask=red_mask1)

    red_mask2 = cv2.dilate(red2_mask, kernal)
    res_red2 = cv2.bitwise_and(imageFrame, imageFrame,
                              mask=red_mask2)

    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask=green_mask)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                               mask=blue_mask)

    # For yellow color
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    res_yellow = cv2.bitwise_and(imageFrame, imageFrame,
                                   mask=yellow_mask)

    # For purple color
    purple_mask = cv2.dilate(purple_mask, kernal)
    res_purple = cv2.bitwise_and(imageFrame, imageFrame,
                                   mask=purple_mask)


    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    red = 0
    Blue = 0
    green = 0
    purple = 0
    yellow = 0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 1500):
            red = 1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(imageFrame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 1500):
            green = 1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 255, 0), 2)

            cv2.putText(imageFrame, "Green Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 1500):
            Blue = 1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)

            cv2.putText(imageFrame, "Blue Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))

    # Creating contour to track yellow color
    contours, hierarchy = cv2.findContours(yellow_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 1500):
            yellow = 1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 255, 255), 2)

            cv2.putText(imageFrame, "Yellow Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 255))

    # Creating contour to track purple color
    contours, hierarchy = cv2.findContours(purple_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 1500):
            purple = 1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 255), 2)

            cv2.putText(imageFrame, "Purple Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 255))

    nb_colors = red + Blue + purple + green + yellow
    colors = [red,Blue,purple,green,yellow]

    single_color = (1 if nb_colors==1 else 0)
    #print(nb_colors)
    if single_color:
        time += clk.get_time()
    elif not single_color:
        time = 0
    print(time)
    if single_color and time>=10000:
        print(color_dtct(colors))

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break