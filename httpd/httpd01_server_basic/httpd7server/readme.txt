

//警告：
//     除非清楚自己在做什么或者就是想要这种效果，否则不要将 'IP-based vhost'
//     与在 VirtualHost指令中用通配符 '*' 指定ip的'name-based vhosts'混用,
//     否则'name-based vhosts'永远无法在与'IP-based vhost'相同的ip:port上对客户端请求
//     进行响应(因为'IP-based vhost'的处理过程总是先于'name-based vhosts')。
//
//虚拟主机的匹配规则见 https://httpd.apache.org/docs/2.4/en/vhosts/details.html


[root@httpd7server ~]# yum -y install httpd
[root@httpd7server ~]# rpm -q httpd
    httpd-2.4.6-88.el7.centos.x86_64

[root@httpd7server ~]# vim /etc/httpd/conf/httpd.conf  #更多具体修改见配置文件
        #启用长连接
        KeepAlive On
        #长连接的超时时间，单位秒；支持ms
        KeepAliveTimeout 5
        #长连接传输文件的次数
        MaxKeepAliveRequests 100

        # 启用memory-mapping内存映射功能,可将部分内核与httpd进程的虚拟的内存地址空间映射到同一块相同的物理内存区域，
        # 减少数据在内核空间与用户空间的拷贝过程，从而提升httpd的性能。
        # https://httpd.apache.org/docs/2.4/en/mod/core.html#enablemmap
        EnableMMAP on
        # 启用内核的sendfile功能，使某些无需httpd进程访问的文件(如static file)可由内核直接发送给客户端，
        # 该功能避免了分离的read和send操作，以及buffer的分配,从而提升httpd的性能。
        # https://httpd.apache.org/docs/2.4/en/mod/core.html#enablesendfile
        EnableSendfile on



虚拟主机
参考：https://www.2daygeek.com/setup-apache-virtual-hosts-on-centos-rhel-fedora/

// 为虚拟主机的配置创建单独的目录
[root@httpd7server ~]# mkdir /etc/httpd/sites-available
[root@httpd7server ~]# mkdir /etc/httpd/sites-enabled

// 创建虚拟主机的配置文件
[root@httpd7server ~]# touch /etc/httpd/sites-available/ip01.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/ip02.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/name01.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/name02.based.com.conf

