#//  https://docs.python.org/3.6/tutorial/introduction.html#strings


#//  python字符串支持单引号和双引号, 还可使用反斜线'\'转义
'spam eggs'  #单引号
"spam eggs"  #双引号
'doesn\'t'   #斜线'\'转义
'111\n222'

#// 可利用print函数输出字符串
s="-a"
print(s)
print("%s" % s)
print("%%")  #输出百分号%时需要使用"%%", 因%有特殊含义(即表示格式字符串)
student01, student02 = "Bob", "Alice"
print("%s and %s" % (student01, student02))

#// raw strings 原始字符串, 关闭了转义功能,通过在字符串常量的第一个引号前添加'r'(即单词raw的首字符)字符实现
r'C:\some\name'

#// 跨多行的字符串字面量，使用3重引号表示，如:  """...""" 或 '''...'''
print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")

#// + 操作符可用于简单的拼接或串联字符串
print('he' + 'llo')

#// * 操作符可用于字符串重复
print('-' * 100)

#// 毗邻的多个字符串字面量会自动地被拼接为一个字符串，该特性在编写代码时将长字符串断行写时很有用
'Py' 'thon'
text = ('Put several strings within parentheses '
            'to have them joined together.')
print(text)

#// 字符串可用下标索引(第一个字符的index为0), python没有独立的字符类型，a character is simply a string of size one
word = 'Python'
word[0]   # 'P'
word[5]   # 'n'

#// 下标也可以使用负数,从右侧开始算起, 注意：因为-0 等于 0, 所以负数的下标从 -1开始算起
word = 'Python'
word[-1]  # last character

#// 切片slice也得到了支持，既然索引是为了获取单个字符，那么切片slice就是为了获取字符串的子串
#// slice的下标还拥有很有用的默认值,第一个下标的缺失默认值为0，而第二个下标的缺失默认值为整个字符串的长度大小
word = 'Python'
word[0:2]  # 'Py'  即索引[0, 2)之间的字符串, 这种设计是为了满足效果：s[:i] + s[i:] is always equal to s
word[2:5]  # 'tho'
word[:2]   # 'Py'
word[4:]   # 'on'
word[-2:]  # 'on'

#// 对于索引字符的操作，如果下标越界，会产生‘string index out of range’这种索引越界的错误异常
#// 然而，slice操作却对索引越界的情况作了矫正处理，所以不会报出异常
word = 'Python'
#word[42]   # 错误异常：IndexError: string index out of range
word[4:42] # 'on'   <---此处slice对小标越界做了矫正处理
word[42:]  # ''

#// 字符串是不可变的(immutable), 这种效果和C语言一致,尝试给字符串指定下标位置赋值会导致错误异常
# word = 'Python'
# word[0] = 'J'  <--- TypeError: 'str' object does not support item assignment

#// 如果你想要一个不同的字符串，你可以基于现有的字符串的内容另起炉灶创造一个新的字符串：
word = 'Python'
'J' + word[1:]   # 'Jython'
word[:2] + 'py'  # 'Pypy'

#// 内置函数 len() 可以用来返回字符串的长度
s = 'supercalifragilisticexpialidocious'
len(s)  # 34
len('中文字符') # 4



#// 字符串的其他参考：
#//   https://docs.python.org/3.6/library/stdtypes.html#textseq
#//   https://docs.python.org/3.6/library/stdtypes.html#string-methods
#//   https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings
#//   https://docs.python.org/3.6/library/string.html#formatstrings







