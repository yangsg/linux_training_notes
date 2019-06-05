

协议: SMB/CIFS

端口:
    smb   tcp/139   tcp/445
    nmb   udp/137   udp/138

[root@sambaserver ~]# yum -y install samba

[root@sambaserver ~]# rpm -q samba
    samba-4.8.3-4.el7.x86_64


[root@sambaserver ~]# vim /etc/samba/smb.conf



网上资料:
    https://linuxhint.com/install_samba_centos7/


    http://www.ubiqx.org/cifs/

man samba
man 5 smb.conf



