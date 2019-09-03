

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/logical_volume_manager_administration/udev_device_manager


udev 机制

  在HA集群环境，由于集群中机器的配置不同，可能会导致连接后端存储时，所识别的设备名称不一致；此时，可以通过udev机制实现配置相同的名称



----------------------------------------------------------------------------------------------------
udev 练习环境:

    node01
      sda
      sdb ------------------------------>+
                                         |
                                         |-------------------> iscsi target(wd-disk)
                                         |
    node02                               |
      sda                                |
      sdb                                |
      sdc ------------------------------>+



----------------------------------------------------------------------------------------------------
使用 targetcli 模拟后端存储(或这说是 模拟 SCSI 总线)

为 iscsi server 加一块 8G 的新硬盘, 然后重启.
后续会通过 iscsi 的方式将 这块硬盘共享出去

关于 targetcli 的更多笔记，见
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs/103-keepalived-lvs-dr-iSCSI-demo01

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
    /dev/sdb                      8:16   0    8G  0 disk   <------观察
    /dev/sr0                     11:0    1 1024M  0 rom




[root@iscsi ~]# targetcli /backstores/block create name=disk01 dev=/dev/sdb    #创建 block 类型的后端存储
    Created block storage object disk01 using /dev/sdb.

[root@iscsi ~]# targetcli /iscsi create iqn.2019-09.com.linux:wd-disk          #创建 iSCSI target (initiator在login时会对其引用)
    Created target iqn.2019-09.com.linux:wd-disk.
    Created TPG 1.
    Global pref auto_add_default_portal=true
    Created default portal listening on all IPs (0.0.0.0), port 3260.

[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:wd-disk/tpg1/luns create /backstores/block/disk01  #创建 storage object 的逻辑存储单元
    Created LUN 0.

[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:wd-disk/tpg1/acls create iqn.2019-09.com.linux:client  # 创建 initiator 连接用的 ACL
    Created Node ACL for iqn.2019-09.com.linux:client
    Created mapped LUN 0.

[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:wd-disk/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260  #删除默认的入口
    Deleted network portal 0.0.0.0:3260

[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:wd-disk/tpg1/portals create ip_address=192.168.175.130  #创建自定义的入口
    Using default IP port 3260
    Created network portal 192.168.175.130:3260.

[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:wd-disk/tpg1/ set auth userid=admin password=redhat     # 设置基于 username 和 password 认证
    Parameter password is now 'redhat'.
    Parameter userid is now 'admin'.

[root@iscsi ~]# targetcli saveconfig
    Last 10 configs saved in /etc/target/backup/.
    Configuration saved to /etc/target/saveconfig.json

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
        | o- iqn.2019-09.com.linux:wd-disk ..................................................................................... [TPGs: 1]
        |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
        |     o- acls .......................................................................................................... [ACLs: 1]
        |     | o- iqn.2019-09.com.linux:client ......................................................................... [Mapped LUNs: 1]
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


[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:wd-disk








































