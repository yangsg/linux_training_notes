

mutipath多路径
  作用：通过双线连接后端存储实现线路的备份

  出现问题：
    在FC SAN中，多路径会导致前端的应用服务器在本地映射出多块磁盘


        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/dm_multipath/mpio_overview
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/dm_multipath/mpio_setup
        https://www.thegeekdiary.com/beginners-guide-to-device-mapper-dm-multipathing/



    node01 ------------------------> iscsi
    ens33: 192.168.175.121           ens33: 192.168.175.130
                                     ens37: 192.168.175.140



----------------------------------------------------------------------------------------------------

为 iscsi server 加一块 8G 的新硬盘, 然后重启.
后续会通过 iscsi 的方式将 这块硬盘共享出去

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
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals create ip_address=192.168.175.140      #创建自定义的入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute generate_node_acls=0   #使用 user-created ACLs' settings, 而非 the TPG-wide settings
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute authentication=1       # 启用认证
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls/iqn.2019-09.com.linux:client set auth userid=admin password=redhat #设置用户名和密码
[root@iscsi ~]# targetcli saveconfig   #保存配置


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
        |     o- portals .................................................................................................... [Portals: 2]
        |       o- 192.168.175.130:3260 ............................................................................................. [OK]
        |       o- 192.168.175.140:3260 ............................................................................................. [OK]
        o- loopback ......................................................................................................... [Targets: 0]




----------------------------------------------------------------------------------------------------
在 node01 准备  多路径练习环境


[root@node01 ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk
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


[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01
      192.168.175.140:3260,1 iqn.2019-09.com.linux:target01

[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.140
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01
      192.168.175.140:3260,1 iqn.2019-09.com.linux:target01


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
      /dev/sdb                      8:16   0    8G  0 disk   <----------观察
      /dev/sr0                     11:0    1 1024M  0 rom

[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.140:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.140,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.140,3260] successful.


[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk
      /dev/sdc                      8:32   0    8G  0 disk   <-----------观察
      /dev/sr0                     11:0    1 1024M  0 rom


此时的磁盘设备名 对应情况:

          /dev/sdb  --------------------------> iscsi target (target01)
          /dev/sdc  --------------------------> iscsi target (target01)






----------------------------------------------------------------------------------------------------
在 node01 上 解决处理 多路径问题




[root@node01 ~]# yum -y install device-mapper-multipath
[root@node01 ~]# rpm -q device-mapper-multipath
      device-mapper-multipath-0.4.9-123.el7.x86_64



[root@node01 ~]# rpm -ql device-mapper-multipath
      /etc/multipath
      /usr/lib/systemd/system/multipathd.service
      /usr/lib/udev/rules.d/11-dm-mpath.rules
      /usr/lib/udev/rules.d/62-multipath.rules
      /usr/sbin/mpathconf
      /usr/sbin/mpathpersist
      /usr/sbin/multipath
      /usr/sbin/multipathd
      /usr/share/doc/device-mapper-multipath-0.4.9
      /usr/share/doc/device-mapper-multipath-0.4.9/AUTHOR
      /usr/share/doc/device-mapper-multipath-0.4.9/COPYING
      /usr/share/doc/device-mapper-multipath-0.4.9/FAQ
      /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf
      /usr/share/man/man5/multipath.conf.5.gz
      /usr/share/man/man8/mpathconf.8.gz
      /usr/share/man/man8/mpathpersist.8.gz
      /usr/share/man/man8/multipath.8.gz
      /usr/share/man/man8/multipathd.8.gz



[root@node01 ~]# vim /etc/multipath.conf

      defaults {
          user_friendly_names no
      }

      blacklist {
          devnode "sda"
      }

[root@node01 ~]# systemctl start multipathd
[root@node01 ~]# systemctl enable multipathd



[root@node01 ~]# multipath -ll
      360014050b4a1dd902b14ef49a4128130 dm-2 LIO-ORG ,disk01
      size=8.0G features='0' hwhandler='0' wp=rw
      |-+- policy='service-time 0' prio=1 status=active
      | `- 6:0:0:0 sdb 8:16 active ready running
      `-+- policy='service-time 0' prio=1 status=enabled
        `- 7:0:0:0 sdc 8:32 active ready running


[root@node01 ~]# lsblk -p
      NAME                                            MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
      /dev/sda                                          8:0    0   20G  0 disk
      ├─/dev/sda1                                       8:1    0  200M  0 part  /boot
      └─/dev/sda2                                       8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root                     253:0    0 17.8G  0 lvm   /
        └─/dev/mapper/centos-swap                     253:1    0    2G  0 lvm   [SWAP]
      /dev/sdb                                          8:16   0    8G  0 disk
      └─/dev/mapper/360014050b4a1dd902b14ef49a4128130 253:2    0    8G  0 mpath  <--------观察
      /dev/sdc                                          8:32   0    8G  0 disk
      └─/dev/mapper/360014050b4a1dd902b14ef49a4128130 253:2    0    8G  0 mpath  <--------观察
      /dev/sr0                                         11:0    1 1024M  0 rom


[root@node01 ~]# ls -l /dev/mapper/360014050b4a1dd902b14ef49a4128130
      lrwxrwxrwx 1 root root 7 Sep  4 18:48 /dev/mapper/360014050b4a1dd902b14ef49a4128130 -> ../dm-2


[root@node01 ~]# ls -l /dev/dm-2
      brw-rw---- 1 root disk 253, 2 Sep  4 18:48 /dev/dm-2





















