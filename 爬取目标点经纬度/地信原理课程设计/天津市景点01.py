"""以下部分引入第三方包用于协程操作"""
# 从 gevent 库里导入 monkey 模块
import gevent
from gevent import monkey
monkey.patch_all()
# monkey.patch_all() 能把程序变成协作式运行，就是可以帮助程序实现异步。
import time
# 从 gevent 库里导入 queue 模块
from gevent.queue import Queue

"""以下部分引用用于爬虫部分"""
import requests
import  openpyxl
from  bs4 import  BeautifulSoup

"""爬虫部分代码"""
def spyder(uil, header):
    """
    此函数属于爬虫主体代码，用于获取网站资料
    :param uil:
    :param header:
    :return:
    """
    try:
        # 保存文件准备
        wb = openpyxl.Workbook()  # 打开一个工作文件，用于记录数据
        sheet = wb.active  # 活动表
        sheet.title = "天津市景点"
        t = ['景点名称', '区域', '级别', '标语']
        sheet.append(t)
        actions = requests.get(uil,headers=header)
        print(actions.status_code)
        actions.encoding ='utf-8'
        response_action = BeautifulSoup(actions.text,'html.parser')
        allmovie=response_action.find(class_='module-list')#所有的景点集
        movies = allmovie.find_all(class_='module-list-item')
        for movie in movies:
            spot = movie.find(class_='ml-info')
            title = spot.find('a', target="_blank")  #景点名称
            word = spot.find(class_='oneWords')  # 标语
            score = spot.find('dt').find_all('span')
            p = title.text
            n = score[0].text  # 区域
            m = score[1].text  # 等级
            w = word.text
            h=[p,n,m,w]
            sheet.append(h)
        path = '天津市景点/天津市各景点信息' + m[3:] + '.xlsx'
        wb.save(path)
        wb.close()
    except Exception as a:
        print(a)


"""协程部分代码"""
try:
    start = time.time()
    uil = 'https://www.bendi5.com/tianjin/jingdian/'  #需要请求的网站
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}  # 请求头
    url_list = []
    for i in range(3, 6):
        urlz = uil + str(i) + "a/"
        url_list.append(urlz)
    # 创建队列对象，并赋值给 work
    work = Queue()

    # 遍历 url_list
    for url in url_list:
        # 用 put_nowait() 函数可以把网址都放进队列里
        work.put_nowait(url)

    def crawler():
        """
        此函数用于调用爬虫部分代码，执行爬取网站数据信息并保存为文件
        :return:
        """
        # 当队列不是空的时候，就执行下面的程序
        while not work.empty():
            # 用 get_nowait() 函数可以把队列里的网址都取出
            url = work.get_nowait()
            # 以函数的形式将网站传入爬虫获取相应的数据资料
            spyder(url, header)




    # 创建空的任务列表
    tasks_list = []
    # 相当于创建了 3 个爬虫
    for x in range(2):
        # 用 gevent.spawn() 函数创建执行 crawler() 函数的任务
        task = gevent.spawn(crawler)
        # 往任务列表添加任务。
        tasks_list.append(task)
    # 用 gevent.joinall 方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站
    gevent.joinall(tasks_list)
    end = time.time()
    print(end - start)
except BaseException as err:
    print("协程程序出现错误\n{}".format(err))



