


[root@host ~]# virt-install \
  --name vm-base-centos7.4-64 \
  --graphics vnc,listen=0.0.0.0,port=5920,keymap=en_us \
  --memory 512,maxmemory=1024 \
  --vcpus 1,maxvcpus=2 \
  --disk path=/var/lib/libvirt/images/vm-base-centos7.4-64.qcow2,size=8,format=qcow2 \
  --network bridge=virbr0 \
  --cdrom /tmp/CentOS-7.4-x86_64-Everything-1708.iso


[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0

    DEVICE=ens33
    NAME=ens33
    TYPE=Ethernet
    BOOTPROTO=dhcp
    ONBOOT=yes

[root@localhost ~]# vim /etc/ssh/sshd_config

        GSSAPIAuthentication no
        UseDNS no



[root@host ~]# virsh list --all
 Id    Name                           State
----------------------------------------------------
 -     vm-base-centos7.4-64           shut off


[root@host ~]# mkdir -p /opt/kvm-templates/centos7.4

// copy Guest virtual machine 的 配置文件 和 将想文件作为模板
[root@host ~]# cp /etc/libvirt/qemu/vm-base-centos7.4-64.xml  /opt/kvm-templates/centos7.4/
[root@host ~]# cp /var/lib/libvirt/images/vm-base-centos7.4-64.qcow2  /opt/kvm-templates/centos7.4/

[root@host ~]# chmod 644 /opt/kvm-templates/centos7.4/vm-base-centos7.4-64.qcow2
[root@host ~]# chattr +i /opt/kvm-templates/centos7.4/*
[root@host ~]# lsattr /opt/kvm-templates/centos7.4/*
    ----i----------- /opt/kvm-templates/centos7.4/vm-base-centos7.4-64.qcow2
    ----i----------- /opt/kvm-templates/centos7.4/vm-base-centos7.4-64.xml







