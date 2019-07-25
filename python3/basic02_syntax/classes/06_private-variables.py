
#// https://docs.python.org/3.6/tutorial/classes.html#private-variables

#// Private Variables 私有变量
#// python 没有提供定义 private 私有实例变量的语法机制，只有通过编码 规范约定 来达成，
#//
#// 被大多数python 代码遵循的规范有：
#//     名字以  1 个 下划线‘_’ 作为前缀的, 应当被视为非公共api 的一部分(不管该名字代表的是function, a method or a data member)

'''
    _private_variable = 'this is private variable(这只是普通private variable,
    而不是利用了name mangling机制的class private variable), not part of the public api.
    对于class-private member,要使用双下划线做前缀(或最多一个下划线后缀),
    如 __class_private_member or  __class_private_member_'
'''


def _private_function():
    pass


#// class-private members  类的私有成员 (这种机制的名称叫 name mangling)

'''
name mangling 的实现机制：
   任何identifier 标识符形如 __spam (至少2个下划线前缀，最多一个下划线后缀),
   会被文本替换为 _classname__spam, 其中的 classname 就是当前的类名(即_classname中‘_’前缀被截断的部分)
   This mangling是完成不需要考虑identifier的语法位置， 只要其出现在类的定义中即可


原文：
Since there is a valid use-case for class-private members (namely to avoid name clashes of names
with names defined by subclasses), there is limited support for such a mechanism,
called name mangling. Any identifier of the form __spam (at least two leading underscores,
at most one trailing underscore) is textually replaced with _classname__spam, where classname
is the current class name with leading underscore(s) stripped. This mangling is done without
regard to the syntactic position of the identifier, as long as it occurs within the definition of a class.
'''


class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)

print(Mapping._Mapping__update)            #// <function Mapping.update at 0x7f02bbfb3158>
print(MappingSubclass._Mapping__update)    #// <function Mapping.update at 0x7f02bbfb3158>


print('------------------------------------------------------------')
class MyClass:
    __private_variable  = 'case 01: class private variable, form: __name,  利用了name mangling机制'
    __private_variable_ = 'case 02: class private variable, form: __name_, 利用了name mangling机制'
    __private_member =  'class private member'
    __private_member_ = 'class private member'


print(MyClass._MyClass__private_variable)
print(MyClass._MyClass__private_variable_)
#// print(MyClass.__private_variable)  #// error
#// print(MyClass.__private_variable_) #// error


#// Notice that code passed to exec() or eval() does not consider the classname of the invoking
#// class to be the current class; this is similar to the effect of the global statement,
#// the effect of which is likewise restricted to code that is byte-compiled together. The same
#// restriction applies to getattr(), setattr() and delattr(), as well as when referencing __dict__ directly.


























