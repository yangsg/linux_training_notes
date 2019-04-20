

'''
在Python中，有些名称很特别，开头和结尾都是两个下划线。你在本书前面已经见过一些，
如__future__。这样的拼写表示名称有特殊意义，因此绝不要在程序中创建这样的名称。在这样
的名称中，很大一部分都是魔法（特殊）方法的名称。如果你的对象实现了这些方法，它们将在
特定情况下（具体是哪种情况取决于方法的名称）被Python调用，而几乎不需要直接调用。

'''


'''
            如果你使用的不是Python 3

    在Python 2.2中，Python对象的工作方式有了很大的变化。这种变化带来了多个方面的影响。
这些影响对Python编程新手来说大都不重要，但有一点需要注意：即便你使用的是较新的Python 2
版本，有些功能（如特性和函数super）也不适用于旧式类。要让你的类是新式的，要么在模块
开头包含赋值语句__metaclass__ = type（这在第7章提到过），要么直接或间接地继承内置类
object或其他新式类。请看下面两个类：
class NewStyle(object):
    more_code_here

class OldStyle:
    more_code_here
    在这两个类中，NewStyle是一个新式类，而OldStyle是一个旧式类。如果文件开头包含赋值
语句__metaclass__ = type，这两个类都将是新式类。

注意  也 可 在 类 的 作 用 域 内 给 变 量 __metaclass__ 赋值， 但这样做只设置当前类的元类
     （metaclass）。元类是其他类所属的类，这是一个非常复杂的主题。

    在本书中，我并没有在所有示例中都显式地设置元类或继承object。然而，如果你的程序
无需与旧版Python兼容，建议将所有类都定义为新式类，并使用将在9.2.3节介绍的函数super
等功能。
    请注意，在Python 3中没有旧式类，因此无需显式地继承object或将__metaclass__设置为
type。所有的类都将隐式地继承object。如果没有指定超类，将直接继承它，否则将间接地继
承它。

'''

# 构造函数
'''
。你可能从未听说过构造函数（constructor），它其
实就是本书前面一些示例中使用的初始化方法，只是命名为__init__。然而，构造函数不同于普
通方法的地方在于，将在对象创建后自动调用它们。


构造函数让你只需像下面这样做：
>>> f = FooBar()
在Python中，创建构造函数很容易，只需将方法init的名称从普通的init改为魔法版__init__
即可。

class FooBar:
    def __init__(self):
        self.somevar = 42
>>> f = FooBar()
>>> f.somevar
42

你认为该如何使用这个构造函数呢？由于参数是可选的，你可以当什么事都没发生，还像原
来那样做。但如果要指定这个参数（或者说如果这个参数不是可选的）呢？你肯定猜到了，不过
这里还是演示一下。
>>> f = FooBar('This is a constructor argument')
>>> f.somevar
'This is a constructor argument'

在所有的Python魔法方法中，__init__绝对是你用得最多的。

注意 Python提供了魔法方法__del__，也称作析构函数（destructor）。这个方法在对象被销毁
（作为垃圾被收集）前被调用，但鉴于你无法知道准确的调用时间，建议尽可能不要使用__del__。

'''


# 重写普通方法和特殊的构造函数

# 调用未关联的超类构造函数 (在新版本的python中，应使用 super )

class SongBird(Bird):
    def __init__(self):
        Bird.__init__(self)  # 本节介绍的方法主要用于解决历史遗留问题。在较新的Python版本中，显然应使用函数 super（这将在下一节讨论） # 然而，如果你通过类调用方法（如Bird.__init__），就没有实例与其相关联。在这种情况下，你可随便设置参数self。这样的方法称为未关联的。
        self.sound = 'Squawk!'
    def sing(self):
        print(self.sound)

'''
在SongBird类中，只添加了一行，其中包含代码Bird.__init__(self)。先来证明这确实管用，
再解释这到底意味着什么。
>>> sb = SongBird()
>>> sb.sing()
Squawk!
>>> sb.eat()
Aaaah ...
>>> sb.eat()
No, thanks!

这样做为何管用呢？对实例调用方法时，方法的参数self将自动关联到实例（称为关联的方
法），这样的示例你见过多个。然而，如果你通过类调用方法（如Bird.__init__），就没有实例
与其相关联。在这种情况下，你可随便设置参数self。这样的方法称为未关联的。这就对本节的
标题做出了解释。

'''

