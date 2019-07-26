
#// Properties vs. Getters and Setters
#// https://www.python-course.eu/python3_properties.php

#// python3 语言中 不需要 getter 和 setter,
#// 因为 python3 支持 property 特性, 其已经为你保留了
#// 后期 修改 代码实现的 权利(这其实也是 其他语言(如java)中
#// getter 和  setter 方法存在的意义或目的 )

#// 比如, 在 python3 中, 对于如下例子中的 User 类,
#// 最开始可以做最简单的实现(避免过度设计)
class User:
  def __init__(self, name):
    self.name = name;

tom = User('Tom')
print(tom.name)
tom.name = 'Jerry'
print(tom.name)


#// OK, 可是后来增加一个需求: 即 user 的属性 name 的长度 必须在 8到10个字符之间,
#// 假设该 判断检查 要 放在 赋值时 判断, 且不符合条件则抛出异常, 则可将 User 类的实现修改为 如下即可:

class User:
  def __init__(self, name):
    self.name = name;

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, name):
    if 8 <= len(name) <= 10:
      self.__name = name
    else:
      raise ValueError;


try:
  print('-' * 100)
  tom = User('Tom')
  print(tom.name)
  tom.name = 'Jerry'
  print(tom.name)
except ValueError:
  print('ValueError occurs')














