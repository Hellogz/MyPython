def show_heart_rate(old):
	print("年龄:%d 最大心率:%d次/分钟\n" %(old, (220-old)))
	print("|心率范围|好处|维持的活动时间|")
	print("|---|---|---|")
	print("|%d次~%d次|恢复、重新运动|20分钟~40分钟|" %((220-old)*0.5, (220-old)*0.6))
	print("|%d次~%d次|减肥|40分钟~80分钟|" %((220-old)*0.6, (220-old)*0.7))
	print("|%d次~%d次|提高状态|10分钟~40分钟|" %((220-old)*0.7, (220-old)*0.8))
	print("|%d次~%d次|提高绩效|2分钟~10分钟|" %((220-old)*0.8, (220-old)*0.9))
	print("|增加到%d次|让速度最大提升|少于5分钟|" %((220-old)*0.9))
  
if __name__ == "__main__":
  show_heart_rate(20)
