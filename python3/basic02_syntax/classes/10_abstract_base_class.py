#// https://docs.python.org/3.6/library/abc.html

#// 注: 与 java 的抽象方法不同, python的抽象方法可以拥有实现

from abc import ABC, abstractmethod

class Animal(ABC):
  @abstractmethod
  def greet(self):
    pass



class Dog(Animal):
  def greet(self):
    super().greet()
    print('汪' * 10)

class Cat(Animal):
  def greet(self):
    super().greet()
    print('喵' * 10)


spike = Dog()
tom = Cat()

tom.greet()
spike.greet()




