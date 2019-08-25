
----------------------------------------------------------------------------------------------------

                                                                            |web01_server-------------------------------------------
                                                                            |    ens33: rip:     192.168.175.121                    |
                                                                            |           gateway: 192.168.175.2                      |
                                                                            |                                                       |
                                                                            |    lo: vip: 192.168.175.100/32->                      |
                      |--------------------------------------------------|  |     (hidden: arp_ignore=1, arp_announce=2)            |
                      |                                                  |  |      注意:一定要先设置好hidden效果, 然后再去配置vip   |
vip: 192.168.175.100  |                                                  |  |                                                       |
                      |   lvs_director01                                 |  |                                                       |
                      |->vip: 192.168.175.100/32(visible, by keepalived) |  |                                                       |
                      |     dip: 192.168.175.101->                       |  |                                                       |
                      |     gateway:192.168.175.2                        |  |                                                       |
                      |                                                  |  |                                                       |
                      |                                                  |->|                                                       |
                      |                                                  |  |                                                       |
                      |                                                  |  |                                         iscsi_share_storage
                      |                                                  |  |                                              ip: 192.168.175.130
                      |                                                  |  |                                                       |
                      |   lvs_director02                                 |  |                                                       |
                      |-> vip: 192.168.175.100/32(visible, by keepalived)|  |                                                       |
                      |     dip: 192.168.175.102->                       |  |                                                       |
                      |     gateway:192.168.175.2                        |  |                                                       |
                      |                                                  |  |                                                       |
                      |--------------------------------------------------|  |                                                       |
                                                                            |----web02_server ---------------------------------------
                                                                                   ens33: rip:     192.168.175.122
                                                                                          gateway: 192.168.175.2

                                                                                     lo: vip: 192.168.175.100/32->
                                                                                         (hidden: arp_ignore=1, arp_announce=2)
                                                                                          注意:一定要先设置好hidden效果, 然后再去配置vip



----------------------------------------------------------------------------------------------------
已经设置好时间同步

----------------------------------------------------------------------------------------------------
使用 Linux 模拟 iSCSI 存储

    参考:
          https://www.thegeekdiary.com/complete-guide-to-configuring-iscsi-in-centos-rhel-7/
          https://www.lisenet.com/2016/iscsi-target-and-initiator-configuration-on-rhel-7/
          https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Storage_Administration_Guide/ch24.html





// 列出 磁盘
[root@iscsi_share_storage ~]# lsblk -p
NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
/dev/sda                      8:0    0   20G  0 disk
├─/dev/sda1                   8:1    0  200M  0 part /boot
└─/dev/sda2                   8:2    0 19.8G  0 part
  ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
  └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
/dev/sdb                      8:16   0    8G  0 disk   <---------------
/dev/sr0                     11:0    1 1024M  0 rom

// 安装 targetcli
[root@iscsi_share_storage ~]# yum -y install targetcli
[root@iscsi_share_storage ~]# systemctl start target
[root@iscsi_share_storage ~]# systemctl enable target

// 执行 targetcli 进入 交互式的管理 shell
// 注: 因为 targetcli 是 storage targets 的 管理shell, 其由自己的目录和命令,
//     其执行命令语法如下:
//       [TARGET_PATH] COMMAND_NAME [OPTIONS]
// 技巧: [tab] 键 可用于 自动补齐 或 提示

[root@iscsi_share_storage ~]# targetcli
/> help   <=========== 执行 help 命令查看帮助

        AVAILABLE COMMANDS
        ==================
        The following commands are available in the
        current path:

          - bookmarks action [bookmark]
          - cd [path]
          - clearconfig [confirm]
          - exit
          - get [group] [parameter...]
          - help [topic]
          - ls [path] [depth]
          - pwd
          - refresh
          - restoreconfig [savefile] [clear_existing]
          - saveconfig [savefile]
          - sessions [action] [sid]
          - set [group] [parameter=value...]
          - status
          - version


