import pygame as pg
from gtts import gTTS

import os

pg.mixer.init()
pg.mixer.music.set_volume(1.0)

mytext = "Ready for the next tshirt"
path = "./audio_samples/"
# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed


# myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome 
# myobj.save(path + "ready.mp3")

# Playing the converted file

# os.system("mpg321 "+path+"Left.mp3")

# mpg321 ./audio_samples/color.mp3 ./audio_sample3s/color.mp3

color = path + "color_simple.mp3"
to_sort = path + "to_sort.mp3"
choose = path + "Choose.mp3"

selected = path + "selected.mp3"
start_message = path + "PowerOn.mp3"

the = path + "the.mp3"
left = path + "To_the_left_of.mp3"
right = path + "To_the_right_of.mp3"
tshirt = path + "Tshirt.mp3"
All = path + "All.mp3"
hanger = path + "Hanger.mp3"
start = path + "Starting_from.mp3"
Right = path + "Right.mp3"
Left = path + "Left.mp3"

# add_apology = 'Sorry I didnt get you, can you repeat?'.split()

positions = {

    1: path + "First.mp3",
    2: path + "Second.mp3",
    3: path + "Third.mp3",
    4: path + "Forth.mp3"

}

colors = {
    "red": path + "Red.mp3",
    "blue": path + "Blue.mp3",
    "green": path + "Green.mp3",
    "yellow": path + "Yellow.mp3",
    "purple": path + "Purple.mp3",
    "orange": path + "Orange.mp3"
}


# Right = path + "To_the_right_of.mp3"
# Left = path + "To_the_left_of.mp3"


def startMessage():
    """
    Power on message to tell the user that everithing is set up and he can start the sorting task
    :return:
    """
    if os.name == 'nt':
        pg.mixer.music.load(start_message)
        pg.mixer.music.play()
        pg.time.wait(1200)

    else:
        os.system("mpg321 " + start_message)


def task_finished():
    """
    Message to say to the user when the sorting is completely finished
    :return: None
    """
    if os.name == 'nt':
        pg.mixer.music.load(path + "Finished.mp3")
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + path + "Finished.mp3")


def ready():
    """
    message to say to give ok to the user the take another tshirt
    :return: None
    """
    if os.name == 'nt':
        pg.mixer.music.load(path + "ready.mp3")
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + path + "ready.mp3")


