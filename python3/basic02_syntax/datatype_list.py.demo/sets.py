#// https://docs.python.org/3.6/tutorial/datastructures.html#sets

empty=set()   #创建空set必须用set()语法，而不能用{}, 应为{}这种语法已经预留给dict字典了


basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)                      # show that duplicates have been removed
'orange' in basket                 # fast membership testing
'crabgrass' in basket

# Demonstrate set operations on unique letters from two words
a = set('abracadabra')
b = set('alacazam')
a                                  # unique letters in a
a - b                              # letters in a but not in b
a | b                              # letters in a or b or both
a & b                              # letters in both a and b
a ^ b                              # letters in a or b but not both


#// 同 list comprehensions 类似，set 也支持 comprehensions
a = {x for x in 'abracadabra' if x not in 'abc'}
a








