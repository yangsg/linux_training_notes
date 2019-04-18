
# 使用字符串

# 字符串基本操作
'''
所有标准序列操作（索引、切片、乘法、成员资格检查、长度、最小值和最
大值）都适用于字符串，但别忘了字符串是不可变的，因此所有的元素赋值和切片赋值都是非
法的。
>>> website = 'http://www.python.org'
>>> website[-3:] = 'com'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
'''


# 设置字符串的格式：精简版
'''
将值转换为字符串并设置其格式是一个重要的操作，需要考虑众多不同的需求，因此随着时
间的流逝，Python提供了多种字符串格式设置方法。以前，主要的解决方案是使用字符串格式设
置运算符——百分号。这个运算符的行为类似于C语言中的经典函数printf：在%左边指定一个字
符串（格式字符串），并在右边指定要设置其格式的值。指定要设置其格式的值时，可使用单个
值（如字符串或数字），可使用元组（如果要设置多个值的格式），还可使用字典（这将在下一章
讨论），其中最常见的是元组
'''
format = "Hello, %s. %s enough for ya?"  # %s称为转换说明符 #s意味着将值视为字符串进行格式设置。如果指定的值不是字符串，将使用str将其转换为字符串
values = ('world', 'Hot')
format % values  # 'Hello, world. Hot enough for ya?'


'''
这种格式设置方法现在依然管用，且依然活跃在众多代码中，因此你很可能遇到。可能遇到
的另一种解决方案是所谓的模板字符串。它使用类似于UNIX shell的语法，旨在简化基本的格式
设置机制，如下所示：
>>> from string import Template
>>> tmpl = Template("Hello, $who! $what enough for ya?")  #它使用类似于UNIX shell的语法，旨在简化基本的格式设置机制
>>> tmpl.substitute(who="Mars", what="Dusty")  # 包含等号的参数称为关键字参数
'Hello, Mars! Dusty enough for ya?'
'''

'''
编写新代码时，应选择使用字符串方法format，它融合并强化了早期方法的优点。使用这种
方法时，每个替换字段都用花括号括起，其中可能包含名称，还可能包含有关如何对相应的值进
行转换和格式设置的信息。
>>> "{}, {} and {}".format("first", "second", "third")  # 在最简单的情况下，替换字段没有名称或将索引用作名称
'first, second and third'
>>> "{0}, {1} and {2}".format("first", "second", "third")
'first, second and third'
>>> "{3} {0} {2} {1} {3} {0}".format("be", "not", "or", "to")  # 然而，索引无需像上面这样按顺序排列。
'to be or not to be'


>>> from math import pi
>>> "{name} is approximately {value:.2f}.".format(value=pi, name="π")  # 命名字段的工作原理与你预期的完全相同
'π is approximately 3.14.'

当然，关键字参数的排列顺序无关紧要。在这里，我还指定了格式说明符.2f，并使用冒号
将其与字段名隔开。它意味着要使用包含2位小数的浮点数格式。如果没有指定.2f，结果将如下：
>>> "{name} is approximately {value}.".format(value=pi, name="π")
'π is approximately 3.141592653589793.'

最后，在Python 3.6中，如果变量与替换字段同名，还可使用一种简写。在这种情况下，可
使用f字符串——在字符串前面加上f。
>>> from math import e
>>> f"Euler's constant is roughly {e}."   # 带有 f 前缀的字符串
"Euler's constant is roughly 2.718281828459045."

在这里，创建最终的字符串时，将把替换字段e替换为变量e的值。这与下面这个更明确一些
的表达式等价：
>>> "Euler's constant is roughly {e}.".format(e=e)
"Euler's constant is roughly 2.718281828459045."
'''


