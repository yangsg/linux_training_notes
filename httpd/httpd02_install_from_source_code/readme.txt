

[root@httpd7server ~]# mkdir download
[root@httpd7server ~]# cd download/


// apr apr-util相关的网址:
// http://apr.apache.org/
// http://apr.apache.org/download.cgi
// apr: Apache Portable Runtime library,一个免费的C语言库，包含一些数据结构和例程，形成一个在不同操作系统之间的可移植层。
// apr-util和apr类似，也是一个包含了数据结构和例程的C语言库，它为apr提供了额外的实用程序接口,
// 包含了对XML, LDAP, database interfaces, URI parsing等的支持


// 下载httpd的tarball源码包及其相关的依赖库
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/httpd/httpd-2.4.38.tar.gz
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/apr/apr-1.6.5.tar.gz
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/apr/apr-util-1.6.1.tar.gz

// 新建独立的程序安装目录
[root@httpd7server ~]# mkdir /app

// 安装
// 构建基础编译环境
[root@httpd7server ~]# yum -y install gcc gcc-c++ autoconf automake

// 安装apr
[root@httpd7server download]# tar -xvf apr-1.6.5.tar.gz
[root@httpd7server download]# cd apr-1.6.5/
[root@httpd7server apr-1.6.5]# ./configure --help
[root@httpd7server apr-1.6.5]# ./configure --prefix=/app/apr
[root@httpd7server apr-1.6.5]# make
[root@httpd7server apr-1.6.5]# make install

// 安装apr-util
[root@httpd7server ~]# yum install expat-devel   #如果不安装,make apr-util时会报错"fatal error: expat.h: No such file or directory"
[root@httpd7server download]# tar -xvf apr-util-1.6.1.tar.gz
[root@httpd7server download]# cd apr-util-1.6.1/
[root@httpd7server apr-util-1.6.1]# ./configure --help
[root@httpd7server apr-util-1.6.1]# ./configure --prefix=/app/apr-util --with-apr=/app/apr
[root@httpd7server apr-util-1.6.1]# make
[root@httpd7server apr-util-1.6.1]# make install

// 安装httpd
[root@httpd7server download]# tar -xvf httpd-2.4.38.tar.gz
[root@httpd7server download]# cd httpd-2.4.38/
[root@httpd7server httpd-2.4.38]# ./configure \
                                     --prefix=/app/httpd \
                                     --with-apr=/app/apr \
                                     --with-apr-util=/app/apr-util \
                                     --enable-so \
                                     --enable-rewrite \
                                     --enable-ssl \
                                     --enable-cgi --enable-cgid \
                                     --enable-modules=most \
                                     --enable-mods-shared=most \
                                     --enable-mpm-shared=all \
                                     --with-mpm=event