def make_sentence(color, position, group, nb_shirts):
    """
    This function creates a string that tells the position of a T-shirt with the given color on a hanger.
    it says it loud to the user playing concatenated mp3 files that are already generated in the audio_samples folder.

    :param color: Color of the T-shirt.
    :param position: Position of the T-shirt on the array group.
    :param group: Group of T-shirts (0: left side of the hanger, 1: right side of the hanger).
    :param nb_shirts: Total number of T-shirts already on the hanger.
    :return: res (str): frase that is spelled to the user
    """

    res = ("mpg321 " if (os.name != 'nt') else "") + path + "color.mp3 " + colors[color] + " "
    position += 1
    # message for positioning

    # group of t-shirts that will be on the left of the hanger

    if group == 0:

        # no t-shirts already on hanger
        if nb_shirts == 0:
            res = res + " " + left + " " + the + " " + hanger

        # already one tshirt on hanger
        if nb_shirts == 1:
            if position == 1:
                res = res + left + " " + All + " " + tshirt

            elif position == 2:
                res += right + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Left

        # 2 Tshirts already on hanger
        if nb_shirts == 2:
            if position == 1:
                res = res + left + " " + All + " " + tshirt

            if position == 2:
                res += right + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Left

            if position == 3:
                res += right + " " + positions[2] + " " + tshirt + " " + start + " " + the + " " + Left

        # 3 Tshirts already on hanger
        if nb_shirts == 3:
            if position == 1:
                res = res + left + " " + All + " " + tshirt

            if position == 2:
                res += right + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Left

            if position == 3:
                res += right + " " + positions[2] + " " + tshirt + " " + start + " " + the + " " + Left

            if position == 4:
                res += right + " " + positions[3] + " " + tshirt + " " + start + " " + the + " " + Left

    # group of tshirts that will be on the right of the hanger

    if group == 1:
        if nb_shirts == 0:
            res = res + " " + right + " " + the + " " + hanger

        if nb_shirts == 1:
            if position == 2:
                res = res + right + " " + All + " " + tshirt

            elif position == 1:
                res += left + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Right

        if nb_shirts == 2:
            if position == 3:
                res = res + right + " " + All + " " + tshirt

            if position == 2:
                res += left + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Right

            if position == 1:
                res += left + " " + positions[2] + " " + tshirt + " " + start + " " + the + " " + Right

        if nb_shirts == 3:
            if position == 4:
                res = res + right + " " + All + " " + tshirt

            if position == 3:
                res += left + " " + positions[1] + " " + tshirt + " " + start + " " + the + " " + Right

            if position == 2:
                res += left + " " + positions[2] + " " + tshirt + " " + start + " " + the + " " + Right

            if position == 1:
                res += left + " " + positions[3] + " " + tshirt + " " + start + " " + the + " " + Right

    # we differentiate btween windows first case and linux second case.

    if os.name == 'nt': # for windows
        # ws.PlaySound()
        res_w = res.split()
        for sound in res_w:
            # if pg.mixer.music.get_busy():
            #     pg.mixer.music.queue(sound)
            pg.mixer.music.load(sound)
            pg.mixer.music.play()
            pg.time.wait(1200)
    else: # for linux
        os.system(res)

    return res

# to test the audio uncomment this lines
# make_sentence(color, position, group, nb_shirts)

# res = make_sentence("RED",1,1,3)
# print(res)
# os.system(res)
# Ready()



# ----------------------------------------------------------------------------------------------------------------------
# ------------------- FROM HERE THE METHODS ARE NOT USED BUT THEY CAN BE USEFULL FOR FUTURE -------------------
# ------------------------- IMPROVEMENTS WHERE MORE INTERACRION WITH THE USER WILL BE PRESENT --------------------------
# ----------------------------------------------------------------------------------------------------------------------

def colorSel(pos):
    """

    :param pos:
    :return:
    """
    msg = choose + " " + positions[pos] + " " + color + " " + to_sort
    if os.name == 'nt':
        pg.mixer.music.load(msg)
        pg.mixer.music.play()
        pg.time.wait(1200)

    else:
        os.system("mpg321 " + msg)


## To do
def move_order():
    """
    Tell the user that now he can move
    :return: None
    """
    if os.name == 'nt':
        pg.mixer.music.load(path + "move.mp3")
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + path + "move.mp3")


def found_color(col):
    """
    The speaker tell the user which color has in its hand
    :param col: Color name
    :return: None
    """
    found_color_message = the + " " + color + " " + selected + " " + colors[col]
    if os.name == 'nt':
        pg.mixer.music.load(found_color_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + found_color_message)


def error():
    """
    error message to say to the user in order for him to repeat what he has said
    :returns: None
    """
    if os.name == 'nt':
        pg.mixer.music.load(path + "error.mp3")
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + path + "error.mp3")


def apology():
    """
    Affiliated to the error message tell the user politely to repeat its command
    :return: None
    """
    sorry = path + "Sorry.mp3"
    if os.name == 'nt':
        pg.mixer.music.load(sorry)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 " + sorry)

# ----------------------------------------------------------------------------------------------------------------------
# ------------------- TILL HERE THE PREVIOUS METHODS ARE NOT USED BUT THEY CAN BE USEFULL FOR FUTURE -------------------
# ------------------------- IMPROVEMENTS WHERE MORE INTERACRION WITH THE USER WILL BE PRESENT --------------------------
# ----------------------------------------------------------------------------------------------------------------------