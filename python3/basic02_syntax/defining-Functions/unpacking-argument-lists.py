#// https://docs.python.org/3.6/tutorial/controlflow.html#unpacking-argument-lists

def sum(a, b):
    return a + b

sum(2, 3)
sum(*[2, 3])
sum(**{'a': 2, 'b': 3})

