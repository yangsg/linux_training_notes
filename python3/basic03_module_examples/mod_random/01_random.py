import random

target = random.choice(['apple', 'pear', 'banana'])   #// 随机选择某个元素
print(target)


random.sample(range(100), 10)   # sampling without replacement  #// 从0-99个数中选择不重复的10个数
#// [30, 83, 16, 4, 8, 81, 41, 50, 18, 33]

random.random()    # random float
#//0.17970987693706186

random.randrange(6)    # random integer chosen from range(6)
#// 4


