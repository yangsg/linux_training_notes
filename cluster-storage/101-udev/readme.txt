



udev 机制

  在HA集群环境，由于集群中机器的配置不同，可能会导致连接后端存储时，所识别的设备名称不一致；此时，可以通过udev机制实现配置相同的名称



----------------------------------------------------------------------------------------------------
udev 练习环境:

    node01 (ip: 192.168.175.121)
      sda
      sdb ------------------------------>+
                                         |
                                         |-------------------> iscsi target(target01)
                                         |                      (ip: 192.168.175.130)
    node02 (ip: 192.168.175.122)         |
      sda                                |
      sdb                                |
      sdc ------------------------------>+



----------------------------------------------------------------------------------------------------
使用 targetcli 模拟后端存储(或这说是 模拟 SCSI 总线)

为 iscsi server 加一块 8G 的新硬盘, 然后重启.
后续会通过 iscsi 的方式将 这块硬盘共享出去

关于 targetcli 的更多笔记，见
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs/103-keepalived-lvs-dr-iSCSI-demo01
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-storage/099-iscsi-targetcli

网上资料:
  https://www.ibm.com/developerworks/community/blogs/mhhaque/entry/configure_iscsi_target_initiator_on_rhel7_or_powerlinux?lang=en
  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/osm-setting-up-the-challenge-handshake-authentication-protocol
  https://www.mankier.com/8/targetcli

关于设置 authentication 的 userid 和 password 一个要非常注意的地方,
网上许多的示例资料都没有提及, 还好查看 `man targetcli` 可以找到,
这下这段文字摘自 targetcli 的 man page:

     AUTHENTICATION

         Normal Authentication
         Similarly,  the  four parameters userid, password, mutual_userid, and mutual_password are configured via set auth command
         within the TPG node and ACL nodes. However, LIO only uses one or the other, depending  on  the  TPG's  generate_node_acls
         attribute  setting.  If generate_node_acls is 1, the TPG-wide settings will be used. If generate_node_acls is 0, then the
         user-created ACLs' settings will be used.

         Enable generate_node_acls with set attribute generate_node_acls=1 within the TPG node. This can be thought of as  "ignore
         ACLs mode" -- both authentication and LUN mapping will then use the TPG settings.

            所以, generate_node_acls 的 取值不同, 设置 userid 和 password 的 位置也是不同的



// 安装 targetcli
[root@iscsi ~]# yum -y install targetcli
[root@iscsi ~]# rpm -q targetcli
    targetcli-2.1.fb46-7.el7.noarch

[root@iscsi ~]# systemctl start target
[root@iscsi ~]# systemctl enable target


