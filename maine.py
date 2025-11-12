import pygame
import sys
pygame.init()
h,w = 800,600
sc = pygame.display.set_mode((h, w))
pygame.display.set_caption("kiki")
clock = pygame.time.Clock()


platform_sprites = [
    pygame.image.load("sprites/spr/zemlq1.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq2.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq3.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq4.png").convert_alpha(),
    pygame.image.load("sprites/spr/trava1.png").convert_alpha(),
    pygame.image.load("sprites/spr/trava2.png").convert_alpha(),
    pygame.image.load("sprites/spr/rock_fly1.png").convert_alpha(),
    pygame.image.load("sprites/spr/rock_fly2.png").convert_alpha()
]

class Platform:
    def __init__(self, x, y, w, h, sprite_index=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.sprite = pygame.transform.scale(platform_sprites[sprite_index], (w, h))

    def draw(self):
        sc.blit(self.sprite, self.rect)
class Player:
    def __init__(self):
        pass
    def draw(self):
        pass

class Enemy:
    def __init__(self):
        pass
    def draw(self):
        pass

class Button:
    def __init__(self,image,x,y,scale):
        wight = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(wight*scale,height*scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.cliked = False

    def draw(self, sc):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.cliked:
                action = True
                self.cliked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.cliked = False

        sc.blit(self.image,(self.rect.x,self.rect.y))
        return action

# здесь определяются константы, классы и функции
FPS = 60


bg = pygame.image.load("sprites/bg/bg_menu1.png").convert()
bg = pygame.transform.smoothscale(bg,(800,600))

bg_l1 = pygame.image.load("sprites/bg/bg_level1.png").convert()
bg_l1 = pygame.transform.smoothscale(bg_l1,(800,600))
bg_l2 = pygame.image.load("sprites/bg/bg_level2.png").convert()
bg_l2 = pygame.transform.smoothscale(bg_l2,(800,600))
bg_l3 = pygame.image.load("sprites/bg/bg_level3.png").convert()
bg_l3 = pygame.transform.smoothscale(bg_l3,(800,600))

pygame.display.update()

im_btm_ng = pygame.image.load("sprites/btm/btm_newgame.png").convert_alpha()
im_btm_prd = pygame.image.load("sprites/btm/btm_prodolj.png").convert_alpha()
im_btm_st = pygame.image.load("sprites/btm/btm_setting.png").convert_alpha()
im_btm_sprv = pygame.image.load("sprites/btm/btm_spravka.png").convert_alpha()
im_btm_ex = pygame.image.load("sprites/btm/btm_exit.png").convert_alpha()

im_btm_akk = pygame.image.load("sprites/btm/icon_akk.png").convert_alpha()
im_btm_stat = pygame.image.load("sprites/btm/icon_stat.png").convert_alpha()


#||||||||||||||||||||||||  MENU   ||||||||||||||||||||||||||||||||||||||||||||||
menu_st = "menu"
btm_ng = Button(im_btm_ng,300,90,0.8)
btm_prd = Button(im_btm_prd,300,175,0.8)
btm_st = Button(im_btm_st,300,265,0.8)
btm_sprv = Button(im_btm_sprv,300,350,0.8)
btm_ex = Button(im_btm_ex,300,435,0.8)

btm_akk = Button(im_btm_akk,55,420,0.25)
btm_stat = Button(im_btm_stat,55,470,0.25)

while True:
    sc.blit(bg, (0, 0))
    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()


    if menu_st =="menu":
        if btm_ng.draw(sc):
            menu_st = "main"
            print("new game")
        elif btm_prd.draw(sc):
            print("prodol")
        elif btm_st.draw(sc):
            menu_st = "setting"
            print("setting")
        elif btm_sprv.draw(sc):
            menu_st = "spravka"
            print("spravka")
        elif btm_akk.draw(sc):
            menu_st = "akk"
            print("akk")
        elif btm_stat.draw(sc):
            menu_st = "statistic"
            print("stst")
        elif btm_ex.draw(sc):
            print("exit")
            raise  SystemExit
    if menu_st == "main":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            menu_st = "menu"
            sc.blit(bg,(0,0))
        sc.blit(bg_l1,(0,0))
    elif menu_st == "setting":
        pass
    elif menu_st == "spravka":
        pass
    elif menu_st == "akk":
        pass
    elif menu_st == "akk":
        pass
    pygame.display.update()


#||||||||||||||||||||||||  тееееестт  ||||||||||||||||||||||||||||||||||||||||||||||
