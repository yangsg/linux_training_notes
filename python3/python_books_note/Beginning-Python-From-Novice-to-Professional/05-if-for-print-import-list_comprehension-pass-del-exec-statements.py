
# 下面就来看看print和import隐藏的几个特性。虽然print现在实际上是一个函数，但以前却是一种语句

# 提示 对很多应用程序来说，使用模块logging来写入日志比使用print更合适，

# 再谈print 和import

# 打印多个参数
'''
你知道，print可用于打印一个表达式，这个表达式要么是字符串，要么将自动转换为字符
串。但实际上，你可同时打印多个表达式，条件是用逗号分隔它们：
>>> print('Age:', 42)  # 如你所见，在参数之间插入了一个空格字符。在你要合并文本和变量值，而又不想使用字符串格式设置功能时，这种行为很有帮助
Age: 42

>>> print("I", "wish", "to", "register", "a", "complaint", sep="_")  # I_wish_to_register_a_complaint # 如果需要，可自定义分隔符
'''

print('Hello,', end='')  # 你还可自定义结束字符串，以替换默认的换行符

# 导入时重命名

import somemodule
from somemodule import somefunction
from somemodule import somefunction, anotherfunction, yetanotherfunction
from somemodule import *  # 这种方式极不推荐，不清晰，且容易造成名字空间污染

'''
仅当你确定要导入模块中的一切时，采用使用最后一种方式。但如果有两个模块，它们都包
含函数open，该如何办呢？你可使用第一种方式导入这两个模块，并像下面这样调用函数：
module1.open(...)  # 通过限定名(qualified name)来消除歧义
module2.open(...)
'''


import math as foobar     # 为导入的名字设置别名 alias
foobar.sqrt(4) # 2.0

'''
>>> from math import sqrt as foobar  # 导入特定函数并给它指定别名的例子
>>> foobar(4)
2.0
'''

# 对于前面的函数open，可像下面这样导入它们
from module1 import open as open1
from module2 import open as open2

'''
注意有些模块（如os.path）组成了层次结构（一个模块位于另一个模块中）。有关模块结构
的详细信息，请参阅10.1.4节。
'''



# 赋值魔法

# 序列解包
'''
赋值语句你见过很多，有的给变量赋值，还有的给数据结构的一部分（如列表中的元素和切
片，或者字典项）赋值，但还有其他类型的赋值语句。例如，可同时（并行）给多个变量赋值：
>>> x, y, z = 1, 2, 3  # 可同时（并行）给多个变量赋值 (parallel assignment)
>>> print(x, y, z)
1 2 3


>>> x, y = y, x  # 看似用处不大？看好了，使用这种方式还可交换多个变量的值。# 这种方式是在赋值操作之前会计算出所有右边的值 # 实际上，这里执行的操作称为序列解包（或可迭代对象解包）：将一个序列（或任何可迭代
对象）解包，并将得到的值存储到一系列变量中
>>> print(x, y, z)
2 1 3

>>> values = 1, 2, 3
>>> values
(1, 2, 3)
>>> x, y, z = values  # 这在使用返回元组（或其他序列或可迭代对象）的函数或方法时很有用
>>> x
1


这在使用返回元组（或其他序列或可迭代对象）的函数或方法时很有用。假设要从字典中随
便获取（或删除）一个键值对，可使用方法popitem，它随便获取一个键值对并以元组的方式
返回。接下来，可直接将返回的元组解包到两个变量中。

>>> scoundrel = {'name': 'Robin', 'girlfriend': 'Marion'}
>>> key, value = scoundrel.popitem()  # 这让函数能够返回被打包成元组的多个值，然后通过一条赋值语句轻松地访问这些值。要解包的序列包含的元素个数必须与你在等号左边列出的目标个数相同，否则Python将引发异常。
>>> key
'girlfriend'
>>> value
'Marion'


>>> x, y, z = 1, 2  # error error !!! 因为要解包的序列包含的元素个数必须与你在等号左边列出的目标个数相同，否则Python将引发异常。
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ValueError: need more than 2 values to unpack
>>> x, y, z = 1, 2, 3, 4 # error error !!! 因为要解包的序列包含的元素个数必须与你在等号左边列出的目标个数相同，否则Python将引发异常。
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ValueError: too many values to unpack


>>> a, b, *rest = [1, 2, 3, 4]  # 可使用星号运算符（*）来收集多余的值，这样无需确保值和变量的个数相同
>>> rest
[3, 4]

>>> name = "Albus Percival Wulfric Brian Dumbledore"
>>> first, *middle, last = name.split()   # 还可将带星号的变量放在其他位置
>>> middle
['Percival', 'Wulfric', 'Brian']


>>> a, *b, c = "abc"  # 赋值语句的右边可以是任何类型的序列，但带星号的变量最终包含的总是一个列表。在变量和值的个数相同时亦如此
>>> a, b, c
('a', ['b'], 'c')

这种收集方式也可用于函数参数列表中（参见第6章
'''


