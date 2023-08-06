import random
def intro(*args):
	print("你好我是杜学渊，很高兴认识你!\n")
	print("我有许多功能，你可以来试一试:\n")
	print("duxueyuan.speak()\nduxueyuan.sing()\nduxueyuan.calculate(1+1)\n")

def sing(*args):
	print("我想唱歌!")
	ls = open("sea.txt").readlines()
	print(random.choice(ls))

def speak(*args):
	print("让我们来聊天吧!")
	print("烦恼是自找，快乐是忘怀")

def calculate(x):
	print("我数学不错呢!")
	try:
		if isinstance(x, float) or isinstance(x, int):
			pass
		else:
			x = eval(x)
	except:
		print("但是不好意思，这题我不会")
	else:
		print(x)
		print("我算的对不对？")	
	return x