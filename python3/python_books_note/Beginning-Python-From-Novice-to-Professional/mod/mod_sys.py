# sys

# 模块sys让你能够访问与Python解释器紧密相关的变量和函数，表10-2列出了其中的一些。

'''
                表10-2 模块sys中一些重要的函数和变量
函数/变量            描 述
argv              命令行参数，包括脚本名
exit([arg])       退出当前程序，可通过可选参数指定返回值或错误消息
modules           一个字典，将模块名映射到加载的模块
path              一个列表，包含要在其中查找模块的目录的名称
platform          一个平台标识符，如sunos5或win32
stdin             标准输入流——一个类似于文件的对象
stdout            标准输出流——一个类似于文件的对象
stderr            标准错误流——一个类似于文件的对象


    变量sys.platform（一个字符串）是运行解释器的“平台”名称。这可能是表示操作系统的名
称（如sunos5或win32），也可能是表示其他平台类型（如Java虚拟机）的名称（如java1.4.0）——
如果你运行的是Jython。

    变量sys.stdin、sys.stdout和sys.stderr是类似于文件的流对象，表示标准的UNIX概念：
标准输入、标准输出和标准错误。简单地说，Python从sys.stdin获取输入（例如，用于input中），
并将输出打印到sys.stdout。有关文件和这三个流的详细信息，请参阅第11章。

    举个例子，来看看按相反顺序打印参数的问题。从命令行调用Python脚本时，你可能指定一
些参数，也就是所谓的命令行参数。这些参数将放在列表sys.argv中，其中sys.argv[0]为Python
脚本名。按相反的顺序打印这些参数非常容易，如代码清单10-5所示。

'''

# 代码清单10-5 反转并打印命令行参数
# reverseargs.py
import sys
args = sys.argv[1:]
args.reverse()
print(' '.join(args))

'''
如你所见，我创建了一个sys.argv的副本。也可修改sys.argv，但一般而言，不这样做更安
全，因为程序的其他部分可能依赖于包含原始参数的sys.argv。另外，注意到我跳过了sys.argv
的第一个元素，即脚本的名称。我使用args.reverse()反转这个列表，但不能打印这个操作的返
回值，因为它就地修改列表并返回None。下面是另一种解决方案：

print(' '.join(reversed(sys.argv[1:])))

最后，为美化输出，我使用了字符串的方法join。下面来尝试运行这个程序（假设使用的是 bash shell）。

$ python reverseargs.py this is a test
test a is this
'''




