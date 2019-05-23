import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from random import randint
import pygame.font


class Xiong(Sprite):
    def __init__(self,windows):
        super().__init__()
        self.windows = windows
        self.image = pygame.image.load('xiong200.jpg')
        self.rect = self.image.get_rect()
        self.windows_rect = windows.get_rect()
        self.rect.centerx  = self.windows_rect.centerx
        self.rect.bottom = self.windows_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up= False
        self.moving_down = False
    def blitme(self):
        self.windows.blit(self.image,self.rect)
    def update(self):
        if self.moving_right and self.rect.right <= self.windows_rect.right:
            self.rect.centerx += 10
        if self.moving_left and self.rect.left >= 0:
            self.rect.centerx -= 10
        if self.moving_up and self.rect.top >= 0:
            self.rect.bottom -= 5
        if self.moving_down and self.rect.bottom <= self.windows_rect.bottom:
            self.rect.bottom += 5

class Bullet(Sprite):
    def __init__(self,windows,xiong):
        super().__init__()
        self.windows = windows
        self.rect = pygame.Rect(0,0,1800,50)
        self.color = (0,255,0)
        self.rect.centerx = xiong.rect.centerx
        self.rect.bottom = xiong.rect.top
    def update(self):
        self.rect.y -= 5
    def draw_bullet(self):
        pygame.draw.rect(self.windows,self.color,self.rect)


class Qiang(Sprite):
    def __init__(self,windows):
        super().__init__()
        self.windows = windows
        self.image = pygame.image.load('qiang100.jpg')
        self.rect = self.image.get_rect()
        self.windows_rect = windows.get_rect()
        self.rect.x  = randint(0,1800-self.rect.width)
        self.rect.y = 0
        self.score = 100
    def blitme(self):
        self.windows.blit(self.image,self.rect)
    def update(self):
        self.rect.y += 5

class Button():

    def __init__(self,windows,msg):
        self.windows = windows
        self.windows_rect = windows.get_rect()

        self.width,self.height = 220, 60
        self.button_color = 242, 156, 177
        self.text_color = 100, 100, 100
        self.font = pygame.font.SysFont(None, 60)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.windows_rect.center

        self.prep_msg(msg)

    def prep_msg(self,msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.windows.fill(self.button_color, self.rect)
        self.windows.blit(self.msg_image, self.msg_image_rect)



class Score():
    def __init__(self,windows):
        self.windows = windows
        self.windows_rect = windows.get_rect()
        self.text_color = 30, 30, 30
        self.bg_color = 242, 156, 177
        self.font = pygame.font.SysFont(None, 48)
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):

        score_str = 'Score: ' + str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.windows_rect.right
        self.score_rect.top = self.windows_rect.top + 40

    def prep_high_score(self):
        high_score_str = 'High Score :' + str(self.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.windows_rect.right
        self.high_score_rect.top = self.windows_rect.top + 5

    def prep_level(self):
        level_str = 'Level: ' + str(self.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.windows_rect.right
        self.level_rect.top = self.windows_rect.top + 72



    def show_score(self):
        self.windows.blit(self.score_image,self.score_rect)
        self.windows.blit(self.high_score_image,self.high_score_rect)
        self.windows.blit(self.level_image,self.level_rect)



def check_levle(sb):
    if sb.score <= 1000:
        sb.level = 1
    elif 1000 < sb.score <= 5000:
        sb.level = 2
    elif 5000 < sb.score <= 10000:
        sb.level = 3
    elif 10000 < sb.score <= 50000:
        sb.level = 4
    elif 50000 < sb.score <= 100000:
        sb.level = 5
    sb.prep_level()



def check_score(sb):
    if sb.high_score < sb.score:
        sb.high_score = sb.score
        sb.prep_high_score()



def hit(qiang,xiong):
    if qiang.rect.colliderect(xiong.rect):

        qiang.rect.x = randint(0, 1800 - qiang.rect.width)
        qiang.rect.y = 0

def hit_qiang_bullet(qiang,bullets,sb):
    hit_music = pygame.mixer.Sound('hit.wav')
    hit_music.set_volume(0.8)
    if pygame.sprite.spritecollideany(qiang,bullets):
        hit_music.play()
        sb.score += qiang.score
        sb.prep_score()
        check_score(sb)
        check_levle(sb)
        qiang.rect.x = randint(0, 1800 - qiang.rect.width)
        qiang.rect.y = 0


def drop(qiang):
    if qiang.rect.bottom >= 900:
        qiang.rect.x = randint(0, 1800 - qiang.rect.width)
        qiang.rect.y = 0
def fire_bullet(windows,xiong,bullets):
    new_bullet = Bullet(windows,xiong)
    bullets.add(new_bullet)


def game():
    pygame.init()
    windows = pygame.display.set_mode((1800,900))
    pygame.display.set_caption('xiongchumo')
    bp = pygame.image.load('xiong1800.jpg').convert()
    color = (255,255,255)
    pygame.mixer.music.load('xiongchumo.ogg')
    pygame.mixer.music.play(-1)

    xiong = Xiong(windows)
    qiang = Qiang(windows)
    bullets = Group()
    sb = Score(windows)
    start_button = Button(windows,"Game_Start")

    game_active = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    xiong.moving_right = True
                if event.key == pygame.K_LEFT:
                    xiong.moving_left = True
                if event.key == pygame.K_UP:
                    xiong.moving_up = True
                if event.key == pygame.K_DOWN:
                    xiong.moving_down = True
                if event.key == pygame.K_SPACE:
                    fire_bullet(windows,xiong,bullets)
                if event.key == pygame.K_p:
                    game_active = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    xiong.moving_right = False
                if event.key == pygame.K_LEFT:
                    xiong.moving_left = False
                if event.key == pygame.K_UP:
                    xiong.moving_up = False
                if event.key == pygame.K_DOWN:
                    xiong.moving_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(mouse_x, mouse_y):
                    game_active = True


        if game_active:
            xiong.update()
            qiang.update()
            bullets.update()
            for bullet in bullets.copy():
                if bullet.rect.top <= 0:
                    bullets.remove(bullet)

            hit_qiang_bullet(qiang, bullets,sb)
            hit(qiang,xiong)
            drop(qiang)

        windows.fill(color)
        windows.blit(bp,(0,0))
        xiong.blitme()
        qiang.blitme()
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        sb.show_score()

        if not game_active:
            start_button.draw_button()
        pygame.display.flip()



game()


