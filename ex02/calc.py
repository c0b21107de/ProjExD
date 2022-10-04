import tkinter as tk
import tkinter.messagebox as tkm
import re

# buttonをクリックしたら数字や記号を返す関数
def button_click(event):
    btn = event.widget
    txt = btn["text"]
    if txt == "c": # cボタンが押された場合
        entry.delete(0,tk.END)
    else:
        entry.insert(tk.END,f"{txt}")

# totalを求める関数
def button_total(event):
    total = entry.get()
    if (re.search("\d", total) == None): # 入力式に数字が含まれているかの判定
        entry.delete(0,tk.END)
        tkm.showwarning("警告","数字が含まれていません")
    else:
        total = eval(total)
        entry.delete(0,tk.END)
        entry.insert(tk.END,f"{total}")

root = tk.Tk()
root.geometry("400x600") # 画面の大きさ

entry = tk.Entry(root, justify="right", font=("",50), width=10)
entry.grid(row=0, column=0, columnspan=4)

j, k = 1, 0 #jは行/kは列
for i, num in enumerate(range(9,-1,-1),1):
    button = tk.Button(root, text=f"{num}", font=("",30), width=4, height=2)
    button.bind("<1>",button_click)
    button.grid(row=j, column=k)
    k += 1
    if i%3 == 0:
        j += 1
        k = 0

#00,"."ボタンの追加
zzp = ["00","."]
for i in zzp:
    button_ZZ = tk.Button(root,text=f"{i}",font=("",30),width=4,height=2)
    button_ZZ.bind("<1>",button_click)
    button_ZZ.grid(row=j, column=k)
    k += 1

# plus,minus,times,dividedボタンの追加
fao = ["+", "-", "*", "/"]
r, c = 1, 3 #rは行/cは列
for i in fao:
    fao_ = tk.Button(root,text=f"{i}",font=("",30),width=4,height=2)
    fao_.bind("<1>",button_click)
    fao_.grid(row=r, column=c)
    r += 1

# clearボタンの追加
clear = tk.Button(root, text="c",font=("",30),width=4,height=2)
clear.bind("<1>",button_click)
clear.grid(row=5, column=2)

# eqボタンの追加
eq = tk.Button(root, text="=",font=("",30),width=4,height=2)
eq.bind("<1>",button_total)
eq.grid(row=r, column=c)

root.mainloop()