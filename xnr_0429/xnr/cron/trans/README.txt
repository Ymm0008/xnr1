使用方法：
from trans.trans import trans
q = ['안녕하세요.', 'Hello world','test']
print trans(q)


trans()函数可选参数target_language, 代表翻译成哪种语言。
目前支持：
	target_language='zh-cn'(默认参数)
	target_language='en'(英语)



原理：
依次调用google、baidu、youdao的翻译接口，哪一步成功就返回翻译结果，
或者不成功就使用下一个接口，直到最终所有接口失败。
其中baidu、youdao翻译使用的是官方给出的API，有调用限制，
google翻译使用的是https://github.com/ssut/py-googletrans破解得到的翻译接口。