"""
功能：删除指定路径下的所有空文件夹，不会删除文件
注意！！！删除的文件夹不是移动的"回收站"，直接从电脑上完全删除，无法恢复！请谨慎使用！
"""
import os


def mains(contents):
    if os.path.isdir(contents):    # isdir用于判断路径是否为目录，是目录的话需要进一步的循环读取
        if not os.listdir(contents):
            try:
                # 删除
                os.rmdir(contents)  # 如果rmdir得到的路径是非空文件夹，会抛出异常
                print('已删除空文件夹: ', contents)
            except Exception as e:
                print(e)
        else:
            for i in os.listdir(contents):
                # 含多层级文件目录，所以需要不停的更新
                mains(os.path.join(contents, i))


# 传入路径
path = input("请输入路径：")
mains(path)
print("运行完成！")
