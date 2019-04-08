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

for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))



'1'.rjust(3)  #// '  1'
'1'.center(3) #// ' 1 '
'1'.ljust(3)  #// '1  '


'12'.zfill(5)             #// '00012'
'-3.14'.zfill(7)          #// '-003.14'
'3.14159265359'.zfill(5)  #// '3.14159265359'

print('We are the {} who say "{}!"'.format('knights', 'Ni'))
print('{0} and {1}'.format('spam', 'eggs'))





