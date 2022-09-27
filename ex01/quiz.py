import random
quiz = ["サザエの旦那の名前は？","カツオの妹の名前は？","タラオはカツオから見てどんな関係？"]
ans = [["ますお","マスオ"],["わかめ","ワカメ"],["甥","おい","甥っ子","おいっこ"]]
def shutudai():
    q = random.randint(0,2)
    print(f"問題\n{quiz[q]}")
    a = input("答え:")
    if a == ans[q][0] or a == ans[q][1]:
        print("seikai")
    else:
        print("fuseikai")

c = shutudai()

