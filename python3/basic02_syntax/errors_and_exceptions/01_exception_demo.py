
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

default_exception_handler()









