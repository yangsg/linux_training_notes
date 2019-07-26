#// https://www.python-course.eu/python3_decorators.php


#// demo01：一个简单的 函数的 装饰器 的 例子

def our_decorator(func):
  def function_wrapper(*args, **kwargs):
    print('^' * 50)
    func(*args, **kwargs);
    print('$' * 50)

  print(func)
  print(function_wrapper)
  return function_wrapper

#// 其实类似于调用 f1 = our_decorator(f1), 传参的时候 f1 引用 原始的 'f1' 函数对象,
#// 返回后 f1 引用 的是 function_wrapper 函数对象. 就这样 f1 引用的对象 就被 '偷换' 了 .
@our_decorator
def f1(msg):
  print(msg)

print(f1)

f1('hello world')


''' 结果输出:
<function f1 at 0x7f73febf9048>
<function our_decorator.<locals>.function_wrapper at 0x7f73febf90d0>
<function our_decorator.<locals>.function_wrapper at 0x7f73febf90d0>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hello world
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
'''


#// demo02：一个 带参数的 装饰器 的 例子
#// 来自 https://www.python-course.eu/python3_decorators.php
def greeting(expr):
    def greeting_decorator(func):
        def function_wrapper(x):
            print(expr + ", " + func.__name__ + " returns:")
            func(x)
        return function_wrapper
    return greeting_decorator

#// 类似 foo = (greeting("καλημερα"))(foo)
@greeting("καλημερα")
def foo(x):
    print(42)

foo("Hi")





