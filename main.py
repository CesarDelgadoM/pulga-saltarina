import sys
import pygame
from Pulga import *
from Base import *
import Colors as color
from ImpresorTexto import *
from CargadorImagen import *
import random

class Main():

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.salir = False
        self.WIND_WIDTH = 500
        self.WIND_HEIGHT = 800
        self.pos_personaje_x = (self.WIND_WIDTH - 20) / 2
        self.pos_personaje_y = (self.WIND_HEIGHT - 30) / 2
        self.max_num_bases = 8
        self.sep_entre_bases = 90
        self.gravedad = 0.68
        self.inicio_frame = 2

    def load_game(self):
        self.iniciar_juego()
        self.size_window = (self.WIND_WIDTH, self.WIND_HEIGHT)
        self.window = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption("un pulga con altura")
        ci = CargadorImagen("sprites/fondo.png", True)
        self.fondo = ci.get_image()
        self.rect_fondo = ci.get_rect_image()
        self.bases = self.load_bases_random(self.max_num_bases)
        self.personaje = Pulga(20, 30, "sprites/animacion_completa.png", 6)
        self.personaje.select_image(0)
        self.personaje.set_position(self.pos_personaje_x, self.pos_personaje_y)
        self.msn_game_over = ImpresorTexto(self.window, color.BLACK, 70)
        self.msn_restar = ImpresorTexto(self.window, color.BLACK, 30)
        self.puntuacion = ImpresorTexto(self.window, color.BLACK, 30)
        self.puntuacion.render("SCORE " + str(self.puntaje), (6, 12))
        self.game_loop()

    def play_back(self):
        self.clock = pygame.time.Clock()
        self.bases = self.load_bases_random(self.max_num_bases)
        self.personaje.set_position(self.pos_personaje_x, self.pos_personaje_y)

    def reiniciar_juego(self):
        self.iniciar_juego()
        self.play_back()

    def iniciar_juego(self):
        self.game_over = False
        self.personaje_caido = False
        self.personaje_cayendo = False
        self.vel_impulso = 0
        self.vel_personaje_x = 0
        self.pos_base_menor = 0
        self.puntaje = 0
        self.mult_puntaje = 0

    def game_loop(self):
        while (not self.salir):
            self.control_events()
            self.update()
            self.render()
            self.clock.tick(60)
        print("Juego Terminado!")

    def control_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT]):
            self.vel_personaje_x += 0.7
        elif (keys[pygame.K_LEFT]):
            self.vel_personaje_x -= 0.7
        else:
            if (self.vel_personaje_x > -0.01 and self.vel_personaje_x < 0.01):
                self.vel_personaje_x = 0
            if (self.vel_personaje_x > 0):
                self.vel_personaje_x -= 0.06
            else:
                self.vel_personaje_x += 0.06
        if (self.game_over and keys[pygame.K_SPACE]):
            self.reiniciar_juego()

    def update(self):
        self.vel_impulso -= self.gravedad
        self.personaje.move(self.vel_personaje_x, 0)
        self.mover_personaje()
        self.ctrl_limit_wind_personaje(self.personaje)

    def render(self):
        self.window.blit(self.fondo, self.rect_fondo)
        self.personaje.draw(self.window)
        if (not self.game_over):
            if (self.vel_impulso < 0):
                self.personaje_cayendo = True
                self.personaje.select_image(0)
            else:
                self.personaje_cayendo = False
            for base in self.bases:
                base.draw(self.window)
                self.mover_base(base)
                self.ctrl_limit_wind_base(base)
        else:
            self.state_out_game()
        self.marcar_puntaje()
        pygame.display.update()

    def mover_base(self, base):
        if (base.is_move):
            base.posX += base.velX
            if (base.posX <= 0 or base.posX + base.weidth >= self.WIND_WIDTH):
                base.velX *= -1
        if (self.personaje_cayendo):
            self.detect_colision(self.personaje, base)
        else:
            base.posY += self.vel_impulso
        if (self.personaje_caido):
            base.posY += self.vel_impulso
        base.set_position(base.posX, base.posY)

    def mover_personaje(self):
        if (self.personaje.posY + self.personaje.height < self.WIND_HEIGHT):
            if (self.personaje_cayendo or self.personaje.posY > (self.pos_personaje_y - 100) and not self.personaje_cayendo):
                self.personaje.posY -= self.vel_impulso
        else:
            self.personaje.posY = self.WIND_HEIGHT - self.personaje.height
            self.personaje_caido = True
        self.personaje.set_position(self.personaje.posX, self.personaje.posY)

    def marcar_puntaje(self):
        if (not self.personaje_cayendo):
            self.puntaje += self.mult_puntaje
        if (self.puntaje >= 100000):
            self.puntuacion.render("SCORE  " + str(self.puntaje) + "  HI_SCORE " + str(self.puntaje), (6, 12))
        else:
            self.puntuacion.render("SCORE  " + str(self.puntaje) + "  HI_SCORE 100000", (6, 12))

    def state_out_game(self):
        self.msn_game_over.render("GAME OVER!", (100, 200))
        self.msn_restar.render("Press key space to start", (140, 600))
        self.animar_caida()

    def animar_caida(self):
        if (self.inicio_frame >= self.personaje.cant_frames - 1):
            self.inicio_frame = 2
        else:
            self.inicio_frame += 1
        self.clock.tick(20)
        self.personaje.select_image(self.inicio_frame)

    def ctrl_limit_wind_personaje(self, personaje):
        if (personaje.posX > self.WIND_WIDTH):
            personaje.posX = 0 - personaje.weidth
        elif ((personaje.posX + personaje.weidth) < 0):
            personaje.posX = self.WIND_WIDTH
        personaje.set_position(personaje.posX, personaje.posY)

    def ctrl_limit_wind_base(self, base):
        if (base.posY > self.WIND_HEIGHT):
            posX = random.randint(1, (self.WIND_WIDTH - base.weidth))
            for b in self.bases:
                if (b.posY < self.pos_base_menor):
                    self.pos_base_menor = b.posY
            posY = self.pos_base_menor - self.sep_entre_bases
            self.pos_base_menor = 0
            base.set_position(posX, posY)
            self.gen_property_base(base)
        elif ((base.posY + base.height) < -1000):
            self.game_over = True
            self.destructor_bases()

    def detect_colision(self, personaje, base):
        if (personaje.get_rect().colliderect(base.get_rect())):
            if (personaje.posY + personaje.height > base.posY):
                self.personaje.select_image(1)
                self.vel_impulso = base.impulso
                self.mult_puntaje = base.multiplicador

    def load_bases_random(self, cantidad):
        list_bases = []
        i = 0
        posY = 0
        while (i < cantidad):
            base = Base(64, 12, "sprites/base.png")
            posX = random.randint(1, self.WIND_WIDTH - base.weidth)
            posY += self.sep_entre_bases
            base.set_position(posX, posY)
            list_bases.append(base)
            i += 1
        return list_bases

    def gen_property_base(self, base):
        num = random.randint(0, 5)
        base.property_base(num)

    def destructor_bases(self):
        for b in self.bases:
            self.bases.remove(b)

if (__name__ == "__main__"):
    play = Main()
    play.load_game()
