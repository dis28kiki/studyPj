
import pygame
import sys
pygame.init()
h,w = 800,600
GRAVITY = 0.5
jump = 9
pl_sp = 3
sc = pygame.display.set_mode((h, w))
pygame.display.set_caption("Тайна земли")
clock = pygame.time.Clock()

green = (10,150,10)

def load_player_sor():
    sprites_pl = {}
    sprites_rl = {
        'idle_r1':'player_idle1.png',
        'idle_r2':'player_idle2.png',
        'idle_l1': 'player_idle_l1.png',
        'idle_l2': 'player_idle_l2.png',
        'run_r1': 'player_run_r1.png',
        'run_r2': 'player_run_r2.png',
        'run_l1': 'player_run_l1.png',
        'run_l2': 'player_run_l2.png',
        'jump_r1': 'player_jump_r_1.png',
        'jump_r2': 'player_jump_r_2.png',
        'jump_l1': 'player_jump_l_1.png',
        'jump_l2': 'player_jump_l_2.png'
    }
    for name,filename in sprites_rl.items():
        img = pygame.image.load(f'sprites/player/{filename}').convert_alpha()
        img = pygame.transform.scale(img, (80, 90))
        sprites_pl[name] = img

    return sprites_pl

kivi_spr = [
    pygame.image.load("sprites/kivi/idle1.png").convert_alpha(),
    pygame.image.load("sprites/kivi/idle2.png").convert_alpha(),
    pygame.image.load("sprites/kivi/idle3.png").convert_alpha()
]

belka_spr = [
    pygame.image.load("sprites/belka/idle1.png").convert_alpha(),
    pygame.image.load("sprites/belka/idle2.png").convert_alpha(),
    pygame.image.load("sprites/belka/idle3.png").convert_alpha()
]

kiki_spr = [
    pygame.image.load("sprites/kiki/kiki1.png").convert_alpha(),
    pygame.image.load("sprites/kiki/kiki2.png").convert_alpha(),
    pygame.image.load("sprites/kiki/kiki3.png").convert_alpha(),
]

platform_sprites = [
    pygame.image.load("sprites/spr/zemlq1.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq2.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq3.png").convert_alpha(),
    pygame.image.load("sprites/spr/zemlq4.png").convert_alpha(),
    pygame.image.load("sprites/spr/trava1.png").convert_alpha(),
    pygame.image.load("sprites/spr/trava2.png").convert_alpha(),
    pygame.image.load("sprites/spr/rock_fly1.png").convert_alpha(),
    pygame.image.load("sprites/spr/rock_fly2.png").convert_alpha(),
    pygame.image.load("sprites/spr/liana1.png").convert_alpha(),
    pygame.image.load("sprites/spr/liana2.png").convert_alpha()
]

class Platform:
    def __init__(self, x, y, w, h, sprite_index=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.sprite = pygame.transform.scale(platform_sprites[sprite_index], (w, h))

    def draw(self,surface):
        sc.blit(self.sprite, self.rect)

class Kivi:
    def __init__(self,x,y,w,h, sp_i = 0):
        self.rect = pygame.Rect(x,y,w,h)
        self.kivi_spr = pygame.transform.flip(kivi_spr[sp_i],False,False)
        self.sprite = pygame.transform.scale(self.kivi_spr, (w, h))
    def draw(self,surface):
        sc.blit(self.sprite,self.rect)

class Belka:
    def __init__(self,x,y,w,h, sp_i = 0):
        self.rect = pygame.Rect(x,y,w,h)
        self.belka_spr = pygame.transform.flip(belka_spr[sp_i],True,False)
        self.sprite = pygame.transform.scale(self.belka_spr, (w, h))
    def draw(self,surface):
        sc.blit(self.sprite,self.rect)

class Kiki:
    def __init__(self,x,y,w,h,sp_i=0):
        self.rect = pygame.Rect(x,y,w,h)
        self.sprite = pygame.transform.scale(kiki_spr[sp_i],(w,h))
    def draw(self,surface):
        sc.blit(self.sprite,self.rect)
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 35)
        self.vx = 0
        self.vy = 0
        self.on_gr = False
        self.spr = load_player_sor()

        self.state = "idle_r"
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.facing_right = True

    def update(self, pl):
        self.vy += GRAVITY

        self.rect.x += self.vx
        self.colliz(self.vx, 0, pl)

        self.rect.y += self.vy
        self.on_ground = False
        self.colliz(0, self.vy, pl)

        if not self.on_ground:
            if self.vy < 0:
                self.state = "jump_r" if self.facing_right else "jump_l"
            else:
                self.state = "jump_r" if self.facing_right else "jump_l"
        elif abs(self.vx) > 0:
            self.state = "run_r" if self.vx > 0 else "run_l"
            self.facing_right = self.vx > 0
        else:
            self.state = "idle_r" if self.facing_right else "idle_l"

    def colliz(self, vx, vy, platf):
        for pl in platf:
            if self.rect.colliderect(pl.rect):
                if vx > 0:
                    self.rect.right = pl.rect.left
                if vx < 0:
                    self.rect.left = pl.rect.right

                if vy > 0:
                    self.rect.bottom = pl.rect.top
                    self.on_ground = True
                    self.vy = 0
                if vy < 0:
                    self.rect.top = pl.rect.bottom
                    self.vy = 0

    def jump(self):
        if self.on_ground:
            self.vy = -jump

    def draw(self, surface):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.animation_frame = (self.animation_frame + 1) % 2

        frame_suffix = "1" if self.animation_frame == 0 else "2"

        if self.state.startswith("idle"):
            sprite_key = f"idle_{'r' if self.facing_right else 'l'}{frame_suffix}"
        elif self.state.startswith("run"):
            sprite_key = f"run_{'r' if self.facing_right else 'l'}{frame_suffix}"
        elif self.state.startswith("jump"):
            sprite_key = f"jump_{'r' if self.facing_right else 'l'}{frame_suffix}"
        else:
            sprite_key = "idle_r1"

        if sprite_key in self.spr:
            offset_x = (self.rect.width - 80) // 2
            offset_y = self.rect.height - 90
            surface.blit(self.spr[sprite_key], (self.rect.x + offset_x, self.rect.y + offset_y))