# 链式赋值
x = y = somefunction()  # 链式赋值是一种快捷方式，用于将多个变量关联到同一个值。这有点像前一节介绍的并行赋值，但只涉及一个值
# 上述代码与下面的代码等价：
y = somefunction()
x = y
# 请注意，这两条语句可能与下面的语句不等价：
x = somefunction()
y = somefunction()


# 增强赋值
'''
可以不编写代码x = x + 1，而将右边表达式中的运算符（这里是+）移到赋值运算符（=）
的前面，从而写成x += 1。这称为增强赋值，适用于所有标准运算符，如*、/、%等。
>>> x = 2
>>> x += 1
>>> x *= 2
>>> x
6

增强赋值也可用于其他数据类型（只要使用的双目运算符可用于这些数据类型）。
>>> fnord = 'foo'
>>> fnord += 'bar'
>>> fnord *= 2
>>> fnord
'foobarfoobar'

通过使用增强赋值，可让代码更紧凑、更简洁，同时在很多情况下的可读性更强。
'''

# 代码块：缩进的乐趣
'''
代码块其实并不是一种语句，但要理解接下来两节的内容，你必须熟悉代码块。
代码块是一组语句，可在满足条件时执行（if语句），可执行多次（循环），等等。代码块是
通过缩进代码（即在前面加空格）来创建的。

注意  也可使用制表符来缩进代码块。Python将制表符解释为移到下一个制表位（相邻制表位
      相距8个空格），但标准（也是更佳的）做法是只使用空格（而不使用制表符）来缩进，
      且每级缩进4个空格。

在同一个代码块中，各行代码的缩进量必须相同。下面的伪代码（并非真正的Python代码）
演示了如何缩进：
this is a line
this is another line:  #在Python中，使用冒号（:）指出接下来是一个代码块，并将该代码块中的每行代码都缩进相同的程度
    this is another block
    continuing the same block
    the last line of this block
phew, there we escaped the inner block

    在很多语言中，都使用一个特殊的单词或字符（如begin或{）来标识代码块的起始位置，并
使用另一个特殊的单词或字符（如end或}）来标识结束位置。在Python中，使用冒号（:）指出
接下来是一个代码块，并将该代码块中的每行代码都缩进相同的程度。发现缩进量与之前相同时，
你就知道当前代码块到此结束了。（很多用于编程的编辑器和IDE知道如何缩进代码块，可帮助你
轻松地正确缩进。）
'''

# 条件和条件语句
'''
到目前为止，在你编写的程序中，语句都是逐条执行的。现在更进一步，让程序选择是否执
行特定的语句块。
    这正是布尔值的用武之地

    真值也称布尔值，是以在真值
    方面做出了巨大贡献的George Boole命名的。

用作布尔表达式（如用作if语句中的条件）时，下面的值都将被解释器视为假：
False None 0 "" () [] {}   # 用作布尔表达式（如用作if语句中的条件）时，这些值都将被解释器视为假

换而言之，标准值False和None、各种类型（包括浮点数、复数等）的数值0、空序列（如空
字符串、空元组和空列表）以及空映射（如空字典）都被视为假，而其他各种值都被视为真(至少对内置类型值来说如此。你在第9章将看到，对于自己创建的对象，解释为真还是假由你决定。)，
包括特殊值True(正如Python老手Laura Creighton指出的，这种差别类似于“有些东西”和“没有东西”的差别，而不是真和假
的差别)。


    明白了吗？这意味着任何Python值都可解释为真值。乍一看这有点令人迷惑，但也很有用。
虽然可供选择的真值非常多，但标准真值为True和False。在有些语言（如C语言和2.3之前的Python
版本）中，标准真值为0（表示假）和1（表示真）。实际上，True和False不过是0和1的别名，虽
然看起来不同，但作用是相同的。

>>> True
True
>>> False
False
>>> True == 1
True
>>> False == 0
True
>>> True + False + 42  # 实际上，True和False不过是0和1的别名，虽然看起来不同，但作用是相同的。
43

因此，如果你看到一个返回1或0的表达式（可能是使用较旧的Python版本编写的），就知道
这实际上意味着True或False。

布尔值True和False属于类型bool，而bool与list、str和tuple一样，可用来转换其他的值。
>>> bool('I think, therefore I am')  # bool 类型可用来转换其他的值
True
>>> bool(42)
True
>>> bool('')
False
>>> bool(0)
False

鉴于任何值都可用作布尔值，因此你几乎不需要显式地进行转换（Python会自动转换）

注意   虽然[]和""都为假（即bool([]) == bool("") == False），但它们并不相等（即[] != ""）。
       对其他各种为假的对象来说，情况亦如此（一个更显而易见的例子是() != False）。

'''

