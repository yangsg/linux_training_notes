


[root@host ~]# virt-install \
  --name vm-base-centos7.4-64 \
  --graphics vnc,listen=0.0.0.0,port=5920,keymap=en_us \
  --memory 512,maxmemory=1024 \
  --vcpus 1,maxvcpus=2 \
  --disk path=/var/lib/libvirt/images/vm-base-centos7.4-64.qcow2,size=8,format=qcow2 \
  --network bridge=virbr0 \
  --cdrom /tmp/CentOS-7.4-x86_64-Everything-1708.iso


[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0

    DEVICE=eth0
    NAME=eth0
    TYPE=Ethernet
    BOOTPROTO=none
    ONBOOT=yes

[root@localhost ~]# vim /etc/ssh/sshd_config

        GSSAPIAuthentication no
        UseDNS no

合理的初始化基本的环境:
    安装好相关的软件, 配置好相关的配置 (如关闭防火墙 和 selinux, 备份设置好 yum源 等等)



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



// 编写脚本 (该脚本仅是一个简单示例, 还并不友好和完美)
[root@host ~]# vim /opt/kvm-templates/centos7.4/kvm.sh
     具体内容见:
        https://github.com/yangsg/linux_training_notes/blob/master/kvm/10-template-make-and-apply/opt/kvm-templates/centos7.4/kvm.sh


[root@host ~]# chattr +i /opt/kvm-templates/centos7.4/kvm.sh
[root@host ~]# lsattr /opt/kvm-templates/centos7.4/kvm.sh
      ----i----------- /opt/kvm-templates/centos7.4/kvm.sh


// 执行 脚本创建 2 台 Guest 虚拟机
[root@host ~]# bash /opt/kvm-templates/centos7.4/kvm.sh
虚拟机数量: 2
2

// 启动虚拟机
[root@host ~]# virsh start centos_1
      Domain centos_1 started

// 连接虚拟机
[root@host ~]# ssh root@192.168.122.10



