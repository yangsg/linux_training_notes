#// https://docs.python.org/3.6/tutorial/controlflow.html#defining-functions


#// 关键字 def 用于引入函数定义

#// 定义一个输出斐波那契数列的函数
def fib(n): # 注： 如下的函数体中的第一个字符串是一个documentation string,是一种特殊的注释
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

fib(2000)  # 调用函数

#// function函数体中即使没有return value语句，也会默认返回None(it’s a built-in name). 
#// (类比javascript中function没有return value语句时默认返回undefined)
print(fib(0))  # None


#// 该函数返回一个斐波那契数列的结果list,而非简单输出
def fib2(n):  # return Fibonacci series up to n
    """Return a list containing the Fibonacci series up to n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)    # see below
        a, b = b, a+b
    return result


#// 还可以定义可变长度的参数, 有3中形式, 且它们还可以结合使用
#//
#// 1) Default Argument Values  默认参数值
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):  # in 关键字可用于一个sequence是否包含某事值，即Membership test operations
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)

#// ask_ok 可以有如下调用形式
ask_ok('Do you really want to quit?')
ask_ok('OK to overwrite the file?', 2)
ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')


#// The default values are evaluated at the point of function definition in the defining scope, so that
#// Important warning: The default value is evaluated only once.
i = 5

def f(arg=i):  # 即对于默认值，在python的函数被定义的声明定义的地方就需要被确定和固定下来
    print(arg)

i = 6
f()


#// 2) Keyword Arguments  关键字参数
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")

#// 如上的parrot函数可以有如下的调用形式
parrot(1000)                                          # 1 positional argument
parrot(voltage=1000)                                  # 1 keyword argument
parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

#// 但是如下调用形式是非法的
#//非法 parrot()                     # required argument missing
#//非法 parrot(voltage=5.0, 'dead')  # non-keyword argument after a keyword argument
#//非法 parrot(110, voltage=220)     # duplicate value for the same argument
#//非法 parrot(actor='John Cleese')  # unknown keyword argument

#// 在一个函数调用中,关键字参数(keyword arguments)应该跟随在位置参数(positional arguments)的后面,
#// 传递的实参中的关键字参数必须与函数声明定义时可接收的某个关键字参数的名字匹配(即不要传递非定义过的关键字参数)，
#// 不过它们的顺序并不重要，This also includes non-optional arguments (e.g. parrot(voltage=1000) is valid too).  
#// No argument may receive a value more than once. 


#// 如果函数最后一个形参形如 **name, 则**name接收一个字典，该字典可以包含所有的关键字参数(除了出现在定义列表出现过的形参)
#// 它可以与形如 *name 的一个形参结合使用，*name 接收一个元组,该元组包含一些
#// positional arguments beyond the formal parameter list. (*name 必须位于 **name 之前),
#// 如下示例：
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

#// cheeseshop函数可以按如下方式调用：
cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")


#// 输出结果如下：
#// 注意如下的3个Keyword Arguments的顺序与dictionary中对应的entry的顺序是能够保持一致的
#//            -- Do you have any Limburger ?
#//            -- I'm sorry, we're all out of Limburger
#//            It's very runny, sir.
#//            It's really very, VERY runny, sir.
#//            ----------------------------------------
#//            shopkeeper : Michael Palin
#//            client : John Cleese
#//            sketch : Cheese Shop Sketch


#// 3) Arbitrary Argument Lists 任意参数列表
#// These arguments will be wrapped up in a tuple (see Tuples and Sequences).
#// Before the variable number of arguments, zero or more normal arguments may occur.
def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

#// Normally, these variadic arguments will be last in the list of formal parameters,
#// because they scoop up all remaining input arguments that are passed to the function.
#// Any formal parameters which occur after the *args parameter are ‘keyword-only’ arguments,
#// meaning that they can only be used as keywords rather than positional arguments.
def concat(*args, sep="/"):
    return sep.join(args)

concat("earth", "mars", "venus")          # 'earth/mars/venus'
concat("earth", "mars", "venus", sep=".") # 'earth.mars.venus'

#// Unpacking Argument Lists
#// （这个特性类似于javascript中function的apply和call之间的功能）
#// The reverse situation occurs when the arguments are already in a list or tuple
#// but need to be unpacked for a function call requiring separate positional arguments.
#// For instance, the built-in range() function expects separate start and stop arguments.
#// If they are not available separately, write the function call with the
#// *-operator to unpack the arguments out of a list or tuple:

list(range(3, 6))   # normal call with separate arguments
[3, 4, 5]
args = [3, 6]
list(range(*args)) # <<< 注意此处的 *args  # call with arguments unpacked from a list # [3, 4, 5]

#// In the same fashion, dictionaries can deliver keyword arguments with the **-operator:
def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)   # <<< 注意此处的 **d
#// -- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !


#// Lambda Expressions  这时一种创建小型匿名函数的方法
#// They are syntactically restricted to a single expression.

def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)
f(0)    # 42
f(1)    # 43

#// The above example uses a lambda expression to return a function.
#// Another use is to pass a small function as an argument:
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])
pairs    # [(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]