# 有条件地执行和if 语句
'''
name = input('What is your name? ')
if name.endswith('Gumby'):
    print('Hello, Mr. Gumby')

注意   在第1章的旁注“先睹为快：if语句”中，将有条件执行的语句与if语句放在同一行中。
       这与前一个示例中使用单行代码块的做法等价。

'''
# else 子句  （之所以叫子句是因为else不是独立的语句，而是if语句的一部分）。
'''
name = input('What is your name?')
if name.endswith('Gumby'):
    print('Hello, Mr. Gumby')
else:
    print('Hello, stranger')


还有一个与if语句很像的“亲戚”，它就是条件表达式——C语言中三目运算符的Python版本。
下面的表达式使用if和else确定其值：`

status = "friend" if name.endswith("Gumby") else "stranger"   # python版本的三元运算符 #如果条件（紧跟在if后面）为真，表达式的结果为提供的第一个值（这里为"friend"），否则为第二个值（这里为"stranger"）

'''

# elif 子句
num = int(input('Enter a number: '))
if num > 0:
    print('The number is positive')
elif num < 0:
    print('The number is negative')
else:
    print('The number is zero')

# 代码块嵌套
#     下面穿插点额外的内容。你可将if语句放在其他if语句块中，如下所示：
name = input('What is your name? ')
if name.endswith('Gumby'):
    if name.startswith('Mr.'):
        print('Hello, Mr. Gumby')
    elif name.startswith('Mrs.'):
        print('Hello, Mrs. Gumby')
    else:
        print('Hello, Gumby')
else:
    print('Hello, stranger')



# 更复杂的条件
#     下面来说说条件本身，因为它们是有条件执行中最有趣的部分。
x == y            #  x 等于y
x < y             #  x小于y
x > y             #  x大于y
x >= y            #  x大于或等于y
x <= y            #  x小于或等于y
x != y            #  x不等于y
x is y            #  x和y是同一个对象
x is not y        #  x和y是不同的对象
x in y            #  x是容器（如序列）y的成员
x not in y        #  x不是容器（如序列）y的成员


'''
                    对不兼容的类型进行比较
    从理论上说，可使用<和<=等运算符比较任意两个对象x和y的相对大小，并获得一个真
值，但这种比较仅在x和y的类型相同或相近时（如两个整数或一个整数和一个浮点数）才有
意义。
    将整数与字符串相加毫无意义，检查一个整数是否小于一个字符串也是一样。奇怪的
是，在Python 3之前，竟然可以这样做。不过即便你使用的是较旧的Python版本，也应对这类
比较敬而远之，因为结果是不确定的，每次执行程序时都可能不同。在Python 3中，已经不允
许这样比较不兼容的类型了。

'''

# 与赋值一样，Python也支持链式比较：可同时使用多个比较运算符，如0 < age < 100。
'''
有些比较运算符需要特别注意，下面就来详细介绍。
#   相等运算符
>>> "foo" == "foo"
True
>>> "foo" == "bar"
False
'''


