import sys
import pygame as pg
import random


class Screen:
    def __init__(self, title, width_height, background_image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(width_height)
        # self.color = color
        # self.sfc.fill(self.color)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(background_image)
        self.bgi_rct = self.bgi_sfc.get_rect()
    def blit(self):
        # self.sfc.fill(self.color)
        # self.sfc.blit(self.sfc, self.rct)
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)

class Line:
    def __init__(self,width, height, scr:Screen):
        self.sfc = pg.Surface((width, height))
        self.rct = self.sfc.get_rect()
        self.rct.move_ip(scr.rct.width/2,0)
        pg.draw.line(self.sfc,(255,255,255),(scr.rct.width/2,5),(scr.rct.width/2,scr.rct.height-5),10)

        # self.rct = self.sfc.get_rect()
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

class Ball:
    def __init__(self, color, radius, scr:Screen):
        speed = [-1, 1]
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius,radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = scr.rct.width/2
        self.rct.centery = random.randint(0,scr.rct.height)
        rand1 = random.choice(speed)
        rand2 = random.choice(speed)
        self.vx, self.vy = rand1, rand2  # 練習6

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr)


class Player:
    def __init__(self, color, width, height, xy):
        self.sfc = pg.Surface((width, height))
        pg.draw.rect(self.sfc, color, (width, height, width, height), 10)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vx, self.vy = 0, +1

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]:
            self.vy = -1
            self.rct.move_ip(self.vx, self.vy)
            if check_bound(self.rct, scr.rct) != 1:
                self.vy = 0
                self.rct.move_ip(self.vx, self.vy)
        if key_states[pg.K_DOWN]:
            self.vy = 1
            self.rct.move_ip(self.vx, self.vy)
            if check_bound(self.rct,scr.rct) != 1:
                self.vy = 0
                self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)


class Enemy:
    def __init__(self, color, width, height, xy):
        self.sfc = pg.Surface((width, height))
        pg.draw.rect(self.sfc, color, (width, height, width, height), 10)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vx, self.vy = 0, +1

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr)


class Score:
    def __init__(self, p_score, e_score, ball:Ball, scr:Screen):
        self.p_score = p_score
        self.e_score = e_score
        self.font = pg.font.SysFont(None,80) 

    def blit(self, scr:Screen):
        scr.sfc.blit(self.font.render(str(self.p_score), True,(255,255,255)),(scr.rct.width/4,10.))
        scr.sfc.blit(self.font.render(str(self.e_score), True,(255,255,255)),(scr.rct.width*3/4,10.))
    
    def update(self, ball:Ball, scr:Screen):
        p_score, e_score = score(ball.rct.centerx, self.p_score, self.e_score, scr)
        self.p_score = p_score
        self.e_score = e_score
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    tate = +1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return tate


def score(ball, p_score, e_score, scr:Screen):
    if ball < 0:
        e_score += 1
    if ball > scr.rct.width:
        p_score += 1
    return p_score, e_score


def main():
    scr = Screen("PingPong", (1600, 800),"fig/pg_bg.jpg")
    line = Line(15, scr.rct.height, scr)
    ball = Ball((255, 0, 0), 10, scr)
    player = Player((255, 255, 255), 15, 70, (15, scr.rct.height/2))
    enemy = Enemy((255, 255, 255), 15, 70, (scr.rct.width-15, scr.rct.height/2))
    score = Score(0, 0, ball, scr)
    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit()
        line.blit(scr)
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        ball.update(scr)
        player.update(scr)
        enemy.update(scr)
        score.update(ball, scr)
        if ball.rct.colliderect(enemy.rct): # こうかとんrctが爆弾rctと重なったら
            ball.vx *= -1
        if ball.rct.colliderect(player.rct):
            ball.vx *= -1
        
        if ball.rct.centerx < 0 or ball.rct.centerx > scr.rct.width:
            ball = Ball((255, 0, 0), 10, scr)
        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()