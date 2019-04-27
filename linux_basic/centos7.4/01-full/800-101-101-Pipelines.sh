#!/bin/bash

# keyword SHELL GRAMMAR
# keyword Pipelines
# man bash  #/   Pipelines

#//  Pipelines (管道 其实 是一种进程间通信(IPC)机制)  (原汁原味的描述见 man bash)
#//
#//         A pipeline 是由控制操作符(control operators) | 或 |& 分隔的命令序列(命令可能是一个或多个).  pipeline 的格式如下:
#//                 [time [-p]] [ ! ] command [ [|⎪|&] command2 ... ]
#//
#//         command 的 standard output 经由  pipe 被连接到 command2 的 standard input, 连接的建立操作会在 command 指定的任何 重定向 (any redirections) 之前执行的，
#//         如果使用的是 管道符  |& , 则 command 的 standard error 也会通过 pipe 被连接到 command2 的 standard input; 它其实是   2>&1 |   的简写形式. 这种
#//         隐式的 standard error 的重定向 是在 command 指定的任何重定向(any redirections)之后执行的。
#//
#//         pipeline 的  return status 是 pipeline 中 最后的命令(last command) 的 exit status, 除非 pipefail 选项被启用(enabled)了. 如果  pipefail 被启用,则
#//         pipeline 的 return status 是 最后那条 以 non-zero status 退出(exit) 的 命令的 exit status, 或者如果所有命令都成功，则为 0, 如果在 pipeline 之前存在
#//         保留字 ! , 则 pipeline 的 exit status 则是 对前文所述的 exit status 进行逻辑取反后的结果。shell需先等待 pipeline 中所有命令都终止后才会返回值.
#//
#//         如果 pipeline 之前 存在 time 保留字， pipeline 在终止(terminates)是会报告其执行所耗费的时间以及 user and system time.
#//         选项 -p 与shell 为 POSIX mode的输出格式有关(详细信息见英文版的man bash)
#//
#//         每个 pipeline 中的 command 在其各自的进程中被执行(即在一个子shell (subshell)中执行)
#//
#//         更多与 pipeline 相关的信息，可以参考 book《linux/unix系统编程手册》


time sleep 2
#// real    0m2.002s
#// user    0m0.000s
#// sys     0m0.001s

echo $?
#// 0

time ! sleep 2
#// real    0m2.002s
#// user    0m0.001s
#// sys     0m0.000s
echo $?
#// 1

time -p sleep 2
#// real 2.00
#// user 0.00
#// sys 0.00

cat /etc/fstab | wc -l
echo 'hello' | grep 'e'
ping www.baidu.com |& tee a.txt | less
ping www.baidu.com 2> /dev/null | tee a.txt | less
ping www.baidu.com 2> /dev/null | tee a.txt |  cat > b.txt
time  ping www.baidu.com |& tee a.txt | less

