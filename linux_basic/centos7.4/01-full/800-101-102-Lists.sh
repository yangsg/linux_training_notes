#!/bin/bash

# keyword SHELL GRAMMAR
# keyword Lists
# man bash  #/   Lists

#// Lists  (原汁原味的描述见 man bash)
#//  A list 是 一个 或 多个 pipelines 的序列，各个 pipeline 之间以 操作符  ;, &, &&, or || 分隔, 同时可以选择性的以符号 ;, &, or <newline> 中的某一个符号结束。
#//  在这些  list operators 中， && and || 具有相同的优先级，紧随其后的是  ; and & (注: ; and & 具有相同优先级)
#//
#//  一个或多个 newlines 的序列 可以替代 分号(semicolon) 出现在 list 中来 界定(delimit) commands
#//
#//  如果 command 以控制操作符  & 终止, 则 shell 将以一个子shell (subshell) 在后台 执行该 command. 当前shell 不会等待 该 command 结束, 并且直接返回0 (原文:the return  status  is  0)，
#//  以分号 ; 分隔的命令 会按 顺序被执行，当前shell 会等待 每个 command 被轮流执行完毕，return status 是 最后执行的命令(the last command executed) 的 exit status.
#//
#//  AND and OR lists 是 一个或 多个 pipelines 的序列, 且分别以控制操作符  && and || 分隔,  AND and OR lists 以左关联性 被执行，
#//  AND list 具有如下形式:
#//
#//          command1 && command2
#//
#//  其中 command2 当且仅当 command1 返回的 exit status 为 0 时 才被执行
#//
#//  An OR list 具有如下形式:
#//
#//          command1 || command2
#//
#//  其中 command2 当且仅当 在 command1 返回的 exit status 为 非0 (non-zero)是才被执行.
#//  整个 AND and OR lists 的 return status 为 list 中 最后被执行命令的  exit status.


ls a.txt; sleep 2; ls b.txt
sleep 2;
sleep 3 &

ls a.txt &> /dev/null || touch a.txt && cat a.txt
ls -d dir01 &> /dev/null && touch dir01/a.txt || mkdir dir01


