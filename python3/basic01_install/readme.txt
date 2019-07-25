
系统基本信息
[root@python3lang ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@python3lang ~]# uname -r
    3.10.0-693.el7.x86_64

// 构建基本编译环境
[root@python3lang ~]# yum -y install gcc gcc-c++ autoconf automake

// 安装依赖和一些辅助功能包
[root@python3lang ~]# yum -y install \
  zlib zlib-devel \
  bzip2 bzip2-devel \
  ncurses ncurses-devel \
  readline readline-devel \
  openssl openssl-devel \
  openssl-static \
  xz lzma xz-devel \
  sqlite sqlite-devel \
  gdbm gdbm-devel \
  tk tk-devel


// 下载、编译、安装
[root@python3lang ~]# mkdir /app
[root@python3lang ~]# mkdir download
[root@python3lang ~]# cd download/
[root@python3lang download]# wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
[root@python3lang download]# tar -xvf Python-3.6.8.tgz
[root@python3lang download]# cd Python-3.6.8/
[root@python3lang Python-3.6.8]# ./configure --prefix=/app/python3.6
[root@python3lang Python-3.6.8]# make
[root@python3lang Python-3.6.8]# make install

// 初始化环境变量
[root@python3lang Python-3.6.8]# vim /etc/profile
    export PATH=$PATH:/app/python3.6/bin

[root@python3lang Python-3.6.8]# source /etc/profile

// 测试安装
[root@python3lang ~]# python3.6 --version
[root@python3lang ~]# python3.6 -c 'print("hello world")'



---------------------------------------------------------------------------------------------------
查看相关目录:
[root@python3lang ~]# tree -L 1 /app/python3.6/
/app/python3.6/
      ├── bin
      ├── include
      ├── lib
      └── share


[root@python3lang ~]# tree -L 1 /app/python3.6/lib/python3.6/ | less




