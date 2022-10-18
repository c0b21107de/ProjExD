import tkinter as tk
import maze_maker

def key_down(event):#pra5
    global key
    key = event.keysym


def key_up(event): #pra6
    global key
    key = ""


def main_proc(): #pra7
    global cx, cy
    if key == "Up":
        cy -= 20
    if key == "Down":
        cy += 20
    if key == "Left":
        cx -= 20
    if key == "Right":
        cx += 20
    canv.coords("tori", cx, cy)
    root.after(100,main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") # pra1

    canv = tk.Canvas(root, width=1500, height=900, bg="black") # pra2
    canv.pack()

    tori = tk.PhotoImage(file="fig/5.png") # pra3
    cx, cy = 300, 400
    canv.create_image(cx, cy, image=tori, tag="tori")

    #pra4
    key = "" # 現在押されているキーを表す

    #pra5
    root.bind("<KeyPress>", key_down)
    
    #pra6
    root.bind("<KeyRelease>", key_up)    
    
    #pra7
    main_proc()

    root.mainloop()