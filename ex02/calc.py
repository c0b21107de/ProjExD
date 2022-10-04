import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"{txt}ボタンがクリックされました")

root = tk.Tk()
root.geometry("300x500")

j, k = 0, 0
for i, num in enumerate(range(9,-1,-1),1):
    button = tk.Button(root, text=f"{num}", font=("",30), width=4, height=2)
    button.bind("<1>",button_click)
    button.grid(row=j, column=k)
    k += 1
    if i%3 == 0:
        j += 1
        k = 0

root.mainloop()