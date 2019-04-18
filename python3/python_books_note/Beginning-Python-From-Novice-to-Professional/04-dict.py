
'''
本章介绍一种可
通过名称来访问其各个值的数据结构。这种数据结构称为映射（mapping）。字典是Python中唯一
的内置映射类型，其中的值不按顺序排列，而是存储在键下。键可能是数、字符串或元组。
'''

# 创建和使用字典
phonebook = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}  # 字典由键及其相应的值组成，这种键值对称为项（item）
dictionary = {}  # 创建空字典empty dict的语法： {}
# 注意 在字典（以及其他映射类型）中，键必须是独一无二的，而字典中的值无需如此。


# 函数dict     注；与list、tuple和str一样，dict其实根本就不是函数，而是一个类
'''
>>> items = [('name', 'Gumby'), ('age', 42)]
>>> d = dict(items)  # 可使用函数dict①从其他映射（如其他字典）或键值对序列创建字典。
>>> d
{'name': 'Gumby', 'age': 42}

'''
d = dict([('name', 'Gumby'), ('age', 42)]) # {'name': 'Gumby', 'age': 42}  # 可使用函数dict①从其他映射（如其他字典）或键值对序列创建字典。
d = dict(name='Gumby', age=42)  # {'name': 'Gumby', 'age': 42}  # 还可使用关键字实参来调用这个dict函数

'''
尽管这可能是函数dict最常见的用法，但也可使用一个映射实参来调用它，这将创建一个字
典，其中包含指定映射中的所有项。像函数list、tuple和str一样，如果调用这个函数时没有提
供任何实参，将返回一个空字典。从映射创建字典时，如果该映射也是字典（毕竟字典是Python
中唯一的内置映射类型），可不使用函数dict，而是使用字典方法copy，这将在本章后面介绍。
'''


'''
基本的字典操作
字典的基本行为在很多方面都类似于序列。

    len(d)返回字典d包含的项（键值对）数。
    d[k]返回与键k相关联的值。
    d[k] = v将值v关联到键k。
    del d[k]删除键为k的项。
    k in d检查字典d是否包含键为k的项。

虽然字典和列表有多个相同之处，但也有一些重要的不同之处。

    键的类型：字典中的键可以是整数，但并非必须是整数。字典中的键可以是任何不可变的类型，如浮点数（实数）、字符串或元组。

    自动添加：即便是字典中原本没有的键，也可以给它赋值，这将在字典中创建一个新项。然而，如果不使用append或其他类似的方法，就不能给列表中没有的元素赋值

    成员资格：表达式k in d（其中d是一个字典）查找的是键而不是值，而表达式v in l（其
              中l是一个列表）查找的是值而不是索引。这看似不太一致，但你习惯后就会觉得相当自
              然。毕竟如果字典包含指定的键，检查相应的值就很容易。

提示: 相比于检查列表是否包含指定的值，检查字典是否包含指定的键的效率更高。数据结构越大，效率差距就越大。

>>> d = dict(name='Gumby', age=42)
>>> d
{'name': 'Gumby', 'age': 42}
>>> dict_obj = {'name': 'Bob', 'age': 42, 'gender': 'male'}
>>> len(dict_obj)  # len返回字典对象包含的项（键值对）数。
3
>>> dict_obj['name'] # 返回与键'name'关联的值
'Bob'
>>> del dict_obj['age'] # 删除键为'age'的项
>>> dict_obj
{'name': 'Bob', 'gender': 'male'}
>>> 'name' in dict_obj  # 检查dict_obj是否包含键为 'name' 的项
True
>>> 'age' in dict_obj
False
'''

# 将字符串格式设置功能用于字典
'''
第3章介绍过，可使用字符串格式设置功能来设置值的格式，这些值是作为命名或非命名参
数提供给方法format的。在有些情况下，通过在字典中存储一系列命名的值，可让格式设置更容
易些。例如，可在字典中包含各种信息，这样只需在格式字符串中提取所需的信息即可。为此，
必须使用format_map来指出你将通过一个映射来提供所需的信息。
>>> phonebook = {'Beth': '9102', 'Alice': '2341', 'Cecil': '3258'}
>>> "Cecil's phone number is {Cecil}.".format_map(phonebook)
"Cecil's phone number is 3258."
'''

user = {'name': 'Bob', 'age': 25}
'Hello {name}'.format_map(user)   # 使用format_map来指出你将通过一个映射来提供格式字符串中提取所需的信息
'Hello Bob'

"""
像这样使用字典时，可指定任意数量的转换说明符，条件是所有的字段名都是包含在字典中
的键。在模板系统中，这种字符串格式设置方式很有用（下面的示例使用的是HTML）。
>>> template = '''<html>
... <head><title>{title}</title></head>
... <body>
... <h1>{title}</h1>
... <p>{text}</p>
... </body>'''
>>> data = {'title': 'My Home Page', 'text': 'Welcome to my home page!'}
>>> print(template.format_map(data))
<html>
<head><title>My Home Page</title></head>
<body>
<h1>My Home Page</h1>
<p>Welcome to my home page!</p>
</body>

"""



