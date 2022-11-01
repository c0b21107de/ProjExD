import sys
from random import randint
import pygame as pg
import os
import random
import time


main_dir = os.path.split(os.path.abspath(__file__))[0]


SCREENRECT = pg.Rect(0, 0, 640, 480)

# 画面の表示
class Screen:
    
    def __init__(self, title, width_height, background_image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(width_height)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(background_image)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


# こうかとんの表示
class Bird:
    
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy):
        self.sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # 練習7
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)


# 爆弾の表示
class Bomb:

    def __init__(self, color, radius, speed, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius,radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = speed # 練習6

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr)


# 敵の表示
class NewEnemy:

    def __init__(self, enemy_image, xy, speed):
        self.sfc = pg.image.load(enemy_image)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vx, self.vy = speed

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.vx += 0.3
        self.vy += 0.3
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr)


# gameoverクラス
class GameOver:

    def __init__(self, title, width_height, background_image, kokaton_image, tori_location):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(width_height)
        self.rct = self.sfc.get_rect()
        self.bg_sfc = pg.image.load(background_image)
        self.bg_rct = self.bg_sfc.get_rect()
        self.tori_sfc = pg.image.load(kokaton_image)
        self.tori_sfc = pg.transform.rotozoom(self.tori_sfc, 0, 4.0)
        self.tori_rct = self.tori_sfc.get_rect()
        self.tori_rct.center = tori_location

    def blit(self):
        self.sfc.blit(self.bg_sfc, self.bg_rct)
        self.sfc.blit(self.tori_sfc, self.tori_rct)


class Shot():
    """a bullet the Player sprite fires."""
    def __init__(self, color, radius, speed, scr:Screen, bird:Bird):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = speed # 練習6
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        self.vx = +1
        self.vy = +1
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


# 画像の読み込み
def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()


# 音の読み込み
def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


# gameover画面の追加
def gameover():
    """
    ゲームオーバー画面の表示
    """
    g_scr = GameOver("GameOver", (1600, 900), "fig/gameover.png", "fig/8.png", (800, 450))
    clock =pg.time.Clock()
    while True:
        g_scr.blit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        key_state = pg.key.get_pressed()
        if key_state[pg.K_c]: # コンテニュー
            main()
            return
        if key_state[pg.K_ESCAPE]:
            return
        pg.display.update()
        clock.tick(1000)


def main():
    # 練習1
    scr = Screen("負けるな！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    # 練習3
    tori = Bird("fig/6.png", 2.0, (900, 400))

    # 練習5
    bomb = Bomb((255, 0, 0), 10, (+1, +1), scr)

    # newenemy
    ney = NewEnemy("ex05/data/alien1.jpg", (40, 40), (+1, +1))

    # shot
    shot = Shot((255, 255, 255), 10, (+1, +1), scr, tori)

    # sound
    boom_sound = load_sound("boom.wav")
    # shoot_sound = load_sound("car_door.wav")
    
    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        tori.update(scr)

        bomb.update(scr)

        ney.update(scr)

        key_state = pg.key.get_pressed()
        if   key_state[pg.K_SPACE]:
            shot.update(scr)
            # if shot.rct.colliderect(bomb.rct):
            #     time.sleep(100)
                
            # if shot.rct.collidedict(ney.rct):
            #     time.sleep(100)

        boom_sound.play()
        # 練習8
        if tori.rct.colliderect(bomb.rct): # こうかとんrctが爆弾rctと重なったら
            gameover()
            return

        if tori.rct.colliderect(ney.rct):
            gameover()
            return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
