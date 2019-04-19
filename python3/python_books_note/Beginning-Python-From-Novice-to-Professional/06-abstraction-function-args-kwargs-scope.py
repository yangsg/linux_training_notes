
# 抽象

# 函数 参数和作用域

# 懒惰是一种美德 (真正的程序员很懒。这里说的懒不是贬义词，而是说不做无谓的工作。)

# 那么真正的程序员会如何做呢？让程序更抽象。要让前面的程序更抽象，可以像下面这样做：
num = input('How many numbers do you want? ')
print(fibs(num))   # 此处 fibs 函数即是对 具体实现的抽象


# 抽象和结构
'''
    抽象可节省人力，但实际上还有个更重要的优点：抽象是程序能够被人理解的关键所在（无
论对编写程序还是阅读程序来说，这都至关重要）。计算机本身喜欢具体而明确的指令，但人通
常不是这样的。例如，如果你向人打听怎么去电影院，就不希望对方回答：“向前走10步，向左
转90度，接着走5步，再向右转45度，然后走123步。”听到这样的回答，你肯定一头雾水。
    如果对方回答：“沿这条街往前走，看到过街天桥后走到马路对面，电影院就在你左边。”你
肯定能明白。这里的关键是你知道如何沿街往前走，也知道如何过天桥，因此不需要有关这些方
面的具体说明。

    组织计算机程序时，你也采取类似的方式。程序应非常抽象，如下载网页、计算使用频率、
打印每个单词的使用频率。这很容易理解。下面就将前述简单描述转换为一个Python程序。

page = download_page()
freqs = compute_frequencies(page)
for word, freq in freqs:
    print(word, freq)

    看到这些代码，任何人都知道这个程序是做什么的。然而，至于具体该如何做，你未置一词。
你只是让计算机去下载网页并计算使用频率，至于这些操作的具体细节，将在其他地方（独立的
函数定义）中给出。

'''

# 这种抽象就包含着 自顶向下，逐步求精 的软件设计思想


# 自定义函数
# 一般而言，要判断某个对象是否可调用，可使用内置函数callable。
'''
>>> import math
>>> x = 1
>>> y = math.sqrt
>>> callable(x)  # 一般而言，要判断某个对象是否可调用，可使用内置函数callable
False
>>> callable(y)
True
'''

# 函数是结构化编程的核心。那么如何定义函数呢？使用def（表示定义函数）语句。
def hello(name):
    return 'Hello, ' + name + '!'

print(hello('world')) # Hello, world!
print(hello('Gumby')) # Hello, Gumby!


def fibs(num):
    result = [0, 1]
    for i in range(num-2):
        result.append(result[-2] + result[-1])
    return result


# 给函数编写文档
'''
    要给函数编写文档，以确保其他人能够理解，可添加注释（以#打头的内容）。还有另一种
编写注释的方式，就是添加独立的字符串。在有些地方，如def语句后面（以及模块和类的开
头，这将在第7章和第10章详细介绍），添加这样的字符串很有用。放在函数开头的字符串称为
文档字符串（docstring），将作为函数的一部分存储起来。下面的代码演示了如何给函数添加文
档字符串：
'''
def square(x):
    'Calculates the square of the number x.'
    return x * x
'''
可以像下面这样访问文档字符串
>>> square.__doc__     # 访问文档字符串
'Calculates the square of the number x.'


注意  __doc__是函数的一个属性。属性将在第7章详细介绍。属性名中的双下划线表示这是一
      个特殊的属性。特殊（“魔法”）属性将在第9章讨论。

    特殊的内置函数help很有用。在交互式解释器中，可使用它获取有关函数的信息，其中包含
函数的文档字符串。

>>> help(square)
Help on function square in module __main__:
square(x)
Calculates the square of the number x.

在第10章，你还会遇到函数help。

'''

# 其实并不是函数的函数
'''
什么都不返回的函数不包含return语句，或者包含return语句，但没有在return后面指定值。
所有的函数都返回值。如果你没有告诉它们该返回
什么，将返回None。

                    警告
不要让这种默认行为带来麻烦。如果你在if之类的语句中返回值，务必确保其他分支也
返回值，以免在调用者期望函数返回一个序列时（举个例子），不小心返回了None。

'''


# 参数魔法

'''
注意
 在def语句中，位于函数名后面的变量通常称为形参，而调用函数时提供的值称为实参，
 但本书基本不对此做严格的区分。在很重要的情况下，我会将实参称为值，以便将其与
 类似于变量的形参区分开来。


注意 参数存储在局部作用域内。


注意 你可能会问，函数内的局部名称（包括参数）会与函数外的名称（即全局名称）冲突吗？
     答案是不会。有关这方面的详细信息，请参阅本章后面对作用域的讨论

注意在字典中，键的排列顺序是不固定的，因此打印字典时，每次的顺序都可能不同。如果
你在解释器中打印出来的顺序不同，请不用担心。
'''

# 关键字参数和默认值  keyword arguments and default value
'''
前面使用的参数都是位置参数，因为它们的位置至关重要——事实上比名称还重要。本节介
绍的技巧让你能够完全忽略位置。要熟悉这种技巧需要一段时间，但随着程序规模的增大，你很
快就会发现它很有用。
'''

