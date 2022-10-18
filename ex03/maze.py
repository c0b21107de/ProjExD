import tkinter as tk
import maze_maker # pra8
from random import randint


def count_up(): # 開始からの時刻を計測する
    global tmr,jid
    global mx, my
    tmr = tmr + 1
    label["text"] = tmr
    if mx == random_goal and my == 8: # ゴールで計測終了
        root.after_cancel(jid)
        jid = None
        return
    jid = root.after(1000, count_up)


def key_down(event):# pra5
    global key
    global random_start
    key = event.keysym


def key_up(event): # pra6
    global key
    key = ""


def main_proc(): # pra7
    global cx, cy
    global mx, my
    global tmr
    if key == "c": # ゴールまで直接行く
        mx = random_goal
        my = 8
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1
    if maze_list[my][mx] == 0:
        cx, cy = mx*100+50, my*100+50
    else:
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1
    if mx == random_goal and my == 8: # ゴールに到達したら終了
        canv.coords("tori", cx, cy)
        return
    canv.coords("tori", cx, cy)
    root.after(100,main_proc)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") # pra1

    canv = tk.Canvas(root, width=1500, height=900, bg="black") # pra2
    canv.pack()

    label = tk.Label(root, font=("", 30))
    label.pack()

    # pra9
    maze_list = maze_maker.make_maze(15, 9)
    random_start = randint(1,13)    # スタートとゴールを作成
    maze_list[0][random_start] = 0
    maze_list[1][random_start] = 0
    random_goal = randint(1,7)
    maze_list[8][random_goal] = 0
    maze_list[7][random_goal] = 0

    # pra10
    maze_maker.show_maze(canv, maze_list)

    # pra11
    mx, my = random_start, 0

    random_image = randint(0,9) # ランダムに画像を変える
    tori = tk.PhotoImage(file=f"fig/{random_image}.png") # pra3
    cx, cy = 300, 400
    canv.create_image(cx, cy, image=tori, tag="tori")
    
    tmr = 0
    jid = None
    jid = root.after(1000,count_up)

    # pra4
    key = "" # 現在押されているキーを表す

    # pra5
    root.bind("<KeyPress>", key_down)
    
    # pra6
    root.bind("<KeyRelease>", key_up)    
    
    # pra7
    main_proc()

    root.mainloop()