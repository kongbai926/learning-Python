# 道格拉斯-普克算法是线的化简算法
# 第一：取出首尾两个点，保存
# 第二：计算每个点到首尾连线的距离
# 第三：存距离最大且符合要求的点
# 第四：计算每个点到由首尾两点与距离最大的点构成的两段线段的距离
# 重复以上

import turtle

# 计算点与点之间的距离
def juli(x1, y1, x2, y2):
    # pow(a, b)计算a的b次方
    dic = pow((x1 - x2), 2) + pow((y1 - y2), 2)
    docs = pow(dic, 0.5)
    return docs


# 计算三角形面积
def s_s(x, y, z):  # x y z 为三角形边长
    c = 1 / 2 * (x + y + z)
    s = pow((c * (c - x) * (c - y) * (c - z)), 0.5)
    return s


# 通过面积求点到线的距离
def p_c(s, line_c):  # s为面积，line_c表示线的长度
    point_h = 2 * s / line_c
    return point_h


# 主程序

point_list = []  # 原线段的点
while 1:
    point = input('请输入线段上的各点坐标，以“,”分隔,输入n结束：')

    if point == 'n':
        break
    else:
        points = list(map(int, point.split(',')))
        point_list.append(points)
Nob = int(input('请输入标准值：'))  # 对比值

if point_list:
    # 初始化 趋势线上的点及位置
    point_index_list = [list((point_list[0], 0)), list((point_list[-1], point_list.index(point_list[-1])))]  # 坐标&索引 列表

    # 流程循环
    while 1:
        point_max = []
        for line in range(len(point_index_list) - 1):
            point_start_index = point_index_list[line][1]
            point_end_index = point_index_list[line + 1][1]
            point_2 = point_list[point_start_index: point_end_index + 1]  # 过程量，对原线段分段

            d_list = []  # 符合点的距离集合
            d_index_list = []  # 符合点的索引列表
            point0 = point_2[0]  # 起点
            point1 = point_2[-1]  # 始点
            x = juli(point0[0], point0[1], point1[0], point1[1])  # 起始连线距离
            for po in point_2:
                a = juli(point0[0], point0[1], po[0], po[1])
                b = juli(point1[0], point1[1], po[0], po[1])
                if a == 0 or b == 0:
                    continue
                else:
                    s_sjx = s_s(x, a, b)
                    h_point = p_c(s_sjx, x)
                    if h_point >= Nob:
                        d_list.append(h_point)
                        d_index_list.append(point_list.index(po))
            # 第三
            if d_list:
                max_d = max(d_list)  # 最大距离
                index_max_0 = d_list.index(max_d)  # 最大距离的在d_list中的索引，对应在d_index_list中的索引
                index_max = d_index_list[index_max_0]  # 取出最大值在point_list中应该对应的索引
                point_max = point_list[index_max]  # 距离最大的点的坐标
                point_index_list.append(list((point_max, index_max)))  # 存入最大值点的坐标和对应的索引
            point_index_list.sort(key=lambda x: x[1])
        if not point_max:
            break
    print("原线上的点[x坐标,y坐标]：" + str(point_list),"\n趋势线上的点[[x坐标,y坐标],点的序号-1]：" + str(point_index_list))

    # 根据点的坐标画图

    # 绿色-原线段
    turtle.speed(3000)
    turtle.pencolor('green')
    for po in point_list:
        if point_list.index(po) == 0:
            turtle.penup()
            turtle.goto(po)
            turtle.pendown()
            continue
        else:
            turtle.goto(po)

#     红色-趋势线
    turtle.pencolor('red')
    for po in point_index_list:
        if point_index_list.index(po) == 0:
            turtle.penup()
            turtle.goto(po[0])
            turtle.pendown()
        else:
            turtle.goto(po[0])
else:
    print("线段未输入！")