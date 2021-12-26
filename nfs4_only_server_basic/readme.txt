
参考：
https://opsech.io/posts/2016/Jan/26/nfsv4-only-on-centos-72.html
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/nfs-serverconfig
https://help.ubuntu.com/community/NFSv4Howto

服务器端：
基本信息
[root@nfs4server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@nfs4server ~]# uname -r
    3.10.0-693.el7.x86_64


[root@nfs4server ~]# yum -y install nfs-utils
[root@nfs4server ~]# rpm -q nfs-utils
    nfs-utils-1.3.0-0.61.el7.x86_64

[root@nfs4server ~]# vim /etc/sysconfig/nfs

    # man nfsd   # -N 2 -N 3: 告诉 rpc.nfsd 不提供版本 2 和 版本 3 的服务。-U: 指示内核 nfs 服务器不要打开和监听 UDP 套接字 
    RPCNFSDARGS="-N 2 -N 3 -U"
    # -u is optional, disables UDP
    RPCMOUNTDOPTS="-N 2 -N 3 -u"

[root@nfs4server ~]# systemctl restart nfs-config
[root@nfs4server ~]# cat /run/sysconfig/nfs-utils   #确认 /etc/sysconfig/nfs 中的修改是否生效
    RPCNFSDARGS="-N 2 -N 3 -U 8"
    RPCMOUNTDARGS="-N 2 -N 3 -u"

[root@nfs4server ~]# systemctl mask --now rpc-statd.service rpcbind.service rpcbind.socket
[root@nfs4server ~]# systemctl is-active rpc-statd.service rpcbind.service rpcbind.socket

[root@nfs4server ~]# systemctl start nfs-server
[root@nfs4server ~]# systemctl enable nfs-server

[root@nfs4server ~]# netstat -anptu | grep 2049
[root@nfs4server ~]# netstat -aptu  | grep nfs

// 准备目录 /nfs4_share/data 并导出共享
[root@nfs4server ~]# mkdir -p /nfs4_share/data
[root@nfs4server ~]# vim /etc/exports

      # man 5 exports   #/EXAMPLE
      # exportfs -rav   #man exportfs  #/EXAMPLES

      # 注意给目录 /nfs4_share/data/ 合适的权限,包括mount磁盘时提供合适的options
      /nfs4_share/data/  192.168.175.10(rw,sync,no_root_squash)  192.168.2.0/24(rw,root_squash,anonuid=150,anongid=100)



[root@nfs4server ~]# exportfs -rav


客户端：
[root@nfs4client ~]# yum -y install nfs-utils

[root@nfs4client ~]# mkdir /data
[root@nfs4client ~]# mount -t nfs4 -o proto=tcp,port=2049  192.168.175.111:/nfs4_share/data  /data

// 设置开机自动挂载
[root@nfs4client ~]# vim /etc/fstab
192.168.175.111:/nfs4_share/data  /data         nfs4    defaults,proto=tcp,port=2049  0 0

[root@nfs4client ~]# mount -a











