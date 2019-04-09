s = 'Hello, world.'
str(s)
repr(s)
str(1/7)
x = 10 * 3.25
y = 200 * 200
s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
print(s)
# The repr() of a string adds string quotes and backslashes:
hello = 'hello, world\n'
hellos = repr(hello)
print(hellos)
# The argument to repr() may be any Python object:
repr((x, y, ('spam', 'eggs')))


for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # Note use of 'end' on previous line
    print(repr(x*x*x).rjust(4))

#// https://pyformat.info/   包含了format的许多示例
#// https://www.programiz.com/python-programming/methods/string/format
for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))



'1'.rjust(3)  #// '  1'
'1'.center(3) #// ' 1 '
'1'.ljust(3)  #// '1  '


'12'.zfill(5)             #// '00012'
'-3.14'.zfill(7)          #// '-003.14'
'3.14159265359'.zfill(5)  #// '3.14159265359'

print('We are the {} who say "{}!"'.format('knights', 'Ni'))
print('{0} and {1}'.format('spam', 'eggs'))   #// A number in the brackets can be used to refer to the position of the object passed into the str.format() method.

#// If keyword arguments are used in the str.format() method, their values are referred to by using the name of the argument
print('This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible'))

#// Positional and keyword arguments can be arbitrarily combined:
print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred', other='Georg'))

#// '!a' (apply ascii()), '!s' (apply str()) and '!r' (apply repr()) can be used to convert the value before it is formatted:
contents = 'eels'
print('My hovercraft is full of {}.'.format(contents))
print('My hovercraft is full of {!r}.'.format(contents))


#// An optional ':' and format specifier can follow the field name. This allows greater control over how the value is formatted.
import math
print('The value of PI is approximately {0:.3f}.'.format(math.pi))


table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
    print('{0:10} ==> {1:10d}'.format(name, phone))


#// If you have a really long format string that you don’t want to split up, it would be
#// nice if you could reference the variables to be formatted by name instead of by position.
#// This can be done by simply passing the dict and using square brackets '[]' to access the keys
table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
      'Dcab: {0[Dcab]:d}'.format(table))


#// https://realpython.com/python-string-formatting/
name='bob'
f'hello {name}'   #// 带f前缀的字符串字面量

'{a[name]}'.format(a={'name': 'bob', '1': 'ONE'})
#// '{a[1]}'.format(a={'name': 'bob', '1': 'ONE'})  # error, python也并非完美, 解决办法：使用 % , 如 '%(1)s' % {'name': 'bob', '1': 'ONE'}
#// 参考 https://stackoverflow.com/questions/20677660/python-string-format-with-dict-with-integer-keys
#//      https://www.python.org/dev/peps/pep-3101/


'{age}'.format(**{'name': 'bob', 'age': '17'})

#// https://docs.python.org/3.6/library/functions.html#vars

















