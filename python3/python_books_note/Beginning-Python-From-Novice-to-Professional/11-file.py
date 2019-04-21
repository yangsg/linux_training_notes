
# 文 件

# 打开文件
'''
    要打开文件，可使用函数open，它位于自动导入的模块io中。函数open将文件名作为唯一必
不可少的参数，并返回一个文件对象。如果当前目录中有一个名为somefile.txt的文本文件（可能
是使用文本编辑器创建的），则可像下面这样打开它：
>>> f = open('somefile.txt')

    如果文件位于其他地方，可指定完整的路径。如果指定的文件不存在，将看到类似于下面的
异常：
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    FileNotFoundError: [Errno 2] No such file or directory: 'somefile.txt'

    如果要通过写入文本来创建文件，这种调用函数open的方式并不能满足需求。为解决这种问
题，可使用函数open的第二个参数。


'''

# 文件模式
'''
    调用函数open时，如果只指定文件名，将获得一个可读取的文件对象。如果要写入文件，必
须通过指定模式来显式地指出这一点。函数open的参数mode的可能取值有多个，表11-1对此进行
了总结。

                    表11-1 函数open的参数mode的最常见取值

        值           描 述
        'r'         读取模式（默认值）
        'w'         写入模式
        'x'         独占写入模式
        'a'         附加模式
        'b'         二进制模式（与其他模式结合使用）
        't'         文本模式（默认值，与其他模式结合使用）
        '+'         读写模式（与其他模式结合使用）

    显式地指定读取模式的效果与根本不指定模式相同。写入模式让你能够写入文件，并在文件
不存在时创建它。独占写入模式更进一步，在文件已存在时引发FileExistsError异常。在写入模
式下打开文件时，既有内容将被删除（截断），并从文件开头处开始写入；如果要在既有文件末
尾继续写入，可使用附加模式。

    '+'可与其他任何模式结合起来使用，表示既可读取也可写入。例如，要打开一个文本文件
进行读写，可使用'r+'。（你可能还想结合使用seek，详情请参阅本章后面的旁注“随机存取”。）
请注意，'r+'和'w+'之间有个重要差别：后者截断文件，而前者不会这样做。

    默认模式为'rt'，这意味着将把文件视为经过编码的Unicode文本，因此将自动执行解码和
编码，且默认使用UTF-8编码。要指定其他编码和Unicode错误处理策略，可使用关键字参数
encoding和errors。（有关Unicode的详细信息，请参阅第1章。）这还将自动转换换行字符。默认
情况下，行以'\n'结尾。读取时将自动替换其他行尾字符（'\r'或'\r\n'）；写入时将'\n'替换为
系统的默认行尾字符（os.linesep）。

    通常，Python使用通用换行模式。在这种模式下，后面将讨论的readlines等方法能够识别所
有合法的换行符（'\n'、'\r'和'\r\n'）。如果要使用这种模式，同时禁止自动转换，可将关键字
参数newline设置为空字符串，如open(name, newline='')。如果要指定只将'\r'或'\r\n'视为合
法的行尾字符，可将参数newline设置为相应的行尾字符。这样，读取时不会对行尾字符进行转
换，但写入时将把'\n'替换为指定的行尾字符。


    如果文件包含非文本的二进制数据，如声音剪辑片段或图像，你肯定不希望执行上述自动转
换。为此，只需使用二进制模式（如'rb'）来禁用与文本相关的功能。
    还有几个更为高级的可选参数，用于控制缓冲以及更直接地处理文件描述符。要获取有关这
些参数的详细信息，请参阅Python文档或在交互式解释器中运行help(open)。


'''

