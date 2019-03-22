#// https://docs.python.org/3.6/tutorial/controlflow.html#keyword-arguments


def sum(a, b):
    result = a + b
    print(result)

sum(1, 2)
sum(a=1, b=2)
sum(b=2, a=1)
sum(*[1, 2])
sum(**{'a': 1, 'b': 2})

def f(kind, *arguments, **keywords):
    print(kind)
    for index in arguments:
        print(index)
    for key in keywords:
        print(key, '---', keywords[key])

f('python', 1, 2, 3, 4, username='root', password='1234', host='127.0.0.1')
f('python', *(1, 2, 3, 4), **{'username': 'root', 'password': '1234', 'host': '127.0.0.1'})






