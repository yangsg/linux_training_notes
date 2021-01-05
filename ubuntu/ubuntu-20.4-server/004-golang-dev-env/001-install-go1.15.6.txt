






:) 下载  golang tarball 包

ysg@vm01:~$ mkdir download
ysg@vm01:~$ sudo mkdir /app

ysg@vm01:~$ cd download/
ysg@vm01:~/download$ wget -O go1.15.6.linux-amd64.tar.gz https://golang.google.cn/dl/go1.15.6.linux-amd64.tar.gz
ysg@vm01:~/download$ file go1.15.6.linux-amd64.tar.gz



:) 解压安装
ysg@vm01:~/download$ sudo tar -C /app/ -xvf go1.15.6.linux-amd64.tar.gz

ysg@vm01:~/download$ ls /app/go/
api  AUTHORS  bin  CONTRIBUTING.md  CONTRIBUTORS  doc  favicon.ico  lib  LICENSE  misc  PATENTS  pkg  README.md  robots.txt  SECURITY.md  src  test  VERSION


ysg@vm01:~/download$ sudo vim /etc/profile
export PATH=$PATH:/app/go/bin

ysg@vm01:~/download$ source /etc/profile

:) 验证安装
ysg@vm01:~/download$ go version
go version go1.13.8 linux/amd64



---------------------
设置 goproxy
   https://goproxy.cn/



ysg@vm01:~$ sudo vim /etc/profile
export GO111MODULE=on
export GOPROXY=https://goproxy.cn

ysg@vm01:~$ source /etc/profile

ysg@vm01:~$ go env


