'''
设置字符串的格式：完整版

字符串格式设置涉及的内容很多，因此即便是这里的完整版也无法全面探索所有的细节，而
只是介绍主要的组成部分。这里的基本思想是对字符串调用方法format，并提供要设置其格式的
值。字符串包含有关如何设置格式的信息，而这些信息是使用一种微型格式指定语言
（mini-language）指定的。每个值都被插入字符串中，以替换用花括号括起的替换字段。要在最
终结果中包含花括号，可在格式字符串中使用两个花括号（即{{或}}）来指定。

>>> "{{ceci n'est pas une replacement field}}".format()  # 要在最终结果中包含花括号，可在格式字符串中使用两个花括号（即{{或}}）来指定。
"{ceci n'est pas une replacement field}"


在格式字符串中，最激动人心的部分为替换字段。替换字段由如下部分组成，其中每个部分
都是可选的。

字段名：  索引或标识符，指出要设置哪个值的格式并使用结果来替换该字段。除指定值
          外，还可指定值的特定部分，如列表的元素。
转换标志：跟在叹号后面的单个字符。当前支持的字符包括r（表示repr）、s（表示str）
          和a（表示ascii）。如果你指定了转换标志，将不使用对象本身的格式设置机制，而是使
          用指定的函数将对象转换为字符串，再做进一步的格式设置。

格式说明符：跟在冒号后面的表达式（这种表达式是使用微型格式指定语言表示的）。格
            式说明符让我们能够详细地指定最终的格式，包括格式类型（如字符串、浮点数或十六
            进制数），字段宽度和数的精度，如何显示符号和千位分隔符，以及各种对齐和填充方式。
'''

# 替换字段名
'''
在最简单的情况下，只需向format提供要设置其格式的未命名参数，并在格式字符串中使用
未命名字段。此时，将按顺序将字段和参数配对。你还可给参数指定名称，这种参数将被用于相
应的替换字段中。你可混合使用这两种方法。
>>> "{foo} {} {bar} {}".format(1, 2, bar=4, foo=3)  #这种写法可读性不太好, 慎用
'3 1 4 2'

还可通过索引来指定要在哪个字段中使用相应的未命名参数，这样可不按顺序使用未命名
参数。
>>> "{foo} {1} {bar} {0}".format(1, 2, bar=4, foo=3)
'3 2 4 1'

然而，不能同时使用手工编号和自动编号，因为这样很快会变得混乱不堪。

你并非只能使用提供的值本身，而是可访问其组成部分（就像在常规Python代码中一样），
如下所示：
>>> fullname = ["Alfred", "Smoketoomuch"]
>>> "Mr {name[1]}".format(name=fullname) # 你并非只能使用提供的值本身，而是可访问其组成部分
'Mr Smoketoomuch'
>>> import math
>>> tmpl = "The {mod.__name__} module defines the value {mod.pi} for π"  # 你并非只能使用提供的值本身，而是可访问其组成部分
>>> tmpl.format(mod=math)
'The math module defines the value 3.141592653589793 for π'

如你所见，可使用索引，还可使用句点表示法来访问导入的模块中的方法、属性、变量和函
数（看起来很怪异的变量__name__包含指定模块的名称）。
'''

# 基本转换

# 指定要在字段中包含的值后，就可添加有关如何设置其格式的指令了。首先，可以提供一个转换标志。
'''
>>> print("{pi!s} {pi!r} {pi!a}".format(pi="π"))  # 上述三个标志（s、r和a）指定分别使用str、repr和ascii进行转换
π 'π' '\u03c0'

上述三个标志（s、r和a）指定分别使用str、repr和ascii进行转换。函数str通常创建外观
普通的字符串版本（这里没有对输入字符串做任何处理）。函数repr尝试创建给定值的Python表
示（这里是一个字符串字面量）。函数ascii创建只包含ASCII字符的表示，类似于Python 2中的
repr。

你还可指定要转换的值是哪种类型，更准确地说，是要将其视为哪种类型。例如，你可能提
供一个整数，但将其作为小数进行处理。为此可在格式说明（即冒号后面）使用字符f（表示定
点数）。

>>> "The number is {num}".format(num=42)
'The number is 42'
>>> "The number is {num:f}".format(num=42)
'The number is 42.000000'
>>> "The number is {num:b}".format(num=42)  # 也可以将其作为二进制数进行处理
'The number is 101010'

字符串格式设置中的类型说明符 ------------------
b    将整数表示为二进制数
c    将整数解读为Unicode码点
d    将整数视为十进制数进行处理，这是整数默认使用的说明符
e    使用科学表示法来表示小数（用e来表示指数）
E    与e相同，但使用E来表示指数
f    将小数表示为定点数
F    与f相同，但对于特殊值（nan和inf），使用大写表示
g    自动在定点表示法和科学表示法之间做出选择。这是默认用于小数的说明符，但在默认情况下至少有1位小数
G    与g相同，但使用大写来表示指数和特殊值
n    与g相同，但插入随区域而异的数字分隔符
o    将整数表示为八进制数
s    保持字符串的格式不变，这是默认用于字符串的说明符
x    将整数表示为十六进制数并使用小写字母
X    与x相同，但使用大写字母
%    将数表示为百分比值（乘以100，按说明符f设置格式，再在后面加上%）

'''

