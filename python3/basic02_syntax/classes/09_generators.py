
#// https://docs.python.org/3.6/tutorial/classes.html#generators


#// Generator 是一种简单且强大的创建 iterators 的工具, 它和普通的function在编写
#// 上没什么区别，除了在任何其想要返回data的时候使用 yield 语句. 每次调用其 next()
#// 函数的时候，Generator 都会 从离开的地方继续执行(它会记住所有的数据和上次执行的哪条语句,相当于记住了离开时的现场信息)
#//
#// 原文：
#// Generators are a simple and powerful tool for creating iterators. They are
#// written like regular functions but use the yield statement whenever they want
#// to return data. Each time next() is called on it, the generator resumes where
#// it left off (it remembers all the data values and which statement was last
#// executed). An example shows that generators can be trivially easy to create:

#// 一个 Generator 的简单示例：
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]


print(type(reverse('abcdefg')))  #// <class 'generator'>
print(reverse('abcdefg'))  #// <generator object reverse at 0x7fe4ebcf1150>

for i in reverse('abcdefg'):
    print(i)


#// 任何generator 能做的事情，class-based iterators 也都能做，而 generator 编码能如此紧凑简洁
#// 是因为其 __iter__() 和 __next__() 方法都是自动创建的
#//
#//  原文：
#//  Anything that can be done with generators can also be done with class-based
#//  iterators as described in the previous section. What makes generators so
#//  compact is that the __iter__() and __next__() methods are created
#//  automatically.

#// 自动记录现场信息(本地变量和执行的状态)
#// 原文：
#//     Another key feature is that the local variables and execution state are
#//     automatically saved between calls. This made the function easier to write and
#//     much more clear than an approach using instance variables like self.index and
#//     self.data.

#// 当generator 终止时，它会自动抛出异常(raise StopIteration)
#// 原文：
#//    In addition to automatic method creation and saving program state, when
#//    generators terminate, they automatically raise StopIteration. In combination,
#//    these features make it easy to create iterators with no more effort than
#//    writing a regular function.


#// 生成器表达式 https://docs.python.org/3.6/tutorial/classes.html#generator-expressions
#// Generator Expressions
#// 生成器表达式比起完整的生成器定义 更加紧凑 但功能更单一，比起list comprehensions, 生成器
#// 表达式对内存更加友好
#//
#// 原文：
#//  Some simple generators can be coded succinctly as expressions using a syntax
#//  similar to list comprehensions but with parentheses instead of square brackets.
#//  These expressions are designed for situations where the generator is used right
#//  away by an enclosing function. Generator expressions are more compact but less
#//  versatile than full generator definitions and tend to be more memory friendly
#//  than equivalent list comprehensions.

sum(i*i for i in range(10))                 # sum of squares

xvec = [10, 20, 30]
yvec = [7, 5, 3]
sum(x*y for x,y in zip(xvec, yvec))         # dot product


from math import pi, sin
sine_table = {x: sin(x*pi/180) for x in range(0, 91)}

unique_words = set(word  for line in page  for word in line.split())

valedictorian = max((student.gpa, student.name) for student in graduates)

data = 'golf'
list(data[i] for i in range(len(data)-1, -1, -1))





















