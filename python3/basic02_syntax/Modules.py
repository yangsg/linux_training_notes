#// https://docs.python.org/3.6/tutorial/modules.html#modules

#// main module

#// 创建一个文件 filename.py, 其中文件名 filename 即为 模块名(类似java中 文件名就是类型)
#// 全局变量 __name__ 存储的值即为 模块名

#// demo01-----------------------------------------------------
#// [root@python3lang ~]# mkdir mypackage
#// [root@python3lang ~]# cd mypackage/
#// [root@python3lang mypackage]# vim mymath.py
def sum(a, b):
    return a + b

if __name__ == '__main__':
    print('now mypath.py is as main module')

# [root@python3lang mypackage]# vim hello.py
import mymath

result = mymath.sum(2, 3)
print(result)

fsum = mymath.sum  # python3 中 函数是可以复制给其他变量的(类似于javascript或c语言)

# [root@python3lang mypackage]# python hello.py

#// -----------------------------------------------------

#// https://docs.python.org/3.6/tutorial/modules.html#more-on-modules
#// 模块中的代码在只会在第一次被import时会被执行,每个模块都有自己私有的符号表(private symbol table)
#// 它被该模块中定义的所有functions 当做全局符号表(global symbol table)来使用 (这和nodejs中的module有点类似)

#// Modules can import other modules. It is customary but not required to place all
#// import statements at the beginning of a module (or script, for that matter).
#// The imported module names are placed in the importing module’s global symbol table.

#//import 语句的一些变体:
#// from fibo import fib, fib2  #将模块fibo中的名称 fib, fib2导入到当前模块的符号表而不是将模块本身名称导入
#// from fibo import *          #导出除了以 '_' 开头的所有名称, 该方式不推荐
#// import fibo as fib          #名称 fib 将被绑定到符号表
#// from fibo import fib as fibonacci


#// Note For efficiency reasons, each module is only imported once per interpreter session. Therefore, if you
#// change your modules, you must restart the interpreter – or, if it’s just one module you want to test interactively,
#// use importlib.reload(), e.g.
#//      import importlib;
#//      importlib.reload(modulename)

#// https://docs.python.org/3.6/tutorial/modules.html#executing-modules-as-scripts
#// Executing modules as scripts-------------------------------
#//  python fibo.py <arguments>
if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))

#// python fibo.py 50



#// https://docs.python.org/3.6/tutorial/modules.html#the-module-search-path
#// The Module Search Path -------------------------------------
#// Module 的搜索顺序：
#//  1. 先查找 built-in module
#//  2. 如果1失败，查找 sys.path 变量给定的目录列表

#//  sys.path is initialized from these locations:
#//     The directory containing the input script (or the current directory when no file is specified).
#//     PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).
#//     The installation-dependent default.


#// Note: On file systems which support symlinks, the directory containing the input script is calculated after the
#// symlink is followed. In other words the directory containing the symlink is not added to the module search path.

import sys
sys.ps1    #注：变量 sys.ps1 和 sys.ps2 只有在python解释器处于交互模式(interactive mode)时才会被定义
sys.ps2

import sys
sys.path.append('/ufs/guido/lib/python')   #通过python代码手动修改 sys.path变量


#// export PYTHONPATH=/path/to/extra/python/lib   # 通过shell的环境变量PYTHONPATH修改sys.path变量

import builtins  #python内置的函数和变量都被定义在标准模块 builtins 中
dir(builtins)     #用户返回module所定义的排序后的名称列表
dir()             # 默认返回当前module的名称列表




#// https://docs.python.org/3.6/tutorial/modules.html#packages
#// Packages

import sound.effects.echo  # 导入sound.effects.echo到名字空间，引用是不许使用 'sound.effects.echo'
from sound.effects import echo  # 导入 'echo', 引用是使用 'echo' 即可
from sound.effects.echo import echofilter   #直接导入函数或变量，而非导入模块

#// https://docs.python.org/3.6/tutorial/modules.html#importing-from-a-package
#// Importing * From a Package  #不要在生产环境使用这种import方式，这被认为是最差实践(不提倡)

#//   __init__.py 可有可无，它主要用于类似from sound.effects import * 这样的语句时限制导出的名称
#//   如通过 __all__ = ["echo", "surround", "reverse"] 枚举出可导出的模块名


#// https://docs.python.org/3.6/tutorial/modules.html#intra-package-references
#// Intra-package References

from sound.effects import echo  # 绝对路径方式
from . import echo              # 相对路径方式
from .. import formats
from ..filters import equalizer


















