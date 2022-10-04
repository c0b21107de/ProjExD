import tkinter as tk
import tkinter.messagebox as tkm
from turtle import right

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    # tkm.showinfo(txt, f"{txt}ボタンがクリックされました")
    entry.insert(tk.END,f"{txt}")

root = tk.Tk()
root.geometry("300x500")

entry = tk.Entry(root, justify="right", font=("",40), width=10)
entry.grid(row=0, column=0, columnspan=3)

j, k = 1, 0 #jは行/kは列
for i, num in enumerate(range(9,-1,-1),1):
    button = tk.Button(root, text=f"{num}", font=("",30), width=4, height=2)
    button.bind("<1>",button_click)
    button.grid(row=j, column=k)
    k += 1
    if i%3 == 0:
        j += 1
        k = 0

plus = tk.Button(root,text="+",font=("",30),width=4,height=2)
plus.bind("<1>",button_click)
plus.grid(row=4, column=1)

root.mainloop()