





                                      vip: 192.168.175.100
        |-----------------------------------------------------------------------------------|
        |                                                                                   |
        |                                                                                   |
        |       +-----------------------------------------------------------------+         |
        |       |                                                                 |         |
        |       |          haproxy01               haproxy02                      |         |
        |       |            ip: 192.168.30.101      ip: 192.168.30.102           |         |
        |       |                                                                 |         |
        |       +------------------------------+----------------------------------+         |
        |                                      |                                            |
        |                                      |                                            |
        |                                      |                                            |
        |                    |----------------------------------|                           |
        |                    |                                  |                           |
        |                    |                                  |                           |
        |                    |                                  |                           |
        |      +----------------------------+      +----------------------------+           |
        |      |    bbs01.linux.com         |      |   blog01.linux.com         |           |
        |      |       ip: 192.168.30.121   |      |      ip: 192.168.30.131    |           |
        |      |                            |      |                            |           |
        |      |    bbs02.linux.com         |      |   blog02.linux.com         |           |
        |      |       ip: 192.168.30.122   |      |      ip: 192.168.30.132    |           |
        |      |                            |      |                            |           |
        |      +----------------------------+      +----------------------------+           |
        |                                                                                   |
        |                                                                                   |
        |-----------------------------------------------------------------------------------|






----------------------------------------------------------------------------------------------------


[root@bbs01 ~]# echo bbs01 > /var/www/html/index.html
[root@bbs02 ~]# echo bbs02 > /var/www/html/index.html
[root@blog01 ~]# echo blog01 > /var/www/html/index.html
[root@blog02 ~]# echo blog02 > /var/www/html/index.html


[root@bbs01 ~]# yum -y install httpd
[root@bbs01 ~]# systemctl start httpd
[root@bbs01 ~]# systemctl enable httpd

[root@bbs02 ~]# yum -y install httpd
[root@bbs02 ~]# systemctl start httpd
[root@bbs02 ~]# systemctl enable httpd

[root@blog01 ~]# yum -y install httpd
[root@blog01 ~]# systemctl start httpd
[root@blog01 ~]# systemctl enable httpd

[root@blog02 ~]# yum -y install httpd
[root@blog02 ~]# systemctl start httpd
[root@blog02 ~]# systemctl enable httpd



[root@client ~]# curl 192.168.30.121
    bbs01
[root@client ~]# curl 192.168.30.122
    bbs02
[root@client ~]# curl 192.168.30.131
    blog01
[root@client ~]# curl 192.168.30.132
    blog02


[root@haproxy01 ~]# yum -y install keepalived ipvsadm haproxy
[root@haproxy02 ~]# yum -y install keepalived ipvsadm haproxy


----------------------------------------------------------------------------------------------------































































