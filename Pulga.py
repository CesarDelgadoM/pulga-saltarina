import pygame
from MovRect import *
from CargadorImagen import *

class Pulga(MovRect):

    def __init__(self, _weidth, _height, url_image, _cant_frames):
        cima = CargadorImagen(url_image)
        self.image = cima.get_image()
        self.weidth = _weidth
        self.height = _height
        self.cant_frames = _cant_frames
        self.images = self.div_image()
        self.rect = pygame.Rect(0, 0, self.weidth, self.height)
        MovRect.__init__(self, self.rect)

    def draw(self, window):
        window.blit(self.image.subsurface(self.new_image), self.rect)

    def select_image(self, pos):
        self.new_image = self.images[pos]

    def div_image(self):
        list_images = []
        i = 0
        while (i < self.cant_frames):
            new_image = pygame.Rect(i * self.weidth, 0, self.weidth, self.height)
            list_images.append(new_image)
            i += 1
        return list_images