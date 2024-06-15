import pygame

class CargadorImagen(object):

    def __init__(self, url, convert=False):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(url)
        except pygame.error:
            print("Imagen no encontrada")
        if (convert):
            self.image = self.image.convert()

    def get_image(self):
        return self.image

    def get_rect_image(self):
        return self.image.get_rect()
