import csv #引入csv模块
#import math #引入math模块
#from kkb_tools import open_file
#获取用户输入的贷款总额与贷款年限
total_loan = int(input('请输入贷款总额（贷款总额为整数）：'))
total_loan_year = int(input('银行贷款基准利率：1年期6.56%；2年期6.65%；3年期6.65%；4年期6.90%；5年期6.90%；请选择还款年限，输入数字即可：'))
#年利率
year_rate = 0
if total_loan_year==1: #1年期
    year_rate = 0.0656
elif 1<total_loan_year<=3: #2年期、3年期
    year_rate = 0.0665
elif 3<total_loan_year<=5: #4年期、5年期
    year_rate = 0.069
#月利率
month_rate = year_rate/12
#还款月数
loan_month = total_loan_year*12
#累计还款总额
sum_money = 0
#调用open()方法，文件名是detaillist.csv，追加模式"a", 文件名在代码中称为listfile
with open("车贷.csv","a",newline='',encoding='GBK') as listfile:
    #使用csv.writer（）函数创建writer对象，用于写入
    writer = csv.writer(listfile, dialect='excel')
    #列表头部第一行的字段
    header = ['期次','偿还本息（元）','偿还本金（元）','偿还利息（元）']
    # 使用writer对象写入表头
    writer.writerow(header)
    #循环计算所有月份的数据
    for i in range(1, loan_month + 1):
        print("第" + str(i) + "月还款情况")
        #每月还款总额
        month_money = (total_loan * month_rate * (1 + month_rate) ** loan_month) / (
                (1 + month_rate) ** loan_month - 1)
        #每月偿还本金
        month_capital = total_loan * month_rate * ((1 + month_rate) ** (i - 1)) / ((1 + month_rate) ** loan_month - 1)
        #每月偿还利息
        month_interest = month_money - month_capital
        #累计还款总额计算
        sum_money = sum_money+month_money
        print(month_money)
        print(month_capital)
        print(month_interest)
        writer.writerow([str(i)+"期", round(month_money,2), round(month_capital,2), round(month_interest,2)])
    #累计利息
    sum_interest = sum_money - total_loan
    print(sum_money)
    print(total_loan)
    print(sum_interest)
    #累计字段
    total_header = ['总期次', '累计还款总额', '所借本金', '累计支付利息']
    # 使用writer对象写入表头
    writer.writerow(total_header)
    #累计数据
    total_data = [str(loan_month)+"期次", round(sum_money,2), round(total_loan,2), round(sum_interest,2)]
    writer.writerow(total_data)
open("车贷.csv")