# 宽度、精度和千位分隔符
'''
设置浮点数（或其他更具体的小数类型）的格式时，默认在小数点后面显示6位小数，并根
据需要设置字段的宽度，而不进行任何形式的填充。当然，这种默认设置可能不是你想要的，在
这种情况下，可根据需要在格式说明中指定宽度和精度。

>>> "{num:10}".format(num=3)  # 宽度是使用整数指定的
'         3'

>>> "{name:10}".format(name="Bob")  # 如你所见，数和字符串的对齐方式不同
'Bob       '

>>> "Pi day is {pi:.2f}".format(pi=pi) # 精度也是使用整数指定的，但需要在它前面加上一个表示小数点的句点  # 这里显式地指定了类型f，因为默认的精度处理方式稍有不同
'Pi day is 3.14'


>>> "{pi:10.2f}".format(pi=pi)  # 当然，可同时指定宽度和精度
'      3.14'

>>> "{:.5}".format("Guido van Rossum")  # 实际上，对于其他类型也可指定精度，但是这样做的情形不太常见。
'Guido'

>>> 'One googol is {:,}'.format(10**100)  # 最后，可使用逗号来指出你要添加千位分隔符 # 同时指定其他格式设置元素时，这个逗号应放在宽度和表示精度的句点之间
'One googol is 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000'

如果要使用随区域而异的千位分隔符，应使用类型说明符n。

'''

# 符号、对齐和用0 填充
'''
有很多用于设置数字格式的机制，比如便于打印整齐的表格。在大多数情况下，只需指定宽
度和精度，但包含负数后，原本漂亮的输出可能不再漂亮。另外，正如你已看到的，字符串和数
的默认对齐方式不同。在一栏中同时包含字符串和数时，你可能想修改默认对齐方式。在指定宽
度和精度的数前面，可添加一个标志。这个标志可以是零、加号、减号或空格，其中零表示使用
0来填充数字。

>>> '{:010.2f}'.format(pi)  # 在指定宽度和精度的数前面，可添加一个标志。这个标志可以是零、加号、减号或空格，其中零表示使用 0 来填充(padding)数字
'0000003.14'

>>> print('{0:<10.2f}\n{0:^10.2f}\n{0:>10.2f}'.format(pi))  # 要指定左对齐、右对齐和居中，可分别使用<、>和^
3.14
   3.14
      3.14

>>> "{:$^15}".format(" WIN BIG ")  # 可以使用填充字符来扩充对齐说明符，这样将使用指定的字符而不是默认的空格来填充
'$$$ WIN BIG $$$'




>>> print('{0:10.2f}\n{1:10.2f}'.format(pi, -pi))
      3.14
     -3.14
>>> print('{0:10.2f}\n{1:=10.2f}'.format(pi, -pi))  # 还有更具体的说明符=，它指定将填充字符放在符号和数字之间。
      3.14
-     3.14


>>> print('{0:-.2}\n{1:-.2}'.format(pi, -pi)) #默认设置
3.1
-3.1
>>> print('{0:+.2}\n{1:+.2}'.format(pi, -pi)) # 如果要给正数加上符号，可使用说明符+（将其放在对齐说明符后面），而不是默认的-。
+3.1
-3.1
>>> print('{0: .2}\n{1: .2}'.format(pi, -pi))  # 如果将符号说明符指定为空格，会在正数前面加上空格而不是+。
 3.1
-3.1


需要介绍的最后一个要素是井号（#）选项，你可将其放在符号说明符和宽度之间（如果指
定了这两种设置）。这个选项将触发另一种转换方式，转换细节随类型而异。例如，对于二进制、
八进制和十六进制转换，将加上一个前缀。

>>> "{:b}".format(42)
'101010'
>>> "{:#b}".format(42)  # 将井号(#)放在符号说明符和宽度之间（如果指定了这两种设置）,对于二进制、 八进制和十六进制转换，将加上一个前缀。
'0b101010'

>>> "{:g}".format(42)
'42'
>>> "{:#g}".format(42)  # 对于各种十进制数，它要求必须包含小数点（对于类型g，它保留小数点后面的零）。
'42.0000'


'''