# 使用函数super   # https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
'''
https://docs.python.org/3.6/library/functions.html#super
super([type[, object-or-type]])   # Return a proxy object that delegates method calls to a parent or sibling class of type.


    如果你使用的不是旧版Python，就应使用函数super。这个函数只适用于新式类，而你无论
如何都应使用新式类。调用这个函数时，将当前类和当前实例作为参数。对其返回的对象调用方
法时，调用的将是超类（而不是当前类）的方法。因此，在SongBird的构造函数中，可不使用Bird，
而是使用super(SongBird, self)。另外，可像通常那样（也就是像调用关联的方法那样）调用方
法__init__。在Python 3中调用函数super时，可不提供任何参数（通常也应该这样做），而它将
像变魔术一样完成任务。
下面是前述示例的修订版本：
'''
class Bird:
    def __init__(self):
        self.hungry = True
    def eat(self):
        if self.hungry:
            print('Aaaah ...')
            self.hungry = False
        else:
            print('No, thanks!')

class SongBird(Bird):
    def __init__(self):
        super().__init__()  # 在Python 3中调用函数super时，可不提供任何参数（通常也应该这样做），而它将像变魔术一样完成任务。# 如果方法在类定义范围之外定义的，调用父类方法需要使用类似super(SongBird, self)这样带参数的语句
        self.sound = 'Squawk!'
    def sing(self):
        print(self.sound)

'''
这个新式版本与旧式版本等效：
>>> sb = SongBird()
>>> sb.sing()
Squawk!
>>> sb.eat()
Aaaah ...
>>> sb.eat()
No, thanks!


            使用函数super有何优点

    在我看来，相比于直接对超类调用未关联方法，使用函数super更直观，但这并非其唯一
的优点。实际上，函数super很聪明，因此即便有多个超类，也只需调用函数super一次（条件
是所有超类的构造函数也使用函数super）。另外，对于使用旧式类时处理起来很棘手的问题
（如两个超类从同一个类派生而来），在使用新式类和函数super时将自动得到处理。你无需知
道函数super的内部工作原理，但必须知道的是，使用函数super比调用超类的未关联构造函
数（或其他方法）要好得多。
    函数super返回的到底是什么呢？通常，你无需关心这个问题，只管假定它返回你所需的
超类即可。实际上，它返回的是一个super对象，这个对象将负责为你执行方法解析。当你访
问它的属性时，它将在所有的超类（以及超类的超类，等等）中查找，直到找到指定的属性或
引发AttributeError异常。

'''

# https://www.programiz.com/python-programming/methods/built-in/super
# Example 2: super() with Multiple Inheritance
class Animal:
  def __init__(self, animalName):
    print(animalName, 'is an animal.');

class Mammal(Animal):
  def __init__(self, mammalName):
    print(mammalName, 'is a warm-blooded animal.')
    super().__init__(mammalName)

class NonWingedMammal(Mammal):
  def __init__(self, NonWingedMammalName):
    print(NonWingedMammalName, "can't fly.")
    super().__init__(NonWingedMammalName)

class NonMarineMammal(Mammal):
  def __init__(self, NonMarineMammalName):
    print(NonMarineMammalName, "can't swim.")
    super().__init__(NonMarineMammalName)

class Dog(NonMarineMammal, NonWingedMammal):
  def __init__(self):
    print('Dog has 4 legs.');
    super().__init__('Dog')   # 多重继承中使用 super  的例子

d = Dog()
print('')
bat = NonMarineMammal('Bat')
'''
Method Resolution Order (MRO)
It's the order in which method should be inherited in the presence of multiple inheritance. You can view the MRO by using __mro__ attribute.
>>> Dog.__mro__
(<class 'Dog'>,
<class 'NonMarineMammal'>,
<class 'NonWingedMammal'>,
<class 'Mammal'>,
<class 'Animal'>,
<class 'object'>)

'''


