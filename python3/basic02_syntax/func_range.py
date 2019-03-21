#// https://docs.python.org/3.6/tutorial/controlflow.html#the-range-function
#// https://docs.python.org/3.6/library/stdtypes.html#range

for i in range(5):  # 此处 range(5) 生成表示 0,1,2,3,4 的range对象
    print(i)

range(5, 10)   #range:  5, 6, 7, 8, 9
range(0, 10, 3) #range: 0, 3, 6, 9
range(-10, -100, -30) #range: -10, -40, -70

# 可结合 range() and len() 来遍历序列
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])      # << 对于该例的情况，大多数时候，可以考虑使用enumerate()函数，见 https://docs.python.org/3.6/library/functions.html#enumerate

# 注意：简单的print输出range对象得到的输出结果可能不是您期望的：
print(range(10)) #输出： range(0, 10)

# range对象表现出的效果有点像list, 但是range并未真实的在内部分配内存列出了每一个列表元素，从而相对list对象来说range节省了空间,
# 其实 range() 返回的是一个 iterable 对象
list(range(5))  # [0, 1, 2, 3, 4]