# 字符串方法
'''
前面介绍了列表的方法，而字符串的方法要多得多，因为其很多方法都是从模块string那里
“继承”而来的。（在较早的Python版本中，这些方法为模块string中的函数。如果需要，现在依
然能够找到这些函数。）
字符串的方法太多了，这里只介绍一些最有用的。完整的字符串方法清单请参阅附录B。这
里描述字符串的方法时，将列出其他相关的方法。如果这些相关方法在本章做了介绍，将用“另
请参见”标识，否则用“附录B”标识。

虽然字符串方法完全盖住了模块string的风头，但这个模块包含一些字符串没有的常量
和函数。下面就是模块string中几个很有用的常量①。

string.digits：包含数字0～9的字符串。
string.ascii_letters：包含所有ASCII字母（大写和小写）的字符串。
string.ascii_lowercase：包含所有小写ASCII字母的字符串。
string.printable：包含所有可打印的ASCII字符的字符串。
string.punctuation：包含所有ASCII标点字符的字符串。
string.ascii_uppercase：包含所有大写ASCII字母的字符串。

虽然说的是ASCII字符，但值实际上是未解码的Unicode字符串
'''
import string
string.digits            # '0123456789'
string.ascii_letters     # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
string.ascii_lowercase   # 'abcdefghijklmnopqrstuvwxyz'
string.printable         # '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
string.punctuation       # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
string.ascii_uppercase   # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# center
'''
>>> "The Middle by Jimmy Eat World".center(39)  # 方法center通过在两边添加填充字符（默认为空格）让字符串居中。 附录B：ljust、rjust和zfill。
'     The Middle by Jimmy Eat World     '
>>> "The Middle by Jimmy Eat World".center(39, "*")
'*****The Middle by Jimmy Eat World*****'


>>> "The Left by Jimmy Eat World".ljust(39)
'The Left by Jimmy Eat World            '
>>> "The Left by Jimmy Eat World".ljust(39, "*")
'The Left by Jimmy Eat World************'


>>> "The Right by Jimmy Eat World".rjust(39)
'           The Right by Jimmy Eat World'
>>> "The Right by Jimmy Eat World".rjust(39, "*")
'***********The Right by Jimmy Eat World'

>>> "42".zfill(5)
'00042'
>>> "-42".zfill(5)
'-0042'

'''

