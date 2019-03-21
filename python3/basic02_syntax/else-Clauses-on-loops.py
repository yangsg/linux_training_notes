#// https://docs.python.org/3.6/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops

#//  python中else子句区别于C语言的一个地方是loops 操作也可以带有else子句
#//  该else子句在类似for循环将list消耗殆尽或while 循环的condition为false而终止时，
#//  而非通过break语句退出时被执行
for n in range(2, 10):   # 一个寻找素数的例子
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:  #<< 注：该else子句属于for循环，而非if 语句
        # loop fell through without finding a factor
        print(n, 'is a prime number')

i = 0
while i < 4:
   i += 1
   print(i)
else:
   print('terminate normally, not by break statement')


