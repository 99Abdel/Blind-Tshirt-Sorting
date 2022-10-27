import numpy as np
import colorsys
class Tshirt:
    def __init__(self, h, s, v, colour):
        self.h = h
        self.s = s
        self.v = v
        self.p = -1
        self.brightness = 0
        self.compute_brightness()
        self.main_colour = colour

    def compute_brightness(self):
        (r, g, b) = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        self.brightness = np.sqrt(0.241 * pow(r, 2) + 0.691 * pow(g, 2) + 0.068 * pow(b, 2))

    def get_brightness(self):
        return self.brightness

    def get_colour(self):
        return self.main_colour

    def update_position(self, new_pos):
        self.p = new_pos