# find
'''
>>> 'With a moo-moo here, and a moo-moo there'.find('moo')  # 方法find在字符串中查找子串。如果找到，就返回子串的第一个字符的索引，否则返回-1
7
>>> title = "Monty Python's Flying Circus"
>>> title.find('Monty')
0
>>> title.find('Python')
6
>>> title.find('Flying')
15
>>> title.find('Zirquss')  #  方法find在字符串中查找子串。如果找到，就返回子串的第一个字符的索引，否则返回-1
-1

第2章初识成员资格时，我们在垃圾邮件过滤器中检查主题是否包含'$$$'。这种检查也可使
用find来执行。（在Python 2.3之前的版本中，这种做法也管用，但in只能用于检查单个字符是否
包含在字符串中。）

>>> subject = '$$$ Get rich now!!! $$$'
>>> subject.find('$$$')
0

>>> '$$$' in subject  # subject.find('$$$') != -1
True

注意字符串方法find返回的并非布尔值。如果find像这样返回0，就意味着它在索引0处找到
了指定的子串。


你还可指定搜索的起点和终点（它们都是可选的）。

>>> subject = '$$$ Get rich now!!! $$$'
>>> subject.find('$$$')
0
>>> subject.find('$$$', 1) # 只指定了起点
20
>>> subject.find('!!!')
16
>>> subject.find('!!!', 0, 16) # 同时指定了起点和终点 # 请注意，起点和终点值（第二个和第三个参数）指定的搜索范围包含起点，但不包含终点。这是Python惯常的做法。
-1

附录B：rfind、index、rindex、count、startswith、endswith。
>>> subject = '$$$ Get rich now!!! $$$'
>>> subject.rfind('$$$')
20
>>> subject.rfind('$$$', 1) # 只指定了起点
20
>>> subject.find('$$$', 0, 7) # 同时指定了起点和终点
0
>>> subject.find('######')  # 返回找到的最后一个子串的索引，如果没有找到这样的子串，就返回-1； 还可将搜索范围限定为string[start:end]
-1

# string.index(sub[, start[, end]]) 返回找到的第一个子串sub的索引，如果没有找到这样的子串，将引发ValueError异常；还可将搜索范围限制为string[start:end]
>>> subject.index('$$$')  # 与find 功能类似，区别是index没找到子串时，会抛出 ValueError 异常，所以通常建议使用find方法
0
>>> subject.index('###')  # 应优先考虑使用find方法，避免未找到子串时抛出ValueError异常(除非抛出异常是你想要的结果)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found


# string.rindex(sub[,start[,end]]) 返回找到的最后一个子串sub的索引，如果没有找到这样的子串，就引发 ValueError异常；还可将搜索范围限定为string[start:end]
>>> subject = '$$$ Get rich now!!! $$$'
>>> subject.rindex('$$$')   # 与rfind 功能类似，区别是index没找到子串时，会抛出 ValueError 异常，所以通常建议使用rfind方法
20
>>> subject.rindex('###')   # 应优先考虑使用rfind方法，避免未找到子串时抛出ValueError异常(除非抛出异常是你想要的结果)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: substring not found


# string.count(sub[, start[, end]]) 计算子串sub出现的次数，可搜索范围限定为string[start:end]
>>> subject = '$$$ Get rich now!!! $$$'
>>> subject.count('$$')
2
>>> subject.count('$')
6
>>> subject.count('$', 4) # 只指定了起点
3
>>> subject.count('$$$', 0, 7) # 同时指定了起点和终点
1
>>> subject.count('#')
0

# string.endswith(suffix[,start[,end]]) 检查字符串是否以suffix结尾，还可使用索引start和end来指定匹配范围
>>> 'hello world'.endswith('world')
True
>>> 'hello world'.endswith('ld', 2)     # 只指定了起点
True
>>> 'hello world'.endswith('l', 2, 3)   # 同时指定了起点和终点
True

'''

# join
'''
>>> seq = [1, 2, 3, 4, 5]
>>> sep = '+'
>>> sep.join(seq) # 尝试合并一个数字列表会抛出TypeError异常  error !!!!!!!!!!
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: sequence item 0: expected str instance, int found
>>> seq = ['1', '2', '3', '4', '5']
>>> sep.join(seq) # 合并一个字符串列表 可以成功
'1+2+3+4+5'
>>> dirs = '', 'usr', 'bin', 'env'
>>> '/'.join(dirs)
'/usr/bin/env'
>>> print('C:' + '\\'.join(dirs))
C:\usr\bin\env

如你所见，所合并序列的元素必须都是字符串。注意到在最后两个示例中，我使用了一系列
目录，并按UNIX和DOS/Windows的约定设置其格式：通过使用不同的分隔符（并在DOS版本中
添加了盘符）。
另请参见：split。
'''

