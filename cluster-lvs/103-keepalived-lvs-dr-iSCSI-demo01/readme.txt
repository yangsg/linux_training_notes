
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
配置 web01_server (与 iscsi 相关)


[root@web01_server ~]# yum -y install iscsi-initiator-utils

[root@web01_server ~]# systemctl start iscsi iscsid
[root@web01_server ~]# systemctl enable iscsi iscsid

[root@web01_server ~]# ls /etc/iscsi/
      initiatorname.iscsi  iscsid.conf


  重要:
    iscsid.service 和 iscsi.service 的作用:
      https://www.lisenet.com/2016/iscsi-target-and-initiator-configuration-on-rhel-7/
        Note well that on the iSCSI initiator both services are needed.
            The iscsid service is the main service that accesses all configuration files involved.
            The iscsi service is the service that establishes the iSCSI connections.


// 配置 InitiatorName
// 注: 修改了 文件 /etc/iscsi/iscsid.conf 或 /etc/iscsi/initiatorname.iscsi 后 一定要 restart iscsid 其修改的配置才会生效.
//     更多详细见 `man iscsid`
[root@web01_server ~]# vim /etc/iscsi/initiatorname.iscsi
      InitiatorName=iqn.2019-08.com.linux:client


          注: 如下就是修改 /etc/iscsi/initiatorname.iscsi 后 没有 restart iscsid.service 时 login 时报的错误信息:
          https://unix.stackexchange.com/questions/207534/iscsi-login-failed-with-error-24-could-not-log-in-to-all-portals
            iscsiadm -m node -T iqn.2019-08.com.linux:wd-disk -p 192.168.175.130:3260 -l

                Logging in to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260] (multiple)
                iscsiadm: Could not login to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260].
                iscsiadm: initiator reported error (24 - iSCSI login failed due to authorization failure) <---- 注意这里
                iscsiadm: Could not log into all portals

// 重新启动 iscsid
// 注: 修改了 文件 /etc/iscsi/iscsid.conf 或 /etc/iscsi/initiatorname.iscsi 后 一定要 restart iscsid 其修改的配置才会生效.
//     更多详细见 `man iscsid`
[root@web01_server ~]# systemctl restart iscsid


// 探测(Discover) target
[root@web01_server ~]# iscsiadm -m discovery -t st -p 192.168.175.130:3260
      192.168.175.130:3260,1 iqn.2019-08.com.linux:wd-disk

// 登录 target (Log in to the target with the target IQN)
[root@web01_server ~]# iscsiadm -m node -T iqn.2019-08.com.linux:wd-disk -p 192.168.175.130:3260 -l
      Logging in to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260] (multiple)
      Login to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260] successful.

      如上命令等价于: (更多示例见 `man iscsiadm  #/^EXAMPLES`)
        iscsiadm --mode node --targetname iqn.2019-08.com.linux:wd-disk --portal 192.168.175.130:3260 --login


