
class MovRect(object):

    def __init__(self, _rect):
        self.rect = _rect
        self.posX = 0
        self.posY = 0

    def move(self, _posX, _posY):
        self.rect.x += _posX
        self.rect.y += _posY
        self.posX = self.rect.x
        self.posY = self.rect.y
        
    def set_position(self, _posX, _posY):
        self.rect.x = _posX
        self.rect.y = _posY
        self.posX = self.rect.x
        self.posY = self.rect.y

    def get_rect(self):
        return self.rect