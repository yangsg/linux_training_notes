
# os

'''
    模块os让你能够访问多个操作系统服务。它包含的内容很多，表10-3只描述了其中几个最有
用的函数和变量。除此之外，os及其子模块os.path还包含多个查看、创建和删除目录及文件的
函数，以及一些操作路径的函数（例如，os.path.split和os.path.join让你在大多数情况下都可
忽略os.pathsep）。有关这个模块的详细信息，请参阅标准库文档。在标准库文档中，还可找到
有关模块pathlib的描述，它提供了一个面向对象的路径操作接口。

            表10-3 模块os中一些重要的函数和变量
函数/变量                描 述
environ               包含环境变量的映射
system(command)       在子shell中执行操作系统命令
sep                   路径中使用的分隔符
pathsep               分隔不同路径的分隔符
linesep               行分隔符（'\n'、'\r'或'\r\n'）
urandom(n)            返回n个字节的强加密随机数据


    映射os.environ包含本章前面介绍的环境变量。例如，要访问环境变量PYTHONPATH，可使用表达
式os.environ['PYTHONPATH']。这个映射也可用于修改环境变量，但并非所有的平台都支持这样做。
函数os.system用于运行外部程序。还有其他用于执行外部程序的函数，如execv和popen。前
者退出Python解释器，并将控制权交给被执行的程序，而后者创建一个到程序的连接（这个连接
类似于文件）。

有关这些函数的详细信息，请参阅标准库文档。


提示    请参阅模块subprocess，它融合了模块os.system以及函数execv和popen的功能。

    变量os.sep是用于路径名中的分隔符。在UNIX（以及macOS的命令行Python版本）中，标准
分隔符为/。在Windows中，标准分隔符为\\（这种Python语法表示单个反斜杠）。在旧式macOS
中，标准分隔符为:。（在有些平台中，os.altsep包含替代路径分隔符，如Windows中的/。）

    可使用os.pathsep来组合多条路径，就像PYTHONPATH中那样。pathsep用于分隔不同的路径名：
在UNIX/macOS中为:，而在Windows中为;。

变量os.linesep是用于文本文件中的行分隔符：在UNIX/OS X中为单个换行符（\n），在
Windows中为回车和换行符（\r\n）。


    函数urandom使用随系统而异的“真正”（至少是强加密）随机源。如果平台没有提供这样的
随机源，将引发NotImplementedError异常。


    例如，看看启动Web浏览器的问题。命令system可用于执行任何外部程序，这在UNIX等环境
中很有用，因为你可从命令行执行程序（或命令）来列出目录的内容、发送电子邮件等。它还可
用于启动图形用户界面程序，如Web浏览器。在UNIX中，可像下面这样做（这里假定/usr/bin/firefox
处有浏览器）：
    os.system('/usr/bin/firefox')

在Windows中，可以这样做（同样，这里指定的是你安装浏览器的路径）：
    os.system(r'C:\"Program Files (x86)"\"Mozilla Firefox"\firefox.exe')

    请注意，这里用引号将Program Files和Mozilla Firefox括起来了。如果不这样做，底层shell
将受阻于空白处（对于PYTHONPATH中的路径，也必须这样做）。另外，这里必须使用反斜杆，因
为Windows shell 无法识别斜杠。如果你执行这个命令， 将发现浏览器试图打开名为
Files"\Mozilla…（空白后面的命令部分）的网站。另外，如果你在IDLE中执行这个命令，将出
现一个DOS窗口，关闭这个窗口后浏览器才会启动。总之，结果不太理想。

    另一个函数更适合用于完成这项任务，它就是Windows特有的函数os.startfile。
    os.startfile(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

    如你所见，os.startfile接受一个普通路径，即便该路径包含空白也没关系（无需像os.system
示例中那样用引号将Program Files括起）。
    请注意，在Windows中，使用os.system或os.startfile启动外部程序后，当前Python程序将
继续运行；而在UNIX中，当前Python程序将等待命令os.system结束。

                        更佳的解决方案：webbrowser
    函数os.system可用于完成很多任务，但就启动Web浏览器这项任务而言，有一种更佳的
解决方案：使用模块webbrowser。这个模块包含一个名为open的函数，让你能够启动启动Web
浏览器并打开指定的URL。例如，要让程序在Web浏览器中打开Python网站（启动浏览器或使
用正在运行的浏览器，只需像下面这样做：

    import webbrowser
    webbrowser.open('http://www.python.org')

这将弹出指定的网页。




'''























