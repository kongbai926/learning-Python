def zf(x, y):  # 自反性与反自反性
    s = 0
    k1 = list(set(x))
    k2 = list(set(y))
    for i in k1:
        if i not in k2:
            k2.append(i)
    print(k2)
    for i in range(len(x)):
        if x[i] == y[i]:
            s = s+1
    if s == len(k2):
        print("该关系有自反性。")
    else:
        print("该关系没有自反性。")
    if s == 0:
        print("该关系有反自反性。")
    else:
        print("该关系没有反自反性。")


# 对称性与反对称性
def dc(x, y):
    s = p = 0
    for i in range(len(x)):
        k1 = x[i]
        k2 = y[i]
        for m in range(len(y)):
            if y[m] == k1 and x[m] == k2:
                s = s+1
            if (y[m] == k1 and x[m] == k2 and y[m] == x[m]) or (k1 != k2 and ((y[m] == k1 and x[m] != k1) or (y[m] != k1 and x[m] == k1))):
                p = p + 1
    if s == len(x):
        print("该关系有对称性。")
    else:
        print("该关系没有对称性。")
    if p == len(x) :
        print("该关系有反对称性。")
    else:
        print("该关系没有反对称性。")
        print(p,len(x))

# 传递性
def chuandx(x, y):
    s = 0
    t = 0
    l = 0
    q = []
    for i in x:
        if i not in q:
            q.append(i)
    for i in y:
        if i not in q:
            q.append(i)
    jz = [[0] * len(q) for i in range(len(q))]
    for i in range(len(q)):
        h1 = q[i]
        for m in range(len(x)):
            x1 = x[m]
            if x1 == h1:
                y1 = y[m]
                for f in range(len(q)):
                    if y1 == q[f]:
                        jz[i][f] = 1
    print("该关系的关系矩阵为：")
    for i in jz:
        print(i)

    for i in range(len(x)):
        o = x[i]
        p = y[i]
        for g in range(len(y)):
            p1 = x[g]
            o1 = y[g]
            if p == p1:
                s = s+1
                for i1 in range(len(x)):
                    o2 = x[i1]
                    p2 = y[i1]
                    if o2 == o and p2 == o1:
                        t = t+1
                        break
    if l == s and s == t and t != 0:
        print("该关系有传递性。")
        print(t)
    else:
        print("该关系没有传递性。")
        print(s,t)


# 获取全部序偶
gxs = []
m = int(input("请输入序偶对数：\n"))
for i in range(m):
    guanx = []
    for m in range(2):
        y1 = input("请输入序偶第%d元素：\n" % (m+1))
        guanx.append(y1)
    gxs.append(guanx)
for i in range(len(gxs)):
    gs = gxs[i]
    x1 = gs[0]
    x2 = gs[1]
    print("(%c,%c)\t" % (x1, x2))  # 输出序偶
# 获取前域和后域
qy = []
hy = []
for i in gxs:
    qy.append(i[0])
    hy.append(i[1])
print(qy, hy)  # 打印前后域
# 判断是否有自反性、反自反性
zf(qy, hy)
# 判断对称性、反对称性
dc(qy, hy)
# 判断传递性
chuandx(qy,hy)
print('''运  行  结  束  ！''')