/> help help   <============== 执行 help help 命令查看 help 命令的 help

        SYNTAX
        ======
        help [topic]


        DESCRIPTION
        ===========

        Displays the manual page for a topic, or list available topics.


/> ls   <============== 显示 nodes trees
      o- / ......................................................................................................................... [...]
        o- backstores .............................................................................................................. [...]
        | o- block ............(<------ 用于 block 类型的后端存储 的管理)............................................ [Storage Objects: 0]
        | o- fileio ................................................................................................. [Storage Objects: 0]
        | o- pscsi .................................................................................................. [Storage Objects: 0]
        | o- ramdisk ................................................................................................ [Storage Objects: 0]
        o- iscsi ............................................................................................................ [Targets: 0]
        o- loopback ......................................................................................................... [Targets: 0]

/> /backstores/block  <============ [技巧] 和 bash shell 类似, 利用 tab 键可以实现 自动补齐 和 提示
        bookmarks  cd         create     delete     exit       get        help       ls         pwd        refresh    set        status
/> /backstores/block create  <========== [技巧] 和 bash shell 类似, 利用 tab 键可以实现 自动补齐 和 提示
        dev=       name=      readonly=  wwn=

/> /backstores/block create name=disk01 dev=/dev/sdb    <===========定义后端存储
        Created block storage object disk01 using /dev/sdb.

/> ls
      o- / ......................................................................................................................... [...]
        o- backstores .............................................................................................................. [...]
        | o- block .................................................................................................. [Storage Objects: 1]
        | | o- disk01 .....(<------观察)....................................................... [/dev/sdb (8.0GiB) write-thru deactivated]
        | |   o- alua ................................................................................................... [ALUA Groups: 1]
        | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
        | o- fileio ................................................................................................. [Storage Objects: 0]
        | o- pscsi .................................................................................................. [Storage Objects: 0]
        | o- ramdisk ................................................................................................ [Storage Objects: 0]
        o- iscsi ............................................................................................................ [Targets: 0]
        o- loopback ......................................................................................................... [Targets: 0]


/> /iscsi  <========[tab]
      @last      bookmarks  cd         create     delete     exit       get        help       info       ls         pwd        refresh
      set        status     version
/> /iscsi create iqn.2019-08.com.linux:wd-disk   <==========创建共享名称
      Created target iqn.2019-08.com.linux:wd-disk.
      Created TPG 1.
      Global pref auto_add_default_portal=true
      Created default portal listening on all IPs (0.0.0.0), port 3260.


/> ls
    o- / ......................................................................................................................... [...]
      o- backstores .............................................................................................................. [...]
      | o- block .................................................................................................. [Storage Objects: 1]
      | | o- disk01 ......................................................................... [/dev/sdb (8.0GiB) write-thru deactivated]
      | |   o- alua ................................................................................................... [ALUA Groups: 1]
      | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
      | o- fileio ................................................................................................. [Storage Objects: 0]
      | o- pscsi .................................................................................................. [Storage Objects: 0]
      | o- ramdisk ................................................................................................ [Storage Objects: 0]
      o- iscsi ............................................................................................................ [Targets: 1]
      | o- iqn.2019-08.com.linux:wd-disk .......(<--------观察)............................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 0]
      |     o- luns .......................................................................................................... [LUNs: 0]
      |     o- portals .................................................................................................... [Portals: 1]
      |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
      o- loopback ......................................................................................................... [Targets: 0]



/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/luns  <==========[tab]
      @last      bookmarks  cd         create     delete     exit       get        help       ls         pwd        refresh    set
      status
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/luns create  <==========[tab]
      /backstores/block/disk01  anaconda-ks.cfg           add_mapped_luns=          lun=                      storage_object=
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/luns create /backstores/block/disk01  <==========共享名 ---- 后端存储 绑定
      Created LUN 0.
