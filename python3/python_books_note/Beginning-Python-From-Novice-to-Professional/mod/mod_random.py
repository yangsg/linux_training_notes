
# random
'''
    模块random包含生成伪随机数的函数，有助于编写模拟程序或生成随机输出的程序。请注意，
虽然这些函数生成的数字好像是完全随机的，但它们背后的系统是可预测的。如果你要求真正的
随机（如用于加密或实现与安全相关的功能），应考虑使用模块os中的函数urandom。模块random
中的SystemRandom类基于的功能与urandom类似，可提供接近于真正随机的数据。

                表10-8 模块random中一些重要的函数
函 数                                    描 述
random()                               返回一个0~1（含）的随机实数
getrandbits(n)                         以长整数方式返回n个随机的二进制位
uniform(a, b)                          返回一个a~b（含）的随机实数
randrange([start], stop, [step])       从range(start, stop, step)中随机地选择一个数
choice(seq)                            从序列seq中随机地选择一个元素
shuffle(seq[, random])                 就地打乱序列seq
sample(seq, n)                         从序列seq中随机地选择n个值不同的元素

    函数random.random是最基本的随机函数之一，它返回一个0~1（含）的伪随机数。除非这正
是你需要的，否则可能应使用其他提供了额外功能的函数。函数random.getrandbits以一个整数
的方式返回指定数量的二进制位。

    向函数random.uniform提供了两个数字参数a和b时，它返回一个a~b（含）的随机（均匀分布
的）实数。例如，如果你需要一个随机角度，可使用uniform(0, 360)。

    函数random.randrange是生成随机整数的标准函数。为指定这个随机整数所在的范围，
你可像调用range那样给这个函数提供参数。例如，要生成一个1~10（含）的随机整数，可
使用randrange(1, 11)或randrange(10) + 1。要生成一个小于20的随机正奇数，可使用randrange(1,
20, 2)。

    函数random.choice从给定序列中随机（均匀）地选择一个元素。

    函数random.shuffle随机地打乱一个可变序列中的元素，并确保每种可能的排列顺序出现的概率相同

    函数random.sample从给定序列中随机（均匀）地选择指定数量的元素，并确保所选择元素的值各不相同。

注意  编写与统计相关的程序时，可使用其他类似于uniform的函数，它们返回按各种分布随机采集的数字，如贝塔分布、指数分布、高斯分布等。

来看几个使用模块random的示例。在这些示例中，我将使用前面介绍的模块time中的几个函
数。首先，获取表示时间段（2016年）上限和下限的实数。为此，可使用时间元组来表示日期（将
星期、儒略日和夏令时都设置为1，让Python去计算它们的正确值），并对这些元组调用mktime：

from random import *
from time import *
date1 = (2016, 1, 1, 0, 0, 0, -1, -1, -1)
time1 = mktime(date1)
date2 = (2017, 1, 1, 0, 0, 0, -1, -1, -1)
time2 = mktime(date2)

接下来，以均匀的方式生成一个位于该范围内（不包括上限）的随机数：
>>> random_time = uniform(time1, time2)

然后，将这个数转换为易于理解的日期。
>>> print(asctime(localtime(random_time)))
Tue Aug 16 10:11:04 2016

在接下来的示例中，我们询问用户要掷多少个骰子、每个骰子有多少面。掷骰子的机制是使用randrange和for循环实现的。
'''

from random import randrange
num   = int(input('How many dice? '))
sides = int(input('How many sides per die? '))
sum = 0
for i in range(num):
    sum += randrange(sides) + 1
print('The result is', sum)

# 如果将这些代码放在一个脚本文件中并运行它，将看到类似于下面的交互过程：
'''
How many dice? 3
How many sides per die? 6
The result is 10

现在假设你创建了一个文本文件，其中每行都包含一种运气情况（fortune），那么就可使用
前面介绍的模块fileinput将这些情况放到一个列表中，再随机地选择一种。
'''
# fortune.py
import fileinput, random
fortunes = list(fileinput.input())
print random.choice(fortunes)
'''
在UNIX和macOS中，可使用标准字典文件/usr/share/dict/words来测试这个程序，这将获得一
个随机的单词。
$ python fortune.py /usr/share/dict/words
dodge
'''



