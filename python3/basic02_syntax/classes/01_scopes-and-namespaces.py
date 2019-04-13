#// https://docs.python.org/3.6/tutorial/classes.html#python-scopes-and-namespaces

#// Attributes may be read-only or writable.
#// 为模块属性赋值
#// 语法； modname.attribute_name =  value

#// https://stackoverflow.com/questions/990422/how-to-get-a-reference-to-current-modules-attributes-in-python
import sys
current_module = sys.modules[__name__]
current_module.greeting = 'hello world'

print(current_module.greeting)
print(globals()['greeting'])
print(globals().get('greeting'))
print(greeting)


def print_global_variable():
    global greeting
    print(greeting)
    greeting = '您好！'

print_global_variable()


print(current_module.greeting)
print(globals()['greeting'])
print(globals().get('greeting'))
print(greeting)
print_global_variable()


#//  可写的attributes 可以使用 del 语句来删除
#//  Writable attributes may also be deleted with the del statement.
del current_module.greeting

#// print(current_module.greeting)  #// error
#// print(globals()['greeting'])    #// error
print(globals().get('greeting'))    #// 输出 None
#// print(greeting)                 #// error
#// print_global_variable()         #// error

#// Namespaces 在不同的时机被创建且具有不同的生命周期
#//    原文：
#//    Namespaces are created at different moments and have different lifetimes. 
#//    1. The namespace containing the built-in names is created when the Python interpreter starts up, and is never deleted.
#//    2. The global namespace for a module is created when the module definition is read in; normally, module namespaces also last until the interpreter quits.

#//    The statements executed by the top-level invocation of the interpreter, either read from a script file
#//    or interactively, are considered part of a module called __main__, so they have their own global namespace.
#//    (The built-in names actually also live in a module; this is called builtins.)

#//    3. The local namespace for a function is created when the function is called, and deleted when the
#//       function returns or raises an exception that is not handled within the function.
#//       (Actually, forgetting would be a better way to describe what actually happens.)
#//       Of course, recursive invocations each have their own local namespace.



#// 作用域 scope
#// 一个作用域是 一个名字空间可以被直接访问的 Python 程序的 文本区域("直接访问"是指对一个name不加限定的引用将试图在该namespace中查找该name)
#// A scope is a textual region of a Python program where a namespace is directly accessible.
#// “Directly accessible” here means that an unqualified reference to a name attempts to find the name in the namespace.

#// 尽管 scopes 是被静态确定的，但却是被动态的使用. 在执行的任何时间，存在至少3个其 namespaces可以直接访问的 nested scopes.
#// Although scopes are determined statically, they are used dynamically.
#// At any time during execution, there are at least three nested scopes whose namespaces are directly accessible:
#//
#//   •the innermost scope, which is searched first, contains the local names
#//   •the scopes of any enclosing functions, which are searched starting with the nearest enclosing scope, contains non-local, but also non-global names
#//   •the next-to-last scope contains the current module’s global names
#//   •the outermost scope (searched last) is the namespace containing built-in names
#//
#// 上面几句话的大概意思参考下图, 而变量直接引用时的顺序就是从当前scope开始向外层scope一层一层查找，知道知道为止：
#// |----------------------------------------|
#// |  built-in scope                        |
#// |  ------------------------------------  |
#// |  |   gloal scope                    |  | global variable
#// |  |   -----------------------------  |  |
#// |  |   | non-local non-global scope|  |  | nonlocal variable(当引用nonlocal variable是,如果不加nonlocal关键字,则variable是只读的,如果此时为 variable赋值,则创建了一个新的lcoal变量)
#// |  |   |   ----------------------  |  |  |
#// |  |   |   |                    |  |  |  |
#// |  |   |   |    local-scope     |  |  |  | variable
#// |  |   |   |                    |  |  |  |
#// |  |   |   ----------------------  |  |  |
#// |  |   |                           |  |  |
#// |  |   ----------------------------   |  |
#// |  |                                  |  |
#// |  ------------------------------------  |
#// |                                        |
#// |----------------------------------------|


#// It is important to realize that scopes are determined textually:
#// name所属的scope是由其定义确定的(即在编译时静态确定，所以不要依靠dynamic name resolution来判断name的scope)


#// https://docs.python.org/3.6/tutorial/classes.html#scopes-and-namespaces-example
#// Scopes and Namespaces Example
print('-' * 100)

def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)  #// test spam
    do_nonlocal()
    print("After nonlocal assignment:", spam)  #// nonlocal spam
    do_global()
    print("After global assignment:", spam)    #// nonlocal spam

scope_test()
print("In global scope:", spam)  #// global spam



print('----------------------------------------------------------------------')

gloal_var = 'global_variable'

def outer_function_as_nonlocal_scope():
    nonlocal_var = 'nonlocal_variable'

    def inner_function_as_lcoal_scope():

        local_var = 'local_variable'
        global gloal_var
        nonlocal nonlocal_var

        print(local_var)
        print(nonlocal_var)
        print(gloal_var)


    inner_function_as_lcoal_scope()

outer_function_as_nonlocal_scope()


print('----------------------------------------------------------------------')



