def hello_1(greeting, name):
    print('{}, {}!'.format(greeting, name))

hello_1('Hello', 'world')

hello_1(greeting='Hello', name='world')  #(Keyword Arguments) # 有时候，参数的排列顺序可能难以记住，尤其是参数很多时。为了简化调用工作，可指定参数的名称。# 像这样使用名称指定的参数称为关键字参数，主要优点是有助于澄清各个参数的作用

def hello_3(greeting='Hello', name='world'): #(Keyword Arguments)  # 然而，关键字参数最大的优点在于，可以指定默认值。
    print('{}, {}!'.format(greeting, name))

'''
注意 通常不应结合使用位置参数(positional argument)和关键字参数(Keyword Arguments)，除非你知道这样做的后果。一般而言，除非
必不可少的参数很少，而带默认值的可选参数很多，否则不应结合使用关键字参数和位
置参数。

'''

# 收集参数
def print_params(*params): # 允许用户提供任意数量的姓名 # Arbitrary Argument Lists
    print(params)
print_params('Testing')  # ('Testing',)
print_params(1, 2, 3)    # (1, 2, 3)
'''
    参数前面的星号将提供的所有值都放在一个元组中，也就是将这些值收集起来。这样的行为
我们在5.2.1节见过：赋值时带星号的变量收集多余的值。它收集的是列表而不是元组中多余的值，
但除此之外，这两种用法很像。下面再来编写一个函数：
def print_params_2(title, *params):
    print(title)
    print(params)

并尝试调用它：
>>> print_params_2('Params:', 1, 2, 3)
Params:
(1, 2, 3)

>>> print_params_2('Nothing:')  #星号意味着收集余下的位置参数。如果没有可供收集的参数，params将是一个空元组。
Nothing:
()

>>> def in_the_middle(x, *y, z):  # 与赋值时一样，带星号的参数也可放在其他位置（而不是最后），但不同的是，在这种情况下你需要做些额外的工作：使用名称来指定后续参数
... print(x, y, z)
...
>>> in_the_middle(1, 2, 3, 4, 5, z=7)
1 (2, 3, 4, 5) 7
>>> in_the_middle(1, 2, 3, 4, 5, 7)
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: in_the_middle() missing 1 required keyword-only argument: 'z'


'''

'''
>>> def print_params_3(**params):  # 星号不会收集关键字参数。 要收集关键字参数，可使用两个星号。
... print(params)
...
>>> print_params_3(x=1, y=2, z=3)
{'z': 3, 'x': 1, 'y': 2}

'''

def print_params_4(x, y, z=3, *pospar, **keypar):
    print(x, y, z)
    print(pospar)
    print(keypar)

print_params_4(1, 2, 3, 5, 6, 7, foo=1, bar=2)

# 分配参数
'''
前面介绍了如何将参数收集到元组和字典中，但用同样的两个运算符（*和**）也可执行相
反的操作。与收集参数相反的操作是什么呢？假设有如下函数：
def add(x, y):
    return x + y

同时假设还有一个元组，其中包含两个你要相加的数。
params = (1, 2)
这与前面执行的操作差不多是相反的：不是收集参数，而是分配参数。这是通过在调用函数
（而不是定义函数）时使用运算符*实现的。

>>> add(*params)  # 分配参数
3

这种做法也可用于参数列表的一部分，条件是这部分位于参数列表末尾。通过使用运算符**，
可将字典中的值分配给关键字参数。
>>> params = {'name': 'Sir Robin', 'greeting': 'Well met'}
>>> hello_3(**params)
Well met, Sir Robin!

提示 使用这些拆分运算符来传递参数很有用，因为这样无需操心参数个数之类的问题，如下
所示：

def foo(x, y, z, m=0, n=0):
    print(x, y, z, m, n)
def call_foo(*args, **kwds):
    print("Calling foo!")
    foo(*args, **kwds)

这在调用超类的构造函数时特别有用（有关这方面的详细信息，请参阅第9章）

'''

# 作用域
'''
    变量到底是什么呢？可将其视为指向值的名称。因此，执行赋值语句x = 1后，名称x指向值
1。这几乎与使用字典时一样（字典中的键指向值），只是你使用的是“看不见”的字典。实际上，
这种解释已经离真相不远。有一个名为vars的内置函数，它返回这个不可见的字典：
>>> x = 1
>>> scope = vars()
>>> scope['x']
1
>>> scope['x'] += 1  # warning 警告一般而言，不应修改vars返回的字典，因为根据Python官方文档的说法，这样做的结果是不确定的。换而言之，可能得不到你想要的结果
>>> x
2

这种“看不见的字典”称为命名空间或作用域。那么有多少个命名空间呢？除全局作用域外，
每个函数调用都将创建一个。
>>> def foo(): x = 42
...
>>> x = 1
>>> foo()
>>> x
1


    在这里，函数foo修改（重新关联）了变量x，但当你最终查看时，它根本没变。这是因为调
用foo时创建了一个新的命名空间，供foo中的代码块使用。赋值语句x = 42是在这个内部作用域
（局部命名空间）中执行的，不影响外部（全局）作用域内的x。在函数内使用的变量称为局部变
量（与之相对的是全局变量）。参数类似于局部变量，因此参数与全局变量同名不会有任何问题。
'''


