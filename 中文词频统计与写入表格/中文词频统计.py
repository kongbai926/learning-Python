import jieba

txt = input("请输入文段：")
fuhaos = "\'/.,\\][-=+/*!@#$%^&*()<> \?\":;{}_~`，。、‘；、】【·.~！@#￥%……&*（）——{}|：“《》？"
for fuhao in fuhaos:
    txt = txt.replace(fuhao,"")
txts = jieba.lcut(txt)
words = {}
for i in txts:
    words[i] = words.get(i, 0) + 1
word_itme = list(words.items())
word_itme.sort(key=lambda x:x[1],reverse=True)