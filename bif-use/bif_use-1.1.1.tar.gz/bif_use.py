"""这是“bif_use.py”模块，提供了一个print_lol()的函数用来打印列表，其中包含或不包含嵌套列表。"""
def print_lol(the_list, indent=False, level=0):
	"""这个函数有一个位置参数，名为“the_list”,这可以是任何Python列表（包含或不包含嵌套列表），
		所提供列表中的各个数据项会（递归地）打印到屏幕上，而且各站一行,
		第二个参数名为“indent”，用来表示在遇到嵌套列表时选择是否缩进，默认不缩进，
		第三个参数名为“level”，用来在遇到嵌套列表时插入制表符。"""
	for item in the_list:
		if(isinstance(item,list)):
			print_lol(item, indent, level+1)
		elif indent:		
			#使用level的值来控制使用多少个制表符
			for tab_stop in range(level):
				#每一层缩进显示一个tab制表符
				print("\t", end='')
			#下面这一句可以代替上面的for循环	
			#print("\t" * level, end='')
			print(item)
		else:
			print(item)

#在IDLE上运行这句话才会显示结果
dir(__builtins__)