# 字典方法

# clear
'''
方法clear删除所有的字典项，这种操作是就地执行的（就像list.sort一样），因此什么都不
返回（或者说返回None）
>>> d = {}
>>> d['name'] = 'Gumby'
>>> d['age'] = 42
>>> d
{'name': 'Gumby', 'age': 42}
>>> returned_value = d.clear()  # returned_value的值为None # 方法clear删除所有的字典项，这种操作是就地执行的（就像list.sort一样），因此什么都不返回（或者说返回None）
>>> d
{}
>>> print(returned_value)
None
>>>

这为何很有用呢？我们来看两个场景。下面是第一个场景：
>>> x = {}
>>> y = x
>>> x['key'] = 'value'
>>> y
{'key': 'value'}
>>> x = {}    # 此处只是将名字 x 关联到了一个新的空字典dict对象
>>> x
{}
>>> y
{'key': 'value'}

下面是第二个场景：
>>> x = {}
>>> y = x
>>> x['key'] = 'value'
>>> y
{'key': 'value'}
>>> x.clear()    # 此处将字典对象本身做了clear处理，所以所有引用该字典对象的别名都可以观察到该clear结果
>>> y
{}

在这两个场景中，x和y最初都指向同一个字典。在第一个场景中，我通过将一个空字典赋
给x来“清空”它。这对y没有任何影响，它依然指向原来的字典。这种行为可能正是你想要的，
但要删除原来字典的所有元素，必须使用clear。如果这样做，y也将是空的，如第二个场景所示。

'''

# copy
'''
方法copy返回一个新字典，其包含的键值对与原来的字典相同（这个方法执行的是浅复制，
因为值本身是原件，而非副本）。

>>> x = {'username': 'admin', 'machines': ['foo', 'bar', 'baz']}
>>> y = x.copy()   # dict 的浅拷贝(shallow copy)
>>> y['username'] = 'mlh'
>>> y['machines'].remove('bar')
>>> y
{'username': 'mlh', 'machines': ['foo', 'baz']}
>>> x
{'username': 'admin', 'machines': ['foo', 'baz']}


如你所见，当替换副本中的值时，原件不受影响。然而，如果修改副本中的值（就地修改而
不是替换），原件也将发生变化，因为原件指向的也是被修改的值（如这个示例中的'machines'
列表所示）。

为避免这种问题，一种办法是执行深复制，即同时复制值及其包含的所有值，等等。为此，
可使用模块copy中的函数deepcopy。

>>> from copy import deepcopy
>>> d = {}
>>> d['names'] = ['Alfred', 'Bertrand']
>>> c = d.copy()
>>> dc = deepcopy(d)   # 深复制(深拷贝)
>>> d['names'].append('Clive')
>>> c
{'names': ['Alfred', 'Bertrand', 'Clive']}
>>> dc
{'names': ['Alfred', 'Bertrand']}

'''

# fromkeys  # classmethod fromkeys(seq[, value])
dict.fromkeys(['name', 'age']) # {'name': None, 'age': None}   # 方法fromkeys创建一个新字典，其中包含指定的键，且每个键对应的值都是None。
{}.fromkeys(['name', 'age']) # {'name': None, 'age': None}     # 这行语句创建了一个空字典(empty dict)来调用 fromkeys, 不过因为fromkeys是一个类方法，所以该方式调用有点多余，直接用dict调用即可
'''
这个示例首先创建了一个空字典，再对其调用方法fromkeys来创建另一个字典，这显得有点
多余。你可以不这样做，而是直接对dict（前面说过，dict是所有字典所属的类型。类和类型将
在第7章详细讨论）调用方法fromkeys。
'''

dict.fromkeys(['name', 'age'], '(unknown)') # {'name': '(unknown)', 'age': '(unknown)'}  # 如果你不想使用默认值None，可提供特定的值。


# get  语法： get(key[, default])
# 方法get为访问字典项提供了宽松的环境。通常，如果你试图访问字典中没有的项，将引发错误。
'''
>>> d = {}
>>> print(d['name'])
Traceback (most recent call last):
File "<stdin>", line 1, in ?
KeyError: 'name'

而使用get不会这样：
>>> print(d.get('name')) # None  # 当字典中不存在传入的key时，get方法只是返回None, 而不会抛出异常
None

如你所见，使用get来访问不存在的键时，没有引发异常，而是返回None。你可指定“默认”
值，这样将返回你指定的值而不是None。

>>> d.get('name', 'N/A')  # 指定 'N/A' 作为默认值
'N/A'

如果字典包含指定的键，get的作用将与普通字典查找相同。
>>> d['name'] = 'Eric'
>>> d.get('name')
'Eric'

'''

