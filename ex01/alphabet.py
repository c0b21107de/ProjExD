import random
import time
w_c = 10 #対象文字の表示数
diff = 2 #差分の数

def list_difference(list1, list2):
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    return result

def lfa():
    t1 = time.time()
    a_l = []
    for i in range(w_c):
        r = chr(random.randint(65,90))
        a_l.append(r)
    display_l = random.sample(a_l,w_c-diff)
    diff_l = list_difference(a_l,display_l)
    print(f"対象文字:\n{a_l}")
    print(diff_l)
    print(f"表示文字:\n{display_l}\n")
    ans = int(input("欠損文字数を答えよ:"))
    if ans == diff:
        print("正解　具体的に　文字　答えよ")
        ans2 = input("1宇文字目（順不同）:")
        if ans2 == diff_l[0] or ans2 == diff_l[1]:
            ans3 = input("2文字目:")
            if ans3 == diff_l[0] or ans3 == diff_l[1]:
                print("daiseikai")
                t2 = time.time()
                el_t = t2-t1
                print(f"経過時間:{el_t}")
            else:
                print("最初からやり直し")
                y3 = lfa()
        else:
            print("最初からやり直し")
            y2 = lfa()
    else:
        print("最初からやり直し")
        y = lfa()

c = lfa()