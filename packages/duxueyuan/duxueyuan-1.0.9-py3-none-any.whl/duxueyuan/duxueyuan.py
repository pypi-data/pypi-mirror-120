def intro(*args):
	print("Hello, I am Du Xueyuan, Nice to have you here!\n")
	print("I have many functions, you can try all these:\n")
	print("duxueyuan.speak()\nduxueyuan.sing()\nduxueyuan.calculate(1+1)\n")

def sing(*args):
	print("I love to sing!")
	print("寫信告訴我今天 海是什麼顏色")

def speak(*args):
	print("Let me chat with you!")
	print("烦恼是自找，快乐是忘怀")

def calculate(x):
	print("I am a good mathematician!")
	print(eval(x))
	print("我算的对不对？")
	return eval(x)