# split  split是一个非常重要的字符串方法，其作用与join相反，用于将字符串拆分为序列。
# string.split([sep[, maxsplit]]) 返回一个列表，其中包含以sep为分隔符对字符串进行划分得到的结果（如果没有指定参数sep，将以所有空白字符为分隔符进行划分）；还可将最大划分次数限制为maxsplit

'''
>>> '1 2 3'.split()   # 如果没有指定sep或sep 为 None(其实None为默认sep), 连续的空白字符将被视为sep, 如果被split的字符串包含前导或尾随的空格，结果中也不会包含空字符串('')
['1', '2', '3']
>>> ' abc  '.split()  # 如果没有指定sep或sep 为 None(其实None为默认sep), 连续的空白字符将被视为sep, 如果被split的字符串包含前导或尾随的空格，结果中也不会包含空字符串('')
['abc']
>>> ' abc '.split(maxsplit=1)
['abc']
>>> ''.split()  # 对空字符串('')或纯空白字符串(如'     ')以None作为separator做split操作, 将返回空列表[]
[]
>>> ' \t\n\f '.split() # 对空字符串('')或纯空白字符串(如'     ')以None作为separator做split操作, 将返回空列表[]
[]
>>> ' \t\n\f '.split(maxsplit=1)
[]


'''
'1,2,3'.split(',')             # ['1', '2', '3']
'1,2,3'.split(',', maxsplit=1) # ['1', '2,3']
'1,2,,3,'.split(',')           # ['1', '2', '', '3', '']
'1+2+3+4+5'.split('+')         # ['1', '2', '3', '4', '5']
'/usr/bin/env'.split('/')      # ['', 'usr', 'bin', 'env']
'Using the default'.split()    # ['Using', 'the', 'default']  # 注意，如果没有指定分隔符，将默认在单个或多个连续的空白字符（空格、制表符、换行符等）处进行拆分



# str.rsplit(sep=None, maxsplit=-1)  除了从右边right开始split, rsplit 与 split 其实是类似的
'''
>>> ' abc '.rsplit()  #除了从右边right开始split, rsplit 与 split 其实是类似的
['abc']
>>> ' \t\n\f '.rsplit()
[]
>>> '1,2,3'.rsplit(',')
['1', '2', '3']
>>> '1,2,3'.rsplit(',', maxsplit=1)
['1,2', '3']
>>> '1,2,,3'.rsplit(',')
['1', '2', '', '3']

'''


# str.partition(sep) 在第一个分隔符 sep 出现的地方将字符串进行分割且返回一个三元组，第一个元素为sep左边的内容，第二个元素为sep本身，第三个为sep右边的内容，如果字符串中没有sep, 则返回的三元组中第一个元素为整个字符串本身，第二个和第三个元素都为空字符串
'www.google.com'.partition('.') # ('www', '.', 'google.com')
'abc'.partition('.')  # ('abc', '', '')

# str.rpartition(sep) # 在最后一个分隔符 sep 出现的地方将字符串进行分割且返回一个三元组，第一个元素为sep左边的内容，第二个元素为sep本身，第三个为sep右边的内容，如果字符串中没有sep, 则返回的三元组中第一个和第二个元素都为空字符串, 第三个元素为整个字符串本身，
'www.google.com'.rpartition('.')  # ('www.google', '.', 'com')
'abc'.rpartition('.')    # ('', '', 'abc')

