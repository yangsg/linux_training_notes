#!/bin/bash

#参考: https://superuser.com/questions/272265/getting-curl-to-output-http-status-code
#注意:
#      通过 curl 这种方式会 增加 nginx 的 access.log 访问日志,
#      所以需要考虑是否要避免这种情况 或 采用其他检测方式 绕过该问题
v_http_status_code=$(curl -o -I -L -s -w "%{http_code}" http://127.0.0.1)

if [ "$v_http_status_code" != 200 ]; then
  systemctl stop keepalived
fi

## [root@nginx01 ~]# yum -y install psmisc   #安装killall 所属的包 psmisc, 确保存在 killall 命令
## [root@nginx02 ~]# yum -y install psmisc   #安装killall 所属的包 psmisc, 确保存在 killall 命令
##  参考: https://unix.stackexchange.com/questions/169898/what-does-kill-0-do
##  man 1 kill
##  man 2 kill
#if ! killall -0 nginx &> /dev/null; then   #当 signal 为 0 时, 仅检测对应进程是否存在
#  systemctl stop keepalived
#fi


