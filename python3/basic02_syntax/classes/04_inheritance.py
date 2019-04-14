
#// https://docs.python.org/3.6/tutorial/classes.html#inheritance
#// 继承语法
'''
        class DerivedClassName(BaseClassName):  #// 基类 BaseClassName 的名字必须是在 定义 DerivedClassName 的 scope 内是可用的
            <statement-1>
            .
            .
            .
            <statement-N>
'''
#// 基类 BaseClassName 的名字必须是在 定义 DerivedClassName 的 scope 内是可用的
#// 处理简单的 BaseClassName 的形式，任何其他的表示形式也是允许的：
#// 如：
#// class DerivedClassName(modname.BaseClassName):


#// 如下这种技术经常见于如 模板 设计模式中
#// a method of a base class that calls another method defined in the same base class may end up calling a
#// method of a derived class that overrides it. (For C++ programmers: all methods in Python are effectively virtual.)


#// python中子类方法定义中调用父类中的方法的语法形式就是 BaseClassName.methodname(self, arguments)
#// There is a simple way to call the base class method directly:
#// just call BaseClassName.methodname(self, arguments).
#// This is occasionally useful to clients as well.
#// (Note that this only works if the base class is accessible as BaseClassName in the global scope.)


'''
Python has two built-in functions that work with inheritance:
    Use isinstance() to check an instance’s type: isinstance(obj, int) will be True only if obj.__class__ is int or some class derived from int.
    Use issubclass() to check class inheritance: issubclass(bool, int) is True since bool is a subclass of int.
                    However, issubclass(float, int) is False since float is not a subclass of int.
'''


value = 123
isInt = isinstance(value, int)  #// 检查 value.__class__  是否是 int 或 由 int 派生出来的某个子类
print(isInt)

isSubClass = issubclass(bool, int)  #// 检查 bool 类 是否是 int 的子类
print(isSubClass)  #// True  #// python 中 bool 类 是 int 类的子类

print(issubclass(int, int)) #// True  #// 注； issubclass 中的判断具有 自反性














