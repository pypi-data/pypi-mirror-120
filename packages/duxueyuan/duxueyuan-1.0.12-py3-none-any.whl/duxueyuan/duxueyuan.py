import random
lyrics = ['寫信告訴我今天 海是什麼顏色\n',
	 '夜夜陪著你的海 心情又如何\n',
	 '灰色是不想說 藍色是憂鬱\n',
	 '而漂泊的你 狂浪的心 停在哪裡\n',
	 '寫信告訴我今夜 你想要夢什麼\n',
	 '夢裡外的我是否 都讓你無從選擇\n',
	 '我揪著一顆心 整夜都閉不了眼睛\n',
	 '為何你明明動了情 卻又不靠近\n',
	 '聽 海哭的聲音\n',
	 '嘆惜著誰又被傷了心 卻還不清醒\n',
	 '一定不是我 至少我很冷靜\n',
	 '可是淚水 就連淚水也都不相信\n',
	 '聽 海哭的聲音\n',
	 '這片海未免也太多情 悲泣到天明\n',
	 '寫封信給我 就當最後約定\n',
	 '說你在離開我的時候 是怎樣的心情\n',
	 '寫信告訴我今夜 你想要夢什麼\n',
	 '夢裡外的我是否 都讓你無從選擇\n',
	 '我揪著一顆心 整夜都閉不了眼睛\n',
	 '為何你明明動了情 卻又不靠近\n',
	 '聽 海哭的聲音\n',
	 '嘆惜著誰又被傷了心 卻還不清醒\n',
	 '一定不是我 至少我很冷靜\n',
	 '可是淚水 就連淚水也都不相信\n',
	 '聽 海哭的聲音\n',
	 '這片海未免也太多情 悲泣到天明\n',
	 '寫封信給我 就當最後約定\n',
	 '說你在離開我的時候 是怎樣的心情']
def intro(*args):
	print("你好我是杜学渊，很高兴认识你!\n")
	print("我有许多功能，你可以来试一试:\n")
	print("duxueyuan.speak()\nduxueyuan.sing()\nduxueyuan.calculate(1+1)\n")

def sing(*args):
	print("我想唱歌!")
	print(random.choice(lyrics))

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