// 列出块设备
[root@web01_server ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk  <------ 观察
      /dev/sr0                     11:0    1 1024M  0 rom



[root@web01_server ~]# yum -y install gdisk

[root@web01_server ~]# parted /dev/sdb print   # 使用 parted 命令查看分区表 信息(如类型, 是否存在...)
      Error: /dev/sdb: unrecognised disk label
      Model: LIO-ORG disk01 (scsi)
      Disk /dev/sdb: 8590MB
      Sector size (logical/physical): 512B/512B
      Partition Table: unknown
      Disk Flags:


// 本示例为了简单点，打算直接将整个硬盘创建为一个分区.
// 关于分区的更多信息见
// https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/185-gdisk.txt
[root@web01_server ~]# gdisk /dev/sdb
      GPT fdisk (gdisk) version 0.8.10

      Partition table scan:
        MBR: not present
        BSD: not present
        APM: not present
        GPT: not present

      Creating new GPT entries.

      Command (? for help): ?   <============键入 ? 查看帮助
      b back up GPT data to a file
      c change a partition's name
      d delete a partition
      i show detailed information on a partition
      l list known partition types
      n add a new partition
      o create a new empty GUID partition table (GPT)
      p print the partition table
      q quit without saving changes
      r recovery and transformation options (experts only)
      s sort partitions
      t change a partition's type code
      v verify disk
      w write table to disk and exit
      x extra functionality (experts only)
      ? print this menu

      Command (? for help): p     <============== 查看分区表
      Disk /dev/sdb: 16777216 sectors, 8.0 GiB
      Logical sector size: 512 bytes
      Disk identifier (GUID): 34D7860E-6312-4154-B838-FC97267D8F2B
      Partition table holds up to 128 entries
      First usable sector is 34, last usable sector is 16777182
      Partitions will be aligned on 2048-sector boundaries
      Total free space is 16777149 sectors (8.0 GiB)

      Number  Start (sector)    End (sector)  Size       Code  Name

      Command (? for help): n   <======== 选择菜单 n, 准备新建一个分区
      Partition number (1-128, default 1): 1    <========= 设置分区 number
      First sector (34-16777182, default = 2048) or {+-}size{KMGTP}: <=========== 设置 分区的 First sector, 这里使用默认的 2048, 保持对齐(aligned)
      Last sector (2048-16777182, default = 16777182) or {+-}size{KMGTP}: <=======直接回车, 选择默认值
      Current type is 'Linux filesystem'
      Hex code or GUID (L to show codes, Enter = 8300): <========= 设置 Hex code, 这里直接回车表示选择 8300 Linux Filesystem(注意根据实际情况设置)
      Changed type of partition to 'Linux filesystem'

      Command (? for help): p <============== 查看当前分区表效果
      Disk /dev/sdb: 16777216 sectors, 8.0 GiB
      Logical sector size: 512 bytes
      Disk identifier (GUID): 34D7860E-6312-4154-B838-FC97267D8F2B
      Partition table holds up to 128 entries
      First usable sector is 34, last usable sector is 16777182
      Partitions will be aligned on 2048-sector boundaries
      Total free space is 2014 sectors (1007.0 KiB)

      Number  Start (sector)    End (sector)  Size       Code  Name
         1            2048        16777182   8.0 GiB     8300  Linux filesystem

      Command (? for help): w  <============ 保存修改到磁盘 并退出

      Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
      PARTITIONS!!

      Do you want to proceed? (Y/N): y <========= 确认保存并退出
      OK; writing new GUID partition table (GPT) to /dev/sdb.
      The operation has completed successfully.


[root@web01_server ~]# partprobe -s /dev/sdb  # 通知请求 内核 重新读取 磁盘 /dev/sdb 的分区表(虽然好像 gdisk 保存退出时已经通知了kernel, 但保险起见还是执行一次 partprobe 较好)
    /dev/sdb: gpt partitions 1


[root@web01_server ~]# cat /proc/partitions   # 核心的分割纪录
      major minor  #blocks  name

         8        0   20971520 sda
         8        1     204800 sda1
         8        2   20765696 sda2
        11        0    1048575 sr0
       253        0   18665472 dm-0
       253        1    2097152 dm-1
         8       16    8388608 sdb
         8       17    8387567 sdb1 <----- 观察


// 格式化 (在 分区上 创建 文件系统)
//   https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/190-mkfs.ext4.txt
[root@web01_server ~]# mkfs.ext4 /dev/sdb1   # 在 分区 /dev/sdb1 上创建 ext4 文件系统
      mke2fs 1.42.9 (28-Dec-2013)
      Filesystem label=
      OS type: Linux
      Block size=4096 (log=2)
      Fragment size=4096 (log=2)
      Stride=0 blocks, Stripe width=1024 blocks
      524288 inodes, 2096891 blocks
      104844 blocks (5.00%) reserved for the super user
      First data block=0
      Maximum filesystem blocks=2147483648
      64 block groups
      32768 blocks per group, 32768 fragments per group
      8192 inodes per group
      Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

      Allocating group tables: done
      Writing inode tables: done
      Creating journal (32768 blocks): done
      Writing superblocks and filesystem accounting information: done


[root@web01_server ~]# blkid /dev/sdb1       # 使用命令 blkid 查看 分区 /dev/sdb1 的文件系统类型
    /dev/sdb1: UUID="e3df86a6-6516-4cc0-8877-f7c46acc40a3" TYPE="ext4" PARTLABEL="Linux filesystem" PARTUUID="fc59e57f-3452-44ea-b047-6c7cb58d5b94"

[root@web01_server ~]# file -sL /dev/sdb1    # 使用命令 file 查看 分区 /dev/sdb1 的文件系统类型
    /dev/sdb1: Linux rev 1.0 ext4 filesystem data, UUID=e3df86a6-6516-4cc0-8877-f7c46acc40a3 (extents) (64bit) (large files) (huge files)



[root@web01_server ~]# mkdir -p /var/www/html/

//  https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/194-mount.txt
[root@web01_server ~]# mount /dev/sdb1 /var/www/html/
[root@web01_server ~]# mount | grep /var/www/html
      /dev/sdb1 on /var/www/html type ext4 (rw,relatime,stripe=1024,data=ordered)

[root@web01_server ~]# rmdir /var/www/html/lost+found/
[root@web01_server ~]# umount /var/www/html/


[root@web01_server ~]# vim /etc/fstab

      /dev/sdb1 /var/www/html/  ext4     defaults,_netdev        0 0




[root@web01_server ~]# mount -a   # 挂载 /etc/fstab 中 描述的 所有文件系统(包含关键字 noauto 的 行除外)
[root@web01_server ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root xfs        18G  1.9G   16G  11% /
      devtmpfs                devtmpfs  478M     0  478M   0% /dev
      tmpfs                   tmpfs     489M     0  489M   0% /dev/shm
      tmpfs                   tmpfs     489M  6.7M  482M   2% /run
      tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1               xfs       197M  103M   95M  53% /boot
      tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
      /dev/sdb1               ext4      7.8G   36M  7.3G   1% /var/www/html   <---- 观察









----------------------------------------------------------------------------------------------------
配置 web02_server (与 iscsi 相关)

[root@web02_server ~]# yum -y install iscsi-initiator-utils


[root@web02_server ~]# systemctl start iscsi iscsid
[root@web02_server ~]# systemctl enable iscsi iscsid

[root@web02_server ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@web02_server ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-08.com.linux:client

[root@web02_server ~]# systemctl restart iscsid

[root@web02_server ~]# iscsiadm -m discovery -t st -p 192.168.175.130:3260
      192.168.175.130:3260,1 iqn.2019-08.com.linux:wd-disk

[root@web02_server ~]# iscsiadm -m node -T iqn.2019-08.com.linux:wd-disk -p 192.168.175.130:3260 -l
        Logging in to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260] (multiple)
        Login to [iface: default, target: iqn.2019-08.com.linux:wd-disk, portal: 192.168.175.130,3260] successful.


[root@web02_server ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk
    ├─/dev/sda1                   8:1    0  200M  0 part /boot
    └─/dev/sda2                   8:2    0 19.8G  0 part
      ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
      └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
    /dev/sdb                      8:16   0    8G  0 disk  <---- 观察
    └─/dev/sdb1                   8:17   0    8G  0 part  <----
    /dev/sr0                     11:0    1 1024M  0 rom


// 查看文件分区格式化信息(因为已经存在分区及文件系统, 所以在 web02_server 上可以直接了, 不要再做分区格式化操作了)
[root@web02_server ~]# parted /dev/sdb print  # 使用 parted 命令查看分区表 信息(如类型, 是否存在...)
    Model: LIO-ORG disk01 (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: gpt
    Disk Flags:

    Number  Start   End     Size    File system  Name              Flags
     1      1049kB  8590MB  8589MB  ext4         Linux filesystem



[root@web02_server ~]# mkdir -p /var/www/html/


[root@web01_server ~]# vim /etc/fstab

      /dev/sdb1 /var/www/html/  ext4     defaults,_netdev        0 0


[root@web01_server ~]# mount -a

[root@web01_server ~]# df -hT
    Filesystem              Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root xfs        18G  1.9G   16G  11% /
    devtmpfs                devtmpfs  478M     0  478M   0% /dev
    tmpfs                   tmpfs     489M     0  489M   0% /dev/shm
    tmpfs                   tmpfs     489M  6.7M  482M   2% /run
    tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
    /dev/sda1               xfs       197M  103M   95M  53% /boot
    tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
    /dev/sdb1               ext4      7.8G   36M  7.3G   1% /var/www/html  <-----观察










----------------------------------------------------------------------------------------------------
配置 web01_server (与 lvs 相关)

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
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo   <----- 观察
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

[root@web01_server ~]# echo 'keepalived_lvs_dr_iscsi' > /var/www/html/index.html

[root@web01_server ~]# curl http://192.168.175.121:80
    keepalived_lvs_dr_iscsi


----------------------------------------------------------------------------------------------------
配置 web02_server (与 lvs 相关)

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
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo <----- 观察
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

// 因为前面 格式化磁盘时 使用的是单机文件系统, 所以这里这里需要重新挂载一下才能显示 /var/www/html/index.html .
// 实际生产环境中 应该使用 集群文件系统
[root@web02_server ~]# umount /var/www/html/
[root@web02_server ~]# mount -a

[root@web02_server ~]# ls /var/www/html/index.html
    /var/www/html/index.html

[root@web02_server ~]# systemctl restart httpd

[root@web02_server ~]# curl http://192.168.175.122:80
    keepalived_lvs_dr_iscsi















----------------------------------------------------------------------------------------------------
配置 lvs_director01

// 先手动测试一下 能否正常访问 后端的 real servers
[root@lvs_director01 ~]# curl http://192.168.175.121:80
    keepalived_lvs_dr_iscsi
[root@lvs_director01 ~]# curl http://192.168.175.122:80
    keepalived_lvs_dr_iscsi


// 安装 相应的软件 (注: 此时 ipvsadm 仅用于测试方便)
[root@lvs_director01 ~]# yum -y install keepalived ipvsadm
[root@lvs_director01 ~]# rpm -q keepalived ipvsadm
      keepalived-1.3.5-8.el7_6.5.x86_64
      ipvsadm-1.27-7.el7.x86_64



// 查看一下 软件包 keepalived 中包含的文件
[root@lvs_director01 ~]# rpm -ql keepalived | less

            /etc/keepalived
            /etc/keepalived/keepalived.conf   <------
            /etc/sysconfig/keepalived
            /usr/bin/genhash
            /usr/lib/systemd/system/keepalived.service  <------
            /usr/libexec/keepalived
            /usr/sbin/keepalived
            /usr/share/doc/keepalived-1.3.5
            /usr/share/doc/keepalived-1.3.5/AUTHOR
            /usr/share/doc/keepalived-1.3.5/CONTRIBUTORS
            /usr/share/doc/keepalived-1.3.5/COPYING
            /usr/share/doc/keepalived-1.3.5/ChangeLog
            /usr/share/doc/keepalived-1.3.5/NOTE_vrrp_vmac.txt
            /usr/share/doc/keepalived-1.3.5/README
            /usr/share/doc/keepalived-1.3.5/TODO
            /usr/share/doc/keepalived-1.3.5/keepalived.conf.SYNOPSIS  <---------------
            /usr/share/doc/keepalived-1.3.5/samples  <--------------------------------
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.HTTP_GET.port
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.IPv6
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.SMTP_CHECK
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.SSL_GET
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.fwmark
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.inhibit
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.misc_check
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.misc_check_arg
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.quorum
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.sample
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.status_code
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.track_interface
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.virtual_server_group
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.virtualhost
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.localcheck
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.lvs_syncd
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.routes
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.rules
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.scripts
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.static_ipaddress
            /usr/share/doc/keepalived-1.3.5/samples/keepalived.conf.vrrp.sync
            /usr/share/doc/keepalived-1.3.5/samples/sample.misccheck.smbcheck.sh
            /usr/share/man/man1/genhash.1.gz
            /usr/share/man/man5/keepalived.conf.5.gz
            /usr/share/man/man8/keepalived.8.gz
            /usr/share/snmp/mibs/KEEPALIVED-MIB.txt
            /usr/share/snmp/mibs/VRRP-MIB.txt
            /usr/share/snmp/mibs/VRRPv3-MIB.txt


// 查看一下文件 keepalived.service
[root@lvs_director01 ~]# cat /usr/lib/systemd/system/keepalived.service
      [Unit]
      Description=LVS and VRRP High Availability Monitor
      After=syslog.target network-online.target

      [Service]
      Type=forking
      PIDFile=/var/run/keepalived.pid
      KillMode=process
      EnvironmentFile=-/etc/sysconfig/keepalived
      ExecStart=/usr/sbin/keepalived $KEEPALIVED_OPTIONS
      ExecReload=/bin/kill -HUP $MAINPID

      [Install]
      WantedBy=multi-user.target


// 修改 keepalived.conf 前先备份一份
[root@lvs_director01 ~]# cp /etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf.bak


// keepalived 的文档:
//      https://keepalived.org/doc/
// keepalived 的 官网:
//      https://www.keepalived.org/
//  `man keepalived.conf`  其中 man page 包含了最详细的参数解释
//   在线man page 见 https://www.systutorials.com/docs/linux/man/5-keepalived.conf/
// 注: keepalived.conf 的 单行注释以 符号 '#' or '!' 开始
[root@lvs_director01 ~]# vim /etc/keepalived/keepalived.conf    # https://www.keepalived.org/doc/configuration_synopsis.html

            ! Configuration File for keepalived
            #man keepalived.conf
            #https://www.systutorials.com/docs/linux/man/5-keepalived.conf/

            global_defs {
               router_id director01
            }

            #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
            vrrp_instance web_service_group {
                state MASTER
                interface ens33
                virtual_router_id 55
                priority 100    #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
                advert_int 1    # master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
                authentication {
                    auth_type PASS
                    auth_pass 1234
                }
                virtual_ipaddress {
                    192.168.175.100
                }
            }

            # 注: virtual_server 的定义仅在 keepalived 结合 lvs 时需要(用于帮助 lvs 生成负载均衡规则),
            #     其他情况下是不需要的, 如 keepalived 结合 haproxy 时
            virtual_server 192.168.175.100 80 {
                delay_loop 6
                lb_algo rr
                lb_kind DR
                persistence_timeout 300
                protocol TCP

                real_server 192.168.175.121 80 {
                    weight 1
                    TCP_CHECK {
                        connect_timeout 3
                        nb_get_retry 3
                        delay_before_retry 3
                        connect_port 80
                    }
                }

                real_server 192.168.175.122 80 {
                    weight 1
                    TCP_CHECK {
                        connect_timeout 3
                        nb_get_retry 3
                        delay_before_retry 3
                        connect_port 80
                    }
                }
            }


----------------------------------------------------------------------------------------------------

// 先手动测试一下 能否正常访问 后端的 real servers
[root@lvs_director02 ~]# curl http://192.168.175.121:80
    keepalived_lvs_dr_iscsi
[root@lvs_director02 ~]# curl http://192.168.175.122:80
    keepalived_lvs_dr_iscsi




// 安装 相应的软件 (注: 此时 ipvsadm 仅用于测试方便)
[root@lvs_director02 ~]# yum -y install keepalived ipvsadm2
[root@lvs_director02 ~]# rpm -q keepalived ipvsadm
    keepalived-1.3.5-8.el7_6.5.x86_64
    ipvsadm-1.27-7.el7.x86_64



[root@lvs_director02 ~]# rsync -av root@192.168.175.101:/etc/keepalived/keepalived.conf  /etc/keepalived/keepalived.conf

[root@lvs_director02 ~]# vim /etc/keepalived/keepalived.conf

            ! Configuration File for keepalived
            #man keepalived.conf
            #https://www.systutorials.com/docs/linux/man/5-keepalived.conf/

            global_defs {
               router_id director02
            }

            #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
            vrrp_instance web_service_group {
                state BACKUP
                interface ens33
                virtual_router_id 55
                priority 80    #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
                advert_int 1    # master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
                authentication {
                    auth_type PASS
                    auth_pass 1234
                }
                virtual_ipaddress {
                    192.168.175.100
                }
            }

            # 注: virtual_server 的定义仅在 keepalived 结合 lvs 时需要(用于帮助 lvs 生成负载均衡规则),
            #     其他情况下是不需要的, 如 keepalived 结合 haproxy 时
            virtual_server 192.168.175.100 80 {
                delay_loop 6
                lb_algo rr
                lb_kind DR
                persistence_timeout 300
                protocol TCP

                real_server 192.168.175.121 80 {
                    weight 1
                    TCP_CHECK {
                        connect_timeout 3
                        nb_get_retry 3
                        delay_before_retry 3
                        connect_port 80
                    }
                }

                real_server 192.168.175.122 80 {
                    weight 1
                    TCP_CHECK {
                        connect_timeout 3
                        nb_get_retry 3
                        delay_before_retry 3
                        connect_port 80
                    }
                }
            }