/> ls
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
      | o- iqn.2019-08.com.linux:wd-disk ..................................................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 0]
      |     o- luns .......................................................................................................... [LUNs: 1]
      |     | o- lun0 .................(<--------观察)..................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
      |     o- portals .................................................................................................... [Portals: 1]
      |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
      o- loopback ......................................................................................................... [Targets: 0]





/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/acls  <=========[tab]
      @last      bookmarks  cd         create     delete     exit       get        help       ls         pwd        refresh    set
      status     tag        untag
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/acls create <=========[tab]
      add_mapped_luns=  wwn=
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/acls create iqn.2019-08.com.linux:client  <========= 定义 acl
      Created Node ACL for iqn.2019-08.com.linux:client
      Created mapped LUN 0.
/> ls
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
      | o- iqn.2019-08.com.linux:wd-disk ..................................................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 1]
      |     | o- iqn.2019-08.com.linux:client .......(<--------观察)................................................... [Mapped LUNs: 1]
      |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
      |     o- luns .......................................................................................................... [LUNs: 1]
      |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
      |     o- portals .................................................................................................... [Portals: 1]
      |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
      o- loopback ......................................................................................................... [Targets: 0]



/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals   <=========[tab]
      @last      bookmarks  cd         create     delete     exit       get        help       ls         pwd        refresh    set
      status
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals delete   <=========[tab]
      0.0.0.0      ip_address=  ip_port=
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260   <=========== 删除入口 0.0.0.0:3260
      Deleted network portal 0.0.0.0:3260
/> ls
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
      | o- iqn.2019-08.com.linux:wd-disk ..................................................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 1]
      |     | o- iqn.2019-08.com.linux:client ......................................................................... [Mapped LUNs: 1]
      |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
      |     o- luns .......................................................................................................... [LUNs: 1]
      |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
      |     o- portals ................(<--------观察)..................................................................... [Portals: 0]
      o- loopback ......................................................................................................... [Targets: 0]



/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals create  <===========[tab]
      0.0.0.0                   127.0.0.1                 192.168.175.130           ::0                       ::1
      fe80::20c:29ff:fe52:8e39  ip_address=               ip_port=
/> /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals create ip_address=192.168.175.130   <========创建入口 192.168.175.130:3260
      Using default IP port 3260
      Created network portal 192.168.175.130:3260.
/> ls
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
      | o- iqn.2019-08.com.linux:wd-disk ..................................................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 1]
      |     | o- iqn.2019-08.com.linux:client ......................................................................... [Mapped LUNs: 1]
      |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
      |     o- luns .......................................................................................................... [LUNs: 1]
      |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
      |     o- portals .................................................................................................... [Portals: 1]
      |       o- 192.168.175.130:3260 ......(<--------观察)........................................................................ [OK]
      o- loopback ......................................................................................................... [Targets: 0]

/> exit   <======== 自动保存并退出
    Global pref auto_save_on_exit=true
    Configuration saved to /etc/target/saveconfig.json





   注: 如上所执行的命令还可以用如下 非交互式的方式来执行:
        targetcli /backstores/block create name=disk01 dev=/dev/sdb    #创建 block 类型的后端存储
        targetcli /iscsi create iqn.2019-08.com.linux:wd-disk          #创建 iSCSI target (initiator在login时会对其引用)
        targetcli /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/luns create /backstores/block/disk01  #创建 storage object 的逻辑存储单元
        targetcli /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/acls create iqn.2019-08.com.linux:client  # 创建 initiator 连接用的 ACL
        targetcli /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260  #删除默认的入口
        targetcli /iscsi/iqn.2019-08.com.linux:wd-disk/tpg1/portals create ip_address=192.168.175.130       #创建自定义的入口
        targetcli saveconfig


    注: 对于 使用 targetcli 做的 修改配置, 这些设置在 reboot 之后不会被保留 除非 显示的 调用了 saveconfig 或 通过在
        全局首选项 auto_save_on_exit 为 true 时 退出(exit) 来隐式地调用 saveconfig.
        更多细节 或 注意事项见 `man targetcli`





