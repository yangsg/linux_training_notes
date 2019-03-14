
参考：
https://opsech.io/posts/2016/Jan/26/nfsv4-only-on-centos-72.html
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/nfs-serverconfig
https://help.ubuntu.com/community/NFSv4Howto

服务器端：
基本信息
[root@ntf4server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@ntf4server ~]# uname -r
    3.10.0-693.el7.x86_64


[root@ntf4server ~]# yum install nfs-utils
[root@ntf4server ~]# rpm -q nfs-utils
    nfs-utils-1.3.0-0.61.el7.x86_64

[root@ntf4server ~]# vim /etc/sysconfig/nfs

    RPCNFSDARGS="-N 2 -N 3 -U"
    # -u is optional, disables UDP
    RPCMOUNTDOPTS="-N 2 -N 3 -u"

[root@ntf4server ~]# cat /run/sysconfig/nfs-utils   #确认该文件是否为如下内容，如果不是，可命令`systemctl restart nfs-config`后再确认一次
    RPCNFSDARGS="-N 2 -N 3 -U 8"
    RPCMOUNTDARGS="-N 2 -N 3 -u"

[root@ntf4server ~]# systemctl mask --now rpc-statd.service rpcbind.service rpcbind.socket
[root@ntf4server ~]# systemctl is-active rpc-statd.service rpcbind.service rpcbind.socket

[root@ntf4server ~]# systemctl start nfs-server
[root@ntf4server ~]# systemctl enable nfs-server

[root@ntf4server ~]# netstat -anptu | grep 2049
[root@ntf4server ~]# netstat -aptu  | grep nfs

// 准备目录 /nfs4_share/data 并导出共享
[root@ntf4server ~]# mkdir -p /nfs4_share/data
[root@ntf4server ~]# vim /etc/exports


[root@ntf4server ~]# exportfs -rav


客户端：
[root@nfs4client ~]# yum -y install nfs-utils

[root@nfs4client ~]# mkdir /data
[root@nfs4client ~]# mount -t nfs4 -o proto=tcp,port=2049  192.168.175.111:/nfs4_share/data  /data

// 设置开机自动挂载
[root@nfs4client ~]# vim /etc/fstab
192.168.175.111:/nfs4_share/data  /data         nfs4    defaults,proto=tcp,port=2049  0 0

[root@nfs4client ~]# mount -a











