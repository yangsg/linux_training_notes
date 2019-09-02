
Openfiler (openfileresa-2.99.1-x86_64-disc1.iso)下载地址:
  https://www.openfiler.com/community/download


VMware Workstation 上安装 Openfiler 的 指南:
    https://communities.vmware.com/docs/DOC-28326
    https://communities.vmware.com/servlet/JiveServlet/previewBody/28326-102-1-38053/Configuring%20Openfiler.pdf

  注: VMware Workstation 选择系统时 选择 'linux' 和 'Red Hat Enterprise Linux 5 64-bit'


Web administraction GUI: https://192.168.175.133:446/


添加一块新硬盘


[root@iscsi ~]# fdisk -l

        Disk /dev/sda: 21.5 GB, 21474836480 bytes
        255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
        Units = sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
        Disk identifier: 0x0002cc75

           Device Boot      Start         End      Blocks   Id  System
        /dev/sda1   *          63      610469      305203+  83  Linux
        /dev/sda2          610470    17382329     8385930   83  Linux
        /dev/sda3        17382330    19486844     1052257+  82  Linux swap / Solaris

        Disk /dev/sdb: 21.5 GB, 21474836480 bytes  <---------- 观察新添加的硬盘
        255 heads, 63 sectors/track, 2610 cylinders, total 41943040 sectors
        Units = sectors of 1 * 512 = 512 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
        Disk identifier: 0x00000000

        Disk /dev/sdb doesn't contain a valid partition table



浏览器访问   https://192.168.175.133:446/

                  Username: openfilter
                  Password: password

    SAN 存储 为了增强安全性, 通过都要同时做 基于 client 端的 ip 和 用户名密码的认证.


// 客户端 配置 及 操作:
[root@node01 ~]# yum -y install iscsi-initiator-utils

[root@node01 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat


[root@node01 ~]# systemctl restart iscsid


[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.133
      iscsiadm: No portals found  <------ 观察(这时不正常的现象, 解决方法如下)

// 出现以上错误提示，需要注释掉openfiler端/etc/initiators.deny文件中内容
[root@iscsi ~]# vim /etc/initiators.deny

        #iqn.2019-09.com.linux:test ALL


[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.133

      192.168.175.133:3260,1 iqn.2019-09.com.linux:test


[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:test -p 192.168.175.133:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:test, portal: 192.168.175.133,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:test, portal: 192.168.175.133,3260] successful.


[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0  7.2G  0 disk  <----------观察
      /dev/sr0                     11:0    1 1024M  0 rom



[root@node01 ~]# mkfs.ext4 /dev/sdb
      mke2fs 1.42.9 (28-Dec-2013)
      /dev/sdb is entire device, not just one partition!
      Proceed anyway? (y,n) y <----
      Filesystem label=
      OS type: Linux
      Block size=4096 (log=2)
      Fragment size=4096 (log=2)
      Stride=0 blocks, Stripe width=0 blocks
      469568 inodes, 1875968 blocks
      93798 blocks (5.00%) reserved for the super user
      First data block=0
      Maximum filesystem blocks=1920991232
      58 block groups
      32768 blocks per group, 32768 fragments per group
      8096 inodes per group
      Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

      Allocating group tables: done
      Writing inode tables: done
      Creating journal (32768 blocks):

      done
      Writing superblocks and filesystem accounting information: done

[root@node01 ~]# blkid /dev/sdb
    /dev/sdb: UUID="52f643dd-6dac-474a-9351-c0396d12f299" TYPE="ext4"

[root@node01 ~]# mkdir /data


[root@node01 ~]# vim /etc/fstab

    #挂载 SAN 时 建议不要使用 磁盘名, 而是使用 UUID 挂载
    UUID="52f643dd-6dac-474a-9351-c0396d12f299" /data  ext4   defaults,_netdev  0 0

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
      /dev/sdb                ext4      7.0G   33M  6.6G   1% /data  <------观察



---------------------------------------------------------------------------------------------------

其他与 iscsi 有关的笔记:

  通过 targetcli 模拟存储:
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs/103-keepalived-lvs-dr-iSCSI-demo01


















