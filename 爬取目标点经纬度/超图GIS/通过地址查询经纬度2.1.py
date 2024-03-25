"""
根据2.0改编；
采用一次性传入地址数据，控制异步请求数量的方法防止系统文件符过量；
在出现服务器响应错误的情况下不重新尝试请求，程序运行成功。但是结果存在大量的请求错误未获取到值；
在服务器响应出现错误时重新请求，程序出现了类似于死循环的结果之中，运行十分钟未出结果。
"""

import pandas as pd

# 获取Excel文件数据
Excles = pd.read_excel(r'D:\奇幻时空\Files\超图GIS\固定命题开发组数据\旅行社名录.xlsx', 'Sheet1')
# 景区地址文字
address = Excles['地址'][: 200]

adds_list = []  # 处理后的地址。后续处理只针对这一个地址列表
for i, va in enumerate(address):
    dars_list = [i, va]

    adds_list.append(dars_list)

# 使用异步的方式发送请求，增加速度，也降低返回错误的风险
import asyncio
import aiohttp

import nest_asyncio

nest_asyncio.apply()


async def get_location(address, key, semaphore, max_retry=3):
    url = "https://restapi.amap.com/v3/geocode/geo"
    param = {
        'address': address[1],
        'key': key
    }
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as response:
                data = await response.json()
                if data['status'] == '1' and data['geocodes']:
                    location = data['geocodes'][0].get('location', '0, 0')
                    return address[0], location[1], location[0]
                else:
                    # if max_retry > 0:
                    #     await asyncio.sleep(0.5)
                    #     return await get_location(address, key, semaphore, max_retry - 1)
                    # else:
                    print("请求地址：{} 失败，原因：{}".format(address, data['info']))
                    return address[0], '未知', '未知'


async def main(address_list, key, max_concurrency):
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [asyncio.ensure_future(get_location(address, key, semaphore)) for address in address_list]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    results.sort(key=lambda x: x[0], reverse=False)
    return results


if __name__ == '__main__':
    addresses = adds_list
    key = 'a047a3fcda80247621864b29205d2554'
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(addresses, key, 30))
    loop.close()
    # 保存到文件
    loc_tuple = pd.DataFrame(results, columns=['id', '纬度', '经度'])
    loc_tuple.to_excel('旅行社目录2.1.xlsx', index=False)
