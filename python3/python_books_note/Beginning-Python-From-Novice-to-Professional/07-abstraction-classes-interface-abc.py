

# 再谈抽象

# 面向对象  类  对象

# 强内聚 弱耦合

# 封装 继承 多态

# 多态和方法

# 除非万不得已，否则应避免使用多重继承，因为在有些情况下，它可能带来意外的“并发症” (这也是java只支持单根继承的原因)

'''
>>> object.get_price()  # 像这样与对象属性相关联的函数称为方法
2.5
'''

from random import choice  # 标准库模块random包含一个名为choice的函数，它从序列中随机选择一个元素
x = choice(['Hello, world!', [1, 2, 'e', 'e', 4]])


# 多态形式多样
# 每当无需知道对象是什么样的就能对其执行操作时，都是多态在起作用。这不仅仅适用于方法，我们还通过内置运算符和函数大量使用了多态

1 + 2 # 3
'Fish' + 'license'  # 'Fishlicense'


def length_message(x):
    print("The length of", repr(x), "is", len(x))  # 这个函数还使用了repr。repr是多态的集大成者之一，可用于任何对象

'''
注意 这里讨论的多态形式是Python编程方式的核心，有时称为鸭子类型。这个术语源自如下
     说法：“如果走起来像鸭子，叫起来像鸭子，那么它就是鸭子。”有关鸭子类型的详细信
     息，请参阅http://en.wikipedia.org/wiki/Duck_typing。


    很多函数和运算符都是多态的，你编写的大多数函数也可能如此，即便你不是有意为之。每
当你使用多态的函数和运算符时，多态都将发挥作用。事实上，要破坏多态，唯一的办法是使用
诸如type、issubclass等函数显式地执行类型检查，但你应尽可能避免以这种方式破坏多态。重
要的是，对象按你希望的那样行事，而非它是否是正确的类型（类）。然而，不要使用类型检查
的禁令已不像以前那么严格。引入本章后面将讨论的抽象基类和模块abc后，函数issubclass本
身也是多态的了！
'''


# 封装
'''
    封装（encapsulation）指的是向外部隐藏不必要的细节。这听起来有点像多态（无需知道对
象的内部细节就可使用它）。这两个概念很像，因为它们都是抽象的原则。它们都像函数一样，
可帮助你处理程序的组成部分，让你无需关心不必要的细节。

    但封装不同于多态。多态让你无需知道对象所属的类（对象的类型）就能调用其方法，而封
装让你无需知道对象的构造就能使用它。
'''

# 继承
'''
继承是另一种偷懒的方式（这里是褒义）。程序员总是想避免多次输入同样的代码。
'''

# 类
# 类到底是什么
'''
本书前面反复提到了类，并将其用作类型的同义词。从很多方面来说，这正是类的定义——
一种对象。每个对象都属于特定的类，并被称为该类的实例。


注意 在英语日常交谈中，使用复数来表示类，如birds（鸟类）和larks（云雀）。在Python中，
     约定使用单数并将首字母大写，如Bird和Lark。

注意 在较旧的Python版本中，类型和类之间泾渭分明：内置对象是基于类型的，而自定义对
     象是基于类的。因此，你可以创建类，但不能创建类型。在较新的Python 2版本中，这种
     差别不那么明显。在Python 3中，已不再区分类和类型了。
'''

# 创建自定义类
__metaclass__ = type # 如果你使用的是Python 2，请包含这行代码

class Person:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def greet(self):
        print("Hello, world! I'm {}.".format(self.name))

'''
self很有用，甚至必不可少。如果没有它，所有的方法都无法访问对象本身——要操
作的属性所属的对象

>>> foo = Person()
>>> bar = Person()
>>> foo.set_name('Luke Skywalker')
>>> bar.set_name('Anakin Skywalker')
>>> foo.greet()
Hello, world! I'm Luke Skywalker.
>>> bar.greet()
Hello, world! I'm Anakin Skywalker.
'''

