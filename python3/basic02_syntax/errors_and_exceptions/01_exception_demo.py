
def demo01():  #// 如果输出非整数字符，该例子需要按 Control-C 来抛出 KeyboardInterrupt 异常中止
    while True:
        try:  #// python3 的 try ... except 的处理流程和 java 的 异常流程是类似的
            x = int(input("Please enter a number: "))
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

#// demo01()


def multiple_exceptions_in_parenthesized_tuple():
    try:
        x = input("Please enter a number: ")
        if x == '1':
            raise RuntimeError()
        elif x == '2':
            raise TypeError()
        else:
            raise NameError()
    except (RuntimeError, TypeError, NameError):  #// 在一个 except 子句中声明捕获多种类型的异常
        print("Oops!  error catched!!!")

#// multiple_exceptions_in_parenthesized_tuple()

def exception_inheritance():
    class B(Exception):
        pass

    class C(B):
        pass

    class D(C):
        pass

    for cls in [B, C, D]:
        try:             #// 类似于java对具有继承关系的异常的处理, 参考：<thinking in java> https://legacy.gitbook.com/book/alleniverson/thinking-in-java/details
            raise cls()
        except D:
            print("D")
        except C:
            print("C")
        except B:
            print("B")

#// exception_inheritance()


def default_exception_handler():
    import sys
    try:
        f = open('/etc/fstab')
        s = f.readline()
        i = int(s.strip())
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:  #// <---- 没有给出具体的异常名，相当于提供了一个匹配所有异常的通配符来捕获所有的异常(小心使用该特性，因为可能容易隐藏某些程序错误)
        print("Unexpected error:", sys.exc_info()[0])
        raise    #// <---- 重新抛出异常(好处是在向上层抛出异常前可以做一些处理)

#// default_exception_handler()


def else_clause_after_except_clause():
    import sys
    for arg in sys.argv[1:]:
        try:
            f = open(arg, 'r')
            print('try clause成功执行完毕')
        except OSError:
            print('cannot open', arg)
            print('try clause 发生了异常')
        else:  #// else 只会在 try 成功执行结束(即没抛出任何异常)后得到执行机会, 且语法上必须更在所有 except 子句之后
            print(arg, 'has', len(f.readlines()), 'lines')
            print('else clause 执行了')
            f.close()

#// 分别使用下面两条命令对 else_clause_after_except_clause 函数效果进行观察
#// python3 01_exception_demo.py /etc/fstab
#// python3 01_exception_demo.py
#// else_clause_after_except_clause()

def arguments_to_except_clause():
    #// If an exception has arguments, they are printed as the last part (‘detail’) of the message for unhandled exceptions.
    try:
        raise Exception('spam', 'eggs')
    except Exception as inst:  #// 类似于 java 中 ‘catch(Exception e)’ 这种语句, 捕获异常的同时持有了异常对象的引用
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)

#// arguments_to_except_clause()


def except_handler_also_handle_innermost_exception(): #// 意思就是 异常 会向上层层抛出，直到被捕获处理为止
    def this_fails():
        x = 1/0

    try:
        this_fails()
    except ZeroDivisionError as err:
        print('Handling run-time error:', err)

#// except_handler_also_handle_innermost_exception()


def raise_exception():  #// 手动抛出异常
    try:
        raise NameError('HiThere')  #// 类似java 中 'throw new Exception()' 语句
    except NameError as e1:
        print(NameError)

    try:
        #// raise语句对无参的异常构造器函数的一种简化调用方法
        raise ValueError  # shorthand for 'raise ValueError()'
    except ValueError as e1:
        print(ValueError)

#// raise_exception()


def re_raise_exception():
    try:
        try:
            raise NameError('HiThere')
        except NameError:
            print('An exception flew by!')
            raise  #// 重新抛出异常
    except:
        print('---outer except handler handle the exception actually')

#// re_raise_exception()


#// python 语言中异常类的类名 喜欢以 Error 作为后缀名
def user_defined_exception():  #// 用户自定义异常, 异常应该直接或间接派生自  Exception 类
    #// 设计模块时， 对于根据不同条件抛出不同类型的错误时，一个通常的实践是针对于该模块创建一个异常基类(即base Error),
    #// 然后针对不同的情况创建其 不同的子类表表示不同的异常
    class Error(Exception):
        """Base class for exceptions in this module."""
        pass

    class InputError(Error):
        """Exception raised for errors in the input.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the error
        """

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

    class TransitionError(Error):
        """Raised when an operation attempts a state transition that's not
        allowed.

        Attributes:
            previous -- state at beginning of transition
            next -- attempted new state
            message -- explanation of why the specific transition is not allowed
        """

        def __init__(self, previous, next, message):
            self.previous = previous
            self.next = next
            self.message = message


def defining_clean_up_actions():  #// finally 子句的例子, 和java中的finally 子句类似
    def divide(x, y):
        try:
            result = x / y
            return
        except ZeroDivisionError:
            print("division by zero!")
            print("except clause >>>>>")
        else:
            print("result is", result)
            print('else clause >>>>>')
        finally: #// finally 子句 主要用于释放必须释放的资源,尤其是外部资源(如 file 或 network connections等)
            print("executing finally clause")

    print('divide(2, 2)----------')
    divide(2, 2)
    print('divide(2, 0)----------')
    divide(2, 0)

#// defining_clean_up_actions()

def predefined_clean_up_actions():
    with open("/etc/shells") as f:  #// 此处 with 会保证自动清理 f 表示的文件资源(不论是否发生异常), 这样简化的代码的编写
    #//with open("myfile.txt") as f:
        for line in f:
            print(line, end="")

predefined_clean_up_actions()












