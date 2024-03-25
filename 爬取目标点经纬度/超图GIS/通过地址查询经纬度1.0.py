"""
采用协程的方式将获取地址经纬度任务添加到任务列表中并依次执行，提高效率；
对于未获取到值的情况，选择跳过的做法，以防止程序报错终止。
"""

import gevent
from gevent import monkey

monkey.patch_all()
# monkey.patch_all() 能把程序变成协作式运行，就是可以帮助程序实现异步。

import requests
# 获取地址经纬度
import json
import re
# 设置最大递归次数
import sys
# 读取Excel文档数据
import pandas as pd
# 创建协程，增加运行速度
from gevent.queue import Queue

sys.setrecursionlimit(10000)

# 获取Excel文件数据
Excles = pd.read_excel(r'D:\奇幻时空\Files\超图GIS\固定命题开发组数据\旅行社名录.xlsx', 'Sheet1')
Excles_location = Excles['地址']  # Excel文档中地址文字数据列表

# 创建队列对象，并赋值给 work
work = Queue()
# 遍历 地址列表
for locs in Excles_location:
    # 用 put_nowait() 函数可以把地址都放进队列里
    work.put_nowait(locs)

url = "https://restapi.amap.com/v3/place/text?s=rsv3" \
      "&children=&key=9705880d8f1826ed4f3e713b0069780d&jscode=fa4d7c3b6f512145ff3674271a5bd822&page=1" \
      "&offset=10&city=510100&language=zh_cn" \
      "&callback=jsonp_755735_" \
      "&platform=JS&logversion=2.0" \
      "&sdkversion=1.3" \
      "&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker" \
      "&csid=F028E84F-6601-43AE-88A8-13425E3DE7C7" \
      "&keywords="  # 在线地图的网址


def crawler():
    # 当队列不是空的时候，就执行下面的程序
    while not work.empty():
        # 用 get_nowait() 函数可以把队列里的网址都取出
        loc_wz = work.get_nowait()
        loc_url = url + loc_wz
        gets = get_get_location_m(loc_url)  # 返回地址经纬度

        if gets is None:
            continue
        else:
            gets_location = gets['location']
            gets_location_list = gets_location.split(',')
            dict_location['经度'].append(gets_location_list[1])
            dict_location['纬度'].append(gets_location_list[0])


# 获取传入地址的经纬度
def get_get_location_m(name):
    # 用 requests.get() 函数抓取网址
    res_text = requests.get(name).text  # 获取请求返回的response数据的文本数据
    if re.findall('"info":"OK"', res_text):  # 判断返回数据是否成功，成功便继续
        # res_data = json.loads(res_text.replace(re.findall("jsonp_\d+_\(", res_text)[0], "")[0:-1])["pois"][0]
        res_data = json.loads(res_text)
        item = {
            "name": res_data["name"],
            "type": res_data["type"],
            "location": res_data["location"],
            "pname": res_data["pname"],
            "cityname": res_data["cityname"],
            "adname": res_data["adname"]}  # 返回请求获得的数据，对其进行装饰，将name\localtion等数据进行赋值，便于后续应用与理解
        return item  # 返回
    else:  # 如果请求错误，则返回None
        return None


# 经纬度临时存储
dict_location = {'经度': [], '纬度': []}  # 临时存储查询到的经纬度

# 协程部分，开始所有协程任务
# 创建空的任务列表
tasks_list = []
# 相当于创建了 2 个爬虫
for x in range(5):
    # 用 gevent.spawn() 函数创建执行 crawler() 函数的任务
    task = gevent.spawn(crawler)
    # 往任务列表添加任务。
    tasks_list.append(task)
# 用 gevent.joinall 方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站
gevent.joinall(tasks_list)

# 数据处理并保存到文件中
# 字典转为DataFrame
Excel_location_data = pd.DataFrame(dict_location)
Excel_data = pd.concat([Excles, Excel_location_data], axis=1)
# 写入CSV文档
Excel_data.to_csv('旅行社目录.csv', encoding='utf-8')
print('程序运行成功！')
