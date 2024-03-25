"""
04 将网址改为天津市旅游局网站进行数据收集。

运行成功！数据保存在./result_file/data.csv
"""

import time

import pandas as pd
import pretty_errors

# 帮助信息
pretty_errors.configure(
    separator_character='*',
    filename_display=pretty_errors.FILENAME_EXTENDED,
    line_number_first=True,
    display_link=True,
    lines_before=5,
    lines_after=2,
    line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
    code_color='  ' + pretty_errors.BLUE,
    truncate_code=True,
    display_locals=True
    )

"""以下部分引用用于爬虫部分"""
# 引用selenium处理动态网页
from selenium import webdriver

"""爬虫部分代码"""


def spyder(uil, header):
    """
    此函数属于爬虫主体代码，用于获取网站资料
    :param uil: 爬虫请求网址
    :param header: 浏览器请求头
    :return: 解析获取到的数据表
    """
    # 浏览器相关设置
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chromeDriver_path = r'C:\Users\asus\.cache\selenium\chromedriver\win64\123.0.6312.58\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_argument('User-Agent={}'.format(header['user-agent']))
    option.binary_location = chrome_path

    # 创建浏览器实例
    driver = webdriver.Chrome(options=option, executable_path=chromeDriver_path)
    # 使用浏览器请求网页
    driver.get(url=uil)
    time.sleep(2)  # 等待2秒，等待请求返回响应，提高请求成功率

    data_Table = driver.find_element_by_id('gjajlyjqml')  # 数据表格

    if data_Table:

        """
        解析数据与保存数据准备
        """
        # 将找到的元素提取其中的文本信息
        get_txt = lambda x: x.text
        # 保存数据表
        table_DATA = []

        # 解析数据表格
        thead_data = data_Table.find_element_by_tag_name('thead')  # 表头
        tbody_data = data_Table.find_element_by_tag_name('tbody')  # 表数据

        # 处理表头
        thead_data = thead_data.find_elements_by_tag_name('th')
        thead_list = [get_txt(ite) for ite in thead_data]  # 表头行

        table_DATA.append(thead_list)

        # 处理数据表
        tbody_data = tbody_data.find_elements_by_tag_name('td')  # 数据表单元格
        for ind in range(int(len(tbody_data) / 6)):
            line = tbody_data[ind * 6: ind * 6 + 6]  # 表格中一行数据
            table_DATA.append([get_txt(d) for d in line])

        """
        数据获取善后工作
        """
        driver.close()  # 关闭浏览器
        return table_DATA
    else:
        return None


"""程序开始工作代码"""
try:
    start = time.time()
    uil = 'http://whly.tj.gov.cn/WSBSYZXBS4230/WMFW8706/QYML408/202008/t20200817_3486782.html'  # 需要请求的网站
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }  # 请求头
    url_list = []
    url_list.append(uil)

    # 保存文件准备
    table_DataFrame = pd.DataFrame()  # 初始化数据表对象DataFrame

    for url in url_list:
        data = spyder(url, header)
        data = pd.DataFrame(data)
        table_DataFrame = pd.concat([table_DataFrame, data], ignore_index=True).reset_index(drop=True)

    table_DataFrame.columns = table_DataFrame.iloc[0]  # 将DataFrame中的第一行作为数据表表头
    table_DataFrame.drop(index=0, inplace=True)
    # 保存数据到CSV文件
    table_DataFrame.to_csv('./result_file/data.csv', encoding='gbk', index=False)
    end = time.time()
    print('花费时间{}'.format(end - start))
except Exception as err:
    raise Exception("程序出现错误\n{}\n".format(err), '>>>' * 20)
