import 中文词频统计 as zw
import csv

with open("中文词频统计.csv","w") as file:
    files = csv.writer(file)
    for i in zw.word_itme:
        files.writerow(i)
print("运行结束！")