#!/bin/bash


# keyword for-in

# man bash  #/       for name

#// 语法: for name [ [ in [ word ... ] ] ; ] do list ; done
#//      跟在 in 后面的一系列 words 会被 expanded, 同时生成 items 的 序列(list). 变量 name 会 依次轮流地被设置为该 list 中的每个元素,
#//      每次 list(这里的list指的是do后面的list语句) 都会被执行一次.
#//      如果 in word 被省略不写, 则 for 命令针对每个 positional parameter(see PARAMETERS below)
#//      各执行一次(即 `for name` 默认是 `for arg in "$@"` 的简写形式), return status 就是 执行的最后命令的 exit  status.
#//      如果 items 的 expansion 的结果是一个 empty list, 那么 没有 command 会被执行，且 return status 为 0.


array=(one two three 'hello world')
for name in "${array[@]}"; do
  echo $name
done

for index in "${!array[@]}"; do
  printf "%s\t%s\n" "$index" "${array[$index]}"
done

for i in {1..4}; do
  echo $i
done

for i in {10,20,30,40}; do
  echo $i
done

for i in $(seq 1 5); do
  echo $i
done

for name in ; do
  echo "no chance to be executed because the for command iterates an empty list"
done

for name in "$@"; do   # [root@basic 01-full]# bash 800-101-104-for-in.sh  A B C D
  echo $name
done

for name; do    # `for name` 默认是 `for name in "$@"` 的简写形式
  echo $name
done