# 文件的基本方法
'''
    知道如何打开文件后，下一步是使用它们来做些有用的事情。本节介绍文件对象的一些基本
方法以及其他类似于文件的对象（有时称为流）。类似于文件的对象支持文件对象的一些方法，
如支持read或write，或者两者都支持。urlopen（参见第14章）返回的对象就是典型的类似于文
件的对象，它们支持方法read和readline，但不支持方法write和isatty。


                            三个标准流

    在第10章讨论模块sys的一节中，提到了三个标准流。这些流都是类似于文件的对象，你
可将学到的有关文件的知识用于它们。
    一个标准数据输入源是sys.stdin。当程序从标准输入读取时，你可通过输入来提供文
本，也可使用管道将标准输入关联到其他程序的标准输出，这将在11.2.2节介绍。
    你提供给print的文本出现在sys.stdout中，向input提供的提示信息也出现在这里。写
入到sys.stdout的数据通常出现在屏幕上，但可使用管道将其重定向到另一个程序的标准
输入。
    错误消息（如栈跟踪）被写入到sys.stderr，但与写入到sys.stdout的内容一样，可对其
进行重定向。

'''

# 读取和写入
'''
    文件最重要的功能是提供和接收数据。如果有一个名为f的类似于文件的对象，可使用
f.write来写入数据，还可使用f.read来读取数据。与Python的其他大多数功能一样，在哪些东西
可用作数据方面，也存在一定的灵活性，但在文本和二进制模式下，基本上分别将str和bytes类
用作数据。
    每当调用f.write(string)时，你提供的字符串都将写入到文件中既有内容的后面。

>>> f = open('somefile.txt', 'w')
>>> f.write('Hello, ')
7
>>> f.write('World!')
6
>>> f.close()

    请注意，使用完文件后，我调用了方法close，这将在11.2.4节详细介绍。读取也一样简单，
只需告诉流你要读取多少个字符（在二进制模式下是多少字节），如下例所示：
>>> f = open('somefile.txt', 'r')
>>> f.read(4)
'Hell'
>>> f.read()
'o, World!'

    首先，指定了要读取多少（4）个字符。接下来，读取了文件中余下的全部内容（不指定要
读取多少个字符）。请注意，调用open时，原本可以不指定模式，因为其默认值就是'r'。

'''

# 使用管道重定向输出
'''
在bash等shell中，可依次输入多个命令，并使用管道将它们链接起来，如下所示：
    $ cat somefile.txt | python somescript.py | sort

这条管道线包含三个命令。
     cat somefile.txt：将文件somefile.txt的内容写入到标准输出（sys.stdout）。
     python somescript.py：执行Python脚本somescript。这个脚本从其标准输入中读取，并
    将结果写入到标准输出。
     sort：读取标准输入（sys.stdin）中的所有文本，将各行按字母顺序排序，并将结果写
    入到标准输出。

    但这些管道字符（|）有何作用呢？脚本somescript.py的作用是什么呢？管道将一个命令的
标准输出链接到下一个命令的标准输入。很聪明吧？因此可以认为，somescript.py从其
sys.stdin中读取数据（这些数据是somefile.txt写入的），并将结果写入到其sys.stdout（sort
将从这里获取数据）。

代码清单11-1是一个使用sys.stdin的简单脚本（somescript.py）。代码清单11-2显示了文件
somefile.txt的内容。
'''
# 代码清单11-1 计算sys.stdin中包含多少个单词的简单脚本
# somescript.py
import sys
text = sys.stdin.read()
words = text.split()
wordcount = len(words)
print('Wordcount:', wordcount)

'''
# 代码清单11-2 一个内容荒谬的文本文件
Your mother was a hamster and your
father smelled of elderberries.

cat somefile.txt | python somescript.py的结果如下：
Wordcount: 11
'''