class AnimatedPlatform:
    def __init__(self, x, y, w, h, sprite_indices, animation_speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.frames = []
        for idx in sprite_indices:
            sprite = platform_sprites[idx]
            self.frames.append(pygame.transform.scale(sprite, (w, h)))
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()
        self.sprite = self.frames[self.current_frame]

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.sprite = self.frames[self.current_frame]

    def draw(self, surface):
        self.update()
        surface.blit(self.sprite, self.rect)

class AnimatedEnemy:
    def __init__(self, x, y, w, h, spr, sprite_indices, animation_speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.frames = []
        for idx in sprite_indices:
            sprite = spr[idx]
            self.frames.append(pygame.transform.scale(sprite, (w, h)))
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()
        self.sprite = self.frames[self.current_frame]

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.sprite = self.frames[self.current_frame]

    def draw(self, surface):
        self.update()
        surface.blit(self.sprite, self.rect)

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

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
platforms_zemlq = [
    AnimatedPlatform(0,550,50,50,[0,1,2,3,2,1],0.6),
    AnimatedPlatform(50, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(100, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(150, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(200, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(250, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(300, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(350, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(400, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(450, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(500, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(550, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(600, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(650, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(700, 550, 50, 50, [0,1,2,3,2,1],0.6),
    AnimatedPlatform(750, 550, 50, 50, [0,1,2,3,2,1],0.6),
    Platform(-49, 500, 50, 50, 0),
    Platform(-49, 450, 50, 50, 0),
    Platform(-49, 400, 50, 50, 0),
    Platform(-49, 350, 50, 50, 0),
    Platform(-49, 300, 50, 50, 0),
    Platform(-49, 250, 50, 50, 0),
    Platform(-49, 200, 50, 50, 0),
    Platform(-49, 150, 50, 50, 0),
    Platform(-49, 100, 50, 50, 0),
    Platform(-49, 50, 50, 50, 0),
    Platform(-49, 0, 50, 50, 0),
    Platform(799, 500, 50, 50, 0),
    Platform(799, 450, 50, 50, 0),
    Platform(799, 400, 50, 50, 0),
    Platform(799, 350, 50, 50, 0),
    Platform(799, 300, 50, 50, 0),
    Platform(799, 250, 50, 50, 0),
    Platform(799, 200, 50, 50, 0),
    Platform(799, 150, 50, 50, 0),
    Platform(799, 100, 50, 50, 0),
    Platform(799, 50, 50, 50, 0),
    Platform(799, 0, 50, 50, 0),
    Platform(0, -45, 50, 50, 0),
    Platform(50, -45, 50, 50, 0),
    Platform(100, -45, 50, 50, 0),
    Platform(150, -45, 50, 50, 0),
    Platform(200, -45, 50, 50, 0),
    Platform(250, -45, 50, 50, 0),
    Platform(300, -45, 50, 50, 0),
    Platform(350, -45, 50, 50, 0),
    Platform(400, -45, 50, 50, 0),
    Platform(450, -45, 50, 50, 0),
    Platform(500, -45, 50, 50, 0),
    Platform(550, -45, 50, 50, 0),
    Platform(600, -45, 50, 50, 0),
    Platform(650, -45, 50, 50, 0),
    Platform(700, -45, 50, 50, 0),
    Platform(750, -45, 50, 50, 0),
]

platforms_travka = [
    AnimatedPlatform(0, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(50, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(100, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(150, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(200, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(250, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(300, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(350, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(400, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(450, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(500, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(550, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(600, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(650, 500, 50, 50, [4, 5], 0.4),
    AnimatedPlatform(700, 500, 50, 50, [5, 4], 0.4),
    AnimatedPlatform(750, 500, 50, 50, [4, 5], 0.4),
]

platforms_sk_fly_levl3 = [
    Platform(70, 480, 40, 40, 6),
    Platform(110, 480, 40, 40, 7),
    Platform(140, 420, 40, 40, 6),
    Platform(180, 420, 40, 40, 7),
    Platform(220, 420, 40, 40, 7),
    Platform(270, 470, 40, 40, 6),
    Platform(320, 380, 40, 40, 7),
    Platform(360, 380, 40, 40, 6),
    Platform(400, 380, 40, 40, 7),
    Platform(480, 380, 40, 40, 7),
    Platform(560, 380, 40, 40, 6),
    Platform(600, 420, 40, 40, 6),
    Platform(640, 460, 40, 40, 7),
    Platform(680, 500, 40, 40, 7),
    Platform(600, 270, 40, 40, 7),
    Platform(640, 270, 40, 40, 6),
    Platform(680, 270, 40, 40, 7),
    Platform(560, 270, 40, 40, 6),
    Platform(480, 270, 40, 40, 6),
    Platform(400, 270, 40, 40, 7),
    Platform(320, 270, 40, 40, 7),
    Platform(280, 270, 40, 40, 6),
    Platform(200, 220, 40, 40, 6),
    Platform(160, 220, 40, 40, 7),
    Platform(100, 170, 40, 40, 6),
    Platform(60, 170, 40, 40, 7),
    Platform(180, 100, 40, 40, 7),
    Platform(260, 100, 40, 40, 6),
    Platform(340, 100, 40, 40, 7),
    Platform(380, 100, 40, 40, 7),
    Platform(420, 100, 40, 40, 7),
    Platform(460, 100, 40, 40, 7),
    Platform(500, 100, 40, 40, 7),
    Platform(540, 100, 40, 40, 7),
    Platform(580, 100, 40, 40, 7),
    Platform(660, 80, 40, 40, 7),
    Platform(700, 80, 40, 40, 7),
    Platform(740, 80, 40, 40, 7),

    AnimatedPlatform(725, 480, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 420, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 380, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 320, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 280, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 220, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(725, 180, 60, 60, [8, 9], 0.2),
]

platforms_sk_fly_levl2 = [
    Platform(100, 480, 40, 40, 6),
    Platform(220, 430, 40, 40, 7),
    Platform(270, 430, 40, 40, 6),
    Platform(320, 400, 40, 40, 7),
    Platform(360, 380, 40, 40, 6),
    Platform(400, 380, 40, 40, 7),
    Platform(440, 380, 40, 40, 6),
    Platform(480, 380, 40, 40, 7),
    Platform(560, 380, 40, 40, 6),
    Platform(600, 420, 40, 40, 6),
    Platform(640, 460, 40, 40, 7),
    Platform(680, 500, 40, 40, 7),
    Platform(600, 270, 40, 40, 7),
    Platform(640, 270, 40, 40, 6),
    Platform(680, 270, 40, 40, 7),
    Platform(560, 270, 40, 40, 6),
    Platform(520, 270, 40, 40, 6),
    Platform(480, 270, 40, 40, 6),
    Platform(360, 270, 40, 40, 6),
    Platform(400, 270, 40, 40, 7),
    Platform(320, 270, 40, 40, 7),
    Platform(280, 270, 40, 40, 6),
    Platform(200, 220, 40, 40, 6),
    Platform(160, 220, 40, 40, 7),
    Platform(100, 170, 40, 40, 6),
    Platform(60, 170, 40, 40, 7),
    Platform(180, 100, 40, 40, 7),
    Platform(220, 100, 40, 40, 6),
    Platform(260, 100, 40, 40, 6),
    Platform(340, 100, 40, 40, 7),
    Platform(380, 100, 40, 40, 7),
    Platform(420, 100, 40, 40, 7),
    Platform(460, 100, 40, 40, 7),
    Platform(500, 100, 40, 40, 7),
    Platform(540, 100, 40, 40, 7),
    Platform(580, 100, 40, 40, 7),
    Platform(660, 80, 40, 40, 7),
    Platform(700, 80, 40, 40, 7),
    Platform(740, 80, 40, 40, 7),

    AnimatedPlatform(730, 480, 60, 60, [8,9],0.2),
    AnimatedPlatform(730, 420, 60, 60, [8,9],0.2),
    AnimatedPlatform(730, 380, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(730, 320, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(730, 280, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(730, 220, 60, 60, [8, 9], 0.2),
    AnimatedPlatform(730, 180, 60, 60, [8, 9], 0.2),

]
platforms_sk_fly_levl1 = [
    Platform(60, 480, 40, 40, 6),
    Platform(140, 430, 40, 40, 6),
    Platform(180, 430, 40, 40, 7),
    Platform(220, 430, 40, 40, 7),
    Platform(270, 430, 40, 40, 6),
    Platform(320, 400, 40, 40, 7),
    Platform(360, 380, 40, 40, 6),
    Platform(400, 380, 40, 40, 7),
    Platform(440, 380, 40, 40, 6),
    Platform(480, 380, 40, 40, 7),
    Platform(560, 380, 40, 40, 6),
    Platform(620, 370, 40, 40, 7),
    Platform(680, 340, 40, 40, 7),
    Platform(600, 280, 40, 40, 7),
    Platform(730, 280, 40, 40, 7),
    Platform(560, 260, 40, 40, 6),
    Platform(520, 260, 40, 40, 6),
    Platform(480, 260, 40, 40, 6),
    Platform(360, 260, 40, 40, 6),
    Platform(400, 260, 40, 40, 7),
    Platform(320, 260, 40, 40, 7),
    Platform(280, 260, 40, 40, 6),
    Platform(200, 220, 40, 40, 6),
    Platform(160, 220, 40, 40, 7),
    Platform(100, 170, 40, 40, 6),
    Platform(60, 170, 40, 40, 7),
    Platform(20, 170, 40, 40, 7),

    Platform(180, 110, 40, 40, 7),
    Platform(220, 100, 40, 40, 6),
    Platform(260, 100, 40, 40, 6),
    Platform(340, 100, 40, 40, 7),
    Platform(380, 100, 40, 40, 7),
    Platform(420, 100, 40, 40, 7),
    Platform(460, 100, 40, 40, 6),
    Platform(500, 100, 40, 40, 6),
    Platform(540, 100, 40, 40, 7),
    Platform(580, 100, 40, 40, 7),
    Platform(660, 100, 40, 40, 6),
    Platform(700, 100, 40, 40, 7),
    Platform(740, 100, 40, 40, 6),

]

anim_kivi = AnimatedEnemy(700,45,65,65,kivi_spr,[0,1,2,1],0.3)
anim_belka = AnimatedEnemy(690,15,85,85,belka_spr,[1,0,2,0],0.15)
anim_kiki = AnimatedEnemy(700,20,75,75,kiki_spr,[1,0,2,0],0.19)

player = Player(20,500)
kivi = Kivi(700,45,65,65)
belka = Belka(690,15,85,85)
kiki = Kiki(700,20,75,75)
level = 0
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
        level = 1
        if keys[pygame.K_ESCAPE]:
            menu_st = "menu"
            sc.blit(bg, (0, 0))
        if level == 1:
            all_pl = platforms_zemlq+platforms_sk_fly_levl1
            player.update(all_pl)
            sc.blit(bg_l1, (0, 0))
            for platform_s_f in platforms_sk_fly_levl1:
                platform_s_f.draw(sc)
            anim_kivi.draw(sc)
        elif level==2:
            all_pl = platforms_zemlq+platforms_sk_fly_levl2
            player.update(all_pl)
            sc.blit(bg_l2, (0, 0))
            for platform_s_f in platforms_sk_fly_levl2:
                platform_s_f.draw(sc)
            anim_belka.draw(sc)
        elif level==3:
            all_pl = platforms_zemlq+platforms_sk_fly_levl3
            player.update(all_pl)
            sc.blit(bg_l3, (0, 0))
            for platform_s_f in platforms_sk_fly_levl3:
                platform_s_f.draw(sc)
            anim_kiki.draw(sc)
        for platform_z in platforms_zemlq:
            platform_z.draw(sc)
        for platform_t in platforms_travka:
            platform_t.draw(sc)


        if keys[pygame.K_LEFT]:
            player.vx = -pl_sp
            player.facing_right = False
        elif keys[pygame.K_RIGHT]:
            player.vx = pl_sp
            player.facing_right = True
        else:
            player.vx = 0

        if keys[pygame.K_UP]:
            player.jump()

        player.draw(sc)
    elif menu_st == "setting":
        pass
    elif menu_st == "spravka":
        pass
    elif menu_st == "akk":
        pass
    elif menu_st == "akk":
        pass
    pygame.display.update()