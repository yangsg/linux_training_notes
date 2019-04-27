#!/bin/bash

# keyword SHELL GRAMMAR
# keyword Simple Commands
# man bash  #/   Simple Commands


#//    Simple Commands   (原汁原味的描述见 man bash)
#//    A simple command 是 一个可选的赋值序列, 随后接的是由 blank-separated 的  words 和 redirections, 并且 terminated by a control operator.
#//    第一个 word 指明了 被执行的 command, 并且被作为 argument zero 传递, 而剩余的 words 则作为 该被调用 command 的 实参来传递
#//
#//    a simple command 的 exit status 就是它的 return value, 如果该 command 是被 信号n (signal n.)终止的，则 return value 就是 128+n .


#// 简单命令的一些例子 (各种各样不同的命令，重定向 和 其他bash的特性需在学习中不断积累, 在此无法一一列出)
var01=one var02=two var03=three test.sh a.txt b.txt
var01=one var02=two var03=three test.sh
IFS=$' \t\n' ./test.sh
echo $var01  > /dev/null;
cat < /dev/null > /dev/null