// 列出磁盘信息
[root@iscsi ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk
    ├─/dev/sda1                   8:1    0  200M  0 part /boot
    └─/dev/sda2                   8:2    0 19.8G  0 part
      ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
      └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
    /dev/sdb                      8:16   0    8G  0 disk    <------观察
    /dev/sr0                     11:0    1 1024M  0 rom


// 参考笔记 https://github.com/yangsg/linux_training_notes/tree/master/cluster-storage/099-iscsi-targetcli

[root@iscsi ~]# targetcli /backstores/block create name=disk01 dev=/dev/sdb  #创建 block 类型的后端存储
[root@iscsi ~]# targetcli /iscsi create iqn.2019-09.com.linux:target01       #创建 iSCSI target (initiator在login时会对其引用)
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/luns create /backstores/block/disk01  #创建 storage object 的逻辑存储单元
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls create iqn.2019-09.com.linux:client  #创建 initiator 连接用的 ACL
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260 #删除默认的入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals create ip_address=192.168.175.130      #创建自定义的入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute generate_node_acls=0   #使用 user-created ACLs' settings, 而非 the TPG-wide settings
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute authentication=1       # 启用认证
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls/iqn.2019-09.com.linux:client set auth userid=admin password=redhat #设置用户名和密码
[root@iscsi ~]# targetcli saveconfig   #保存配置



    注: 如果想要 清空所有配置, 可以使用命令: `targetcli clearconfig confirm=True`


// 查看结果信息
[root@iscsi ~]# targetcli ls

      o- / ......................................................................................................................... [...]
        o- backstores .............................................................................................................. [...]
        | o- block .................................................................................................. [Storage Objects: 1]
        | | o- disk01 ........................................................................... [/dev/sdb (8.0GiB) write-thru activated]
        | |   o- alua ................................................................................................... [ALUA Groups: 1]
        | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
        | o- fileio ................................................................................................. [Storage Objects: 0]
        | o- pscsi .................................................................................................. [Storage Objects: 0]
        | o- ramdisk ................................................................................................ [Storage Objects: 0]
        o- iscsi ............................................................................................................ [Targets: 1]
        | o- iqn.2019-09.com.linux:target01 .................................................................................... [TPGs: 1]
        |   o- tpg1 .......................................................................................... [no-gen-acls, auth per-acl]
        |     o- acls .......................................................................................................... [ACLs: 1]
        |     | o- iqn.2019-09.com.linux:client ............................................................. [1-way auth, Mapped LUNs: 1]
        |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
        |     o- luns .......................................................................................................... [LUNs: 1]
        |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
        |     o- portals .................................................................................................... [Portals: 1]
        |       o- 192.168.175.130:3260 ............................................................................................. [OK]
        o- loopback ......................................................................................................... [Targets: 0]





----------------------------------------------------------------------------------------------------
配置 node01

[root@node01 ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk  <---------- 观察, 此时仅有一块磁盘
    ├─/dev/sda1                   8:1    0  200M  0 part /boot
    └─/dev/sda2                   8:2    0 19.8G  0 part
      ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
      └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
    /dev/sr0                     11:0    1 1024M  0 rom



[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# rpm -q iscsi-initiator-utils
    iscsi-initiator-utils-6.2.0.874-10.el7.x86_64

[root@node01 ~]# systemctl start iscsi iscsid
[root@node01 ~]# systemctl enable iscsi iscsid

[root@node01 ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@node01 ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-09.com.linux:client


[root@node01 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat

[root@node01 ~]# systemctl restart iscsid


// 探测后端 iscsi target
[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01

[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] successful.


[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk  <-----观察(多了一块磁盘, /dev/sdb 即对应于通过 iscsi 协议连接的 后端存储)
      /dev/sr0                     11:0    1 1024M  0 rom



----------------------------------------------------------------------------------------------------
配置 node02

为 node02 加一块 8G 硬盘, 并重新启动

[root@node02 ~]# lsblk -p
        NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        /dev/sda                      8:0    0   20G  0 disk
        ├─/dev/sda1                   8:1    0  200M  0 part /boot
        └─/dev/sda2                   8:2    0 19.8G  0 part
          ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
          └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
        /dev/sdb                      8:16   0    8G  0 disk   <------观察, 此为新加的那块硬盘(该硬盘在此例中仅用于占一个名字)
        /dev/sr0                     11:0    1 1024M  0 rom


[root@node02 ~]# yum -y install iscsi-initiator-utils
[root@node02 ~]# rpm -q iscsi-initiator-utils
    iscsi-initiator-utils-6.2.0.874-10.el7.x86_64

[root@node02 ~]# systemctl start iscsi iscsid
[root@node02 ~]# systemctl enable iscsi iscsid

[root@node02 ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@node02 ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-09.com.linux:client


[root@node02 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat

[root@node02 ~]# systemctl restart iscsid


// 探测后端 iscsi target
[root@node02 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01


[root@node02 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] successful.


[root@node02 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk
      /dev/sdc                      8:32   0    8G  0 disk  <-----观察(多了一块磁盘, /dev/sdc 即对应于通过 iscsi 协议连接的 后端存储)
      /dev/sr0                     11:0    1 1024M  0 rom




----------------------------------------------------------------------------------------------------
利用 udev 机制 为 不同 nodes 上连接的 相同的 iscsi target 创建相同的、一致的 设备名


此时 磁盘名称 与 后端 iscsi target 的对应关系如下:

    node01 上: /dev/sdb ---------> iscsi target (iqn.2019-09.com.linux:target01)
    node02 上: /dev/sdc ---------> iscsi target (iqn.2019-09.com.linux:target01)


        man udev
        man udevadm


---------------------
在 node01 上 设置 udev 规则


// 检索后端存储的属性信息
[root@node01 ~]# udevadm info -a --name=/dev/sdb | less

      SUBSYSTEM=="block"
      ATTRS{model}=="disk01          "
      ATTRS{vendor}=="LIO-ORG "




// 编辑udev命令规则文件
[root@node01 ~]# vim /etc/udev/rules.d/100-disk.rules

    SUBSYSTEM=="block",ATTRS{model}=="disk01          ",ATTRS{vendor}=="LIO-ORG ",SYMLINK+="websan"


// 重启 systemd-udev-trigger 服务,是如上规则设置生效
[root@node01 ~]# systemctl restart systemd-udev-trigger.service

// 查看 /dev/websan, 可发现 其为 到 /dev/sdb 的 符号连接文件
[root@node01 ~]# ls -l /dev/websan
      lrwxrwxrwx 1 root root 3 Sep  4 16:34 /dev/websan -> sdb




---------------------
在 node02 上 设置 udev 规则(规则应该与 node01 上对应的规则一致)


[root@node02 ~]# rsync -av root@192.168.175.121:/etc/udev/rules.d/100-disk.rules /etc/udev/rules.d/100-disk.rules

[root@node02 ~]# cat /etc/udev/rules.d/100-disk.rules

    SUBSYSTEM=="block",ATTRS{model}=="disk01          ",ATTRS{vendor}=="LIO-ORG ",SYMLINK+="websan"



// 重启 systemd-udev-trigger 服务,是如上规则设置生效
[root@node02 ~]# systemctl restart systemd-udev-trigger.service


// 查看 /dev/websan, 可发现 其为 到 /dev/sdc 的 符号连接文件
[root@node02 ~]# ls -l /dev/websan
      lrwxrwxrwx 1 root root 3 Sep  4 16:49 /dev/websan -> sdc



--------------------

此时 磁盘名称 与 后端 iscsi target 的对应关系如下:

    node01 上: /dev/websan ----------> /dev/sdb ---------> iscsi target (iqn.2019-09.com.linux:target01)
    node02 上: /dev/websan ----------> /dev/sdc ---------> iscsi target (iqn.2019-09.com.linux:target01)

----------------------------------------------------------------------------------------------------
网上资料:

    https://blog.csdn.net/weixin_41072205/article/details/90408126
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/logical_volume_manager_administration/udev_device_manager







