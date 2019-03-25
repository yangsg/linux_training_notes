#// https://docs.python.org/3.6/tutorial/datastructures.html#more-on-conditions


#// python中的条件表达式和javascript类似，都比较灵活

#// in 和 not in 可用于 sequence 中的成员判断
#//  is 和 is not 用于两个对象是否为同一个对象, 对于向list这种可变对象比较重要
a = [1,2]
b = [1,2]
a is b  #// False
a is a  #// True

#// Comparisons can be chained. For example, a < b == c tests whether a is less than b and moreover b equals c.

#// 逻辑运算符 and  or not   括号可用于调整优先级
#// and or 具有短路效果

string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
non_null = string1 or string2 or string3
non_null  #'Trondheim'   # 这种效果和javascript中的语句 a = '' || 'result' || 'not_result'; 类似


#// https://docs.python.org/3.6/tutorial/datastructures.html#comparing-sequences-and-other-types
#// 相同类型的 Sequence 可以按字典比较
(1, 2, 3)              < (1, 2, 4)
[1, 2, 3]              < [1, 2, 4]
'ABC' < 'C' < 'Pascal' < 'Python'
(1, 2, 3, 4)           < (1, 2, 4)
(1, 2)                 < (1, 2, -1)
(1, 2, 3)             == (1.0, 2.0, 3.0)
(1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)