# 随机存取
'''
    在本章中，我将文件都视为流，只能按顺序从头到尾读取。实际上，可在文件中移动，
只访问感兴趣的部分（称为随机存取）。为此，可使用文件对象的两个方法：seek 和tell。

    方法 seek(offset[, whence])将当前位置（执行读取或写入的位置）移到offset 和
whence 指定的地方。参数offset 指定了字节（字符）数，而参数whence 默认为io.SEEK_SET
（0），这意味着偏移量是相对于文件开头的（偏移量不能为负数）。参数whence 还可设置
为io.SEEK_CUR（1）或io.SEEK_END（2），其中前者表示相对于当前位置进行移动（偏移量
可以为负），而后者表示相对于文件末尾进行移动。请看下面的示例：

>>> f = open(r'C:\text\somefile.txt', 'w')
>>> f.write('01234567890123456789')
20
>>> f.seek(5)
5
>>> f.write('Hello, World!')
13
>>> f.close()
>>> f = open(r'C:\text\somefile.txt')
>>> f.read()
'01234Hello, World!89'

方法tell()返回当前位于文件的什么位置，如下例所示：
>>> f = open(r'C:\text\somefile.txt')
>>> f.read(3)
'012'
>>> f.read(2)
'34'
>>> f.tell()
5

'''

# 读取和写入行
'''
    实际上，本章前面所做的都不太实用。与其逐个读取流中的字符，不如成行地读取。要读取
一行（从当前位置到下一个分行符的文本），可使用方法readline。调用这个方法时，可不提供
任何参数（在这种情况下，将读取一行并返回它）；也可提供一个非负整数，指定readline最多
可读取多少个字符。因此，如果some_file. readline()返回的是'Hello, World!\n'，那么
some_file.readline(5)返回的将是'Hello'。要读取文件中的所有行，并以列表的方式返回它们，
可使用方法readlines。
    方法writelines与readlines相反：接受一个字符串列表（实际上，可以是任何序列或可迭代
对象），并将这些字符串都写入到文件（或流）中。请注意，写入时不会添加换行符，因此你必
须自行添加。另外，没有方法writeline，因为可以使用write。

'''

# 关闭文件
'''
    别忘了调用方法close将文件关闭。通常，程序退出时将自动关闭文件对象（也可能在退出
程序前这样做），因此是否将读取的文件关闭并不那么重要。然而，关闭文件没有坏处，在有些
操作系统和设置中，还可避免无意义地锁定文件以防修改。另外，这样做还可避免用完系统可能
指定的文件打开配额。

    对于写入过的文件，一定要将其关闭，因为Python可能缓冲你写入的数据（将数据暂时存储
在某个地方，以提高效率）。因此如果程序因某种原因崩溃，数据可能根本不会写入到文件中。
安全的做法是，使用完文件后就将其关闭。如果要重置缓冲，让所做的修改反映到磁盘文件中，
但又不想关闭文件，可使用方法flush。然而，需要注意的是，根据使用的操作系统和设置，flush
可能出于锁定考虑而禁止其他正在运行的程序访问这个文件。只要能够方便地关闭文件，就应将
其关闭。

    要确保文件得以关闭，可使用一条try/finally语句，并在finally子句中调用close。

# 在这里打开文件
try:
    # 将数据写入到文件中
finally:
    file.close()

实际上，有一条专门为此设计的语句，那就是with语句。
with open("somefile.txt") as somefile:
    do_something(somefile)

    with语句让你能够打开文件并将其赋给一个变量（这里是somefile）。在语句体中，你将数据
写入文件（还可能做其他事情）。到达该语句末尾时，将自动关闭文件，即便出现异常亦如此。

'''

# 上下文管理器
'''
    with语句实际上是一个非常通用的结构，允许你使用所谓的上下文管理器。上下文管理
器是支持两个方法的对象：__enter__和__exit__。
    方法__enter__不接受任何参数，在进入with语句时被调用，其返回值被赋给关键字as后
面的变量。
    方法__exit__接受三个参数：异常类型、异常对象和异常跟踪。它在离开方法时被调用
（通过前述参数将引发的异常提供给它）。如果__exit__返回False，将抑制所有的异常。
    文件也可用作上下文管理器。它们的方法__enter__返回文件对象本身，而方法__exit__
关闭文件。有关这项极其复杂而强大的功能的详细信息，请参阅“Python参考手册”中对上
下文管理器的描述，另请参阅“Python库参考手册”中介绍上下文管理器类型和contextlib
的部分。
'''

