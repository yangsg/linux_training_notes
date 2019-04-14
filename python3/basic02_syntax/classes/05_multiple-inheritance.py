
#// https://docs.python.org/3.6/tutorial/classes.html#multiple-inheritance
#// 多重继承语法：
'''
        class DerivedClassName(Base1, Base2, Base3):
            <statement-1>
            .
            .
            .
            <statement-N>
'''
#// 在父类中查找(如当前类中无法直接找到时) attribute 的过程是 深度优先，从左向右，且不会对继承层级结构中重叠的同一个class查找2次
'''
For most purposes, in the simplest cases, you can think of the search for attributes inherited
from a parent class as depth-first, left-to-right, not searching twice in the same class
where there is an overlap in the hierarchy. Thus, if an attribute is not found in DerivedClassName,
it is searched for in Base1, then (recursively) in the base classes of Base1,
and if it was not found there, it was searched for in Base2, and so on.


In fact, it is slightly more complex than that; the method resolution order changes dynamically
to support cooperative calls to super(). This approach is known in some other multiple-inheritance
languages as call-next-method and is more powerful than the super call found in single-inheritance languages.

Dynamic ordering is necessary because all cases of multiple inheritance exhibit one or more diamond relationships
(where at least one of the parent classes can be accessed through multiple paths from the bottommost class).
For example, all classes inherit from object, so any case of multiple inheritance provides more than one path
to reach object. To keep the base classes from being accessed more than once, the dynamic algorithm linearizes
the search order in a way that preserves the left-to-right ordering specified in each class, that calls each
parent only once, and that is monotonic (meaning that a class can be subclassed without affecting the precedence
order of its parents). Taken together, these properties make it possible to design reliable and extensible classes
with multiple inheritance.
For more detail, see
        https://www.python.org/download/releases/2.3/mro/.

'''
