# items
'''
方法items返回一个包含所有字典项的列表，其中每个元素都为(key, value)的形式。字典项
在列表中的排列顺序不确定。
>>> d = {'title': 'Python Web Site', 'url': 'http://www.python.org', 'spam': 0}
>>> d.items() # 方法items返回一个包含所有字典项的列表，其中每个元素都为(key, value)的形式。字典项在列表中的排列顺序不确定。
dict_items([('title', 'Python Web Site'), ('url', 'http://www.python.org'), ('spam', 0)])
>>> type(d.items())  # <class 'dict_items'>  # 返回值属于一种名为字典视图的特殊类型。字典视图可用于迭代

>>> len(d.items()) # 3 # 你还可确定其长度
>>> ('spam', 0) in d.items() # True # 执行成员资格检查


# 视图的一个优点是不复制，它们始终是底层字典的反映，即便你修改了底层字典亦如此
>>> d = {'title': 'Python Web Site', 'url': 'http://www.python.org', 'spam': 0}
>>> it = d.items()
>>> d['spam'] = 1
>>> ('spam', 0) in it  # 视图的一个优点是不复制，它们始终是底层字典的反映，即便你修改了底层字典亦如此
False
>>> d['spam'] = 0
>>> ('spam', 0) in it
True

>>> list(d.items()) #  [('title', 'Python Web Site'), ('url', 'http://www.python.org'), ('spam', 0)] # 然而，如果你要将字典项复制到列表中（在较旧的Python版本中，方法items就是这样做的），可自己动手做

'''

# keys
d.keys() # dict_keys(['title', 'url', 'spam']) # 方法keys返回一个字典视图，其中包含指定字典中的键
type(d.keys()) # <class 'dict_keys'>


# pop
'''
>>> d = {'x': 1, 'y': 2}
>>> d.pop('x')  # 方法pop可用于获取与指定键相关联的值，并将该键值对从字典中删除。
1
>>> d
{'y': 2}

'''

# popitem
'''
方法popitem类似于list.pop，但list.pop弹出列表中的最后一个元素，而popitem随机地弹
出一个字典项，因为字典项的顺序是不确定的，没有“最后一个元素”的概念。如果你要以高效
地方式逐个删除并处理所有字典项，这可能很有用，因为这样无需先获取键列表。
>>> d = {'url': 'http://www.python.org', 'spam': 0, 'title': 'Python Web Site'}
>>> d.popitem()
('title', 'Python Web Site')
>>> d
{'url': 'http://www.python.org', 'spam': 0}

虽然popitem类似于列表方法pop，但字典没有与append（它在列表末尾添加一个元素）对应
的方法。这是因为字典是无序的，类似的方法毫无意义。

提示 # 如果希望方法popitem以可预测的顺序弹出字典项，请参阅模块collections中的 OrderedDict 类。

'''

# setdefault
'''
方法setdefault有点像get，因为它也获取与指定键相关联的值，但除此之外，setdefault
还在字典不包含指定的键时，在字典中添加指定的键值对。
>>> d = {}
>>> d.setdefault('name', 'N/A')
'N/A'
>>> d
{'name': 'N/A'}
>>> d['name'] = 'Gumby'
>>> d.setdefault('name', 'N/A')
'Gumby'
>>> d
{'name': 'Gumby'}

如你所见，指定的键不存在时，setdefault返回指定的值并相应地更新字典。如果指定的键
存在，就返回其值，并保持字典不变。与get一样，值是可选的；如果没有指定，默认为None。
>>> d = {}
>>> print(d.setdefault('name'))
None
>>> d
{'name': None}

提示  如果希望有用于整个字典的全局默认值，请参阅模块collections中的defaultdict类
'''

# update
'''
>>> d = {
... 'title': 'Python Web Site',
... 'url': 'http://www.python.org',
... 'changed': 'Mar 14 22:09:15 MET 2016'
... }
>>> x = {'title': 'Python Language Website'}
>>> d.update(x)  # 方法update使用一个字典中的项来更新另一个字典。
>>> d
{'title': 'Python Language Website', 'url': 'http://www.python.org', 'changed': 'Mar 14 22:09:15 MET 2016'}
>>> y = {'status': 'on'}
>>> d.update(y)  # 对于通过参数提供的字典，将其项添加到当前字典中。如果当前字典包含键相同的项，就替换它。
>>> d
{'title': 'Python Language Website', 'url': 'http://www.python.org', 'changed': 'Mar 14 22:09:15 MET 2016', 'status': 'on'}

可像调用本章前面讨论的函数dict（类型构造函数）那样调用方法update。这意味着调用
update时，可向它提供一个映射、一个由键值对组成的序列（或其他可迭代对象）或关键字参数
>>> user = {'name': 'Bob'}
>>> user.update([('age', 25)])  # 参数还可以是一个由键值对组成的序列（或其他可迭代对象）
>>> user.update(gender='male')  # 参数还可以是关键字参数
>>> user
{'name': 'Bob', 'age': 25, 'gender': 'male'}

'''

# values
'''
方法values返回一个由字典中的值组成的字典视图。不同于方法keys，方法values返回的视
图可能包含重复的值。
>>> d = {}
>>> d[1] = 1
>>> d[2] = 2
>>> d[3] = 3
>>> d[4] = 1
>>> d.values() # 方法values返回一个由字典中的值组成的字典视图。不同于方法keys，方法values返回的视图可能包含重复的值。
dict_values([1, 2, 3, 1])

'''




