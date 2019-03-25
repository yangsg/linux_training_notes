#// https://docs.python.org/3.6/tutorial/datastructures.html#list-comprehensions

#// List comprehensions 是创建list对象的一种简洁的方式


#// demo01
squares = [x**2 for x in range(10)]
squares = list(map(lambda x: x**2, range(10)))

#// A list comprehension consists of brackets containing an expression
#// followed by a for clause, then zero or more for or if clauses.


#// demo02
[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]


#// 其他示例
vec = [-4, -2, 0, 2, 4]
[x*2 for x in vec]

[x for x in vec if x >= 0]

[abs(x) for x in vec]

freshfruit = ['  banana', '  loganberry ', 'passion fruit  ']
[weapon.strip() for weapon in freshfruit]

[(x, x**2) for x in range(6)]

from math import pi
[str(round(pi, i)) for i in range(1, 6)]




