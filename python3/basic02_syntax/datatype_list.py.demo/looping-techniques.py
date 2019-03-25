#// https://docs.python.org/3.6/tutorial/datastructures.html#looping-techniques


def iterate_dict():
    knights = {'gallahad': 'the pure', 'robin': 'the brave'}
    for k, v in knights.items():    #// 同时获取dict的key, value
        print(k, v)

def iterate_list_with_index_value():
    for i, v in enumerate(['tic', 'tac', 'toe']):  #// 同时获取list的 index, value
        print(i, v)

def iterate_multiple_list():
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):   #// 利用zip构造zip对象(提供类似一种元素为元组的list视图)
        print('What is your {0}?  It is {1}.'.format(q, a))

def iterate_in_reversed():
    for i in reversed(range(1, 10, 2)):  #// 反序迭代
        print(i)

def iterate_with_sorted():
    basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
    for f in sorted(set(basket)):  #// 排序后迭代，注意：此例中使用了set去除重复，如果无序去重复，直接使用 sorted(basket) 即可
        print(f)


#// demo01
import math
raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
filtered_data = []
for value in raw_data:                  # 写在一行也可以：[value for value in raw_data if not math.isnan(value)]
    if not math.isnan(value):
        filtered_data.append(value)

filtered_data



