import pygame as pg
from gtts import gTTS

import os 
pg.mixer.init()
pg.mixer.music.set_volume(1.0)


mytext = 'Power on'
path = "./audio_samples/"
# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
#myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome 
#myobj.save(path + "PowerOn.mp3")

# Playing the converted file

# os.system("mpg321 "+path+"Left.mp3")

# mpg321 ./audio_samples/color.mp3 ./audio_sample3s/color.mp3



start_message = path + "PowerOn.mp3"
first_color_message = path + ""
second_color_message = path + ""
move_message = path + ""
found_color_message = path + ""
apology_message = path + ""
task_finished_message = path + ""
error_message = path + ""



the = path + "the.mp3"
left = path + "To_the_left_of.mp3"
right = path + "To_the_right_of.mp3"
tshirt = path + "Tshirt.mp3"
All = path + "All.mp3"
hanger = path + "Hanger.mp3"
start = path + "Starting_from.mp3"
Right = path + "Right.mp3"
Left = path + "Left.mp3"

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
    if os.name == 'nt':
        pg.mixer.music.load(start_message)
        pg.mixer.music.play()
        pg.time.wait(1200)

    else:
        os.system("mpg321 "+ start_message)

def first_color():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(first_color_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ first_color_message)

def second_color():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(second_color_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ second_color_message)

def move_order():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(move_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ move_message)

def found_color():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(found_color_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ found_color_message)

def apology():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(apology_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ apology_message)

def task_finishedd():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(task_finished_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ task_finished_message)

def error():
    "Joseph do it here"
    if os.name == 'nt':
        pg.mixer.music.load(error_message)
        pg.mixer.music.play()
        pg.time.wait(1200)
    else:
        os.system("mpg321 "+ error_message)


def make_sentence(color, position , group, nb_shirts):
    res = ("mpg321 " if (os.name!='nt') else "")  + path + "color.mp3 " + colors[color] + " "
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

    if os.name == 'nt':
        #ws.PlaySound()
        res_w = res.split()
        for sound in res_w:
            # if pg.mixer.music.get_busy():
            #     pg.mixer.music.queue(sound)
            pg.mixer.music.load(sound)
            pg.mixer.music.play()
            pg.time.wait(1200)

            

    else:
        os.system(res)

    return res



# make_sentence(color, position, group, nb_shirts)

# res = make_sentence("RED",1,1,3)
# print(res)
# os.system(res)
# startMessage()