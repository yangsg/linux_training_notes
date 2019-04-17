# https://docs.python.org/3/library/stdtypes.html

x = 5
y = 3


x + y             #  sum of x and y
x - y             #  difference of x and y
x * y             #  product of x and y
x / y             #  quotient of x and y
x // y            #  floored quotient of x and y
x % y             #  remainder of x / y
-x                #  x negated
+x                #  x unchanged
abs(x)            #  absolute value or magnitude of x
int(x)            #  x converted to integer
float(x)          #  x converted to floating point
#complex(re, im)  #  a complex number with real part re, imaginary part im. im defaults to zero.
#c.conjugate()    #  conjugate of the complex number c
divmod(x, y)      #  the pair (x // y, x % y)
pow(x, y)         #  x to the power y
x ** y            #  x to the power y


1 / 2    # 0.5
1 // 2   # 0   丢弃小数部分，使用双斜杠


# x % y等价于x - ((x // y) * y)


2 ** 3  # 8
-3 ** 2 # -9
(-3) ** 2 # 9

0xAF  # 十六进制
010   # 八进制
0b1011010010  # 二进制

#  变量是表示（或指向）特定值的名称

# 使用Python变量前必须给它赋值，因为Python变量没有默认值


input("The meaning of life: ")   # 获取用户输入


'''
https://docs.python.org/3.6/library/functions.html

内置函数

abs()   dict()  help()  min()   setattr()
all()   dir()   hex()   next()  slice()
any()   divmod()    id()    object()    sorted()
ascii() enumerate() input() oct()   staticmethod()
bin()   eval()  int()   open()  str()
bool()  exec()  isinstance()    ord()   sum()
bytearray() filter()    issubclass()    pow()   super()
bytes() float() iter()  print() tuple()
callable()  format()    len()   property()  type()
chr()   frozenset() list()  range() vars()
classmethod()   getattr()   locals()    repr()  zip()
compile()   globals()   map()   reversed()  __import__()
complex()   hasattr()   max()   round()
delattr()   hash()  memoryview()    set()


还有一些类似的函数，可用于转换类型，如str和float。实际上，它们并不是函数，而
是类。
'''


import math
math.ceil(32.3)
math.ceil(32)

from math import sqrt
sqrt(9)

sqrt(-1)  # nan  nan具有特殊含义，指的是“非数值”（not a number）。


import cmath   # 可处理复数的math 模块
cmath.sqrt(-1)  # 1j

str('hello')
repr('hello')
print('hello')
print(repr('hello'))

'hello'
r'raw string'  # 原始字符串经常用于表正则表达式的字符串 或 windows 路径
r'C:\Program Files\fnord\foo\bar\baz\frozz\bozz'

# 注意：原始字符串不能以单个反斜杠结尾

# 指定以反斜杠结尾的原始字符串 的 技巧：
r'C:\Program Files\foo\bar' '\\'


# Unicode、bytes和bytearray
# 大致而言，每个Unicode字符都用一个码点（code point）表示，而码点是Unicode标准给每个字符指定的数字

'''
 有一种指定Unicode字符的通用
机制：使用16或32位的十六进制字面量（分别加上前缀\u或\U）或者使用字符的Unicode名称
（\N{name}）。
'''

"\u00C6"  # 'Æ'
"\U0001F60A" # '☺ '
"This is a cat: \N{Cat}" # 'This is a cat: '

# http://unicode-table.com/

'''
为与C语言互操作
以及将文本写入文件或通过网络套接字发送出去，Python提供了两种类似的类型：不可变的bytes
和可变的bytearray。如果需要，可直接创建bytes对象（而不是字符串），方法是使用前缀b：

b'Hello, world!'

Python bytes字面量只
支持ASCII标准中的128个字符，而余下的128个值必须用转义序列表示，如\xf0表示十六进制值
0xf0（即240）

'''

'''
有一种非常巧妙的替代方式：不使用全部32位，而是使用变长编码，
具体地说，进行单字节编码时，依然使用ASCII编码，以便与较旧的系统兼
容；但对于不在这个范围内的字符，使用多个字节（最多为6个）进行编码。
'''

# 下面来使用ASCII、UTF-8和UTF-32编码将字符串转换为bytes。
"Hello, world!".encode("ASCII") # b'Hello, world!'
"Hello, world!".encode("UTF-8") # b'Hello, world!'
"Hello, world!".encode("UTF-32") # b'\xff\xfe\x00\x00H\x00\x00\x00e\x00\x00\x00l\x00\x00\x00l\x00\x00\x00o\x00\x00\x00,\x00\x00\x00 \x00\x00\x00w\x00\x00\x00o\x00\x00\x00r\x00\x00\x00l\x00\x00\x00d\x00\x00\x00!\x00\x00\x00'

len("How long is this?".encode("UTF-8")) # 17
len("How long is this?".encode("UTF-32")) # 72

# 只要字符串包含较怪异的字符，ASCII和UTF-8之间的差别便显现出来了：
'''
>>> "Hællå, wørld!".encode("ASCII")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character '\xe6' in position 1: ordinal not in range(128)
'''
# 几乎在所有情况下，都最好使用UTF-8。事实上，它也是默认使用的编码。
"Hællå, wørld!".encode() # b'H\xc3\xa6ll\xc3\xa5, w\xc3\xb8rld!'
# 可将字符串编码为bytes，同样也可将bytes解码为字符串
b'H\xc3\xa6ll\xc3\xa5, w\xc3\xb8rld!'.decode() # 'Hællå, wørld!'


# 可不使用方法encode和decode，而直接创建bytes和str（即字符串）对象，如下所示：
bytes("Hællå, wørld!", encoding="utf-8") # b'H\xc3\xa6ll\xc3\xa5, w\xc3\xb8rld!'
str(b'H\xc3\xa6ll\xc3\xa5, w\xc3\xb8rld!', encoding="utf-8") # 'Hællå, wørld!'

'''
编码和解码的最重要用途之一是，将文本存储到磁盘文件中。然而，Python提供的文件读写
机制通常会替你完成这方面的工作！只要文件使用的是UTF-8编码，就无需操心编码和解码的问
题。但如果原本正常的文本变成了乱码，就说明文件使用的可能是其他编码。在这种情况下，对
导致这种问题的原因有所了解将大有裨益。

'''

'''
最后，Python还提供了bytearray，它是bytes的可变版。从某种意义上说，它就像是可修改
的字符串——常规字符串是不能修改的。然而，bytearray其实是为在幕后使用而设计的，因此
作为类字符串使用时对用户并不友好。例如，要替换其中的字符，必须将其指定为0～255的值。
因此，要插入字符，必须使用ord获取其序数值（ordinal value）。
>>> x = bytearray(b"Hello!")
>>> x[1] = ord(b"u")
>>> x
bytearray(b'Hullo!')
'''



