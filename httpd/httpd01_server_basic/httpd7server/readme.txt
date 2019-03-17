

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

// 禁用httpd自带的测试页
[root@httpd7server ~]# mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.disable

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

[root@httpd7server ~]# vim /etc/httpd/sites-available/require.demo.com.conf
      <VirtualHost *:80>
      # warning:
      #     don't use 'ip-based vhosts'(eg: <VirtualHost 192.168.175.10:80>) together with the 'name-based vhosts' of which
      #     ip specified by wildcard '*'(eg: <VirtualHost *:80>), becase
      #     Name-based virtual hosting is a process applied after the server has selected the best matching IP-based virtual host.
      #     and
      #     the wildcard (*) matches are considered only when there are no exact matches for the address and port.
      #     otherwise, your 'name-based vhosts'(eg: <VirtualHost *:80>) will never serve the client on the same ip:port as the
      #     'ip-based vhosts'(eg: <VirtualHost 192.168.175.10:80>)
      # for more details: https://httpd.apache.org/docs/2.4/en/vhosts/details.html
          ServerName     require.demo.com
          DocumentRoot   /var/www/require.demo.com
          ErrorLog       /var/log/httpd/require.demo.com/error.log
          CustomLog      /var/log/httpd/require.demo.com/access.log combined

      # https://httpd.apache.org/docs/2.4/en/mod/mod_authz_core.html#require
          <Directory "/var/www/require.demo.com">
              Require all granted
          </Directory>

          <Directory "/var/www/require.demo.com/private_dir">
              Require all denied
          </Directory>

          <Directory "/var/www/require.demo.com/allow_dir_by_ip">
              Require ip 192.168.175.20
          </Directory>

          <Directory "/var/www/require.demo.com/allow_dir_except_ip">
              <RequireAll>
                Require all granted
                Require not ip 192.168.175.44
              </RequireAll>
          </Directory>

#警告：
#  htpasswd 的 -c 选项只能第一次在创建密码文件时使用，否则会truncate现有的密码文件内容
# [root@httpd7server ~]# htpasswd -c /etc/httpd/.webuser Bob
# [root@httpd7server ~]# htpasswd    /etc/httpd/.webuser Alice  #此处不能再使用-c选项
          <Directory "/var/www/require.demo.com/allow_by_auth">
              AuthType Basic
              AuthName "Need to Login: "
              AuthUserFile "/etc/httpd/.webuser"
              Require valid-user
          </Directory>

      </VirtualHost>




[root@httpd7server ~]# ln -s /etc/httpd/sites-available/require.demo.com.conf  /etc/httpd/sites-enabled/require.demo.com.conf
[root@httpd7server ~]# systemctl restart httpd



-----------------------------------------------------------

# https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
# https://www.digitalocean.com/community/tutorials/how-to-create-an-ssl-certificate-on-apache-for-centos-7
# https://www.sslshopper.com/article-how-to-create-and-install-an-apache-self-signed-certificate.html
# https://www.linode.com/docs/security/ssl/ssl-apache2-centos/


https 示例


服务器端
[root@httpd7server ~]# yum -y install mod_ssl
[root@httpd7server ~]# rpm -q mod_ssl
      mod_ssl-2.4.6-88.el7.centos.x86_64

[root@httpd7server ~]# ls /etc/httpd/modules/ | grep mod_ssl.so
[root@httpd7server ~]# cat /etc/httpd/conf.modules.d/00-ssl.conf
      LoadModule ssl_module modules/mod_ssl.so

// man httpd
//      -M     Dump a list of loaded Static and Shared Modules.
[root@httpd7server ~]# httpd -M | grep ssl
[root@httpd7server ~]# apachectl -M | grep ssl


// 生成密钥
[root@httpd7server ~]# mkdir /etc/httpd/ssl
[root@httpd7server ~]# openssl genrsa 1024 > /etc/httpd/ssl/ssl.com.key