# 元素访问
'''
    虽然__init__无疑是你目前遇到的最重要的特殊方法，但还有不少其他的特殊方法，让你能
够完成很多很酷的任务。本节将介绍一组很有用的魔法方法，让你能够创建行为类似于序列或映
射的对象。
    基本的序列和映射协议非常简单，但要实现序列和映射的所有功能，需要实现很多魔法方法。
所幸有一些捷径可走，我马上就会介绍。

注意
    在Python中，协议通常指的是规范行为的规则，有点类似于第7章提及的接口。协议指定
应实现哪些方法以及这些方法应做什么。在Python中，多态仅仅基于对象的行为（而不
基于祖先，如属于哪个类或其超类等），因此这个概念很重要：其他的语言可能要求对象
属于特定的类或实现了特定的接口，而Python通常只要求对象遵循特定的协议。因此，
要成为序列，只需遵循序列协议即可。
'''


# 基本的序列和映射协议
'''
序列和映射基本上是元素（item）的集合，要实现它们的基本行为（协议），不可变对象需
要实现2个方法，而可变对象需要实现4个。
   __len__(self)：这个方法应返回集合包含的项数，对序列来说为元素个数，对映射来说
    为键值对数。如果__len__返回零（且没有实现覆盖这种行为的__nonzero__），对象在布
    尔上下文中将被视为假（就像空的列表、元组、字符串和字典一样）。
   __getitem__(self, key)：这个方法应返回与指定键相关联的值。对序列来说，键应该是
    0~n 1的整数（也可以是负数，这将在后面说明），其中n为序列的长度。对映射来说，
    键可以是任何类型。
   __setitem__(self, key, value)：这个方法应以与键相关联的方式存储值，以便以后能够
    使用__getitem__来获取。当然，仅当对象可变时才需要实现这个方法。
   __delitem__(self, key)：这个方法在对对象的组成部分使用__del__语句时被调用，应
    删除与key相关联的值。同样，仅当对象可变（且允许其项被删除）时，才需要实现这个
    方法。

对于这些方法，还有一些额外的要求。
     对于序列，如果键为负整数，应从末尾往前数。换而言之，x[-n]应与x[len(x)-n]等效。
     如果键的类型不合适（如对序列使用字符串键），可能引发TypeError异常。
     对于序列，如果索引的类型是正确的，但不在允许的范围内，应引发IndexError异常。
要了解更复杂的接口和使用的抽象基类（Sequence），请参阅有关模块collections的文档。

'''

