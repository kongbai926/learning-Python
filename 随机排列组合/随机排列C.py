# 处理n * (n -1) * (n - 2) *.........* m
def cj(n, m):
    if n == m:
        return 1
    else:
        return n * cj(n - 1, m)


# 处理随机排列
def c(a, b):
    x = cj(a, a - b)
    y = cj(b, 1)
    return x / y

lies = list(map(int, input('请输入n，m。以”，“分隔：').split('，')))
x = c(lies[0], lies[1])
print('{:0}'.format(x))