'''
注意  旧式类和新式类是有差别的。现在实在没有理由再使用旧式类了，但在Python 3之前，默
      认创建的是旧式类。在较旧的Python版本中，要创建新式类，应在脚本或模块开头放置
      赋值语句__metaclass__ = type，但我不会在每个示例中都显式地包含这条语句。当然，
      还有其他解决方案，如从新式类（如object）派生出子类。有关如何派生子类，稍后将
      详细介绍。如果你使用的是Python 3，就无需考虑这一点，因为根本没有旧式类了。有关
      这方面的详细信息，请参阅第9章。

'''


# 实际上，完全可以让另一个变量指向同一个方法。
'''
>>> class Bird:
...     song = 'Squaawk!'
...     def sing(self):
...         print(self.song)
...
>>> bird = Bird()
>>> bird.sing()
Squaawk!
>>> birdsong = bird.sing
>>> birdsong()   # 虽然最后一个方法调用看起来很像函数调用，但变量birdsong指向的是关联的方法 bird.sing，这意味着它也能够访问参数self（即它也被关联到类的实例）。
Squaawk!

'''

# 再谈隐藏
'''
私有属性不能从对象外部访问，而只能通过存取器方法（如get_name和
set_name）来访问

注意 第9章将介绍特性（property），这是一种功能强大的存取器替代品

    Python没有为私有属性提供直接的支持，而是要求程序员知道在什么情况下从外部修改属性
是安全的。毕竟，你必须在知道如何使用对象之后才能使用它。然而，通过玩点小花招，可获得
类似于私有属性的效果。
    要让方法或属性成为私有的（不能从外部访问），只需让其名称以两个下划线打头即可。

class Secretive:
    def __inaccessible(self):   # 类的定义中名称以两个下划线打头约定为私有的 private  # 这种方式会使用name mangling 机制将原本的名字改造为 _Secretive__inaccessible 这种形式
        print("Bet you can't see me ...")
    def accessible(self):
        print("The secret message is:")
        self.__inaccessible()

如果你不希望名称被修改，又想发出不要从外部修改属性或方法的信号，可用一个下划线打
头。这虽然只是一种约定，但也有些作用。例如，from module import *不会导入以一个下划线
打头的名称①。


对于成员变量（属性），有些语言支持多种私有程度。例如，Java支持4种不同的私有程度。Python没有提供这样
的支持，不过从某种程度上说，以一个和两个下划线打头相当于两种不同的私有程度。

'''


'''
在class语句中定义
的代码都是在一个特殊的命名空间（类的命名空间）内执行的，而类的所有成员都可访问这个命
名空间。类定义其实就是要执行的代码段，并非所有的Python程序员都知道这一点，但知道这一
点很有帮助。例如，在类定义中，并非只能包含def语句。
>>> class C:
...     print('Class C being defined...')
...
Class C being defined...
>>>

这有点傻，但请看下面的代码：
>>> class MemberCounter:
...     members = 0
...     def init(self):
...         MemberCounter.members += 1
...
>>> m1 = MemberCounter()
>>> m1.init()
>>> MemberCounter.members
1
>>> m2 = MemberCounter()
>>> m2.init()
>>> MemberCounter.members
2

'''

# 指定超类
class Filter:
    def init(self):
        self.blocked = []
    def filter(self, sequence):
        return [x for x in sequence if x not in self.blocked]

class SPAMFilter(Filter): # SPAMFilter是Filter的子类  # 要指定超类，可在class语句中的类名后加上超类名，并将其用圆括号括起。
    def init(self): # 重写超类Filter的方法init
        self.blocked = ['SPAM']

# 深入探讨继承
'''
>>> issubclass(SPAMFilter, Filter)  # 要确定一个类是否是另一个类的子类，可使用内置方法issubclass。
True
>>> issubclass(Filter, SPAMFilter)
False

如果你有一个类，并想知道它的基类，可访问其特殊属性__bases__。
>>> SPAMFilter.__bases__
(<class __main__.Filter at 0x171e40>,)
>>> Filter.__bases__
(<class 'object'>,)

同样，要确定对象是否是特定类的实例，可使用isinstance。
>>> s = SPAMFilter()
>>> isinstance(s, SPAMFilter)
True
>>> isinstance(s, Filter)
True
>>> isinstance(s, str)
False


注意使用isinstance通常不是良好的做法，依赖多态在任何情况下都是更好的选择。一个重要
的例外情况是使用抽象基类和模块abc时。

如你所见，s是SPAMFilter类的（直接）实例，但它也是Filter类的间接实例，因为SPAMFilter
是Filter的子类。换而言之，所有SPAMFilter对象都是Filter对象。从前一个示例可知，isinstance
也可用于类型，如字符串类型（str）。

如果你要获悉对象属于哪个类，可使用属性__class__。
>>> s.__class__
<class __main__.SPAMFilter at 0x1707c0>

'''

