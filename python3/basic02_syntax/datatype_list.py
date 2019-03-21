#// https://docs.python.org/3.6/tutorial/introduction.html#lists


#// python中的列表有点类似于javascript的数组
squares = [1, 4, 9, 16, 25]

#// 类似字符串和所有内置的sequence类型，list支持索引和分片 Like strings (and all other built-in sequence type), lists can be indexed and sliced:
squares[0]   # 1
squares[-1]  # 25
squares[-3:] # [9, 16, 25]
squares[:]   # [1, 4, 9, 16, 25], 注：所有的slice操作返回的都是一个新的list(即一种副本)

#// 列表也支持拼接
squares + [36, 49, 64, 81, 100]

#// 列表是可变类型，即 immutable
cubes = [1, 8, 27, 65, 125]
cubes[3] = 64
cubes.append(216)  # 末尾追加
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']  #也可以赋值给slices,这甚至可以修改list的大小
letters[2:5] = ['C', 'D', 'E']   #letters is ['a', 'b', 'C', 'D', 'E', 'f', 'g']
letters[2:5] = []   #['a', 'b', 'f', 'g']
letters[:] = []     # letters is []


#// 内置函数len()可返回列表大小
letters = ['a', 'b', 'c', 'd']
len(letters)  # 4

#// 列表支持嵌套(即支持列表的列表)
a = ['a', 'b', 'c']
n = [1, 2, 3]
x = [a, n]  # x is [['a', 'b', 'c'], [1, 2, 3]]
x[0]   # ['a', 'b', 'c']
x[0][1]  # 'b'







#// ----
# 其他： 如下这个例子演示使用了python的多个语法特性：
a, b = 0, 1    #<< python支持多项赋值,在多项赋值操作中，右边的所有值会在任何赋值执行前被计算出来
while b < 10:
    print(b)
    a, b = b, a+b
#//  类似C语言，在python中，在使用condition的上下文中，任何非0整数被视为true, 0被视为false。
#//  condition也可以是string 或 list,  in fact any sequence;
#//  anything with a non-zero length is true, empty sequences are false.

#// 缩进在python中用于组织多条语句(类似于C语言中的{}来组织复合语句块)


















