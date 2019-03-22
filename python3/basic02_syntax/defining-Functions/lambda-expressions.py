#// https://docs.python.org/3.6/tutorial/controlflow.html#unpacking-argument-lists


#// demo01
def make_incrementor(n):
    return lambda x: x + n  #此处类似javascript中创建了一个闭包

f = make_incrementor(42)
f(0)
f(1)


#// demo02

pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])   #类似javascript中传递一个回调函数或钩子函数，可以理解为是一种策略设计模式
pairs



