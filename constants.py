import cv2
# dictionary with all the limits for the colors in HSV with upper boundaries and lower boundaries
# most of them require still an accurate tuning, currently only orange and blue are checked to be good.

colors = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'gray']

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