# is：相同运算符   # is检查两个对象是否相同（而不是相等）  # 警告 不要将is用于数和字符串等不可变的基本值。鉴于Python在内部处理这些对象的方式， 这样做的结果是不可预测的。
'''
>>> x = y = [1, 2, 3]
>>> z = [1, 2, 3]
>>> x == y
True
>>> x == z
True
>>> x is y
True
>>> x is z
False

# 总之，==用来检查两个对象是否相等，而is用来检查两个对象是否相同（是同一个对象）。

警告 不要将is用于数和字符串等不可变的基本值。鉴于Python在内部处理这些对象的方式，
这样做的结果是不可预测的。
'''

# in：成员资格运算符
name = input('What is your name?')
if 's' in name:
    print('Your name contains the letter "s".')
else:
    print('Your name does not contain the letter "s".')


# 字符串和序列的比较
'''
字符串是根据字符的字母排列顺序进行比较的
>>> "alpha" < "beta"
True

实际上，字符是根据顺序值排列的。要获悉字母的顺序值，可使用函数ord。这个函数的作用与函数chr相反
>>> ord('a')
97
>>> chr(97)
'a'

这种方法既合理又一致，但可能与你排序的方式相反。例如，涉及大写字母时，排列顺序就
可能与你想要的不同。


虽然基于的是字母排列顺序，但字母都是Unicode字符，它们是按码点排列的。
>>> "a" < "B"  # 涉及大写字母时，排列顺序就可能与你想要的不同。
False

>>> "a".lower() < "B".lower()  # 一个诀窍是忽略大小写。为此可使用字符串方法lower
True

其他序列的比较方式与此相同，但这些序列包含的元素可能不是字符，而是其他类型的值。
>>> [1, 2] < [2, 1]
True

如果序列的元素为其他序列，将根据同样的规则对这些元素进行比较。
>>> [2, [1, 4]] < [2, [1, 5]]
True

'''

# 布尔运算符
number = int(input('Enter a number between 1 and 10: '))
if number <= 10 and number >= 1:  # 注意通过使用链式比较1 <= number <= 10可进一步简化这个示例。也许原本就应该这样做。
    print('Great!')
else:
    print('Wrong!')

# 运算符and是一个布尔运算符。它接受两个真值，并在这两个值都为真时返回真，否则返回假。还有另外两个布尔运算符：or和not。通过使用这三个运算符，能以任何方式组合真值。
if ((cash > price) or customer_has_good_credit) and not out_of_stock:
    give_goods()


'''
            短路逻辑和条件表达式
    布尔运算符有个有趣的特征：只做必要的计算。例如，仅当x和y都为真时，表达式x and
y才为真。因此如果x为假，这个表达式将立即返回假，而不关心y。实际上，如果x为假，这
个表达式将返回x，否则返回y。（这将提供预期的结果，你明白了其中的原理吗？）这种行为
称为短路逻辑（或者延迟求值）：布尔运算符常被称为逻辑运算符，如你所见，在有些情况下
将“绕过”第二个值。对于运算符or，情况亦如此。在表达式x or y中，如果x为真，就返回
x，否则返回y。（你明白这样做合理的原因吗？）请注意，这意味着位于布尔运算符后面的代
码（如函数调用）可能根本不会执行。像下面这样的代码就利用了这种行为：
        name = input('Please enter your name: ') or '<unknown>'
    如果没有输入名字，上述or表达式的结果将为'<unknown>'。在很多情况下，你都宁愿使
用条件表达式，而不耍这样的短路花样。不过前面这样的语句确实有其用武之地。
'''

# 断言
'''
>>> age = 10
>>> assert 0 < age < 100
>>> age = -1
>>> assert 0 < age < 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError


>>> age = -1
>>> assert 0 < age < 100, 'The age must be realistic'  # 还可在条件后面添加一个字符串，对断言做出说明
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError: The age must be realistic
'''

# 循环

# while 循环
x = 1
while x <= 100:
    print(x)
    x += 1

# 你还可以使用循环来确保用户输入名字，如下所示：
name = ''
while not name or name.isspace():  # while not name.strip():
    name = input('Please enter your name: ')
print('Hello, {}!'.format(name))

# for 循环
#    注意 基本上，可迭代对象是可使用for循环进行遍历的对象。

words = ['this', 'is', 'an', 'ex', 'parrot']
for word in words:
    print(word)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for number in numbers:
    print(number)


