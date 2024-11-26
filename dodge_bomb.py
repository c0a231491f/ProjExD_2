import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数:こうかとんRect or ばくだんRect
    戻り値:真理値タプル（横, 縦) / 画面内ならTrue, 画面外ならFalse
    """
    yoko , tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface):
    """
    ゲームオーバー画面を表示する関数
    引数:ゲーム画面のSurfaceのオブジェクト
    戻り値:ゲームオーバー画面のブラックアウトSurfaceの位置情報
    """
    black_out = pg.Surface((WIDTH, HEIGHT)) # ブラックアウト用Surface
    pg.draw.rect(black_out, (0,0,0), (0, 0, 1100, 650))
    black_out_rct = black_out.get_rect()
    black_out_rct.center = WIDTH/2, HEIGHT/2
    black_out.set_alpha(128)
    screen.blit(black_out, black_out_rct)

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(txt, txt_rct)
    
    kkcry_img = pg.image.load("fig/8.png")
    kkcry_rct1 = kkcry_img.get_rect()
    kkcry_rct2 = kkcry_img.get_rect()
    kkcry_rct1.center = WIDTH/2-200, HEIGHT/2
    kkcry_rct2.center = WIDTH/2+200, HEIGHT/2
    screen.blit(kkcry_img, kkcry_rct1)
    screen.blit(kkcry_img, kkcry_rct2)

    pg.display.update()
    time.sleep(5)
    return black_out_rct


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大、加速する関数
    引数:なし
    戻り値:サイズの異なる爆弾Surfaceオブジェクトを要素とするリスト
           爆弾の加速度を示す整数値を要素とするリスト
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()  # 拡大爆弾と加速リストを初期化
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect() #爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # bb_rctの位置を表す変数に乱数を設定する
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, taple in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += taple[0]
                sum_mv[1] += taple[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾動く

        idx = min(tmr // 500, 9)  # 0～9の範囲でインデックスを選択
        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)  # 拡大・加速された速度で爆弾が動く

        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