# string.splitlines([keepends])  # 返回一个列表，其中包含字符串中的所有行；如果参数keepends为True，将包含换行符  # Return a list of the lines in the string, breaking at line boundaries. Line breaks are not included in the resulting list unless keepends is given and true.
'ab c\n\nde fg\rkl\r\n'.splitlines() # ['ab c', '', 'de fg', 'kl'] # 在line boundaries对字符串进行切分，并返回以每行字符串(当未指定keepends=True参数时)为元素的列表
'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True) # ['ab c\n', '\n', 'de fg\r', 'kl\r\n'] # 在line boundaries对字符串进行切分，并返回以每行字符串(包含了line boundaries，因指定了keepends=True参数)为元素的列表
"""
>>> '''
... line02
... line03
... line04
... '''.splitlines()
['', 'line02', 'line03', 'line04']

>>> '''\
... line01
... line02
... line03
... '''.splitlines()
['line01', 'line02', 'line03']

>>> '''\
... line01
... line02
... line03
... '''.splitlines(keepends=True)
['line01\n', 'line02\n', 'line03\n']
"""




# lower
'''
>>> 'Trondheim Hammer Dance'.lower()  # 方法lower返回字符串的小写版本
'trondheim hammer dance'

>>> 'Gumby'.lower() in ['gumby', 'smith', 'jones']  # 不分区大小写的成员判断: 一种解决方案是在存储和搜索时，将所有的用户名都转换为小写
True

另请参见：islower、istitle、isupper、translate。
附录B：capitalize、casefold、swapcase、title、upper。
'''

# upper()
'''
>>> 'Trondheim Hammer Dance'.upper()  # 方法upper返回字符串的大写版本
'TRONDHEIM HAMMER DANCE'
'''

# islower   检查字符串中的所有字母都是小写的 且 至少有一个是 cased character
'abc'.islower()   # True
'aBc'.islower()   # False
'a中文'.islower() # True
'中文'.islower()  # False # 因为字符串中不包含任何 cased character




# isupper   检查字符串中的字母是否都是大写的 且l 至少有一个是 cased character
'ABC'.isupper() # True
'aBb'.isupper() # False
'A中文'.isupper() # True
'中文'.isupper()  # False # 因为字符串中不包含任何 cased character


# string.istitle() 检查字符串中位于非字母后面的字母都是大写的，且其他所有字母都是小写的
'''
Return true if the string is a titlecased string and there is at least one character,
for example uppercase characters may only follow uncased characters and lowercase characters only cased ones. Return false otherwise.
'''
'Nice To Meet You'.istitle() # True
'Nice to meet you'.istitle() # False
'中文Nice To Meet You'.istitle() # True
'中文 Nice To Meet You'.istitle() # True
'中文 nice To Meet You'.istitle() # False


# capitalize
'abc def'.capitalize()  # 'Abc def' # capitalize 将string的首字母大写且其他字母小写
'aBC DEF'.capitalize() # 'Abc def'  # capitalize 将string的首字母大写且其他字母小写

# swapcase
'abc DEF'.swapcase() # 'ABC def'  # 将字符串中的大写转小写，小写的转大写, 右边的公式不一定成立： s.swapcase().swapcase() == s
'abc中文字符DEF'.swapcase()  # 'ABC中文字符def'

'''
词首大写
一个与lower相关的方法是title（参见附录B）。它将字符串转换为词首大写，即所有单
词的首字母都大写，其他字母都小写。然而，它确定单词边界的方式可能导致结果不合理。
>>> "that's all folks".title()
"That'S All, Folks"

另一种方法是使用模块string中的函数capwords。
>>> import string
>>> string.capwords("that's all, folks")
That's All, Folks"

当然，要实现真正的词首大写（根据你采用的写作风格，冠词、并列连词以及不超过5个
字母的介词等可能全部小写），你得自己编写代码。

'''

# replace  语法：str.replace(old, new[, count])
'This is a test'.replace('is', 'eez')  # 方法replace将指定子串都替换为另一个字符串，并返回替换后的结果
'abc def abc def abc'.replace('abc', 'xxx') # 'xxx def xxx def xxx'
'abc def abc def abc'.replace('abc', 'xxx', 2) # 'xxx def xxx def abc'  # 如果指定了count参数，则只有最先匹配的count个字符串会被替换
'abc def abc def abc'.replace('abc', 'xxx', 9) # 'xxx def xxx def xxx'


