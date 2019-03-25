#// https://docs.python.org/3.6/tutorial/datastructures.html#dictionaries
#// https://docs.python.org/3.6/library/stdtypes.html#typesmapping

#// https://docs.python.org/3.6/library/stdtypes.html#mapping-types-dict

#// 字典的key只能是不可变数据类型，因为如果可变类型能作为key, 那么dict内部的数据结构容易遭到破坏
#// keys, which can be any immutable type; strings and numbers can always be keys.
#// Tuples can be used as keys if they contain only strings, numbers, or tuples;


empty={}   #创建空字典

{'a':1, 'b':2}
{
    'a': 1,
    'b': 2
}

x, y = 'key01', 'key02'
{            #结果：{'key01': 1, 'key02': 2}
  x: 1,
  y: 2
}

#// The dict() constructor builds dictionaries directly from sequences of key-value pairs:
dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
dict([['sape', 4139], ['guido', 4127], ['jack', 4098]])

#// dict comprehensions 也得到了支持
{x: x**2 for x in (2, 4, 6)}

dict(sape=4139, guido=4127, jack=4098)





tel = {'jack': 4098, 'sape': 4139}
tel['guido'] = 4127
tel
tel['jack']
del tel['sape']
tel['irv'] = 4127
tel
list(tel.keys())    #// 返回无序的keys的列表
sorted(tel.keys())  #// 返回有序的keys的列表
'guido' in tel
'jack' not in tel



