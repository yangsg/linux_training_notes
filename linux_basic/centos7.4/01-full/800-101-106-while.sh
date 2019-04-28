#!/bin/bash


# keyword while

# man bash  #/       while


#// 语法: while list-1; do list-2; done
#//    只要 list-1 中最后执行的命令返回的 exit status 为 0 (zero), 则 while 就会不断的执行 list-2,
#//    while 命令的 exit status 为  list-2 中 被执行的最后的命令的 exit status, 或者如果没有 任何 list-2
#//    中的命令被执行(如没有进入循环体)，则返回 0 .


endtime=$(date -d '+2 seconds' +%s)
while true; do
  now=$(date +%s)
  if [ $now -gt $endtime ]; then
    break
  fi

  date -d "@$now" '+%F_%T'
  sleep 1
done


start_time=$(date -d '+2 seconds' +%s)
while true; do
  now=$(date +%s)
  if [ $now -lt $start_time ]; then
    continue
  fi

  date -d "@$now" '+%F_%T'
  break
done


