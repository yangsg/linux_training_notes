import re

#// https://docs.python.org/3.6/tutorial/stdlib.html#string-pattern-matching

#// String Pattern Matching

result = re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
print(result)       #// ['foot', 'fell', 'fastest']
print(type(result)) #// <class 'list'>

result = re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat')
print(result)       #// cat in the hat
print(type(result)) #// <class 'str'>

#// 如果只是简单地替换，可以直接使用str 自己的 method
result = 'tea for too'.replace('too', 'two')
print(repr(result))  #// 'tea for two'




