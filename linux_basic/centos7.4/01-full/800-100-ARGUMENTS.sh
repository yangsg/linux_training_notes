#!/bin/bash


#// keyword ARGUMENTS
#// man bash #/^ARGUMENTS

echo "脚本名": $0
echo "位置参数个数:": $#

#// man bash #/   Special Parameters
echo '测试 $@ -----------------------------------------'
echo "$@"
# 注：for arg  等价于 for arg in "$@", 注意, 这里一定是加了双引号版本的  "$@", 不加引号或加单引号都不正确, 具体原因见 http://mywiki.wooledge.org/BashPitfalls
for var in "$@"  #  "$@"  is equivalent  to  "$1" "$2" ...  # When there are no positional parameters, "$@" and $@ expand  to  nothing (i.e., they are removed)
do
  echo "$var"
done


#//  "$*" is equivalent to "$1c$2c...", where c is the first character of the value of the IFS variable.
#//  If IFS is unset, the parameters are separated by spaces.  If IFS is null, the parameters are joined without intervening separators.
echo '测试 $* -----------------------------------------'
echo "$*"
for var in "$*"    # "$*" is equivalent to "$1c$2c..."
do
  echo "$var"
done


#  其他
echo $#      #变量 井字符 # Expands to the number of positional parameters in decimal.

echo '--------观察 ${#VAR} 的用法, 参考 《advanced bash script guide》------------------------------------'
# 形如语法 ${#VAR} 用于计算字符个数, 如果 VAR 为 "*" or "@", 则${#VAR}表示位置参数(positional parameters)个数或数组(array)元素个数
message_text='hello'
echo ${#message_text}  # 输出5, 因为 ${#var} 中的var是字符串变量， 则计算 String length (number of characters in $var).
echo ${#@}   # ${#*} and ${#@} give the number of positional parameters.
echo ${#*}   # ${#*} and ${#@} give the number of positional parameters.


ARRAY=(one two three, four, five)
echo ${#ARRAY[@]}  # For an array, ${#array[*]} and ${#array[@]} give the number of elements in the array.
echo ${#ARRAY[*]}  # For an array, ${#array[*]} and ${#array[@]} give the number of elements in the array.

echo ${#ARRAY}     # For an array, ${#array} is the length of the first element in the array.

exit 0


