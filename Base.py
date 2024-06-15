import pygame
from MovRect import *
from CargadorImagen import *

class Base(MovRect):

    def __init__(self, _weidth, _height, url_image):
        ci = CargadorImagen(url_image)
        self.image_base = ci.get_image()
        self.rect_base = ci.get_rect_image()
        MovRect.__init__(self, self.rect_base)
        self.weidth = _weidth
        self.height = _height
        self.impulso = 30
        self.is_move = False
        self.multiplicador = 10
        self.velX = 7
        self.velY = 0

    def draw(self, window):
        window.blit(self.image_base, self.rect_base)
    
    def property_base(self, num):
        if (num == 2):
            self.impulso = 186
            self.is_move = True
            self.multiplicador = 80
        elif (num == 3):
            self.impulso = 66
            self.is_move = False
            self.multiplicador = 40
        else:
            self.impulso = 36
            self.is_move = False
            self.multiplicador = 10