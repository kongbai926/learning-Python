import  requests
import  openpyxl
from  bs4 import  BeautifulSoup
uil = 'https://v.qq.com/channel/movie?listpage=1&channel=movie&itype=100061'
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
try:
    actions = requests.get(uil,headers=header)
    print(actions.status_code)
    actions.encoding ='utf-8'
    response_action = BeautifulSoup(actions.text,'html.parser')
    wb = openpyxl.Workbook()
    sheet = wb.active
    t=['片名','主演','播放次数','影片时长','评分']
    sheet.append(t)
    lists = response_action.find(class_='mod_row_box')
    allmovie=lists.find(class_='mod_figure mod_figure_v_default mod_figure_list_box')#所有的电影箱子
    movies = allmovie.find_all(class_='list_item')
    for movie in movies:
        title = movie.find(class_='figure_detail figure_detail_two_row')
        number = movie.find(class_='figure_count')#播放次数
        actor = title.find('a')  # 片名
        tit = title.find(class_='figure_desc')  # 主演
        score = movie.find('a',class_="figure").find('div',class_='figure_score').text # 评分
        times = movie.find('a',class_="figure").find('div',class_='figure_caption').text # 影片时长
        p = actor.text
        n = tit.text
        m = number.text
        h=[p,n,m,times,score]
        sheet.append(h)
    for x in range(1,41):
        y=x*30
        uil2 = 'https://v.qq.com/x/bu/pagesheet/list?append=1&channel=movie&itype=100061&listpage=2&offset='+str(y)+'&pagesize=30'
        header2 = {
            'referer': 'https://v.qq.com/channel/movie?listpage=1&channel=movie&itype=100061',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }
        data = {
            'append': '1',
            'channel': 'movie',
            'itype': '100061',
            'listpage': ' 2',
            'offset': str(y),
            'pagesize': ' 30'}
        resques = requests.post(uil2,headers=header2,data=data)
        # print(resques.status_code)
        resques.encoding ='utf-8'
        respon = BeautifulSoup(resques.text, 'html.parser')
        movies = respon.find_all('div', class_="list_item")
        for movie in movies:
            title = movie.find(class_='figure_detail figure_detail_two_row')
            number = movie.find(class_='figure_count')  # 播放次数
            actor = title.find('a')  # 片名
            tit = title.find(class_='figure_desc')  # 主演
            score = movie.find('a', class_="figure").find('div', class_='figure_score').text # 评分
            times = movie.find('a', class_="figure").find('div', class_='figure_caption').text # 影片时长
            p = actor.text
            n = tit.text
            m = number.text
            h = [p, n, m,times,score]
            sheet.append(h)
    wb.save('腾讯视频动作类电影信息.xlsx')
    wb.close()
    print("爬取完成！")
except Exception as a:
    print(a)