# 多个超类
class Calculator:
    def calculate(self, expression):
        self.value = eval(expression)
class Talker:
    def talk(self):
        print('Hi, my value is', self.value)
class TalkingCalculator(Calculator, Talker):
    pass

'''
子类TalkingCalculator本身无所作为，其所有的行为都是从超类那里继承的。关键是通过从
Calculator那里继承calculate，并从Talker那里继承talk，它成了会说话的计算器。
>>> tc = TalkingCalculator()
>>> tc.calculate('1 + 2 * 3')
>>> tc.talk()
Hi, my value is 7

这被称为多重继承，是一个功能强大的工具。然而，除非万不得已，否则应避免使用多重继
承，因为在有些情况下，它可能带来意外的“并发症”

使用多重继承时，有一点务必注意：如果多个超类以不同的方式实现了同一个方法（即有多
个同名方法），必须在class语句中小心排列这些超类，因为位于前面的类的方法将覆盖位于后面
的类的方法。因此，在前面的示例中，如果Calculator类包含方法talk，那么这个方法将覆盖Talker
类的方法talk（导致它不可访问）。如果像下面这样反转超类的排列顺序：

    class TalkingCalculator(Talker, Calculator): pass

    将导致Talker的方法talk是可以访问的。多个超类的超类相同时，查找特定方法或属性时访
问超类的顺序称为方法解析顺序（MRO），它使用的算法非常复杂。所幸其效果很好，你可能根
本无需担心。

'''

# 接口和内省
'''
    接口这一概念与多态相关。处理多态对象时，你只关心其接口（协议）——对外暴露的方
法和属性。在Python中，不显式地指定对象必须包含哪些方法才能用作参数。例如，你不会像
在Java中那样显式编写接口(interface)，而是假定对象能够完成你要求它完成的任务。如果不能完成，程
序将失败。

    通常，你要求对象遵循特定的接口（即实现特定的方法），但如果需要，也可非常灵活地提
出要求：不是直接调用方法并期待一切顺利，而是检查所需的方法是否存在；如果不存在，就改
弦易辙。

>>> hasattr(tc, 'talk')
True
>>> hasattr(tc, 'fnord')
False

在上述代码中，你发现tc（本章前面介绍的TalkingCalculator类的实例）包含属性talk（指
向一个方法），但没有属性fnord。如果你愿意，还可以检查属性talk是否是可调用的
>>> callable(getattr(tc, 'talk', None))
True
>>> callable(getattr(tc, 'fnord', None))
False

    请注意，这里没有在if语句中使用hasattr并直接访问属性，而是使用了getattr（它让我能
够指定属性不存在时使用的默认值，这里为None），然后对返回的对象调用callable。


注意  setattr与getattr功能相反，可用于设置对象的属性：
    >>> setattr(tc, 'name', 'Mr. Gumby')
    >>> tc.name
    'Mr. Gumby'


要查看对象中存储的所有值，可检查其__dict__属性。如果要确定对象是由什么组成的，应
研究模块inspect。这个模块主要供高级用户创建对象浏览器（让用户能够以图形方式浏览Python
对象的程序）以及其他需要这种功能的类似程序。

>>> class User:
...     def __init__(self, name, age):
...             self.name = name
...             self.age = age
...     def say(self):
...             print('{name}, {age}'.format(name=self.name, age=self.age))
...
>>> u = User('Bob', 25)
>>> u.__dict__   # 要查看对象中存储的所有值，可检查其__dict__属性。
{'name': 'Bob', 'age': 25}
>>> u.say()
Bob, 25


'''

