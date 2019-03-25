#// https://docs.python.org/3.6/tutorial/datastructures.html#tuples-and-sequences
#// https://docs.python.org/3.6/library/stdtypes.html#typesseq

#// https://docs.python.org/3.6/library/stdtypes.html#sequence-types-list-tuple-range


#// tuples 是不可变数据类型

empty = ()    #创建空元组
singleton = 'hello',   #创建单个元素的元组, 必须加尾随的逗号是为了和('hello')区分
singleton = ('hello',) #创建单个元素的元组
len(singleton)


t = 12345, 54321, 'hello!'     # tuple packing, 这和java中的Integer i = 1;这种自动封装的思想有点类似
x, y, z = t
t[0]
t
# Tuples may be nested:
u = t, (1, 2, 3, 4, 5)
u
# Tuples are immutable:
#t[0] = 88888  # error
# but they can contain mutable objects:
v = ([1, 2, 3], [3, 2, 1])
v





