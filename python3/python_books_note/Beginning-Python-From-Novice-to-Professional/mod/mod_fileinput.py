

# fileinput
'''
    第11章将深入介绍如何读写文件，这里先来预演一下。模块fileinput让你能够轻松地迭代
一系列文本文件中的所有行。如果你这样调用脚本（假设是在UNIX命令行中）：
    $ python some_script.py file1.txt file2.txt file3.txt

    就能够依次迭代文件file1.txt到file3.txt中的行。你还可在UNIX管道中对使用UNIX标准命令
cat提供给标准输入（sys.stdin）的行进行迭代。
    $ cat file.txt | python some_script.py


    如果使用模块fileinput，在UNIX管道中使用cat调用脚本的效果将与以命令行参数的方式
向脚本提供文件名一样。表10-4描述了模块fileinput中最重要的函数。

                    表10-4 模块fileinput中一些重要的函数

函 数                                       描 述
input([files[, inplace[, backup]]])    帮助迭代多个输入流中的行
filename()                             返回当前文件的名称
lineno()                               返回（累计的）当前行号
filelineno()                           返回在当前文件中的行号
isfirstline()                          检查当前行是否是文件中的第一行
isstdin()                              检查最后一行是否来自sys.stdin
nextfile()                             关闭当前文件并移到下一个文件
close()                                关闭序列

    fileinput.input是其中最重要的函数，它返回一个可在for循环中进行迭代的对象。如果要
覆盖默认行为（确定要迭代哪些文件），可以序列的方式向这个函数提供一个或多个文件名。还
可将参数inplace设置为True（inplace=True），这样将就地进行处理。对于你访问的每一行，都
需打印出替代内容，这些内容将被写回到当前输入文件中。就地进行处理时，可选参数backup用
于给从原始文件创建的备份文件指定扩展名。

    函数fileinput.filename返回当前文件（即当前处理的行所属文件）的文件名。
    函数fileinput.lineno返回当前行的编号。这个值是累计的，因此处理完一个文件并接着处
理下一个文件时，不会重置行号，而是从前一个文件最后一行的行号加1开始。
    函数fileinput.filelineno返回当前行在当前文件中的行号。每次处理完一个文件并接着处
理下一个文件时，将重置这个行号并从1重新开始。
    函数fileinput.isfirstline在当前行为当前文件中的第一行时返回True，否则返回False。
    函数fileinput.isstdin在当前文件为sys.stdin时返回True，否则返回False。

    函数fileinput.nextfile关闭当前文件并跳到下一个文件，且计数时忽略跳过的行。这在你
知道无需继续处理当前文件时很有用。例如，如果每个文件包含的单词都是按顺序排列的，而你
要查找特定的单词，则过了这个单词所在的位置后，就可放心地跳到下一个文件。

    函数fileinput.close关闭整个文件链并结束迭代。


    来看一个fileinput使用示例。假设你编写了一个Python脚本，并想给其中的代码行加上行号。
鉴于你希望这样处理后程序依然能够正常运行，因此必须在每行末尾以注释的方式添加行号。为
让这些行号对齐，可使用字符串格式设置功能。假设只允许每行代码最多包含40个字符，并在第
41个字符处开始添加注释。代码清单10-6演示了一种使用模块fileinput和参数inplace来完成这
种任务的简单方式。

'''
# 代码清单10-6 在Python脚本中添加行号
# numberlines.py

import fileinput

for line in fileinput.input(inplace=True):
    line = line.rstrip()
    num = fileinput.lineno()
    print('{:<50} # {:2d}'.format(line, num))

# 如果像下面这样运行这个程序，并将其作为参数传入：
# $ python numberlines.py numberlines.py

'''
    这个程序将变成代码清单10-7那样。注意到程序本身被修改了，如果像上面这样运行它多次，
每行都将包含多个行号。本书前面介绍过，rstrip是一个字符串方法，它将删除指定字符串两端
的空白，并返回结果（参见3.4节以及附录B的表B-6）。
'''
# 代码清单10-7 添加行号后的行号添加程序
# numberlines.py                                        # 1
                                                        # 2
import fileinput                                        # 3
                                                        # 4
for line in fileinput.input(inplace=True):              # 5
    line = line.rstrip()                                # 6
    num = fileinput.lineno()                            # 7
    print('{:<50} # {:2d}'.format(line, num))           # 8

'''
警告    务必慎用参数inplace，因为这很容易破坏文件。你应在不设置inplace的情况下仔细测试
        程序（这样将只打印结果），确保程序能够正确运行后再让它修改文件。

    在10.3.6节，提供了另一个fileinput使用示例。
'''


