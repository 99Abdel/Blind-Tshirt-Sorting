from gtts import gTTS

import os

mytext = 'Left'
path = "./audio_samples/"
# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome 
myobj.save(path + "Left.mp3")

# Playing the converted file

# os.system("mpg321 "+path+"Left.mp3")

# mpg321 ./audio_samples/color.mp3 ./audio_sample3s/color.mp3


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

    "RED": path + "Red.mp3",
    "BLUE": path + "Blue.mp3",
    "GREEN": path + "Green.mp3",
    "YELLOW": path + "Yellow.mp3",
    "PURPLE": path + "Purple.mp3",
    "ORANGE": path + "Orange.mp3"
}


# Right = path + "To_the_right_of.mp3"
# Left = path + "To_the_left_of.mp3"


def make_sentence(color, position, group, nb_shirts):
    res = "mpg321 " + path + "color.mp3 " + colors[color] + " "

    # message for positionning

    # group of tshirts that will be on the left of the hanger

    if group == 0:

        # no tshirts already on hanger
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

    return res

# make_sentence(color, position, group, nb_shirts)

res = make_sentence("RED",1,1,3)
print(res)
os.system(res)