# 从list、dict 和str 派生
'''
    基本的序列/映射协议指定的4个方法能够让你走很远，但序列还有很多其他有用的魔法方法
和普通方法，其中包括将在9.6节介绍的方法__iter__。要实现所有这些方法，不仅工作量大，而
且难度不小。如果只想定制某种操作的行为，就没有理由去重新实现其他所有方法。这就是程序
员的懒惰（也是常识）。
    那么该如何做呢？“咒语”就是继承。在能够继承的情况下为何去重新实现呢？在标准库中，
模块collections提供了抽象和具体的基类，但你也可以继承内置类型。因此，如果要实现一种
行为类似于内置列表的序列类型，可直接继承list。
    来看一个简单的示例——一个带访问计数器的列表。
'''
class CounterList(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.counter = 0
    def __getitem__(self, index):  # 注意 重写__getitem__并不能保证一定会捕捉用户的访问操作，因为还有其他访问列表内容的方式，如通过方法pop。
        self.counter += 1
        return super(CounterList, self).__getitem__(index)

'''
CounterList类深深地依赖于其超类（list）的行为。CounterList没有重写的方法（如
append、extend、index等）都可直接使用。在两个被重写的方法中，使用super来调用超类的
相应方法，并添加了必要的行为：初始化属性counter（在__init__中）和更新属性counter（在
__getitem__中）

下面的示例演示了CounterList的可能用法：
>>> cl = CounterList(range(10))
>>> cl
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> cl.reverse()
>>> cl
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
>>> del cl[3:6]
>>> cl
[9, 8, 7, 3, 2, 1, 0]
>>> cl.counter
0
>>> cl[4] + cl[2]
9
>>> cl.counter
2

如你所见，CounterList的行为在大多数方面都类似于列表，但它有一个counter属性（其初
始值为0）。每当你访问列表元素时，这个属性的值都加1。执行加法运算cl[4] + cl[2]后，counter
的值递增两次，变成了2。
'''

# 其他魔法方法  other special method
'''
    特殊（魔法）名称的用途很多，前面展示的只是冰山一角。魔法方法大多是为非常高级的用
途准备的，因此这里不详细介绍。然而，如果你感兴趣，可以模拟数字，让对象像函数一样被调
用，影响对象的比较方式，等等。要更详细地了解有哪些魔法方法，可参阅“Python Reference
Manual”的Special method names一节。

'''

# 特性
'''
    第7章提到了存取方法，它们是名称类似于getHeight和setHeight的方法，用于获取或设置属
性（这些属性可能是私有的，详情请参阅7.2.4节）。如果访问给定属性时必须采取特定的措施，
那么像这样封装状态变量（属性）很重要。例如，请看下面的Rectangle类：
'''
class Rectangle:
    def __init__(self):
        self.width = 0
        self.height = 0
    def set_size(self, size):   # python中，对于新式类，应使用propert特性而不是存取方法。
        self.width, self.height = size
    def get_size(self): # python中，对于新式类，应使用propert特性而不是存取方法。
        return self.width, self.height

# 通过存取方法定义的属性通常称为特性（property）。
'''
在Python中，实际上有两种创建特定的机制，我将重点介绍较新的那种——函数property，
它只能用于新式类。随后，我将简单说明如何使用魔法方法来实现特性。
'''

# 函数property
class Rectangle:
    def __init__ (self):
        self.width = 0
        self.height = 0
    def set_size(self, size):
        self.width, self.height = size
    def get_size(self):
        return self.width, self.height
    size = property(get_size, set_size)  # 注意这里获取方法在前，设置方法在后

'''
在这个新版的Rectangle中，通过调用函数property并将存取方法作为参数（获取方法在前，
设置方法在后）创建了一个特性，然后将名称size关联到这个特性。这样，你就能以同样的方式
对待width、height和size，而无需关心它们是如何实现的。
>>> r = Rectangle()
>>> r.width = 10
>>> r.height = 5
>>> r.size
(10, 5)
>>> r.size = 150, 100
>>> r.width
150

如你所见，属性size依然受制于get_size和set_size执行的计算，但看起来就像普通属性一样。

注意
    如果特性的行为怪异，务必确保你使用的是新式类（通过直接或间接地继承object或直
    接设置__metaclass__）。不然，特性的获取方法依然正常，但设置方法可能不正常（是否
    如此取决于使用的Python版本）。这可能有点令人迷惑。

实际上，调用函数property时，还可不指定参数、指定一个参数、指定三个参数或指定四
个参数。如果没有指定任何参数，创建的特性将既不可读也不可写。如果只指定一个参数（获
取方法），创建的特性将是只读的。第三个参数是可选的，指定用于删除属性的方法（这个方
法不接受任何参数）。第四个参数也是可选的，指定一个文档字符串。这些参数分别名为fget、
fset、fdel和doc。如果你要创建一个只可写且带文档字符串的特性，可使用它们作为关键字参
数来实现。
本节虽然很短（旨在说明函数property很简单），却非常重要。这里要说明的是，对于新式
类，应使用特性而不是存取方法。

'''

'''

                    函数property的工作原理
    你可能很好奇，想知道特性是如何完成其魔法的，下面就来说一说。如果你对此不感兴
趣，可跳过这些内容。
    property其实并不是函数，而是一个类。它的实例包含一些魔法方法，而所有的魔法都
是由这些方法完成的。这些魔法方法为__get__、__set__和__delete__，它们一道定义了所谓
的描述符协议。只要对象实现了这些方法中的任何一个，它就是一个描述符。描述符的独特
之处在于其访问方式。例如，读取属性（具体来说，是在实例中访问类中定义的属性）时，如
果它关联的是一个实现了__get__的对象，将不会返回这个对象，而是调用方法__get__并将
其结果返回。实际上，这是隐藏在特性、关联的方法、静态方法和类方法（详细信息请参阅下
一小节）以及super后面的机制。
    有关描述符的详细信息，请参阅Descriptor HowTo Guide（https://docs.python.org/3/howto/
descriptor.html）。


https://docs.python.org/3/howto/descriptor.html#properties

'''


# 静态方法和类方法  static method  and class method
'''
    讨论旧的特性实现方式之前，先来说说另外两种实现方式类似于新式特性的功能。静态方法
和类方法是这样创建的：将它们分别包装在staticmethod和classmethod类的对象中。静态方法的
定义中没有参数self，可直接通过类来调用。类方法的定义中包含类似于self的参数，通常被命
名为cls。对于类方法，也可通过对象直接调用，但参数cls将自动关联到类。下面是一个简单的
示例：

'''

class MyClass:
    def smeth():
        print('This is a static method')
    smeth = staticmethod(smeth)    # 这样有点繁琐，Python 2.4以上版本可使用装饰器 @staticmethod
    def cmeth(cls):
        print('This is a class method of', cls)
    cmeth = classmethod(cmeth)     # 这样有点繁琐，Python 2.4以上版本可使用装饰器 @classmethod

'''
像这样手工包装和替换方法有点繁琐。在Python 2.4中，引入了一种名为装饰器(decorator)的新语法，
可用于像这样包装方法。（实际上，装饰器可用于包装任何可调用的对象，并且可用于方法和函
数。）可指定一个或多个装饰器，为此可在方法（或函数）前面使用运算符@列出这些装饰器（指
定了多个装饰器时，应用的顺序与列出的顺序相反）。
'''

class MyClass:

    @staticmethod  # static method 与 class method 的区别见： https://www.geeksforgeeks.org/class-method-vs-static-method-python/
    def smeth():
        print('This is a static method')

    @classmethod  # static method 与 class method 的区别见： https://www.geeksforgeeks.org/class-method-vs-static-method-python/
    def cmeth(cls):
        print('This is a class method of', cls)

# 定义这些方法后，就可像下面这样使用它们（无需实例化类）：
'''
>>> MyClass.smeth()
This is a static method
>>> MyClass.cmeth()
This is a class method of <class '__main__.MyClass'>

    在Python中，静态方法和类方法以前一直都不太重要，主要是因为从某种程度上说，总是可
以使用函数或关联的方法替代它们，而且早期的Python版本并不支持它们。因此，虽然较新的代
码没有大量使用它们，但它们确实有用武之地（如工厂函数），因此你或许应该考虑使用它们。

注意 实际上，装饰器(decorator)语法也可用于特性，详情请参阅有关函数property的文档。


static method 与 class method 的区别见：(differences between staticmethod and classmethod) https://www.geeksforgeeks.org/class-method-vs-static-method-python/
总体来说，静态方法 static method 通用用于实现与class 或 class状态(state) 无关的一些工具辅助函数
          而类方法 class method 用于实现依赖 class 或 class状态(state)的函数，如工厂方法Factory method
'''
#-------------------------------------------------------------------
# 如下是 @staticmethod 和 @classmethod 的使用示例, 该例子来自 https://www.geeksforgeeks.org/class-method-vs-static-method-python/
# Python program to demonstrate
# use of class method and static method.
from datetime import date

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # a class method to create a Person object by birth year.
    @classmethod
    def fromBirthYear(cls, name, year):  # 因为 python不像c++和java那样支持方法重载，所以可以提供额外的工厂函数来创建实例对象
        return cls(name, date.today().year - year)

    # a static method to check if a Person is adult or not.
    @staticmethod
    def isAdult(age):
        return age > 18

person1 = Person('mayank', 21)
person2 = Person.fromBirthYear('mayank', 1996)

print person1.age
print person2.age

# print the result
print Person.isAdult(22)

#-------------------------------------------------------------------


# __getattr__、__setattr__等方法
'''
    可以拦截对对象属性的所有访问企图，其用途之一是在旧式类中实现特性（在旧式类中，函
数property的行为可能不符合预期）。要在属性被访问时执行一段代码，必须使用一些魔法方法。
下面的四个魔法方法提供了你需要的所有功能（在旧式类中，只需使用后面三个）。

  __getattribute__(self, name)：在属性被访问时自动调用（只适用于新式类）。
  __getattr__(self, name)：在属性被访问而对象没有这样的属性时自动调用。
  __setattr__(self, name, value)：试图给属性赋值时自动调用。
  __delattr__(self, name)：试图删除属性时自动调用。

相比函数property，这些魔法方法使用起来要棘手些（从某种程度上说，效率也更低），但
它们很有用，因为你可在这些方法中编写处理多个特性的代码。然而，在可能的情况下，还是使
用函数property吧。
'''
# 再来看前面的Rectangle示例，但这里使用的是魔法方法：
class Rectangle:
    def __init__ (self):
        self.width = 0
        self.height = 0
    def __setattr__(self, name, value):  # 即便涉及的属性不是size，也将调用方法__setattr__
        if name == 'size':
            self.width, self.height = value
        else:
            self. __dict__[name] = value  # 之所以使用__dict__而不是执行常规属性赋值，是因为旨在避免再次调用__setattr__，进而导致无限循环。
    def __getattr__(self, name):
        if name == 'size':
            return self.width, self.height
        else:
            raise AttributeError()

'''
    如你所见，这个版本需要处理额外的管理细节。对于这个代码示例，需要注意如下两点。

    即便涉及的属性不是size，也将调用方法__setattr__。因此这个方法必须考虑如下两种
情形：如果涉及的属性为size，就执行与以前一样的操作；否则就使用魔法属性__dict__。
__dict__属性是一个字典，其中包含所有的实例属性。之所以使用它而不是执行常规属性
赋值，是因为旨在避免再次调用__setattr__，进而导致无限循环。

  仅当没有找到指定的属性时，才会调用方法__getattr__。这意味着如果指定的名称不是
size，这个方法将引发AttributeError异常。这在要让类能够正确地支持hasattr和getattr
等内置函数时很重要。如果指定的名称为size，就使用前一个实现中的表达式。

注意
    前面说过，编写方法__setattr__时需要避开无限循环陷阱，编写__getattribute__时
    亦如此。由于它拦截对所有属性的访问（在新式类中），因此将拦截对__dict__的访问！
    在__getattribute__中访问当前实例的属性时，唯一安全的方式是使用超类的方
    法__getattribute__（使用super）。
'''

# 迭代器  iterator iterable
'''
本书前面粗略地提及了迭代器（和可迭代对象），本节将更详细地介绍。对于魔法方法，这
里只介绍__iter__，它是迭代器协议的基础。
'''

# 迭代器协议
'''
    迭代（iterate）意味着重复多次，就像循环那样。本书前面只使用for循环迭代过序列和字典，
但实际上也可迭代其他对象：实现了方法__iter__的对象。

    方法__iter__返回一个迭代器，它是包含方法__next__的对象，而调用这个方法时可不提供
任何参数。当你调用方法__next__时，迭代器应返回其下一个值。如果迭代器没有可供返回的值，
应引发StopIteration异常。你还可使用内置的便利函数next，在这种情况下，next(it)与
it.__next__()等效。

注意 在Python 3中，迭代器协议有细微的变化。在以前的迭代器协议中，要求迭代器对象包含方法next而不是__next__。

这有什么意义呢？为何不使用列表呢？因为在很多情况下，使用列表都有点像用大炮打蚊
子。例如，如果你有一个可逐个计算值的函数，你可能只想逐个地获取值，而不是使用列表一次
性获取。这是因为如果有很多值，列表可能占用太多的内存。但还有其他原因：使用迭代器更通
用、更简单、更优雅。下面来看一个不能使用列表的示例，因为如果使用，这个列表的长度必须
是无穷大的！

这个“列表”为斐波那契数列，表示该数列的迭代器如下：
'''
class Fibs:
    def __init__(self):
        self.a = 0
        self.b = 1
    def __next__(self):  # 注意 更正规的定义是，实现了方法__iter__的对象是可迭代的，而实现了方法__next__的对象是迭代器。
        self.a, self.b = self.b, self.a + self.b
        return self.a
    def __iter__(self):  # 注意 更正规的定义是，实现了方法__iter__的对象是可迭代的，而实现了方法__next__的对象是迭代器。
        return self

'''
    注意到这个迭代器实现了方法__iter__，而这个方法返回迭代器本身。在很多情况下，都在
另一个对象中实现返回迭代器的方法__iter__，并在for循环中使用这个对象。但推荐在迭代器
中也实现方法__iter__（并像刚才那样让它返回self），这样迭代器就可直接用于for循环中。

注意 更正规的定义是，实现了方法__iter__的对象是可迭代的，而实现了方法__next__的对象是迭代器。

首先，创建一个Fibs对象。
>>> fibs = Fibs()
然后就可在for循环中使用这个对象，如找出第一个大于1000的斐波那契数。
>>> for f in fibs:
...     if f > 1000:
...         print(f)
...         break
...
1597

提示通过对可迭代对象调用内置函数iter，可获得一个迭代器。
>>> it = iter([1, 2, 3])
>>> next(it)
1
>>> next(it)
2

还可使用它从函数或其他可调用对象创建可迭代对象，详情请参阅库参考手册。
'''

# 从迭代器创建序列
'''
    除了对迭代器和可迭代对象进行迭代（通常这样做）之外，还可将它们转换为序列。在可以
使用序列的情况下，大多也可使用迭代器或可迭代对象（诸如索引和切片等操作除外）。一个这
样的例子是使用构造函数list显式地将迭代器转换为列表。
'''

class TestIterator:
    value = 0
    def __next__(self):
        self.value += 1
        if self.value > 10:
            raise StopIteration
        return self.value
    def __iter__(self):
        return self

ti = TestIterator()
list(ti)    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# 生成器
'''
    生成器是一个相对较新的Python概念。由于历史原因，它也被称为简单生成器（simple
generator）。生成器和迭代器可能是近年来引入的最强大的功能，但生成器是一个相当复杂的概
念，你可能需要花些功夫才能明白其工作原理和用途。虽然生成器让你能够编写出非常优雅的代
码，但请放心，无论编写什么程序，都完全可以不使用生成器。
    生成器是一种使用普通函数语法定义的迭代器。生成器的工作原理到底是什么呢？通过示例
来说明最合适。下面先来看看如何创建和使用生成器，然后再看看幕后的情况。
'''

# 创建生成器
'''
生成器创建起来与函数一样简单。你现在肯定厌烦了老套的斐波那契数列，所以下面换换口
味，创建一个将嵌套列表展开的函数。这个函数将一个类似于下面的列表作为参数：
'''
nested = [[1, 2], [3, 4], [5]]

'''
换而言之，这是一个列表的列表。函数应按顺序提供这些数字，下面是一种解决方案：
'''
def flatten(nested):
    for sublist in nested:
        for element in sublist:
            yield element

'''
    这个函数的大部分代码都很简单。它首先迭代所提供嵌套列表中的所有子列表，然后按顺序
迭代每个子列表的元素。倘若最后一行为print(element)，这个函数将容易理解得多，不是吗？
    在这里，你没有见过的是yield语句。包含yield语句的函数都被称为生成器。这可不仅仅是
名称上的差别，生成器的行为与普通函数截然不同。差别在于，生成器不是使用return返回一个
值，而是可以生成多个值，每次一个。每次使用yield生成一个值后，函数都将冻结，即在此停
止执行，等待被重新唤醒。被重新唤醒后，函数将从停止的地方开始继续执行。


为使用所有的值，可对生成器进行迭代。
>>> nested = [[1, 2], [3, 4], [5]]
>>> for num in flatten(nested):
...     print(num)
...
1
2
3
4
5

或

>>> list(flatten(nested))
[1, 2, 3, 4, 5]

                                简单生成器
    在Python 2.4中，引入了一个类似于列表推导（参见第5章）的概念：生成器推导（也叫生
成器表达式）。其工作原理与列表推导相同，但不是创建一个列表（即不立即执行循环），而
是返回一个生成器，让你能够逐步执行计算。
>>> g = ((i + 2) ** 2 for i in range(2, 27))
>>> next(g)
16

Generator expressions
    如你所见，不同于列表推导，这里使用的是圆括号。在像这样的简单情形下，还不如使
用列表推导；但如果要包装可迭代对象（可能生成大量的值），使用列表推导将立即实例化一
个列表，从而丧失迭代的优势。
    另一个好处是，直接在一对既有的圆括号内（如在函数调用中）使用生成器推导时，无需
再添加一对圆括号。换而言之，可编写下面这样非常漂亮的代码：
    sum(i ** 2 for i in range(10))


# 递归式生成器
# 通用生成器
# 生成器的方法

'''


