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









