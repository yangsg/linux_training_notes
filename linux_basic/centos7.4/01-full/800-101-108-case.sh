#!/bin/bash


# keyword case

# man bash  #/       case word

#// 语法: case word in [ [(] pattern [ | pattern ] ... ) list ;; ] ... esac
#//     case 命令首先 expands word, 并依次轮流尝试与每个 pattern 进行匹配操作
#//     (使用与 pathname expansion 匹配时相同的匹配规则)(见 man bash帮助页的 Pathname Expansion 部分),
#//     word 会被 expanded 的 类型有 tilde expansion, parameter and variable expansion, arithmetic substitution,
#//     command  substitution,  process  substitution  and  quote removal. 每个用于检验的 pattern 会被 expanded
#//     的类型有 tilde expansion, parameter and variable expansion, arithmetic substitution, command substitution, and process substitution.
#//     如果shell 的 nocasematch 被启用, 则 匹配操作执行时会忽略 字母字符的大小写情况, 如果某个成功匹配被找到, 则其对应的 list 会被执行.
#//     如果 操作符 ;; 被使用了，则在首次 pattern 匹配成功后，不会再试图执行后续的匹配.
#//     使用 ;& 替换 ;; 导致继续执行与下一组 patterns 关联的 list. 使用 ;;& 替换 ;; 导致 shell 测试 语句中的 下一个 pattern 序列, 如果有的话，
#//     并在匹配成功的时候执行与之关联的 list. 如果没有 任何 pattern 匹配成功，则整个复合命令的 exit status 为 0. 否则， 其 exit status 为
#//     list 中最后被执行的命令的 exit status.