[root@httpd7server ~]# vim /etc/httpd/conf/httpd.conf
      IncludeOptional sites-enabled/*.conf


// 通过别名为网卡添加额外的ip地址(基于ip的虚拟主机用)
// 临时添加ip的方法
[root@httpd7server ~]# ip addr add 192.168.175.20/24 dev ens33 label 'ens33:0'

// 持久化修改ip的方法
[root@httpd7server ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33:0
      TYPE=Ethernet
      BOOTPROTO=none
      NAME=ens33:0
      DEVICE=ens33:0
      ONBOOT=yes

      IPADDR=192.168.175.20
      PREFIX=24

[root@httpd7server ~]# nmcli conn reload
[root@httpd7server ~]# nmcli conn up ens33

[root@httpd7server ~]# cat /etc/httpd/sites-available/ip01.based.com.conf    #此处省略了 ip02.based.com.conf 的内容
    <VirtualHost 192.168.175.10:80>
        ServerName     ip01.based.com
        DocumentRoot   /var/www/ip01.based.com
        ErrorLog       /var/log/httpd/ip01.based.com/error.log
        CustomLog      /var/log/httpd/ip01.based.com/access.log combined

        <Directory "/var/www/ip01.based.com">
            Require all granted
        </Directory>
    </VirtualHost>

[root@httpd7server ~]# vim /etc/httpd/sites-available/name01.based.com.conf  #此处省略了 name02.based.com.conf 的内容
    <VirtualHost *:80>
        ServerName     name01.based.com
        DocumentRoot   /var/www/name01.based.com
        ErrorLog       /var/log/httpd/name01.based.com/error.log
        CustomLog      /var/log/httpd/name01.based.com/access.log combined

        <Directory "/var/www/name01.based.com">
            Require all granted
        </Directory>
    </VirtualHost>



[root@httpd7server ~]# tree /etc/httpd/sites-available
    /etc/httpd/sites-available
    ├── ip01.based.com.conf
    ├── ip02.based.com.conf
    ├── name01.based.com.conf
    └── name02.based.com.conf



// 创建虚拟主机内容目录
[root@httpd7server ~]# mkdir /var/www/ip01.based.com
[root@httpd7server ~]# mkdir /var/www/ip02.based.com
[root@httpd7server ~]# mkdir /var/www/name01.based.com
[root@httpd7server ~]# mkdir /var/www/name02.based.com

// 创建虚拟主机的日志目录
[root@httpd7server ~]# mkdir /var/log/httpd/ip01.based.com
[root@httpd7server ~]# mkdir /var/log/httpd/ip02.based.com
[root@httpd7server ~]# mkdir /var/log/httpd/name01.based.com
[root@httpd7server ~]# mkdir /var/log/httpd/name02.based.com

// 为虚拟主机创建首页
[root@httpd7server ~]# echo 'ip01.based.com'    >    /var/www/ip01.based.com/index.html
[root@httpd7server ~]# echo 'ip02.based.com'    >    /var/www/ip02.based.com/index.html
[root@httpd7server ~]# echo 'name01.based.com'  >    /var/www/name01.based.com/index.html
[root@httpd7server ~]# echo 'name02.based.com'  >    /var/www/name02.based.com/index.html

// 发布虚拟主机
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/ip01.based.com.conf    /etc/httpd/sites-enabled/ip01.based.com.conf
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/ip02.based.com.conf    /etc/httpd/sites-enabled/ip02.based.com.conf

// 警告：
//     因为我的配置中 ip-based 的虚拟主机和name-based的虚拟主机有冲突
//     (即'<VirtualHost 192.168.175.10:80>' 与'<VirtualHost *:80>'冲突)
//     所以单独测试name-based的虚拟主机时可以先disable掉ip-based的虚拟主机
[root@httpd7server ~]# mv /etc/httpd/sites-enabled/ip01.based.com.conf /etc/httpd/sites-enabled/ip01.based.com.conf.disabled
[root@httpd7server ~]# mv /etc/httpd/sites-enabled/ip02.based.com.conf /etc/httpd/sites-enabled/ip02.based.com.conf.disabled
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/name01.based.com.conf  /etc/httpd/sites-enabled/name01.based.com.conf
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/name02.based.com.conf  /etc/httpd/sites-enabled/name02.based.com.conf

[root@httpd7server ~]# systemctl restart httpd

// 调试虚拟主机配置
[root@httpd7server ~]# httpd -S   # 同 apachectl -S
[root@httpd7server ~]# httpd -t   # 配置文件语法检查
[root@httpd7server ~]# httpd -t -D DUMP_VHOSTS   # 显示虚拟主机
[root@httpd7server ~]# httpd -t -D DUMP_MODULES  # 显示加载的module
[root@httpd7server ~]# httpd -t -D DUMP_VHOSTS -D DUMP_MODULES



客户端测试：
[root@client ~]# vim /etc/hosts
    192.168.175.10           ip01.based.com
    192.168.175.20           ip02.based.com
    192.168.175.10           name02.based.com
    192.168.175.10           name01.based.com

[root@client ~]# curl ip01.based.com
[root@client ~]# curl ip02.based.com
[root@client ~]# curl name01.based.com
[root@client ~]# curl name02.based.com

// 也可以利用 elinks 访问
[root@client ~]# yum -y install elinks
[root@client ~]# elinks ip01.based.com

// windows操作系统可以通过修改文件 C:\Windows\System32\drivers\etc\hosts 来测试


---------------------------------------------------------
// ServerAlias 示例
[root@httpd7server ~]# vim  /etc/httpd/sites-available/www.serveralias.com.conf
    <VirtualHost *:80>
        ServerName     www.serveralias.com
        ServerAlias    demo.serveralias.com serveralias.com
        ServerAlias    *.serveralias.com
        DocumentRoot   /var/www/www.serveralias.com
        ErrorLog       /var/log/httpd/www.serveralias.com/error.log
        CustomLog      /var/log/httpd/www.serveralias.com/access.log combined

        <Directory "/var/www/www.serveralias.com">
            Require all granted
        </Directory>
    </VirtualHost>

[root@httpd7server ~]# mkdir /var/www/www.serveralias.com
[root@httpd7server ~]# mkdir /var/log/httpd/www.serveralias.com
[root@httpd7server ~]# echo 'www.serveralias.com'  >  /var/www/www.serveralias.com/index.html
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/www.serveralias.com.conf  /etc/httpd/sites-enabled/www.serveralias.com.conf

[root@httpd7server ~]# systemctl restart httpd
-----------------------------------------------------------

// Require 指令示例

[root@httpd7server ~]# mkdir -p /var/www/require.demo.com
[root@httpd7server ~]# mkdir -p /var/www/require.demo.com/private_dir
[root@httpd7server ~]# mkdir -p /var/www/require.demo.com/allow_dir_by_ip
[root@httpd7server ~]# mkdir -p /var/www/require.demo.com/allow_dir_except_ip
[root@httpd7server ~]# mkdir -p /var/www/require.demo.com/allow_by_auth

[root@httpd7server ~]# mkdir /var/log/httpd/require.demo.com/

# 警告：如果存放密码的文件已存在，则htpasswd不要再加-c选项了
#    -c     Create the passwdfile. If passwdfile already exists, it is rewritten and truncated.
[root@httpd7server ~]# htpasswd -c /etc/httpd/.webuser Bob  #警告: 只有在创建新密码文件时才能加-c选项
[root@httpd7server ~]# cat /etc/httpd/.webuser
      Bob:$apr1$9.mw4Cy0$9/2gjmBwwqihoar6VOVg6/

[root@httpd7server ~]#  htpasswd  /etc/httpd/.webuser Alice   #警告：这里千万不要再加-c选项了，否则已有数据会被truncated
[root@httpd7server ~]# cat /etc/httpd/.webuser
      Bob:$apr1$9.mw4Cy0$9/2gjmBwwqihoar6VOVg6/
      Alice:$apr1$DmQf49FR$x2k0dlaVvVFe5A/sbRbxm.

[root@httpd7server ~]# ln -s /etc/httpd/sites-available/require.demo.com.conf  /etc/httpd/sites-enabled/require.demo.com.conf
[root@httpd7server ~]# systemctl restart httpd











-----------------------------------------------------------


