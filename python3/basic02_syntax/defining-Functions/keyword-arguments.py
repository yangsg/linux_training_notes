#// https://docs.python.org/3.6/tutorial/controlflow.html#keyword-arguments


def sum(a, b):
    result = a + b
    print(result)

sum(1, 2)
sum(a=1, b=2)
sum(b=2, a=1)
sum(*[1, 2])
sum(**{'a': 1, 'b': 2})



