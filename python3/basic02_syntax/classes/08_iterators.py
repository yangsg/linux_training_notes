#// https://docs.python.org/3.6/tutorial/classes.html#iterators

#// Iterators
def iterator_usage_demo():
    for element in [1, 2, 3]:
        print(element)
    for element in (1, 2, 3):
        print(element)
    for key in {'one':1, 'two':2}:
        print(key)
    for char in "123":
        print(char)
    for line in open("/etc/fstab"):
        print(line, end='')

#// iterator_usage_demo()

'''
    for ... in ... 的工作机制(联想java中的迭代器设计模式来帮助理解)：
        调用 iter() 获取容器对象的iterator对象，然后调用
        iterator 对象上的 __next__() 返回容器对象中的一个元素，如果没有更多的元素可返回时,
        __next__() 会抛出 StopIteration 异常来告诉 for 循环终止
        你可以通过 next() 来调用 __next__() 方法

    原文：
        This style of access is clear, concise, and convenient. The use of iterators
        pervades and unifies Python. Behind the scenes, the for statement calls iter()
        on the container object. The function returns an iterator object that defines
        the method __next__() which accesses elements in the container one at a time.
        When there are no more elements, __next__() raises a StopIteration exception
        which tells the for loop to terminate. You can call the __next__() method using
        the next() built-in function; this example shows how it all works:
'''

def iterate_string_sequence_mannual():
    s = 'abc'
    it = iter(s)
    print(it)
    print(next(it)) #// a
    print(next(it)) #// b
    print(next(it)) #// c
    print(next(it)) #// raise StopIteration

#// iterate_string_sequence_mannual()

#// https://docs.python.org/3/library/stdtypes.html#typeiter
#// https://docs.python.org/3/glossary.html
#//     iterable 能够一次一个的返回其 members 的对象
#//     An object capable of returning its members one at a time.

#// iterable 的例子包括：
#// 所有的 sequence 类型(如 list, str, 和 tuple), 一些 non-sequence 类型(如dict, file objects),
#// 任何定义了 __iter__() 方法 或者  定义 实现了sequence语义的 __getitem__()方法的类

#// https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range
#// There are three basic sequence types: lists, tuples, and range objects.


#// https://docs.python.org/3/glossary.html
#// iterator 表示数据流的对象
#// An object representing a stream of data.


#// 自定义
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

rev = Reverse('spam')
print(iter(rev))     #// <__main__.Reverse object at 0x7f7c9398b2e8>
for char in rev:
    print(char)


#// 判断一个对象是否是 iterable 类型
#// https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
import collections
isinstance((x for x in range(10)), collections.Iterable) # 判断一个对象是否是 Iterable
isinstance((x for x in range(10)), collections.Iterator) # 判断一个对象是否是 Iterator
isinstance((x for x in range(10)), collections.Generator) # 判断一个对象是否是 Generator
isinstance([1,2,3], collections.Sequence)                #  判断一个对象是否是 Sequence

issubclass(collections.Iterator, collections.Iterable)
issubclass(collections.Generator, collections.Iterator)


import collections.abc
isinstance((x for x in range(10)), collections.abc.Iterable) # 判断一个对象是否是 Iterable, 从python3.3开始，collections.Iterable 移到了collections.abc.Iterable, 不过因为兼容性，旧的仍然可用


#// https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
#// Collections Abstract Base Classes
#// --------------------------------------------------------------------------------
#// |ABC        | Inherits from  |  Abstract Methods  |  Mixin Methods             |
#// |-----------|----------------|--------------------|----------------------------|
#// |Iterable   |                |  __iter__          |                            |
#// |-----------|----------------|--------------------|----------------------------|
#// |Iterator   | Iterable       |  __next__          |  __iter__                  |
#// |-----------|----------------|--------------------|----------------------------|
#// |Generator  | Iterator       |  send, throw       |  close, __iter__, __next__ |
#// --------------------------------------------------------------------------------