# 鉴于迭代（也就是遍历）特定范围内的数是一种常见的任务，Python提供了一个创建范围的内置函数。
range(0, 10) # range(0, 10)
list(range(0, 10)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
'''
范围类似于切片。它们包含起始位置（这里为0），但不包含结束位置（这里为10）。在很多
情况下，你都希望范围的起始位置为0。实际上，如果只提供了一个位置，将把这个位置视为结
束位置，并假定起始位置为0。
'''

for number in range(1,101):  # 注意，相比前面使用的while循环，这些代码要紧凑得多 # 提示 只要能够使用for循环，就不要使用while循环。
    print(number)


# 迭代字典
d = {'x': 1, 'y': 2, 'z': 3}
for key in d:
    print(key, 'corresponds to', d[key])
'''
也可使用keys等字典方法来获取所有的键。如果只对值感兴趣，可使用d.values。你可能还
记得，d.items以元组的方式返回键值对。for循环的优点之一是，可在其中使用序列解包。
'''
for key, value in d.items():
    print(key, 'corresponds to', value)

for key in d.keys():
    print(key)

for value in d.values():
    print(value)

'''
注意字典元素的排列顺序是不确定的。换而言之，迭代字典的键或值时，一定会处理所有的
键或值，但不知道处理的顺序。如果顺序很重要，可将键或值存储在一个列表中并对列
表排序，再进行迭代。要让映射记住其项的插入顺序，可使用模块collections中的
OrderedDict类。
'''

# 一些迭代工具
'''
Python提供了多个可帮助迭代序列（或其他可迭代对象）的函数
'''

# 并行迭代
'''
names = ['anne', 'beth', 'george', 'damon']
ages = [12, 45, 32, 102]
for i in range(len(names)):   # 对于这个例子，更好的方式是使用zip函数
    print(names[i], 'is', ages[i], 'years old')
i是用作循环索引的变量的标准名称。一个很有用的并行迭代工具是内置函数zip，它将两个
序列“缝合”起来，并返回一个由元组组成的序列。返回值是一个适合迭代的对象，要查看其内
容，可使用list将其转换为列表。

>>> ages = [12, 45, 32, 102]
>>> list(zip(names, ages))
[('anne', 12), ('beth', 45), ('george', 32), ('damon', 102)]
'''

for name, age in zip(names, ages):     # “缝合”后，可在循环中将元组解包
    print(name, 'is', age, 'years old')


list(zip(range(5), range(100000000))) # [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]  # 函数zip可用于“缝合”任意数量的序列。需要指出的是，当序列的长度不同时，函数zip将在最短的序列用完后停止“缝合”。


# 迭代时获取索引
index = 0
for string in strings:  # 这个解决方案虽然可以接受，但看起来也有点笨拙。另一种解决方案是使用内置函数enumerate。
    if 'xxx' in string:
        strings[index] = '[censored]'
    index += 1

for index, string in enumerate(strings):  # enumerate 函数让你能够迭代索引值对，其中的索引是自动提供的
    if 'xxx' in string:
        strings[index] = '[censored]'


# 反向迭代和排序后再迭代
'''
    来看另外两个很有用的函数：reversed和sorted。它们类似于列表方法reverse和sort（sorted
接受的参数也与sort类似），但可用于任何序列或可迭代的对象，且不就地修改对象，而是返回
反转和排序后的版本。

>>> sorted([4, 3, 6, 8, 3])  # 请注意，sorted返回一个列表，而reversed像zip那样返回一个更神秘的可迭代对象
[3, 3, 4, 6, 8]
>>> sorted('Hello, world!')
[' ', '!', ',', 'H', 'd', 'e', 'l', 'l', 'l', 'o', 'o', 'r', 'w']
>>> list(reversed('Hello, world!'))  # 请注意，sorted返回一个列表，而reversed像zip那样返回一个更神秘的可迭代对象
['!', 'd', 'l', 'r', 'o', 'w', ' ', ',', 'o', 'l', 'l', 'e', 'H']
>>> ''.join(reversed('Hello, world!'))
'!dlrow ,olleH'

    请注意，sorted返回一个列表，而reversed像zip那样返回一个更神秘的可迭代对象。你无需
关心这到底意味着什么，只管在for循环或join等方法中使用它，不会有任何问题。只是你不能
对它执行索引或切片操作，也不能直接对它调用列表的方法。要执行这些操作，可先使用list对
返回的对象进行转换。

提示 要按字母表排序，可先转换为小写。为此，可将sort或sorted的key参数设置为str.lower。
    例如，sorted("aBc", key=str.lower)返回['a', 'B', 'c']。

'''

# 跳出循环
# break
from math import sqrt
for n in range(99, 0, -1):
    root = sqrt(n)
    if root == int(root):
        print(n)
        break

# continue
'''
语句continue没有break用得多。它结束当前迭代，并跳到下一次迭代开头。这基本上意味
着跳过循环体中余下的语句，但不结束循环。这在循环体庞大而复杂，且存在多个要跳过它的原
因时很有用。在这种情况下，可使用continue，如下所示：
'''
for x in seq:
    if condition1: continue
    if condition2: continue
    if condition3: continue
    do_something()
    do_something_else()
    do_another_thing()
    etc()
# 然而，在很多情况下，使用一条if语句就足够了。
for x in seq:
    if not (condition1 or condition2 or condition3):
        do_something()
        do_something_else()
        do_another_thing()
        etc()
# continue虽然是一个很有用的工具，但并非不可或缺的。然而，你必须熟悉break语句，因为在while True循环中经常用到它


# while True/break成例
while True:
    word = input('Please enter a word: ')
    if not word: break
    # 使用这个单词做些事情：
    print('The word was ', word)
'''
    while True导致循环永不结束，但你将条件放在了循环体内的一条if语句中，而这条if语句
将在条件满足时调用break。这说明并非只能像常规while循环那样在循环开头结束循环，而是可
在循环体的任何地方结束循环。if/break行将整个循环分成两部分：第一部分负责设置（如果使
用常规while循环，将重复这部分），第二部分在循环条件为真时使用第一部分初始化的数据。
    虽然应避免在代码中过多使用break（因为这可能导致循环难以理解，在一个循环中包含多
个break时尤其如此），但这里介绍的技巧很常见，因此大多数Python程序员（包括你自己）都能
够明白你的意图。
'''

# 循环中的else 子句
'''
    通常，在循环中使用break是因为你“发现”了什么或“出现”了什么情况。要在循环提前
结束时采取某种措施很容易，但有时候你可能想在循环正常结束时才采取某种措施。如何判断循
环是提前结束还是正常结束的呢？可在循环开始前定义一个布尔变量并将其设置为False，再在跳
出循环时将其设置为True。这样就可在循环后面使用一条if语句来判断循环是否是提前结束的。
broke_out = False
for x in seq:
    do_something(x)
    if condition(x):
        broke_out = True
        break
    do_something_else(x)
if not broke_out:
    print("I didn't break out!")

一种更简单的办法是在循环中添加一条else子句，它仅在没有调用break时才执行。继续前
面讨论break时的示例。
'''
from math import sqrt
for n in range(99, 81, -1):
    root = sqrt(n)
    if root == int(root):
        print(n)
        break
else:  # 无论是 在for循环还是while循环中，都可使用continue、break和else子句。
    print("Didn't find it!")
'''
请注意，为测试else子句，我将下限改成了81（不包含）。如果你运行这个程序，它将打印
"Didn't find it!"，因为正如你在前面讨论break时看到的，小于100的最大平方值为81。无论是
在for循环还是while循环中，都可使用continue、break和else子句。
'''

# 简单推导
'''
列表推导是一种从其他列表创建列表的方式，类似于数学中的集合推导。列表推导的工作原
理非常简单，有点类似于for循环。
>>> [x * x for x in range(10)]  # 列表推到 list comprehension
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

>>> [x*x for x in range(10) if x % 3 == 0]  # 可在列表推导(list comprehension)中添加一条if语句
[0, 9, 36, 81]

>>> [(x, y) for x in range(3) for y in range(3)]  # 还可在列表推到(list comprehension)添加更多的for部分。
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

作为对比，下面的两个for循环创建同样的列表：
result = []
for x in range(3):
    for y in range(3)
        result.append((x, y))


与以前一样，使用多个for部分时，也可添加if子句。
>>> girls = ['alice', 'bernice', 'clarice']
>>> boys = ['chris', 'arnold', 'bob']
>>> [b+'+'+g for b in boys for g in girls if b[0] == g[0]]  # 与以前一样，使用多个for部分时，也可添加if子句
['chris+clarice', 'arnold+alice', 'bob+bernice']

                更佳的解决方案
前述男孩/女孩配对示例的效率不太高，因为它要检查每种可能的配对。使用Python解决
这个问题的方法有很多，下面是Alex Martelli推荐的解决方案：

girls = ['alice', 'bernice', 'clarice']
boys = ['chris', 'arnold', 'bob']
letterGirls = {}
for girl in girls:
    letterGirls.setdefault(girl[0], []).append(girl)
print([b+'+'+g for b in boys for g in letterGirls[b[0]]])

    这个程序创建一个名为letterGirls的字典，其中每项的键都是一个字母，而值为以这个
字母打头的女孩名字组成的列表（字典方法setdefault在前一章介绍过）。创建这个字典后，
列表推导遍历所有的男孩，并查找名字首字母与当前男孩相同的所有女孩。这样，这个列表
推导就无需尝试所有的男孩和女孩组合并检查他们的名字首字母是否相同了。

'''

'''
使用圆括号代替方括号并不能实现元组推导，而是将创建生成器(generator)，详细信息请参阅第9章的
旁注“简单生成器”。然而，可使用花括号来执行字典推导(dict conprehension)。
>>> squares = {i:"{} squared is {}".format(i, i**2) for i in range(10)}  #在列表推导中，for前面只有一个表达式，而在字典推导(dict comprehension)中，for前面有两个用冒号分隔的表达式。这两个表达式分别为键及其对应的值
>>> squares[8]
'8 squared is 64'

'''

# 结束本章前，大致介绍一下另外三条语句：pass、del和exec
# 什么都不做 pass
'''
>>> pass   # 在你编写代码时，可将其用作占位符
>>>

if name == 'Ralph Auldus Melish':
    print('Welcome!')
elif name == 'Enid':
    # 还未完成……
    pass   # 注意也可不使用注释和pass语句，而是插入一个字符串。这种做法尤其适用于未完成的函数（参见第6章）和类（参见第7章），因为这种字符串将充当文档字符串
elif name == 'Bill Gates':
    print('Access Denied')
'''

# 使用del 删除
'''
对于你不再使用的对象，Python通常会将其删除（因为没有任何变量或数据结构成员指向它）。
>>> scoundrel = {'age': 42, 'first name': 'Robin', 'last name': 'of Locksley'}
>>> robin = scoundrel
>>> scoundrel
{'age': 42, 'first name': 'Robin', 'last name': 'of Locksley'}
>>> robin
{'age': 42, 'first name': 'Robin', 'last name': 'of Locksley'}
>>> scoundrel = None
>>> robin
{'age': 42, 'first name': 'Robin', 'last name': 'of Locksley'}
>>> robin = None

最初，robin和scoundrel指向同一个字典，因此将None赋给scoundrel后，依然可以通过robin
来访问这个字典。但将robin也设置为None之后，这个字典就漂浮在计算机内存中，没有任何名
称与之相关联，再也无法获取或使用它了。因此，智慧无穷的Python解释器直接将其删除。这被
称为垃圾收集(garbage collection)。请注意，在前面的代码中，也可将其他任何值（而不是None）赋给两个变量，这
样字典也将消失。

另一种办法是使用del语句。（第2章和第4章使用这条语句来删除序列和字典，还记得吗？）
这不仅会删除到对象的引用，还会删除名称本身。
>>> x = 1
>>> del x
>>> x
Traceback (most recent call last):
File "<pyshell#255>", line 1, in ?
x
NameError: name 'x' is not defined

这看似简单，但有时不太好理解。例如，在下面的示例中，x和y指向同一个列表：
>>> x = ["Hello", "world"]
>>> y = x
>>> y[1] = "Python"
>>> x
['Hello', 'Python']

你可能认为通过删除x，也将删除y，但情况并非如此。
>>> del x
>>> y
['Hello', 'Python']

这是为什么呢？x和y指向同一个列表，但删除x对y没有任何影响，因为你只删除名称x，而
没有删除列表本身（值）。事实上，在Python中，根本就没有办法删除值，而且你也不需要这样
做，因为对于你不再使用的值，Python解释器会立即将其删除。
'''

# 使用exec 和eval 执行字符串及计算其结果
'''
有时候，你可能想动态地编写Python代码，并将其作为语句进行执行或作为表达式进行计算。
这可能犹如黑暗魔法，一定要小心。exec和eval现在都是函数，但exec以前是一种语句，而eval
与它紧密相关。这就是我在这里讨论它们的原因所在。

                        警告
本节介绍如何执行存储在字符串中的Python代码，这样做可能带来严重的安全隐患。如
果将部分内容由用户提供的字符串作为代码执行，将无法控制代码的行为。在网络应用
程序，如第15章将介绍的通用网关接口（CGI）脚本中，这样做尤其危险。

'''
# exec (通常应避免使用exec 和 eval 函数, 而是寻找更好的解决方案)
'''
>>> exec("print('Hello, world!')")  # 函数exec将字符串作为代码执行
Hello, world!

然而，调用函数exec时只给它提供一个参数绝非好事。在大多数情况下，还应向它传递一个
命名空间——用于放置变量的地方；否则代码将污染你的命名空间，即修改你的变量。例如，假
设代码使用了名称sqrt，结果将如何呢？

>>> from math import sqrt
>>> exec("sqrt = 1")     # error, 使用exec 造成名字空间污染的一个反例
>>> sqrt(4)
Traceback (most recent call last):
File "<pyshell#18>", line 1, in ?
sqrt(4)
TypeError: object is not callable: 1

既然如此，为何要将字符串作为代码执行呢？函数exec主要用于动态地创建代码字符串。如
果这种字符串来自其他地方（可能是用户），就几乎无法确定它将包含什么内容。因此为了安全
起见，要提供一个字典以充当命名空间。

注意 命名空间（作用域）是个重要的概念，将在下一章深入讨论，但就目前而言，你可将命
     名空间视为放置变量的地方，类似于一个看不见的字典。因此，当你执行赋值语句x = 1
     时，将在当前命名空间存储键x和值1。当前命名空间通常是全局命名空间（到目前为止，
     我们使用的大都是全局命名空间），但并非必然如此。


>>> from math import sqrt
>>> scope = {}
>>> exec('sqrt = 1', scope)  # 添加第二个参数——字典，用作代码字符串的命名空间 # 实际上，可向exec提供两个命名空间：一个全局的和一个局部的。提供的全局命名空间必须是字典，而提供的局部命名空间可以是任何映射。这一点也适用于eval。
>>> sqrt(4)
2.0
>>> scope['sqrt']
1


    如你所见，可能带来破坏的代码并非覆盖函数sqrt。函数sqrt该怎样还怎样，而通过exec执
行赋值语句创建的变量位于scope中。
    请注意，如果你尝试将scope打印出来，将发现它包含很多内容，这是因为自动在其中添加
了包含所有内置函数和值的字典__builtins__。
>>> len(scope)
2
>>> scope.keys()
['sqrt', '__builtins__']

'''

# eval
'''
eval是一个类似于exec的内置函数。exec执行一系列Python语句，而eval计算用字符串表示
的Python表达式的值，并返回结果（exec什么都不返回，因为它本身是条语句）。例如，你可使
用如下代码来创建一个Python计算器：
>>> eval(input("Enter an arithmetic expression: "))  # exec 和 eval 函数都可能带来安全问题，所以应避免使用而寻找更好的替代解决方案
Enter an arithmetic expression: 6 + 18 * 2
42

    与exec一样，也可向eval提供一个命名空间，虽然表达式通常不会像语句那样给变量重新
赋值。

                警告
虽然表达式通常不会给变量重新赋值，但绝对能够这样做，如调用给全局变量重新赋值
的函数。因此，将eval用于不可信任的代码并不比使用exec安全。当前，在Python中执行
不可信任的代码时，没有安全的办法。一种替代解决方案是使用Jython（参见第17章）等
Python实现，以使用Java沙箱等原生机制。



'''

'''
                浅谈作用域
向exec或eval提供命名空间时，可在使用这个命名空间前在其中添加一些值。
>>> scope = {}
>>> scope['x'] = 2
>>> scope['y'] = 3
>>> eval('x * y', scope)
6

同样，同一个命名空间可用于多次调用exec或eval。

>>> scope = {}
>>> exec('x = 2', scope)
>>> eval('x * x', scope)
4

采用这种做法可编写出非常复杂的程序，但你也许不应这样做。

'''



