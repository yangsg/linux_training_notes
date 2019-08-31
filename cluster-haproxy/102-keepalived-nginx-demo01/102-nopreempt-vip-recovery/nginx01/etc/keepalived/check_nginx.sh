#!/bin/bash

#参考: https://superuser.com/questions/272265/getting-curl-to-output-http-status-code
#注意:
#      通过 curl 这种方式会 增加 nginx 的 access.log 访问日志,
#      所以需要考虑是否要避免这种情况 或 采用其他检测方式 绕过该问题
#v_http_status_code=$(curl -o -I -L -s -w "%{http_code}" http://127.0.0.1)
#
#if [ "$v_http_status_code" != 200 ]; then
#  systemctl stop keepalived
#fi

# [root@nginx01 ~]# yum -y install psmisc   #安装killall 所属的包 psmisc, 确保存在 killall 命令
# [root@nginx02 ~]# yum -y install psmisc   #安装killall 所属的包 psmisc, 确保存在 killall 命令
#  参考: https://unix.stackexchange.com/questions/169898/what-does-kill-0-do
#  man 1 kill
#  man 2 kill

#脚本运行时可能会发生一些错误, 这些错误即有可能是编码引起的, 也有可能是运行环境不符合要求引起的.
#所以为了方便调试 发现 错误源, 定义了 v_log_file 来接受脚本的输出, 当 v_log_file 为 /dev/null 时,
#直接丢弃输出, 当 v_log_file 的 filepath 是, 则将 输出定向到 该 filepath 对应的 file
v_debug=false
v_log_file=/dev/null

if [ "$v_debug" = true ]; then
  v_log_file=/tmp/keepalived.log
fi

if ! killall -0 nginx &> $v_log_file; then   #当 signal 为 0 时, 仅检测对应进程是否存在
  systemctl stop keepalived
  exit 1
fi

exit 0


