#!/bin/bash

# keyword Compound Commands
# keyword (list)
# keyword { list; }
# keyword ((expression))
# keyword [[ expression ]]

# man bash  #/   Compound Commands


#// (list)
#//      list 在子shell (subshell) 中被执行, 影响shell环境的变量赋值和shell内置命令(builtin commands) 在命令完成后不再启作用(就是说
#//      command 在子shell的进程中执行，影响环境变量的操作只会在subshell中起作用, 当前shell 不会受任何影响)。
#//      整个Compound Commands 的 return status 就是 list 的 exit status

(umask 077 && touch a.txt)


#// { list; }
#//       list 只是简单的在当前shell环境中被执行. list 必须以 newline 或 semicolon 终止, 这就是所说的 group command. 整个 Compound Commands 的 return  status 就是 list 的
#//       exit  status, 注意： 不像元字符  ( and ),  { 和 } 是保留字(reserved words) 且 必须出现在 保留字(reserved word) 被允许以被识别的地方。
#//       因为它们不会导致word break, 所以它们必须依靠 whitespace 或 其他的 shell 元字符(shell metacharacter) 来分隔

{ echo hello; }

{
  echo hello
}


#// ((expression))
#//      根据man bash文档中 ARITHMETIC EVALUATION 部分描述的规则 对 expression 进行 运算求值, 如果 expression 的值 为 非0 (non-zero), 则 return status 为 0,
#//      否则 return status 为 1, 这完全等价于 let "expression"


((2+3))
echo $?
#// 0
((2-2))
echo $?
#// 1



#// [[ expression ]]
#//       根据条件表达式 expression 返回 0 或 1 的 status, Expressions 由man bash 帮助页中 CONDITIONAL EXPRESSIONS 部分描述的基础条件表达式组成。在
#//       [[ 和 ]] 之间是不会执行 Word splitting 和 pathname expansion 的, 但是 tilde expansion, parameter and variable expansion,
#//       arithmetic  expansion, command substitution, process substitution, and quote removal 依然会被执行. 如 -f 这样的条件操作符(Conditional operators)
#//       不能加引号以使其被视为条件表达式的基本构成成分.
#//
#//       当使用 [[ 时， 操作符 < 和 > 使用当前的 locale 来做 字典顺序排序(sort lexicographically)
#//
#//       当操作符 == 和 != 被使用时, 这些操作符右边的 string 会被视为 pattern 并 按照接下来 描述的 Pattern Matching 的规则进行匹配(match)操作。
#//       如果 shell 的 nocasematch 选项被启用, 执行匹配操作时会 会忽略 字母(alphabetic characters)的大小写情况，
#//           操作符 == 在pattern匹配成功时返回 0, 操作符 != 在 pattern 匹配失败时 返回 0.
#//           反之则返回 1(即操作符 == 在 不匹配时返回 1 ，操作符 != 在成功匹配时返回 1 )。
#//           pattern 的任何部分 都 可以被引号引起来 使其被强制作为 string 来被匹配。
#//
#//       额外的, 二元操作符 =~ 也是 可用的，操作符 =~ 具有与 == 和 != 相同的优先级. 当操作符 =~ 被使用时, 其右边的 string 被视为
#//       扩展的正则表达式extended  regular  expression 并根据 regex(3) (见 man 3 regex 手册页)那样来匹配, 如果匹配成功，则返回 0，
#//       反之匹配失败则返回 1，如果该正则表达式本身 语法上 就存在错误，则 该条件表达式 的返回值 就为 2. 如果 shell 的 nocasematch 选项
#//       被启用, 则 在做匹配操作的时候会忽略 字母(alphabetic  characters) 的大小写情况. pattern 的任何部分 都可以被引号引起来 使其 被
#//       强制作为 string 来被匹配. 字符串中与正则表达式中的 parenthesized subexpressions 匹配成功的 Substrings
#//       会被保存在数组变量 BASH_REMATCH 中， 数组变量 BASH_REMATCH 中 索引 为 0 对应的
#//       元素 是字符串 中 与完整的正则表达式(entire  regular expression)匹配成功的部分.
#//       BASH_REMATCH 中 索引为 n 的元素 是匹配第n个 parenthesized subexpression 匹配成功的部分.
#//       Expressions 可以 使用如下的操作符 连接 起来(它们的优先级按从上到下的顺序依次递减):
#//               ( expression )
#//                      Returns the value of expression.  This may be used to override the normal precedence of operators.
#//               ! expression
#//                      True if expression is false.
#//               expression1 && expression2
#//                      True if both expression1 and expression2 are true.
#//               expression1 || expression2
#//                      True if either expression1 or expression2 is true.
#//
#//               The && and || operators do not evaluate expression2 if the value of expression1 is sufficient to determine the return value of the entire conditional expression.


#//----------------------------------------------------------
#示例:
str='a   b'
if [[ $str =~ ^a[[:space:]]{3}b$ ]];  # 该示例输出 empty or blank, 证明在  [[ expression ]] 中缺失没有执行 Word splitting 操作
#              此处操作符右边的正则表达式千万不要加引号(从bash 3.2开始), 否则其被视为字符串而非一个正则表达式
#              书籍 <Advanced Bash-Scripting Guide> 中有许多示例使用的是 bash 3.2 以前版本的语法,所以这一点要特别小心.
#              或则 可以直接参考 <The Linux Command Line>
then
  echo empty or blank
fi

[root@host ~]# [[ '   ' =~ ^[[:space:]]*$ ]] && echo empty or blank
empty or blank

[root@host ~]# [[ "$s" =~ ^[[:space:]]*$ ]] && echo empty or blank
empty or blank





