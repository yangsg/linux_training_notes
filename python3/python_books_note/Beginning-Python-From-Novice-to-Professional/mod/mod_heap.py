
# 堆

'''
    另一种著名的数据结构是堆（heap），它是一种优先队列。优先队列让你能够以任意顺序添
加对象，并随时（可能是在两次添加对象之间）找出（并删除）最小的元素。相比于列表方法min，
这样做的效率要高得多。

    实际上，Python没有独立的堆类型，而只有一个包含一些堆操作函数的模块。这个模块名为
heapq（其中的q表示队列），它包含6个函数（如表10-5所示），其中前4个与堆操作直接相关。必
须使用列表来表示堆对象本身。

        表10-5 模块heapq中一些重要的函数
函 数                            描 述
heappush(heap, x)           将x压入堆中
heappop(heap)               从堆中弹出最小的元素
heapify(heap)               让列表具备堆特征
heapreplace(heap, x)        弹出最小的元素，并将x压入堆中
nlargest(n, iter)           返回iter中n个最大的元素
nsmallest(n, iter)          返回iter中n个最小的元素


    函数heappush用于在堆中添加一个元素。请注意，不能将它用于普通列表，而只能用于使用
各种堆函数创建的列表。原因是元素的顺序很重要（虽然元素的排列顺序看起来有点随意，并没
有严格地排序）。


>>> from heapq import *
>>> from random import shuffle
>>> data = list(range(10))
>>> shuffle(data)
>>> heap = []
>>> for n in data:
...     heappush(heap, n)
...
>>> heap
[0, 1, 3, 6, 2, 8, 4, 7, 9, 5]
>>> heappush(heap, 0.5)
>>> heap
[0, 0.5, 3, 6, 1, 8, 4, 7, 9, 5, 2]

元素的排列顺序并不像看起来那么随意。它们虽然不是严格排序的，但必须保证一点：位置
i处的元素总是大于位置i // 2处的元素（反过来说就是小于位置2 * i和2 * i + 1处的元素）。
这是底层堆算法的基础，称为堆特征（heap property）。

函数heappop弹出最小的元素（总是位于索引0处），并确保剩余元素中最小的那个位于索引0
处（保持堆特征）。虽然弹出列表中第一个元素的效率通常不是很高，但这不是问题，因为heappop
会在幕后做些巧妙的移位操作。

>>> heappop(heap)
0
>>> heappop(heap)
0.5
>>> heappop(heap)
1
>>> heap
[2, 3, 4, 7, 6, 5, 9, 8]

    函数heapify通过执行尽可能少的移位操作将列表变成合法的堆（即具备堆特征）。如果你的
堆并不是使用heappush创建的，应在使用heappush和heappop之前使用这个函数。

>>> heap = [5, 8, 0, 3, 6, 7, 9, 1, 4, 2]
>>> heapify(heap)
>>> heap
[0, 1, 5, 3, 2, 7, 9, 8, 4, 6]


    函数heapreplace用得没有其他函数那么多。它从堆中弹出最小的元素，再压入一个新元素。
相比于依次执行函数heappop和heappush，这个函数的效率更高。

>>> heapreplace(heap, 0.5)
0
>>> heap
[0.5, 1, 5, 3, 2, 7, 9, 8, 4, 6]
>>> heapreplace(heap, 10)
0.5
>>> heap
[1, 2, 5, 3, 6, 7, 9, 8, 4, 10]

    至此，模块heapq中还有两个函数没有介绍：nlargest(n, iter)和nsmallest(n, iter)，:分
别用于找出可迭代对象iter中最大和最小的n个元素。这种任务也可通过先排序（如使用函数
sorted）再切片来完成，但堆算法的速度更快，使用的内存更少（而且使用起来也更容易）。

>>> import heapq
>>> heapq.nlargest(2, [3,9,7,1,4,6,5])
[9, 7]
>>> heapq.nsmallest(2, [3,9,7,1,4,6,5])
[1, 3]

>>> import heapq
>>> heapq.nlargest(2, [{'tag': 'A', 'num': 2}, {'tag': 'C', 'num': 1}, {'tag': 'B', 'num': 3}], key=lambda item: item['tag'])
[{'tag': 'C', 'num': 1}, {'tag': 'B', 'num': 3}]
>>> heapq.nlargest(2, [{'tag': 'A', 'num': 2}, {'tag': 'C', 'num': 1}, {'tag': 'B', 'num': 3}], key=lambda item: item['num'])
[{'tag': 'B', 'num': 3}, {'tag': 'A', 'num': 2}]

heapq.nlargest and heapq.nsmallest functions perform best for smaller values of n. For larger values, it is more efficient to use the sorted() function.
Also, when n==1, it is more efficient to use the built-in min() and max() functions.
If repeated usage of these functions is required, consider turning the iterable into an actual heap.

更多 heapq.nlargest 的例子见： https://www.programcreek.com/python/example/5338/heapq.nlargest

'''