[root@iscsi_share_storage ~]# targetcli ls
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
      | o- iqn.2019-08.com.linux:wd-disk ..................................................................................... [TPGs: 1]
      |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
      |     o- acls .......................................................................................................... [ACLs: 1]
      |     | o- iqn.2019-08.com.linux:client ......................................................................... [Mapped LUNs: 1]
      |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
      |     o- luns .......................................................................................................... [LUNs: 1]
      |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
      |     o- portals .................................................................................................... [Portals: 1]
      |       o- 192.168.175.130:3260 ............................................................................................. [OK]
      o- loopback ......................................................................................................... [Targets: 0]








----------------------------------------------------------------------------------------------------

[root@web02_server ~]# yum -y install iscsi-initiator-utils



重要:
  https://www.lisenet.com/2016/iscsi-target-and-initiator-configuration-on-rhel-7/
      Note well that on the iSCSI initiator both services are needed.
          The iscsid service is the main service that accesses all configuration files involved.
          The iscsi service is the service that establishes the iSCSI connections.

[root@web02_server ~]# systemctl start iscsi iscsid
[root@web02_server ~]# systemctl enable iscsi iscsid

[root@web02_server ~]# vim /etc/iscsi/initiatorname.iscsi
      InitiatorName=iqn.2019-08.com.linux:client



----------------------------------------------------------------------------------------------------

[root@web01_server ~]# yum install -y iscsi-initiator-utils

[root@web01_server ~]# systemctl start iscsi iscsid
[root@web01_server ~]# systemctl enable iscsi iscsid

[root@web01_server ~]# ls /etc/iscsi/
      initiatorname.iscsi  iscsid.conf

[root@web01_server ~]# vim /etc/iscsi/initiatorname.iscsi
      InitiatorName=iqn.2019-08.com.linux:client

[root@web01_server ~]# iscsiadm -m discovery -t st -p 192.168.175.130:3260
      192.168.175.130:3260,1 iqn.2019-08.com.linux:wd-disk

[root@web02_server ~]# iscsiadm -m node -T iqn.2019-08.com.linux:wd-disk -p 192.168.175.130:3260 -l





----------------------------------------------------------------------------------------------------
[root@web02_server ~]# yum install -y iscsi-initiator-utils


----------------------------------------------------------------------------------------------------
配置 web01_server:

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2

[root@web01_server ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@web01_server ~]# sysctl -p       #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@web01_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@web01_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2

// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@web01_server ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

    IPADDR1=192.168.175.100
    PREFIX1=32


// 使如上 vip 配置生效
[root@web01_server ~]# ifup lo


[root@web01_server ~]# ip addr show lo
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo  <----- 观察
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever


[root@web01_server ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


[root@web01_server ~]# yum -y install httpd
[root@web01_server ~]# systemctl start httpd
[root@web01_server ~]# systemctl enable httpd

[root@web01_server ~]# echo 'web01_server' > /var/www/html/index.html

[root@web01_server ~]# curl http://192.168.175.121:80
    web01_server

----------------------------------------------------------------------------------------------------
配置 web02_server:

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2

[root@web02_server ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@web02_server ~]# sysctl -p       #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@web02_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@web02_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2

// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@web02_server ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

    IPADDR1=192.168.175.100
    PREFIX1=32


// 使如上 vip 配置生效
[root@web02_server ~]# ifup lo


[root@web02_server ~]# ip addr show lo
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever



[root@web02_server ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33



[root@web02_server ~]# yum -y install httpd
[root@web02_server ~]# systemctl start httpd
[root@web02_server ~]# systemctl enable httpd

[root@web02_server ~]# echo 'web02_server' > /var/www/html/index.html

[root@web02_server ~]# curl http://192.168.175.122:80
    web02_server


----------------------------------------------------------------------------------------------------





















