
#// https://docs.python.org/3.6/tutorial/classes.html#odds-and-ends

#// Odds and Ends


#// class 包含空定义是允许的,这种方式可以提供一种类似C语言中struct结构数据类型的效果, 抽象数据类型
class Employee:
    pass

john = Employee()  # Create an empty employee record

# Fill the fields of the record
john.name = 'John Doe'
john.dept = 'computer lab'
john.salary = 1000


#// 实例方法对象也拥有属性(注：python中method也是一种对象类型，其对实例对象 __self__ 和 原始的函数对象 __func__ 进行了封装)
#// Instance method objects have attributes, too:
#//      m.__self__ is the instance object with the method m(), and
#//      m.__func__ is the function object corresponding to the method.

class MyClass:
    def f(self):
        pass

obj = MyClass()

print(obj)            #// <__main__.MyClass object at 0x7f82ebf7e1d0>
print(obj.f.__self__) #// <__main__.MyClass object at 0x7f82ebf7e1d0>
print(obj.f)          #// <bound method MyClass.f of <__main__.MyClass object at 0x7f82ebf7e1d0>>
print(obj.f.__func__) #// <function MyClass.f at 0x7f82ebf82048>
print(MyClass.f)      #// <function MyClass.f at 0x7fc8208ac048>












