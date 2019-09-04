

scsi: Small Computer System Interface
iscsi: Internet Small Computer Systems Interface

    https://en.wikipedia.org/wiki/SCSI
    https://en.wikipedia.org/wiki/ISCSI


    man targetcli

    man iscsiadm
    man iscsi-iname
    man iscsid


其他笔记:
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs/103-keepalived-lvs-dr-iSCSI-demo01

       scsi:   initiator  ------------(总线)--------------------> target
      iscsi:   initiator  ------------(网络)--------------------> target


----------------------------------------------------------------------------------------------------
一个简单的 targetcli 模拟 iscsi 存储(或 模拟 internet scsi 总线) 的示例:


        node01 -----------------------------------------------------> iscsi
       iqn.2019-09.com.linux.client                         iqn.2019-09.com.linux:target01
       192.168.175.121                                      192.168.175.130
                        username: admin
                        password: redhat


----------------------------------------------------------------------------------------------------
设置 iscsi 主机:


为 iscsi server 加一块 8G 的新硬盘, 然后重启.
后续会通过 iscsi 的方式将 这块硬盘共享出去

[root@iscsi ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk <-------观察
      /dev/sr0                     11:0    1 1024M  0 rom



// 安装 targetcli
[root@iscsi ~]# yum -y install targetcli
[root@iscsi ~]# rpm -q targetcli
    targetcli-2.1.fb46-7.el7.noarch


// 启动 target 服务并设置为开机自启 (注: target服务作用: Restore LIO kernel target configuration)
[root@iscsi ~]# systemctl start target
[root@iscsi ~]# systemctl enable target

[root@iscsi ~]# systemctl status target
      ● target.service - Restore LIO kernel target configuration
         Loaded: loaded (/usr/lib/systemd/system/target.service; enabled; vendor preset: disabled)
         Active: active (exited) since Tue 2019-09-03 20:25:10 CST; 1min 22s ago
       Main PID: 1059 (code=exited, status=0/SUCCESS)

      Sep 03 20:25:10 iscsi systemd[1]: Starting Restore LIO kernel target configuration...
      Sep 03 20:25:10 iscsi target[1059]: No saved config file at /etc/target/saveconfig.json, ok, exiting
      Sep 03 20:25:10 iscsi systemd[1]: Started Restore LIO kernel target configuration.


// 如下 以 非交互式的方式 执行 targetcli 命令将 物理的 /dev/sdb 块设备 作为 iscsi 存储共享出去

// 创建 block 类型的后端存储
[root@iscsi ~]# targetcli /backstores/block create name=disk01 dev=/dev/sdb
      Warning: Could not load preferences file /root/.targetcli/prefs.bin.
      Created block storage object disk01 using /dev/sdb.

// 创建 iSCSI target (initiator在login时会对其引用)
[root@iscsi ~]# targetcli /iscsi create iqn.2019-09.com.linux:target01
      Created target iqn.2019-09.com.linux:target01.
      Created TPG 1.
      Global pref auto_add_default_portal=true
      Created default portal listening on all IPs (0.0.0.0), port 3260.


// 基于 storage object 创建逻辑存储单元
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/luns create /backstores/block/disk01
      Created LUN 0.

// 创建访问控制列表 (使其包含 特定的 iscsi qualified name: iqn.2019-09.com.linux:client)
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls create iqn.2019-09.com.linux:client
      Created Node ACL for iqn.2019-09.com.linux:client
      Created mapped LUN 0.


// 删除默认的入口(portal, 即 addr:port 对)
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260
      Deleted network portal 0.0.0.0:3260

// 自定义访问入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals create ip_address=192.168.175.130
      Using default IP port 3260
      Created network portal 192.168.175.130:3260.

// 设置使用 user-created ACLs' settings, 而非 the TPG-wide settings (如使用 user-created ACLs' settings 中的 userid 和 password)
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute generate_node_acls=0
      Parameter generate_node_acls is now '0'.


          ----------------
          注: 如果 将 generate_node_acls 设置为 1, 则可以按如下命令设置用户名和密码
              targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute generate_node_acls=1
              targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute authentication=1
              targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set auth userid=admin password=redhat
              targetcli saveconfig
          ----------------

// 启用认证功能
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute authentication=1
      Parameter authentication is now '1'.

// 设置 用户名 和 密码
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls/iqn.2019-09.com.linux:client set auth userid=admin password=redhat
      Parameter password is now 'redhat'.
      Parameter userid is now 'admin'.


// 保存配置
[root@iscsi ~]# targetcli saveconfig
      Configuration saved to /etc/target/saveconfig.json







----------------------------------------------------------------------------------------------------
设置 node01 主机:


[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# rpm -q iscsi-initiator-utils
    iscsi-initiator-utils-6.2.0.874-10.el7.x86_64

[root@node01 ~]# systemctl start iscsi iscsid
[root@node01 ~]# systemctl enable iscsi iscsid
      Created symlink from /etc/systemd/system/multi-user.target.wants/iscsid.service to /usr/lib/systemd/system/iscsid.service.

[root@node01 ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@node01 ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-09.com.linux:client


[root@node01 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat

// 重启 iscsid 服务, 使 文件 initiatorname.iscsi 和 iscsid.conf 中的修改生效
[root@node01 ~]# systemctl restart iscsid

[root@node01 ~]# systemctl status iscsid
        ● iscsid.service - Open-iSCSI
           Loaded: loaded (/usr/lib/systemd/system/iscsid.service; enabled; vendor preset: disabled)
           Active: active (running) since Wed 2019-09-04 12:05:41 CST; 24s ago
             Docs: man:iscsid(8)
                   man:iscsiadm(8)
          Process: 1582 ExecStop=/sbin/iscsiadm -k 0 2 (code=exited, status=0/SUCCESS)
          Process: 1584 ExecStart=/usr/sbin/iscsid (code=exited, status=0/SUCCESS)
         Main PID: 1586 (iscsid)
           CGroup: /system.slice/iscsid.service
                   ├─1585 /usr/sbin/iscsid
                   └─1586 /usr/sbin/iscsid

        Sep 04 12:05:41 node01 systemd[1]: Starting Open-iSCSI...
        Sep 04 12:05:41 node01 systemd[1]: Failed to read PID from file /var/run/iscsid.pid: Invalid argument
        Sep 04 12:05:41 node01 iscsid[1585]: iSCSI daemon with pid=1586 started!
        Sep 04 12:05:41 node01 systemd[1]: Started Open-iSCSI.

// 探测后端 iscsi target
[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01

          ------
          注: 此例中 如上的 探测命令会在目录 /var/lib/iscsi 下创建如下 3 个文件:
                nodes/iqn.2019-09.com.linux:target01/192.168.175.130,3260,1/default
                send_targets/192.168.175.130,3260/iqn.2019-09.com.linux:target01,192.168.175.130,3260,1,default
                send_targets/192.168.175.130,3260/st_config
          ------


// 登入(log in to) iscsi target
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
      /dev/sdb                      8:16   0    8G  0 disk  <---------观察
      /dev/sr0                     11:0    1 1024M  0 rom


// 支持, 按正常方式使用 /dev/sdb 即可
//  如简单格式化
[root@node01 ~]# mkfs.ext4 /dev/sdb
        mke2fs 1.42.9 (28-Dec-2013)
        /dev/sdb is entire device, not just one partition!
        Proceed anyway? (y,n) y  <=========键入 y
        Filesystem label=
        OS type: Linux
        Block size=4096 (log=2)
        Fragment size=4096 (log=2)
        Stride=0 blocks, Stripe width=1024 blocks
        524288 inodes, 2097152 blocks
        104857 blocks (5.00%) reserved for the super user
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

[root@node01 ~]# blkid /dev/sdb
        /dev/sdb: UUID="a6840e1f-5313-4ab8-ad3f-7e25b05ec6a9" TYPE="ext4"


[root@node01 ~]# mkdir /data
[root@node01 ~]# vim /etc/fstab

      #挂载 SAN 时 建议不要使用 磁盘名, 而是使用 UUID 挂载
      UUID="a6840e1f-5313-4ab8-ad3f-7e25b05ec6a9" /data  ext4 defaults,_netdev 0 0


[root@node01 ~]# mount -a
[root@node01 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root xfs        18G  1.9G   16G  11% /
      devtmpfs                devtmpfs  478M     0  478M   0% /dev
      tmpfs                   tmpfs     489M     0  489M   0% /dev/shm
      tmpfs                   tmpfs     489M  6.8M  482M   2% /run
      tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1               xfs       197M  103M   95M  53% /boot
      tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
      /dev/sdb                ext4      7.8G   36M  7.3G   1% /data

root@node01 ~]# ls /data/
    lost+found
[root@node01 ~]# rm -rf /data/lost+found/















----------------------------------------------------------------------------------------------------
一些有用的命令:

// 临时登出 与 iscsi target 的 连接会话
[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -u
    Logging out of session [sid: 1, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260]
    Logout of [sid: 1, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] successful.

// 如果要永久登出 iscsi target (即 重启系统后 也不会自动 login 后端 iscsi target), 可以使用如下命令:
// 注: 执行此命令时 需要 先确保 后端 iscsi target 已经被 临时 登出(log out)
[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -o delete

          ------
          注: 本例中 如上的 命令其实 是删除了目录 /var/lib/iscsi 下的 如下 2 个文件:
              nodes/iqn.2019-09.com.linux:target01/192.168.175.130,3260,1/default
              send_targets/192.168.175.130,3260/iqn.2019-09.com.linux:target01,192.168.175.130,3260,1,default
          ------





// 获取设置的 auth 信息
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 get auth

// 生成 iscsi qualified name
[root@node01 ~]# iscsi-iname
      iqn.1994-05.com.redhat:268886cae929

// 生成 iscsi qualified name 时指定前缀
[root@node01 ~]# iscsi-iname -p iqn.2019-09.com.linux
      iqn.2019-09.com.linux:4ba5436a80e6









----------------------------------------------------------------------------------------------------
网上资料:

      https://blog.csdn.net/cmzsteven/article/details/80417025