# 使用文件的基本方法
'''
假设文件somefile.txt包含代码清单11-3所示的文本，可对其执行哪些操作呢？

# 代码清单11-3 一个简单的文本文件
Welcome to this file
There is nothing here except
This stupid haiku

我们来试试前面介绍过的方法，首先是read(n)。
>>> f = open(r'C:\text\somefile.txt')
>>> f.read(7)
'Welcome'
>>> f.read(4)
' to '
>>> f.close()

接下来是read()：
>>> f = open(r'C:\text\somefile.txt')
>>> print(f.read())
Welcome to this file
There is nothing here except
This stupid haiku
>>> f.close()

下面是readline()：
>>> f = open(r'C:\text\somefile.txt')
>>> for i in range(3):
print(str(i) + ': ' + f.readline(), end='')
0: Welcome to this file
1: There is nothing here except
2: This stupid haiku
>>> f.close()

最后是readlines()：
>>> import pprint
>>> pprint.pprint(open(r'C:\text\somefile.txt').readlines())
['Welcome to this file\n',
'There is nothing here except\n',
'This stupid haiku']

请注意，这里我利用了文件对象将被自动关闭这一事实。下面来尝试写入，首先是
write(string)

>>> f = open(r'C:\text\somefile.txt', 'w')
>>> f.write('this\nis no\nhaiku')
13
>>> f.close()

运行上述代码后，这个文件包含的文本如代码清单11-4所示。
this
is no
haiku

最后是writelines(list)：

>>> f = open(r'C:\text\somefile.txt')
>>> lines = f.readlines()
>>> f.close()
>>> lines[1] = "isn't a\n"
>>> f = open(r'C:\text\somefile.txt', 'w')
>>> f.writelines(lines)
>>> f.close()

运行这些代码后，这个文件包含的文本如代码清单11-5所示。
代码清单11-5 再次修改后的文本文件
this
isn't a
haiku

'''

# 迭代文件内容
'''
    至此，你见识了文件对象提供的一些方法，还学习了如何获得文件对象。一种常见的文件操
作是迭代其内容，并在迭代过程中反复采取某种措施。这样做的方法有很多，你完全可以找到自
己喜欢的方法并坚持使用。然而，由于其他人可能使用不同的方法，为了能够理解他们编写的程
序，你应熟悉所有的基本方法。
    在本节的所有示例中，我都将使用一个名为process的虚构函数来表示对每个字符或行所做
的处理，你可以用自己的喜欢的方式实现这个函数。下面是一个简单的示例：
    def process(string):
        print('Processing:', string)
    更有用的实现包括将数据存储在数据结构中、计算总和、使用模块re进行模式替换以及添加
行号。
    另外，要尝试运行这些示例，应将变量filename设置为实际使用的文件的名称。

    一种最简单（也可能是最不常见）的文件内容迭代方式是，在while循环中使用方法read。
例如，你可能想遍历文件中的每个字符（在二进制模式下是每个字节），为此可像代码清单11-6
所示的那样做。如果你每次读取多个字符（字节），可指定要读取的字符（字节）数。
'''
# 代码清单11-6 使用read遍历字符
with open(filename) as f:
    char = f.read(1)
    while char:
        process(char)
        char = f.read(1)

'''
这个程序之所以可行，是因为到达文件末尾时，方法read将返回一个空字符串，但在此之前，
返回的字符串都只包含一个字符（对应于布尔值True）。只要char为True，你就知道还没结束。

    如你所见，赋值语句char = f.read(1)出现了两次，而代码重复通常被视为坏事。（还记得懒
惰是一种美德吗？）为避免这种重复，可使用第5章介绍的while True/break技巧。修改后的代码
如代码清单11-7所示。
'''
# 代码清单11-7 以不同的方式编写循环
with open(filename) as f:
    while True:
        char = f.read(1)
        if not char: break
        process(char)

'''
第5章说过，不应过多地使用break语句，因为这会导致代码更难理解。尽管如此，代码清单
11-7通常胜过代码清单11-6，正是因为它避免了重复的代码。
'''

