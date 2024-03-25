"""
采用异步发送请求的方式获取每个地址的经纬度，提高效率；
1、设置有异常处理机制，对于未获取到返回值的情况，程序可以自动进入等待，之后再次尝试获取；
多次未获取的值的情况，进行了赋值处理，使得程序不会报错的同时，可以查询到请求未成功的地址并进行针对性处理；
2、改正跳过操作致使的地址未获取到的同时不清楚是哪个地址未获取。
"""

import pandas as pd

# 获取Excel文件数据
Excles = pd.read_excel(r'D:\奇幻时空\Files\超图GIS\固定命题开发组数据\旅行社名录.xlsx', 'Sheet1')
# 景区地址文字
address = Excles['地址']

adds_list = []  # 处理后的地址。后续处理只针对这一个地址列表
for i, va in enumerate(address):
    dars_list = [i, va]

    adds_list.append(dars_list)

# 使用异步的方式发送请求，增加速度，也降低返回错误的风险
import aiohttp
import asyncio
import json

import nest_asyncio

nest_asyncio.apply()


async def fetch_location(address, key, max_tries=10, retry_delay=5):
    """
    异步获取地址的经纬度
    """
    url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address[1],
        'key': key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.text()
            data = json.loads(data)
            try:
                location = data['geocodes'][0].get('location', '0, 0')
                loc_list = location.split(',')
                return address[0], loc_list[1], loc_list[0]
            except (IndexError, KeyError):
                pass

            # 请求失败，等待一段时间后重试
            if max_tries > 1:
                await asyncio.sleep(retry_delay)
                return await fetch_location(address, key, max_tries - 1, retry_delay)
            else:
                return address[0], '未知', '未知'


#             尝试请求段的代码没有在Except中，也不会平白无故的执行或者正常情况下执行。当try正常运行时，会遇到return，及时退出函数，不会执行下面代码，因
# 此，正常完成情况下不会运行重试代码；若try出现问题，则会接着运行程序以下代码，途中没有遇到return，因此会执行“重试段代码”

async def main(addresses, key):
    """
    异步获取多个地址的经纬度
    """
    tasks = [fetch_location(addr_list, key) for addr_list in addresses]
    results = await asyncio.gather(*tasks)

    #     按照 id 的顺序排序
    results.sort(key=lambda x: x[0])
    return results


# 将程序传入地址查询经纬度的调用封装成函数，便于将地址数据分批次传入函数调用查询，防止文件符超出
import time


def Working(adds_list):
    key = '92c2ef077354043a4c3da1dd9cdf5f7e'
    addresses = adds_list
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(addresses, key))
    return results


#     分批次获取数据
def Go(n):
    # global adds_list

    result_table = pd.DataFrame()  # 初始化结果表格
    for i in range(n):
        if i + 1 != n:
            add_fd_list = adds_list[i * 500: 500 * (i + 1)]
        else:
            add_fd_list = adds_list[500 * i:]
        resu = Working(add_fd_list)
        time.sleep(3)  # 等待3秒，等待函数运行完成
        lc_table = pd.DataFrame(resu, columns=['id', '纬度', '经度'])
        result_table = pd.concat([result_table, lc_table], axis=0)
    return result_table


# 保存到文件
lc_table = Go(3)
lc_table = lc_table.reset_index(drop=True)  # 重置索引
re_table_loc = pd.DataFrame(lc_table.loc[: , ['经度', '纬度']], index=lc_table.loc[: , 'id'])
re_table = pd.concat([Excles, re_table_loc], axis=1)
re_table.to_excel('旅行社目录.xlsx', index=False)
