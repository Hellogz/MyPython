def calc_huabei_minimum_repayment(overdraft, day, day_interest=0.0005, show_detail=False):
	"""
	该函数是：花呗最低还款后，计算累计天数后总共需要还的金额和每天的明细。
	"""
	interest = 0.0
	repayment = overdraft
	if day > 31:
		print("天数超过 31 天，花呗可能要求您先还一次款，所以本次只计数 31 天累计需要还款额。") 
		repayment_day = 31
	else:
		repayment_day = day
	for i in range(1, repayment_day + 1):
		interest = repayment * day_interest
		repayment += interest
		if show_detail:
			print("第 %d 天的利息：%f 元, 还款额：%f 元" %(i, interest, repayment))
	print("花呗 %f 元欠款选择最低还款，在 %d 天后总共要还：%f 元，其中利息总计：%f 元" %(overdraft, repayment_day, repayment, repayment-overdraft))
	return repayment

def get_a_float_number(prompt_information):
	"""
	该函数得到用户输入一个浮点数
	"""
	if type(prompt_information) != str:
		return 

	while True:
		float_number = input(prompt_information)
		try:
			float_number = float(float_number)
		except:
			print("请输入数字，可以带小数。")
		else:
			break
	return float_number

def get_a_int_number(prompt_information):
	"""
	该函数得到用户输入一个整数
	"""
	if type(prompt_information) != str:
		return 

	while True:
		int_number = input(prompt_information)
		try:
			int_number = int(int_number)
		except:
			print("请输入数字，不能带小数。")
		else:
			break
	return int_number

def function_test():
	"""
	测试 get_a_float_number、get_a_int_number、calc_huabei_minimum_repayment 函数
	"""
	overdraft = get_a_float_number("请输入花呗最低还款后的剩余还款金额：￥")
	day = get_a_int_number("请输入需要计算的天数：")
	day_interest = get_a_float_number("请输入花呗的日利率：%") / 100.0
	calc_huabei_minimum_repayment(overdraft, day, day_interest, show_detail=False)

  
if __name__ == '__main__':
	print("*" * 100 + "\r\n")
	while True:
		function_test()
		if input("\r\n\r\n本次计算完毕。按回车继续计算，输入任意字符加回车退出：") != "":
			break
		else:
			print("\r\n" + "*" * 100 + "\r\n")