# 每次一行
'''
处理文本文件时，你通常想做的是迭代其中的行，而不是每个字符。通过使用11.2.1节介绍
的方法readline，可像迭代字符一样轻松地迭代行，如代码清单11-8所示。
'''
# 代码清单11-8 在while循环中使用readline
with open(filename) as f:
    while True:
        line = f.readline()
        if not line: break
        process(line)


# 读取所有内容
'''
如果文件不太大，可一次读取整个文件；为此，可使用方法read并不提供任何参数（将整个
文件读取到一个字符串中），也可使用方法readlines（将文件读取到一个字符串列表中，其中每
个字符串都是一行）。代码清单11-9和11-10表明，通过这样的方式读取文件，可轻松地迭代字符
和行。请注意，除进行迭代外，像这样将文件内容读取到字符串或列表中也对完成其他任务很有
帮助。例如，可对字符串应用正则表达式，还可将列表存储到某种数据结构中供以后使用。
'''
# 代码清单11-9 使用read迭代字符
with open(filename) as f:
    for char in f.read():
        process(char)

# 代码清单11-10 使用readlines迭代行
with open(filename) as f:
    for line in f.readlines():
        process(line)


# 使用fileinput 实现延迟行迭代
'''
    有时候需要迭代大型文件中的行，此时使用readlines将占用太多内存。当然，你可转而
结合使用while循环和readline，但在Python中，在可能的情况下，应首选for循环，而这里就
属于这种情况。你可使用一种名为延迟行迭代的方法——说它延迟是因为它只读取实际需要的
文本部分。

    fileinput在第10章介绍过，代码清单11-11演示了如何使用它。请注意，模块fileinput会负
责打开文件，你只需给它提供一个文件名即可。
'''
# 代码清单11-11 使用fileinput迭代行
import fileinput
for line in fileinput.input(filename):
    process(line)


# 文件迭代器
'''
    该来看看最酷（也是最常见）的方法了。文件实际上是可迭代的，这意味着可在for循环中
直接使用它们来迭代行，如代码清单11-12所示。
'''
# 代码清单11-12 迭代文件
with open(filename) as f:
    for line in f:
        process(line)

'''
    在这些迭代示例中，我都将文件用作了上下文管理器，以确保文件得以关闭。虽然这通常是
个不错的主意，但只要不写入文件，就并非一定要这样做。如果你愿意让Python去负责关闭文件，
可进一步简化这个示例，如代码清单11-13所示。在这里，我没有将打开的文件赋给变量（如其
他示例中使用的变量f），因此没法显式地关闭它。
'''
# 代码清单11-13 在不将文件对象赋给变量的情况下迭代文件
for line in open(filename):
    process(line)

'''
    请注意，与其他文件一样，sys.stdin也是可迭代的，因此要迭代标准输入中的所有行，可
像下面这样做：
'''
import sys
for line in sys.stdin:
    process(line)


'''
    另外，可对迭代器做的事情基本上都可对文件做，如（使用list(open(filename))）将其转
换为字符串列表，其效果与使用readlines相同。
>>> f = open('somefile.txt', 'w')
>>> print('First', 'line', file=f)
>>> print('Second', 'line', file=f)
>>> print('Third', 'and final', 'line', file=f)
>>> f.close()
>>> lines = list(open('somefile.txt'))
>>> lines
['First line\n', 'Second line\n', 'Third and final line\n']
>>> first, second, third = open('somefile.txt')
>>> first
'First line\n'
>>> second
'Second line\n'
>>> third
'Third and final line\n'

在这个示例中，需要注意如下几点。
     使用了print来写入文件，这将自动在提供的字符串后面添加换行符。
     对打开的文件进行序列解包，从而将每行存储到不同的变量中。（这种做法不常见，因为
通常不知道文件包含多少行，但这演示了文件对象是可迭代的。）
     写入文件后将其关闭，以确保数据得以写入磁盘。（如你所见，读取文件后并没有将其关
闭。这可能有点粗糙，但并非致命的。）
'''

