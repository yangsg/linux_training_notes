
# time
'''
    模块time包含用于获取当前时间、操作时间和日期、从字符串中读取日期、将日期格式化为
字符串的函数。日期可表示为实数（从“新纪元”1月1日0时起过去的秒数。“新纪元”是一个随
平台而异的年份，在UNIX中为1970年），也可表示为包含9个整数的元组。表10-6解释了这些整
数。例如，元组(2008, 1, 21, 12, 2, 56, 0, 21, 0)表示2008年1月21日12时2分56秒。这一天是
星期一，2008年的第21天（不考虑夏令时）。

        表10-6 Python日期元组中的字段
索 引        字 段                 值
0             年                如2000、2001等
1             月                范围1~12
2             日                范围1~31
3             时                范围0~23
4             分                范围0~59
5             秒                范围0~61
6             星期              范围0~6，其中0表示星期一
7             儒略日            范围1~366
8             夏令时            0、1或-1

    秒的取值范围为0~61，这考虑到了闰一秒和闰两秒的情况。夏令时数字是一个布尔值（True
或False），但如果你使用-1，那么mktime［将时间元组转换为时间戳（从新纪元开始后的秒数）
的函数］可能得到正确的值。表10-7描述了模块time中一些最重要的函数。

        表10-7 模块time中一些重要的函数
函 数                           描 述
asctime([tuple])              将时间元组转换为字符串
localtime([secs])             将秒数转换为表示当地时间的日期元组
mktime(tuple)                 将时间元组转换为当地时间
sleep(secs)                   休眠（什么都不做）secs秒
strptime(string[, format])    将字符串转换为时间元组
time()                        当前时间（从新纪元开始后的秒数，以UTC为准）

函数time.asctime将当前时间转换为字符串，如下所示：
>>> time.asctime()
'Mon Jul 18 14:06:07 2016'

    如果不想使用当前时间，也可向它提供一个日期元组（如localtime创建的日期元组）。要设
置更复杂的格式，可使用函数strftime，标准文档对此做了介绍。
    函数time.localtime将一个实数（从新纪元开始后的秒数）转换为日期元组（本地时间）。如
果要转换为国际标准时间，应使用gmtime。

    函数time.mktime将日期元组转换为从新纪元后的秒数，这与localtime的功能相反。
    函数time.sleep让解释器等待指定的秒数。
    函数time.strptime将一个字符串（其格式与asctime所返回字符串的格式相同）转换为日期
元组。（可选参数format遵循的规则与strftime相同，详情请参阅标准文档。）

    函数time.time返回当前的国际标准时间，以从新纪元开始的秒数表示。虽然新纪元随平台
而异，但可这样进行可靠的计时：存储事件（如函数调用）发生前后time的结果，再计算它们的
差。有关这些函数的使用示例，请参阅10.3.6节。

    表10-7只列出了模块time的一部分函数。这个模块的大部分函数执行的任务都与本节介绍的
任务类似或相关。如果要完成这里介绍的函数无法执行的任务，请查看“Python库参考手册”中
介绍模块time的部分，在那里你很可能找到刚好能完成这种任务的函数。

    另外，还有两个较新的与时间相关的模块：datetime和timeit。前者提供了日期和时间算术
支持，而后者可帮助你计算代码段的执行时间。“Python库参考手册”提供了有关这两个模块的
详细信息。另外，第16章将简要地讨论timeit。

'''


