import pygame as pg
import sys
import random
import time

# pra7
def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct、または、爆弾rct
    scr_rct：スクリーンrct
    領域内：+1
    領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def gameover(): # gameover画面の追加
    """
    ゲームオーバー画面の表示
    c：コンテニュー
    escape：終了
    """
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/gameover.png")
    bg_rct = bg_sfc.get_rect()
    tori_sfc = pg.image.load("fig/8.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 4.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 800, 450
    clock =pg.time.Clock()
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        scrn_sfc.blit(tori_sfc, tori_rct)
        key_state = pg.key.get_pressed()
        if key_state[pg.K_c]: # コンテニュー
            main()
            return
        if key_state[pg.K_ESCAPE]:
            return
        pg.display.update()
        clock.tick(1000)


        

def main():
    # pra1
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    # pra3
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    # pra5
    bomb_sfc = pg.Surface((20,20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx, bomb_rct.centery = random.randint(10, scrn_rct.width), random.randint(0, scrn_rct.height)
    # 爆弾2の追加
    bomb_sfc2 = pg.Surface((20,20))
    bomb_sfc2.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc2, (255, 0, 0), (10, 10), 10)
    bomb_rct2 = bomb_sfc2.get_rect()
    bomb_rct2.centerx, bomb_rct2.centery = random.randint(10, scrn_rct.width), random.randint(0, scrn_rct.height)

    # pra6
    vx, vy = +1, +1
    vx2, vy2 = +1, +1 
    clock = pg.time.Clock()
    # pra2
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        # pra4
        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]:
            tori_rct.centery -= 1
        if key_states[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_states[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_states[pg.K_RIGHT]:
            tori_rct.centerx += 1
        
        # pra7
        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if key_states[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_states[pg.K_RIGHT]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_states[pg.K_UP]:
                tori_rct.centery += 1
            if key_states[pg.K_DOWN]:
                tori_rct.centery -= 1
        scrn_sfc.blit(tori_sfc, tori_rct)
        
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        if yoko == -1: # 爆弾の加速
            yoko -= 0.5
            tate += 0.5

        if tate == -1: # 爆弾の加速
            yoko += 0.5
            tate -= 0.5

        vx *= yoko
        vy *= tate

        yoko2, tate2 = check_bound(bomb_rct2, scrn_rct) # 爆弾2の動作
        if yoko2 == -1: # 爆弾の加速
            yoko2 -= 0.2
            tate2 += 0.2

        if tate2 == -1: # 爆弾の加速
            yoko2 += 0.2
            tate2 -= 0.2
        vx2 *= yoko2
        vy2 *= tate2

        if key_states[pg.K_1]: # 押している間しか見ることができない爆弾の
            scrn_sfc.blit(bomb_sfc2, bomb_rct2)
            
        
        bomb_rct.move_ip(vx, vy)
        bomb_rct2.move_ip(vx2, vy2)
        scrn_sfc.blit(bomb_sfc, bomb_rct)

        # pra8
        if tori_rct.colliderect(bomb_rct) or tori_rct.colliderect(bomb_rct2): # 爆弾に当たった瞬間gameover画面を表示
            if key_states[pg.K_p]:
                pass
            else:
                gameover()
                return
        

        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()