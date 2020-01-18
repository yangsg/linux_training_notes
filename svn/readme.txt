

搭建基于 http 的 svn server 服务的简单示例

// 查看主机信息
[root@svn_server ~]# cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core)

[root@svn_server ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
192.168.175.100/24


part01: 使用 http 协议-----------------------------------------------------------------------------------

// 安装 apache 的 httpd web 服务器
[root@svn_server ~]# yum -y install httpd
[root@svn_server ~]# rpm -q httpd
    httpd-2.4.6-90.el7.centos.x86_64



// 去掉 httpd 自带的默认 welcome page 页
[root@svn_server ~]# mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.bak


    #解决 问题:  httpd: Could not reliably determine the server's fully qualified domain name
    ServerName 127.0.0.1:80

     <Directory "/var/www/html">
         #去掉 Indexes 选项以 禁止 apache 显示 /var/www/html 目录下的内容
         #Options Indexes FollowSymLinks
         Options FollowSymLinks


[root@svn_server ~]# yum -y install subversion mod_dav_svn
[root@svn_server ~]# rpm -q subversion mod_dav_svn
    subversion-1.7.14-14.el7.x86_64
    mod_dav_svn-1.7.14-14.el7.x86_64


[root@svn_server ~]# vim /etc/httpd/conf.modules.d/10-subversion.conf

    # 追加如下内容
    <Location /svn/repos>
    DAV svn
    SVNParentPath /svn/repos
    AuthName "SVN Repos"
    AuthType Basic
    #AuthUserFile 为 HTTP access authentication file
    AuthUserFile /etc/svn/svn-auth
    #AuthzSVNAccessFile 为 user permission control file
    AuthzSVNAccessFile /svn/authz
    Require valid-user
    </Location>


创建仓库;
[root@svn_server ~]# mkdir -p /svn/repos/project-A
[root@svn_server ~]# svnadmin create /svn/repos/project-A
[root@svn_server ~]# ls /svn/repos/project-A
    conf  db  format  hooks  locks  README.txt

[root@svn_server ~]# chown -R apache:apache /svn/repos
[root@svn_server ~]# mkdir /etc/svn
[root@svn_server ~]# htpasswd -cm /etc/svn/svn-auth user001
[root@svn_server ~]# chown root:apache /etc/svn/svn-auth
[root@svn_server ~]# chmod 640 /etc/svn/svn-auth


[root@svn_server ~]# htpasswd -m /etc/svn/svn-auth user002
[root@svn_server ~]# htpasswd -m /etc/svn/svn-auth user003
[root@svn_server ~]# cp /svn/repos/project-A/conf/authz /svn/authz
[root@svn_server ~]# cp /svn/repos/project-A/conf/authz /svn/authz
      [groups]
      admin=user001
      project-A_user=user002
      project-A_trainee=user003

      [/]
      @admin=rw

      [project-A:/]
      @project-A_user=rw
      @project-A_trainee=r



// 启动 httpd 服务并设置为开机自启
[root@svn_server ~]# systemctl start httpd.service
[root@svn_server ~]# systemctl enable httpd.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.

http://192.168.175.100/svn/repos/project-A/

[root@svn_server ~]# mkdir -p /tmp/project-A/{trunk,branches,tags}
[root@svn_server ~]# svn import /tmp/project-A  http://192.168.175.100/svn/repos/project-A -m "Initial import"
[root@svn_server ~]# svn list http://192.168.175.100/svn/repos/project-A
    branches/
    tags/
    trunk/


part02: 使用 https 协议-----------------------------------------------------------------------------------
[root@svn_server ~]# yum -y update openssl
[root@svn_server ~]# rpm -q openssl mod_ssl
    openssl-1.0.2k-19.el7.x86_64
    mod_ssl-2.4.6-90.el7.centos.x86_64


[root@svn_server ~]# vim /etc/httpd/conf.modules.d/10-subversion.conf

      # 追加如下内容
      <Location /svn/repos>
      DAV svn
      SVNParentPath /svn/repos
      AuthName "SVN Repos"
      AuthType Basic
      #AuthUserFile 为 HTTP access authentication file
      AuthUserFile /etc/svn/svn-auth
      #AuthzSVNAccessFile 为 user permission control file
      AuthzSVNAccessFile /svn/authz
      Require valid-user
      #启用 ssl
      SSLRequireSSL
      </Location>

[root@svn_server ~]# mkdir /etc/httpd/ssl
[root@svn_server ~]# openssl genrsa 2048 > /etc/httpd/ssl/svn.key
[root@svn_server ~]# openssl req -new -key /etc/httpd/ssl/svn.key > /etc/httpd/ssl/svn.csr
[root@svn_server ~]# openssl req -x509 -days 3650 -key /etc/httpd/ssl/svn.key -in /etc/httpd/ssl/svn.csr > /etc/httpd/ssl/svn.crt
[root@svn_server ~]# chmod 400 /etc/httpd/ssl/*
[root@svn_server ~]# ls -l /etc/httpd/ssl/*
    -r-------- 1 root root 1326 Jan 18 19:32 /etc/httpd/ssl/svn.crt
    -r-------- 1 root root 1009 Jan 18 19:10 /etc/httpd/ssl/svn.csr
    -r-------- 1 root root 1675 Jan 18 19:07 /etc/httpd/ssl/svn.key


[root@svn_server ~]# vim /etc/httpd/conf.d/ssl.conf
  SSLCertificateFile /etc/httpd/ssl/svn.crt
  SSLCertificateKeyFile /etc/httpd/ssl/svn.key

[root@svn_server ~]# systemctl restart httpd

// 使用 http 协议访问, 访问失败, 这是预期效果
[root@client ~]# svn list http://192.168.175.100/svn/repos/project-A
    svn: E175013: Unable to connect to a repository at URL 'http://192.168.175.100/svn/repos/project-A'
    svn: E175013: Access to 'http://192.168.175.100/svn/repos/project-A' forbidden

// 使用 https 访问, 预期能够成功
[root@client ~]# svn list https://192.168.175.100/svn/repos/project-A





----------------------------------------------------------------------------------------------------
网上参考资料:
    https://www.vultr.com/docs/how-to-setup-an-apache-subversion-svn-server-on-centos-7
    https://www.server-world.info/en/note?os=CentOS_7&p=subversion&f=1
    https://www.server-world.info/en/note?os=CentOS_7&p=subversion&f=4
    https://www.howtoforge.com/tutorial/subversion-svn-with-apache-and-letsencrypt-on-centos/
    https://www.jianshu.com/p/8b9dc27dc4a0



其他:
    http://gmatcentral.org/display/GW/SVN+and+Git+Command+Mappings


    https://www.visualsvn.com/
    https://www.visualsvn.com/server/
    https://www.cnblogs.com/kinwing/p/11093843.html



