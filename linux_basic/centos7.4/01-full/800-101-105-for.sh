#!/bin/bash


# keyword for ((

# man bash  #/       for \(\(

#// 语法: for (( expr1 ; expr2 ; expr3 )) ; do list ; done
#//
#//   首先, 算术表达式 expr1 会根据 man bash 手册页 ARITHMETIC EVALUATION 部分描述的规则 被计算求值,
#//   算术表达式 expr2 会被重复地计算求值 直到 求得的值为 0 为止. 当每次 expr2 计算的值 为 非0 (non-zero) 时，
#//   list 会被 执行 且 算术表达式 expr3 会被计算求值。如果任意表达式被省略不写，其行为就类似于 求得的值 为 1 .
#//
#//   整个复合命令的 return value 为 执行的最后的 command 的 exit status, 或 false(如果任意表达式为非法的话)


for ((i=0; i<4; i++)); do
  echo $i
done

