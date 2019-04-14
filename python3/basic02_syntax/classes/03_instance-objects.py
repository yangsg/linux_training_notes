#// https://docs.python.org/3.6/tutorial/classes.html#instance-objects

#// Instance Objects

#// 实例对象唯一理解的操作就是 attribute references. There are two kinds of valid attribute names, data attributes and methods.

#// data attributes 不需要被声明(be declared), 类似于 local variables，它们在首次赋值时会立即存在。
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world {}'.format(self.i)

x = MyClass()
x.id = 22
print(x.id)
del x.id

print(x.f())

#//此时x.f并不是一般的函数(虽然具有函数的大部分特征)，而是一个类型为 'method' 的对象, 其内部封装了 'self' 名字关联的实例对象 和 原始的那个f函数
#//  原文(关于method的部分工作原理)：
#//    If you still don’t understand how methods work, a look at the implementation can perhaps clarify matters.
#//    When a non-data attribute of an instance is referenced, the instance’s class is searched.
#//    If the name denotes a valid class attribute that is a function object, a method object is
#//    created by packing (pointers to) the instance object and the function object just found together
#//    in an abstract object: this is the method object. When the method object is called with an argument list,
#//    a new argument list is constructed from the instance object and the argument list,
#//    and the function object is called with this new argument list.

xf = x.f    #// python中方法可以被赋给其他变量(绑定到其他name)，通过其他变量来调用
print(xf())
print(type(x.f)) #// <class 'method'>
print(type(xf))  #// <class 'method'>



#// https://docs.python.org/3.6/tutorial/classes.html#class-and-instance-variables
#// Class and Instance Variables
#// 一般而言，实例变量代表对每个instance特有的唯一的数据，类变量代表该类的所有实例共享的属性和方法

class Dog:

    kind = 'canine'         # class variable shared by all instances

    def __init__(self, name):
        self.name = name    # instance variable unique to each instance

d = Dog('Fido')
e = Dog('Buddy')
print(d.kind)         # shared by all dogs  #// canine
print(e.kind)         # shared by all dogs  #// canine
Dog.kind = '111111111111111'
print(d.kind)         # shared by all dogs  #// '111111111111111'
print(e.kind)         # shared by all dogs  #// '111111111111111'
d.kind = 'aaaaaaaaaaa'
print(d.kind)         #                     #// 'aaaaaaaaaaa'  <<<<<<<<<
print(e.kind)         # shared by all dogs  #// '111111111111111'
print(d.name)         # unique to d
print(e.name)         # unique to e


#// Random Remarks
#//   Data attributes override method attributes with the same name;
#//   一种明智的做法就是使用某种约定来最小化冲突的可能性。
#//   可行的约定包括 method names 首字母大写，为 data attribute 添加一个
#//   小的唯一的 字符串作为前缀(比如可能仅仅是一个下划线符号‘_’)，或者命名methods
#//   时使用动词，而命名 data attributes 时使用名称


#// 事实上，Python 没有语法层面的强制性的机制(如编译时报错, 如java就提供了private这种语法可帮助用于实现数据隐藏)
#// 来实现数据隐藏,这只能通过基于某种规范约定来达成, 这种规范对python语言来说意义非常重要, 只有这样，才能更好地实现
#// 强内聚弱耦合的代码，否则消费端的代码可能无意中就破坏了服务器代码内部的实现机制(因为python没有语法层面的信息隐藏约束机制)

#// 没有简写形式用于 在 methond 内部引用 data attributes 或 其他 methods(所以只能通过self.somedata 或 self.other_method来引用)
#// 这也提供了一种好处：不会混淆本地变量 和 示例的成员变量，因为实例成员变量始终带有前缀'self.'

#// 通常，方法的第1个参数取名为 self, 这只是一种习惯罢了，当然你可以换成任意其他的名字
#// (在javascript的一些设计模式中，也是喜欢使用self这个变量名来保存原有方法中 this 对象的引用)


#// Any function object that is a class attribute defines a method for instances of that class.
#// It is not necessary that the function definition is textually enclosed in the class definition:
#// assigning a function object to a local variable in the class is also ok. For example:

# Function defined outside the class
def f1(self, x, y):
    return min(x, x+y)

class C:
    f = f1  #// 方法f的method object定义不要求必须在class 的scope内部，完全可以定义在其他定法，然后赋值给class的local变量来实现(即此处的f)

    def g(self):
        return 'hello world'

    h = g


#// Methods may call other methods by using method attributes of the self argument:
class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        #// python 引用实例成员时必须加上 'self.' 实例变量作为前缀
        #// (因为不向java那样提供了引用成员变量的简写的语法机制),
        #// 好处就是不会与同名的local variable混淆
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)


#// 方法可以像普通函数一样的方式引用 global names, 一个方法的global scope 就是其被定义所在的那个模块 module
#// (即方法是在那个模块中定义的，那个模块就是这个方法所关联的global scope),注：class 是永远不可能当成 global scope来使用的.
#// 存在许多的对 global scope 的合法的使用：一方面，被导入到 global scope 的 functions 和 modules 可以被 方法使用，同时
#// 定义在该方法内部的 functions 和 classes 也可以被该方法使用。通常，包含method 的 class 本身也是定义在 global scope
#// 中的(因class经常被直接定义在module的global scope中)


#// Each value is an object, and therefore has a class (also called its type). It is stored as object.__class__.
number = 12
print(number.__class__)





















