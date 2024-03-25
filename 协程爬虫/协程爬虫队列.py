# 从 gevent 库里导入 monkey 模块
from gevent import monkey
import gevent
import time
import requests
# 从 gevent 库里导入 queue 模块
from gevent.queue import Queue

monkey.patch_all()
# monkey.patch_all() 能把程序变成协作式运行，就是可以帮助程序实现异步。
start = time.time()
url_list = [
    'https://www.baidu.com/', 'https://www.sina.com.cn/',
    'http://www.sohu.com/', 'https://www.qq.com/', 'https://www.163.com/',
    'http://www.iqiyi.com/', 'https://www.tmall.com/', 'http://www.ifeng.com/'
]
# 创建队列对象，并赋值给 work
work = Queue()

# 遍历 url_list
for url in url_list:
    # 用 put_nowait() 函数可以把网址都放进队列里
    work.put_nowait(url)


def crawler():
    # 当队列不是空的时候，就执行下面的程序
    while not work.empty():
        # 用 get_nowait() 函数可以把队列里的网址都取出
        url = work.get_nowait()
        # 用 requests.get() 函数抓取网址
        r = requests.get(url)
        # 打印网址、队列长度、抓取请求的状态码
        print(url, work.qsize(), r.status_code)


# 创建空的任务列表
tasks_list = []
# 相当于创建了 2 个爬虫
for x in range(2):
    # 用 gevent.spawn() 函数创建执行 crawler() 函数的任务
    task = gevent.spawn(crawler)
    # 往任务列表添加任务。
    tasks_list.append(task)
# 用 gevent.joinall 方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站
gevent.joinall(tasks_list)
end = time.time()
print(end - start)
