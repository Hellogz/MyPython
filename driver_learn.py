from tkinter import *
import tkinter as tk
import random
import time
import os

light = {
	0: ("进入照明良好道路", "近光灯"), 
	1: ("夜间与机动车会车", "近光灯"),
	2: ("夜间同方向近距离行驶", "近光灯"),
	3: ("前方通过路口", "近光灯"),
	4: ("夜间没有路灯，照明不良条件下行驶", "远光灯"),
	5: ("夜间超越前方车辆", "闪灯"),
	6: ("夜间通过急弯、坡路、拱桥、没有交通信号灯控制的路口时", "闪灯"),
	7: ("路边临时停车", "示宽灯"),
	8: ("夜间在道路上发生故障", "示宽灯和危险报警闪光灯")
}

line_1 = {
	0: "起步",
	1: "靠边停车",
	2: "路口直行",
	3: "掉头",
	4: "路口左转",
	5: "直线行驶",
	6: "路口右转",
	7: "前方照明不良",
	8: "前方照明良好",
	9: "路口右转",
	10: "超车",
	11: "人行横道",
	12: "会车",
	13: "学校区域",
	14: "公共汽车站",
	15: "路口直行",
	16: "加减档项目",
	17: "路口右转",
	18: "变更车道",
	19: "路口右转",
	20: "终点"
}

line_3 = {
	0: "起步",
	1: "靠边停车",
	2: "路口直行",
	3: "掉头",
	4: "路口右转",
	5: "公共汽车站",
	6: "学校区域",
	7: "路口左转",
	8: "超车",
	9: "变更车道",
	10: "加减档项目",
	11: "人行横道",
	12: "直线行驶",
	13: "路口左转",
	14: "前方照明不良",
	15: "前方照明良好",
	16: "路口左转",
	17: "会车",
	18: "路口左转",
	19: "终点"
}

if __name__ == '__main__':
	while True:
		c = input("choice project 1: light, 2: line_1, 3: line_3, exit: other.")
		os.system('cls')
		if c == '1':
			while True:
				print("模拟灯光")
				for i in random.sample(range(len(light)), 5):
					print(light[i][0])
					input("enter show answer")
					print(light[i][0], light[i][1])
					input("enter next")
					os.system('cls')
				c = input("again y, exit other:")
				os.system('cls')
				if c.upper() != 'Y':
					break
		elif c == '2':
			while True:
				print("清湖考场线路一")
				for i in range(len(line_1)):
					print(line_1[i])
					input("enter next")
				c = input("again y, exit other:")
				os.system('cls')
				if c.upper() != 'Y':
					break
		elif c == '3':
			while True:
				print("清湖考场线路三")
				for i in range(len(line_3)):
					print(line_3[i])
					input("enter next")
				c = input("again y, exit other:")
				os.system('cls')
				if c.upper() != 'Y':
					break
		else:
			break
	
		
