
#// https://docs.python.org/3.6/tutorial/classes.html#a-first-look-at-classes

#// 类定义需要先执行才能生效(可以将class 定义放在if 语句块或函数的内部)
if True:
    class ClassInIfBlock():
        pass

def function():
    class ClassInFunction:
        pass


#// 当进入 class definition 时，被当做 local scope的一个新的名字空间(namespace) 就被创建了
#// When a class definition is entered, a new namespace is created, and used as the local scope — thus,
#// all assignments to local variables go into this new namespace. In particular,
#// function definitions bind the name of the new function here.


#// When a class definition is left normally (via the end), a class object is created.
#// This is basically a wrapper around the contents of the namespace created by the class definition;
#// we’ll learn more about class objects in the next section. The original local scope
#// (the one in effect just before the class definition was entered) is reinstated,
#// and the class object is bound here to the class name given in the class definition header (ClassName in the example).


#// Class objects 支持两种类型的操作：成员引用 和 实例化
#// Class objects support two kinds of operations: attribute references and instantiation.
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'


print(MyClass.i)  #// 12345
print(MyClass.f)  #// <function MyClass.f at 0x7efe4bb270d0>

MyClass.i = 7777
print(MyClass.i)  #// 7777

print(MyClass.__doc__) #// A simple example class


#// 类的实例化，即创建一个属于该类的对象
x = MyClass()  #// 有点类似于java 中的 'new MyClass()', 但是python中没有new关键字


#// python中的 __init__ 函数作用类似于 java中的构造器函数的作用
class ClassWithInitFunction():
    def __init__(self): #// 带有 __init__ 初始函数的类, 每次实例化时会被自动调用
        self.data = ['a', 'b']

x = ClassWithInitFunction()
print(x.data)  #// ['a', 'b']


#// __init__ 函数接收参数的类
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = Complex(3.0, -4.5)
print('x.r = {}, x.i = {}'.format(x.r, x.i))  #// x.r = 3.0, x.i = -4.5