// 生成证书请求文件
[root@httpd7server ~]# openssl req -new -key /etc/httpd/ssl/ssl.com.key > /etc/httpd/ssl/ssl.com.csr
            You are about to be asked to enter information that will be incorporated
            into your certificate request.
            What you are about to enter is what is called a Distinguished Name or a DN.
            There are quite a few fields but you can leave some blank
            For some fields there will be a default value,
            If you enter '.', the field will be left blank.
            -----
            Country Name (2 letter code) [XX]:cn
            State or Province Name (full name) []:cn
            Locality Name (eg, city) [Default City]:bj
            Organization Name (eg, company) [Default Company Ltd]:ssl
            Organizational Unit Name (eg, section) []:ssl
            Common Name (eg, your name or your server's hostname) []:www.ssl.com
            Email Address []:12345@qq.com

            Please enter the following 'extra' attributes
            to be sent with your certificate request
            A challenge password []:
            An optional company name []:



// 颁发证书 (自签名证书)
[root@httpd7server ~]#  openssl req -x509 -days 365 -key /etc/httpd/ssl/ssl.com.key -in /etc/httpd/ssl/ssl.com.csr > /etc/httpd/ssl/ssl.com.crt
[root@httpd7server ~]# ls /etc/httpd/ssl/
      ssl.com.crt  ssl.com.csr  ssl.com.key

[root@httpd7server ~]# chmod 400 /etc/httpd/ssl/*
[root@httpd7server ~]# ls -l /etc/httpd/ssl/*
      -r-------- 1 root root 1005 Mar 17 17:09 /etc/httpd/ssl/ssl.com.crt
      -r-------- 1 root root  672 Mar 17 17:06 /etc/httpd/ssl/ssl.com.csr
      -r-------- 1 root root  887 Mar 17 17:01 /etc/httpd/ssl/ssl.com.key


[root@httpd7server ~]# mkdir /var/www/www.ssl.com
[root@httpd7server ~]# mkdir /var/log/httpd/www.ssl.com

[root@httpd7server ~]# vim /etc/httpd/sites-available/www.ssl.com.conf
      <VirtualHost *:443>
      # https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html
          SSLEngine On
          SSLCertificateFile      /etc/httpd/ssl/ssl.com.crt
          SSLCertificateKeyFile   /etc/httpd/ssl/ssl.com.key

          ServerAdmin    info@ssl.com
          ServerName     www.ssl.com
          ServerAlias    ssl.com
          ServerAlias    *.ssl.com
          DocumentRoot   /var/www/www.ssl.com
          ErrorLog       /var/log/httpd/www.ssl.com/error.log
          CustomLog      /var/log/httpd/www.ssl.com/access.log combined

          <Directory "/var/www/www.ssl.com">
              Require all granted
          </Directory>
      </VirtualHost>


[root@httpd7server ~]# ln -s /etc/httpd/sites-available/www.ssl.com.conf  /etc/httpd/sites-enabled/www.ssl.com.conf

[root@httpd7server ~]# systemctl restart httpd

禁用默认的httpd自带的默认ssl virtualhost
[root@httpd7server ~]# cp /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.bak
[root@httpd7server ~]# vim /etc/httpd/conf.d/ssl.conf   #删除其中的虚拟主机部分

[root@httpd7server ~]# systemctl restart httpd



客户端:

[root@client ~]# vim /etc/hosts
    192.168.175.10   www.ssl.com
    192.168.175.10   ssl.com
    192.168.175.10   web.ssl.com


[root@client ~]# curl --insecure https://www.ssl.com
[root@client ~]# curl --insecure https://ssl.com
[root@client ~]# curl --insecure https://web.ssl.com

[root@client ~]# wget --no-check-certificate https://www.ssl.com




-------------------------------------------------

php 示例

[root@httpd7server ~]# yum -y install php
[root@httpd7server ~]# ls /etc/httpd/modules/ | grep libphp5.so
[root@httpd7server ~]# cat /etc/httpd/conf.modules.d/10-php.conf
      #
      # PHP is an HTML-embedded scripting language which attempts to make it
      # easy for developers to write dynamically generated webpages.
      #
      <IfModule prefork.c>
        LoadModule php5_module modules/libphp5.so
      </IfModule>

[root@httpd7server ~]# mkdir /var/www/php.demo.com
[root@httpd7server ~]# mkdir /var/log/httpd/php.demo.com
[root@httpd7server ~]# vim /etc/httpd/sites-available/php.demo.com.conf
      <VirtualHost *:80>
      # warning:
      #     don't use 'ip-based vhosts'(eg: <VirtualHost 192.168.175.10:80>) together with the 'name-based vhosts' of which
      #     ip specified by wildcard '*'(eg: <VirtualHost *:80>), becase
      #     Name-based virtual hosting is a process applied after the server has selected the best matching IP-based virtual host.
      #     and
      #     the wildcard (*) matches are considered only when there are no exact matches for the address and port.
      #     otherwise, your 'name-based vhosts'(eg: <VirtualHost *:80>) will never serve the client on the same ip:port as the
      #     'ip-based vhosts'(eg: <VirtualHost 192.168.175.10:80>)
      # for more details: https://httpd.apache.org/docs/2.4/en/vhosts/details.html
          ServerName     php.demo.com
          DocumentRoot   /var/www/php.demo.com
          ErrorLog       /var/log/httpd/php.demo.com/error.log
          CustomLog      /var/log/httpd/php.demo.com/access.log combined

          <Directory "/var/www/php.demo.com">
              Require all granted
          </Directory>
      </VirtualHost>


[root@httpd7server ~]# vim /var/www/php.demo.com/test.php
    <?php
      phpinfo();
    ?>

[root@httpd7server ~]# ln -s /etc/httpd/sites-available/php.demo.com.conf  /etc/httpd/sites-enabled/php.demo.com.conf
[root@httpd7server ~]# systemctl restart httpd


客户端：
浏览器访问     http://php.demo.com/test.php









