import tkinter as tk
import maze_maker # pra8
from random import randint


def key_down(event):# pra5
    global key
    key = event.keysym


def key_up(event): # pra6
    global key
    key = ""


def main_proc(): # pra7
    global cx, cy
    global mx, my
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
    canv.coords("tori", cx, cy)
    root.after(100,main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") # pra1

    canv = tk.Canvas(root, width=1500, height=900, bg="black") # pra2
    canv.pack()

    # pra9
    maze_list = maze_maker.make_maze(15, 9)

    # pra10
    maze_maker.show_maze(canv, maze_list)

    # pra11
    mx, my = 1, 1

    random_image = randint(0,9)
    tori = tk.PhotoImage(file=f"fig/{random_image}.png") # pra3
    cx, cy = 300, 400
    canv.create_image(cx, cy, image=tori, tag="tori")

    # pra4
    key = "" # 現在押されているキーを表す

    # pra5
    root.bind("<KeyPress>", key_down)
    
    # pra6
    root.bind("<KeyRelease>", key_up)    
    
    # pra7
    main_proc()

    root.mainloop()