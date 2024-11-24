import pygame
import sys
from configs import *

pygame.init()

canvas = pygame.display.set_mode((OKNO_SZEROKOSC, OKNO_WYSOKOSC))
pygame.display.set_caption('Mario z kółka programistycznego')

cactus_img = pygame.image.load('assets/cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()

fire_img = pygame.image.load('assets/fire_bricks.png')
fire_img_rect = fire_img.get_rect()

zegar = pygame.time.Clock()

font = pygame.font.SysFont('forte', 20)


class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = pygame.image.load('assets/dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width += 10
        self.dragon_img_rect.height += 10
        self.dragon_img_rect.top = OKNO_WYSOKOSC/2
        self.dragon_img_rect.right = OKNO_SZEROKOSC
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load('assets/fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30

    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class Mario:
    mario_velocity = 10

    def __init__(self):
        self.mario_img = pygame.image.load('assets/mario.png')
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = OKNO_WYSOKOSC/2 - 100
        self.mario_score = 0
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.mario_img, self.mario_img_rect)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if wynik > self.mario_score:
                self.mario_score = wynik
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if wynik > self.mario_score:
                self.mario_score = wynik
        if self.up:
            self.mario_img_rect.top -= self.mario_velocity
        if self.down:
            self.mario_img_rect.bottom += self.mario_velocity


class Topscore:
    def __init__(self):
        self.high_score = 0

    def top_score(self, poprzedni_wynik):
        if poprzedni_wynik > self.high_score:
            self.high_score = poprzedni_wynik
        return self.high_score


topscore = Topscore()


def start_game():
    canvas.fill(TLO)
    start_img = pygame.image.load('assets/start.webp')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = OKNO_SRODEK
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('assets/mario_dies.wav')
    music.play()
    topscore.top_score(wynik)
    game_over_img = pygame.image.load('assets/start.webp')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = OKNO_SRODEK
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def check_level(wynik):
    global LEVEL
    if wynik in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = OKNO_WYSOKOSC - 50
        LEVEL = 1
    elif wynik in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = OKNO_WYSOKOSC - 100
        LEVEL = 2
    elif wynik in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = OKNO_WYSOKOSC - 150
        LEVEL = 3
    elif wynik > 30:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = OKNO_WYSOKOSC - 200
        LEVEL = 4


def game_loop():
    while True:
        global dragon
        global mario
        dragon = Dragon()
        mario = Mario()
        add_new_flame_counter = 0
        global wynik
        wynik = 0
        flames_list = []
        pygame.mixer.music.load('assets/mario_theme.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(TLO)
            check_level(wynik)
            dragon.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == CZESTOTLIWOSC_OGNIA:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)

            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    wynik += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mario.up = True
                        mario.down = False
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        mario.up = False
                        mario.down = True
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False

            score_font = font.render('Wynik:'+str(wynik), True, NAPIS_KOLOR)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (100, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Poziom:'+str(LEVEL), True, NAPIS_KOLOR)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (300, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Wynik:'+str(topscore.high_score), True, NAPIS_KOLOR)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            mario.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(mario.mario_img_rect):
                    game_over()
                    if wynik > mario.mario_score:
                        mario.mario_score = wynik

            pygame.display.update()
            zegar.tick(SZYBKOSC_GRY)


start_game()