# 抽象基类 (abstract base class)
'''
    然而，有比手工检查各个方法更好的选择。在历史上的大部分时间内，Python几乎都只依赖
于鸭子类型，即假设所有对象都能完成其工作，同时偶尔使用hasattr来检查所需的方法是否存
在。很多其他语言（如Java和Go）都采用显式指定接口的理念，而有些第三方模块提供了这种理
念的各种实现。最终，Python通过引入模块abc提供了官方解决方案。这个模块为所谓的抽象基
类提供了支持。一般而言，抽象类是不能（至少是不应该）实例化的类，其职责是定义子类应实
现的一组抽象方法。下面是一个简单的示例：
'''

from abc import ABC, abstractmethod
class Talker(ABC):
    @abstractmethod
    def talk(self):
        pass

'''
    形如@this的东西被称为装饰器，其用法将在第9章详细介绍。这里的要点是你使用
@abstractmethod来将方法标记为抽象的——在子类中必须实现的方法。

    注意 如果你使用的是较旧的Python版本，将无法在模块abc中找到ABC类。在这种情况下，需要
导入ABCMeta，并在类定义开头包含代码行__metaclass__ = ABCMeta（紧跟在class语句后
面并缩进）。如果你使用的是3.4之前的Python 3版本，也可使用Talker(metaclass=ABCMeta)
代替Talker(ABC)。



>>> Talker()  # 抽象类（即包含抽象方法的类）最重要的特征是不能实例化。
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: Can't instantiate abstract class Talker with abstract methods talk

'''

class Knigget(Talker):  # 由于没有重写方法talk，因此这个类也是抽象的，不能实例化。如果你试图这样做，将出现类似于前面的错误消息。
    pass


# 然而，你可重新编写这个类，使其实现要求的方法。
class Knigget(Talker):  # 现在实例化它没有任何问题
    def talk(self):
        print("Ni!")

'''
这是抽象基类的主要用途，而且只有在这种情形下使用
isinstance才是妥当的：如果先检查给定的实例确实是Talker对象，就能相信这个实例在需要的
情况下有方法talk。

>>> k = Knigget()
>>> isinstance(k, Talker)
True
>>> k.talk()
Ni!

'''

'''
    然而，还缺少一个重要的部分——让isinstance的多态程度更高的部分。正如你看到的，抽
象基类让我们能够本着鸭子类型的精神使用这种实例检查！我们不关心对象是什么，只关心对象
能做什么（它实现了哪些方法）。因此，只要实现了方法talk，即便不是Talker的子类，依然能
够通过类型检查。下面来创建另一个类。

class Herring:
    def talk(self):
        print("Blub.")

这个类的实例能够通过是否为Talker对象的检查，可它并不是Talker对象

>>> h = Herring()
>>> isinstance(h, Talker)
False

    诚然，你可从Talker派生出Herring，这样就万事大吉了，但Herring可能是从他人的模块中
导入的。在这种情况下，就无法采取这样的做法。为解决这个问题，你可将Herring注册为Talker
（而不从Herring和Talker派生出子类），这样所有的Herring对象都将被视为Talker对象。

>>> Talker.register(Herring)   # 可将Herring注册为Talker（而不从Herring和Talker派生出子类），这样所有的Herring对象都将被视为Talker对象 # 然而，这种做法存在一个缺点，就是直接从抽象类派生提供的保障没有了。
<class '__main__.Herring'>
>>> isinstance(h, Talker)
True
>>> issubclass(Herring, Talker)
True

'''
# 然而，这种做法存在一个缺点，就是直接从抽象类派生提供的保障没有了。
'''
>>> class Clam:
... pass
...
>>> Talker.register(Clam)  # 然而，这种做法存在一个缺点，就是直接从抽象类派生提供的保障没有了。
<class '__main__.Clam'>
>>> issubclass(Clam, Talker)
True
>>> c = Clam()
>>> isinstance(c, Talker)
True
>>> c.talk()
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
AttributeError: 'Clam' object has no attribute 'talk'

    换而言之，应将isinstance返回True视为一种意图表达。在这里，Clam有成为Talker的意图。
本着鸭子类型的精神，我们相信它能承担Talker的职责，但可悲的是它失败了。
    标准库（如模块collections.abc）提供了多个很有用的抽象类，有关模块abc的详细信息，
请参阅标准库参考手册。
'''

# 关于面向对象设计的一些思考


