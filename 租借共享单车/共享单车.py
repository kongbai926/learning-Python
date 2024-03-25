import random


# 定义Bike类、属性和方法
class Bike:
	def __init__(self, no, age, state=0):
		self.no = no  # 车辆编号
		self.age = age  # 车辆运行年龄
		self.state = state  # 车辆状态,0代表休息，1代表工作

	def __str__(self):
		if self.state == 0:
			res = '此车辆可以借用！'
		elif self.state == 1:
			res = '此车辆正在借用中！'
		return '车辆号码: %d 车辆年龄: %d 车辆状态: %s' % (self.no, self.age, res)


# 定义主菜单，实现各功能与转换
class Massage:
	bike_list = []  # 用于储存车辆及其信息

	def __init__(self):
		for i in range(6):
			bike_ages = random.randint(0, 5)  # 车辆年龄
			bike_nos = 1000 + i  # 车辆编号
			bike = Bike(bike_nos, bike_ages)
			self.bike_list.append(bike)  # 实例化车辆，获取其相关信息

	def menu(self):  # 主菜单
		works = ["1、租用车辆", "2、分享车辆", "3、归还车辆", "4、退出"]
		while True:
			print('全部车辆：')
			for i in self.bike_list:
				print(i)  # 输出所有车辆信息
			for job in works:  # 输出菜单选项
				print(job)
			choose = int(input())
			if choose == 1:
				self.brow_bike()  # 借用车辆
			elif choose == 2:
				self.add_bike()  # 分享车辆
			elif choose == 3:
				self.reback_bike()  # 归还车辆
			elif choose == 4:
				print("感谢您的使用，下次再见！")
				break
			else:
				print('功能正在开发中，敬请期待…')

	def add_bike(self):  # 添加车辆
		bike_nos = int(input('车辆编号:'))
		bike_ages = int(input('车辆年龄:'))

		new_bike = Bike(bike_nos, bike_ages)
		self.bike_list.append(new_bike)  # 向车辆储存列表中添加车辆
		print("车辆添加成功！感谢您的共享！")

	def select_bike(self, no):  # 选择车辆
		for bk in self.bike_list:
			if no == bk.no:
				return bk

	def brow_bike(self):  # 借用车辆
		bike_nos = int(input('请输入车辆:'))
		bike = self.select_bike(bike_nos)  # 遍历车辆列表选择出来的车辆信息

		if bike != None and bike.state == 0:
			bike.state = 1
			print(bike, '\n车辆租用成功！祝您骑行愉快！')
		else:
			print('车辆不存在或已被租用！请重新输入车辆编号！')
			self.brow_bike()

	def reback_bike(self):  # 归还车辆
		bike_nos = int(input("车辆编号："))
		bike = self.select_bike(bike_nos)
		if bike != None and bike.state == 1:
			bike.state = 0
			print("车辆归还成功！")
		else:
			print("找不到车辆或车辆未被借用，请检查车辆编号是否输入正确！")


user = Massage()
user.menu()