# str.expandtabs(tabsize=8)
'''
>>> '01\t012\t0123\t01234'.expandtabs() # 返回将字符串中的制表符展开为空格后的结果，可指定可选参数tabsize（默认为8） #注意这里指的是expand展开，而不是简单的将'\t'替换为指定个数的空格
'01      012     0123    01234'
>>> '01\t012\t0123\t01234'.expandtabs(4)
'01  012 0123    01234'
'''


# strip  语法：str.lstrip([chars]) 附录B：lstrip、rstrip
' internal whitespace is kept '.strip() # 'internal whitespace is kept' # 方法strip将字符串开头和末尾的空白（但不包括中间的空白）删除，并返回删除后的结果
'*** SPAM * for * everyone!!! ***'.strip(' *!') # 'SPAM * for * everyone' # 你还可在一个字符串参数中指定要删除哪些字符。#这个方法只删除开头或末尾的指定字符，因此中间的星号未被删除。

# lstrip 将字符串开头所有的chars（默认为所有的空白字符，如空格、制表符和换行符）都删除，并返回结果
' internal whitespace is kept '.lstrip() # 'internal whitespace is kept '
'*** SPAM * for * everyone!!! ***'.lstrip(' *!') # 'SPAM * for * everyone!!! ***'

# rstrip  将字符串末尾所有的chars字符（默认为所有的空白字符，如空格、制表符和换行符）都删除，并返回结果
' internal whitespace is kept '.rstrip() # ' internal whitespace is kept'
'*** SPAM * for * everyone!!! ***'.rstrip(' *!') # '*** SPAM * for * everyone'


# translate
'''
    方法translate与replace一样替换字符串的特定部分，但不同的是它只能进行单字符替换。
这个方法的优势在于能够同时替换多个字符，因此效率比replace高。
    这个方法的用途很多（如替换换行符或其他随平台而异的特殊字符），但这里只介绍一个比
较简单（也有点傻）的示例。假设你要将一段英语文本转换为带有德国口音的版本，为此必须将
字符c和s分别替换为k和z。
    然而，使用translate前必须创建一个转换表。这个转换表指出了不同Unicode码点之间的转
换关系。要创建转换表，可对字符串类型str调用方法maketrans，这个方法接受两个参数：两个
长度相同的字符串，它们指定要将第一个字符串中的每个字符都替换为第二个字符串中的相应字
符①。就这个简单的示例而言，代码类似于下面这样：
>>> table = str.maketrans('cs', 'kz')

如果愿意，可查看转换表的内容，但你看到的只是Unicode码点之间的映射。
>>> table
{115: 122, 99: 107}

创建转换表后，就可将其用作方法translate的参数。
>>> 'this is an incredible test'.translate(table)
'thiz iz an inkredible tezt'

调用方法maketrans时，还可提供可选的第三个参数，指定要将哪些字母删除。例如，要模
仿语速极快的德国口音，可将所有的空格都删除。
>>> table = str.maketrans('cs', 'kz', ' ')
>>> 'this is an incredible test'.translate(table)
'thizizaninkredibletezt'
'''
'abc中文deft'.translate(str.maketrans('ab', 'AB')) # 'ABc中文deft'
'abc中文deft'.translate(str.maketrans('ab', 'AB', 'deft')) # 'ABc中文' # 其中str.maketrans方法的第三个可选的参数表示要删除的那些字符


# 判断字符串是否满足特定的条件
'''
很多字符串方法都以is打头，如isspace、isdigit和isupper，它们判断字符串是否具有特定
的性质（如包含的字符全为空白、数字或大写）。如果字符串具备特定的性质，这些方法就返回
True，否则返回False。

附录B：isalnum、isalpha、isdecimal、isdigit、isidentifier、islower、isnumeric、
isprintable、isspace、istitle、isupper。
'''




































