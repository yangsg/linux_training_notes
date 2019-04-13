#// https://docs.python.org/3.6/tutorial/classes.html

python的类的机制借鉴了 C++ and Modula-3 这两种语言

python 允许多重继承

在python中，同 modules 一样，classes 也具有 python语言的动态特性：它们在运行时
   被创建，同时还能在创建之后被修改


相比于c++, python在面向对象的语义上更接近于 Modula-3
python中类的方法需要显示声明所属对象为第一个参数，而这个参数在方法调用时会被自动传入，
和 Smalltalk 语言类似， classes 本身也是对象， 这位 importing and renaming 提供了语义支持

https://docs.python.org/3.6/tutorial/classes.html#a-word-about-names-and-objects
对象具有独立性，且多个作用域中的多个 名字 可以绑定到同一个对象，
在其他语言中这被称为 别名 (类比生活中一个独立的个人(这个独立的生命物体), 除了身份证上的名字外，还可能有其他不同的绰号)
牢记这一点会帮助你更容易理解 python 中涉及处理可变对象(如 lists, dictionaries, and most other types)的某些代码
是在语义上的解释


https://docs.python.org/3.6/tutorial/classes.html#python-scopes-and-namespaces
Python Scopes and Namespaces
    A namespace is a mapping from names to objects. Most namespaces are currently implemented as Python dictionaries

    Examples of namespaces are:
        1. the set of built-in names (containing functions such as abs(), and built-in exception names)
        2. the global names in a module;
        3. the local names in a function invocation.
    In a sense the set of attributes of an object also form a namespace.

    不同的各个 namespaces 之间没有任何联系(这好比每个不同的教室之间，当作为独立空间时，每个空间对于内部的作为编号是不受其他教室空间的影响的)

严格的说，引用模块中的名字其实就用引用模块对象的一个属性(注：这里的术语'属性'没有区分property 和 method, 可理解为'成员')
Strictly speaking, references to names in modules are attribute references:
in the expression modname.funcname, modname is a module object and funcname is an attribute of it.
In this case there happens to be a straightforward mapping between the module’s
attributes and the global names defined in the module: they share the same namespace!

module的attributes 与 定义与其中的global names 具有直接的映射关系：它们共享同一名字空间

为模块属性赋值：
modname.the_answer = 42













