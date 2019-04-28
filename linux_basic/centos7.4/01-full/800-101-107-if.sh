#!/bin/bash


# keyword if

# man bash  #/       if list;


#// 语法: if list; then list; [ elif list; then list; ] ... [ else list; ] fi
#//    if list 被执行, 如果其 exit status 为 0, 那么 then list 会被执行. 否则, 各个 elif list
#//    将会按次序轮流被执行, 如果其 exit status 为 0, 则与其对应的 then list 会被执行 且 整个 if 命令在此结束.
#//    否则， else list 会被执行(如果else list存在的话). 该整个复合命令的 exit status 就是
#//    最后被执行命令的exit status, 或者如果没有 condition 被测试为 true, 则 exit status 为 0

index=$(($RANDOM%3))
genders=('male' 'female' 'unknown')

gender=${genders[$index]}

if [ "$gender" = 'male' ]; then
  echo 'man'
elif [ "$gender" = 'female' ]; then
  echo 'woman'
else
  echo 'unknown'
fi