'''
                “遮盖”的问题
    读取全局变量的值通常不会有问题，但还是存在出现问题的可能性。如果有一个局部
变量或参数与你要访问的全局变量同名，就无法直接访问全局变量，因为它被局部变量遮
住了。
    如果需要，可使用函数globals来访问全局变量。这个函数类似于vars，返回一个包含全
局变量的字典。（locals返回一个包含局部变量的字典。）



'''
def combine(parameter):
    print(parameter + globals()['parameter'])  # 借助 globals() 函数访问同名的全局变量

parameter = 'berry'
combine('Shrub')  # Shrubberry

'''
    重新关联全局变量（使其指向新值）是另一码事。在函数内部给变量赋值时，该变量默认为
局部变量，除非你明确地告诉Python它是全局变量。那么如何将这一点告知Python呢？
>>> x = 1
>>> def change_global():
... global x
... x = x + 1
...
>>> change_global()
>>> x
2

'''


'''
                        作用域嵌套
Python函数可以嵌套，即可将一个函数放在另一个函数内，如下所示：
def foo():
    def bar():
        print("Hello, world!")
    bar()

嵌套通常用处不大，但有一个很突出的用途：使用一个函数来创建另一个函数。这意味
着可像下面这样编写函数：

def multiplier(factor):
    def multiplyByFactor(number):
        return number * factor
    return multiplyByFactor


    在这里，一个函数位于另一个函数中，且外面的函数返回里面的函数。也就是返回一个
函数，而不是调用它。重要的是，返回的函数能够访问其定义所在的作用域。换而言之，它
携带着自己所在的环境（和相关的局部变量）！

    每当外部函数被调用时，都将重新定义内部的函数，而变量factor的值也可能不同。由
于Python的嵌套作用域，可在内部函数中访问这个来自外部局部作用域（multiplier）的变
量，如下所示：

>>> double = multiplier(2)
>>> double(5)
10
>>> triple = multiplier(3)
>>> triple(3)
9
>>> multiplier(5)(4)
20

像multiplyByFactor这样存储其所在作用域的函数称为闭包(closure)。

    通常，不能给外部作用域内的变量赋值，但如果一定要这样做，可使用关键字 nonlocal。
这个关键字的用法与global很像，让你能够给外部作用域（非全局作用域）内的变量赋值。

提示 实际上，模块bisect提供了标准的二分查找实现
'''

'''
                    函数式编程
    至此，你可能习惯了像使用其他对象（字符串、数、序列等）一样使用函数：将其赋
给变量，将其作为参数进行传递，以及从函数返回它们。在有些语言（如scheme 和Lisp）
中，几乎所有的任务都是以这种方式使用函数来完成的。在Python 中，通常不会如此倚
重函数（而是创建自定义对象，这将在下一章详细介绍），但完全可以这样做。

    Python提供了一些有助于进行这种函数式编程的函数：map、filter和reduce。在较新的
Python版本中，函数map和filter的用途并不大，应该使用列表推导来替代它们。你可使用map
将序列的所有元素传递给函数。


>>> list(map(str, range(10))) # 与[str(i) for i in range(10)]等价  # 在较新的Python版本中，函数map和filter的用途并不大，应该使用列表推导来替代它们
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

你可使用filter根据布尔函数的返回值来对元素进行过滤。
>>> def func(x):
... return x.isalnum()
...
>>> seq = ["foo", "x41", "?!", "***"]
>>> list(filter(func, seq))  # 就这个示例而言，如果转而使用列表推导，就无需创建前述自定义函数, 在较新的Python版本中，函数map和filter的用途并不大，应该使用列表推导来替代它们。
['foo', 'x41']

>>> [x for x in seq if x.isalnum()]
['foo', 'x41']

实际上，Python提供了一种名为lambda表达式(lambda来源于希腊字母，在数学中用于表示匿名函数。)的功能，让你能够创建内嵌的简单函数（主要供map、filter和reduce使用）。
>>> filter(lambda x: x.isalnum(), seq)
['foo', 'x41']

要使用列表推导来替换函数reduce不那么容易，而这个函数提供的功能即便能用到，也
用得不多。它使用指定的函数将序列的前两个元素合二为一，再将结果与第3个元素合二为
一，依此类推，直到处理完整个序列并得到一个结果。例如，如果你要将序列中的所有数相
加，可结合使用reduce和lambda x, y: x+y(实际上，可不使用这个lambda函数，而是导入模块operator中的函数add（这个模块包含对应于每个内置运算符的
函数）。与使用自定义函数相比，使用模块operator中的函数总是效率更高。)。
>>> numbers = [72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33]
>>> from functools import reduce
>>> reduce(lambda x, y: x + y, numbers)
1161
当然，就这个示例而言，还不如使用内置函数sum。







'''























