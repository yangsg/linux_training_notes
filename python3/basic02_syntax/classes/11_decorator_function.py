#// https://www.python-course.eu/python3_decorators.php


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


