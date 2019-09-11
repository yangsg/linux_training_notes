

网上资料:
    fastdfs 的安装部署:
        https://www.cnblogs.com/Yin-BloodMage/p/5480608.html
        https://www.jianshu.com/p/1de9b0383bb9
        https://www.iteye.com/blog/liuyieyer-2065562
        https://blog.csdn.net/qq_34301871/article/details/80060235



      +-----------client------------------+                +-----------tracker群-----+
      |                                   |                |                         |
      |                                   |--------------->|                         |
      |  client1  client2 ...  clientN    |                |    tracker1  tracker2   |
      |                                   |<---------------|                         |
      |                                   |                |                         |
      +-----------------------------------+                +-------------------------+
                 |        Λ                                      Λ        |
                 |        |                                      |        |
                 |        |                                      |        |
                 V        |                                      |        V
      +----------------------------------storage 群-----------------------------------------+
      |                                                                                     |
      |                                                                                     |
      |       +--卷1-(或group1)------+                   +---卷2--(或group2)----+           |
      |       |                      |                   |                      |           |
      |       |                      |                   |                      |           |
      |       |  storager1_1 ---+    |                   |  storager2_1 ---+    |           |
      |       |                 |同  |                   |                 |同  |           |
      |       |                 |步  |                   |                 |步  |           |
      |       |                 |线  |                   |                 |线  |           |
      |       |                 |程  |                   |                 |程  |           |
      |       |  storager1_2 ---+    |                   |  storager2_2 ---+    |           |
      |       |                      |                   |                      |           |
      |       |                      |                   |                      |           |
      |       +----------------------+                   +----------------------+           |
      |                                                                                     |
      |                                                                                     |
      +-------------------------------------------------------------------------------------+

----------------------------------------------------------------------------------------------------
示例: 仅搭建最简单基础的 FastDFS 存储系统


tracker_server01    192.168.175.101
tracker_server02    192.168.175.102
storage_server01    192.168.175.111
storage_server02    192.168.175.112


client  192.168.175.80  <------作为测试用的客户端

----------------------------------------------------------------------------------------------------
在所有节点安装fastdfs软件, 即在如下 4 台 servers 上分别安装 fastdfs 软件
          tracker_server01
          tracker_server02
          storage_server01
          storage_server02


// 此处以 tracker_server01 上安装 fastdfs 为例
// 构建基础编译环境
[root@tracker_server01 ~]# yum -y install gcc gcc-c++ autoconf automake

[root@tracker_server01 ~]# mkdir download
[root@tracker_server01 ~]# cd download/

// 安装 fastdfs 依赖库 libfastcommon
[root@tracker_server01 download]# git clone https://github.com/happyfish100/libfastcommon.git
[root@tracker_server01 download]# ls
      libfastcommon

[root@tracker_server01 download]# cd libfastcommon/
[root@tracker_server01 libfastcommon]# ls
      doc  HISTORY  INSTALL  libfastcommon.spec  make.sh  php-fastcommon  README  src

// 查看一下 所有的 tags
[root@tracker_server01 fastdfs]# git tag
      V5.04
      V5.05
      V5.08
      V5.09
      V5.10
      V5.11

// 查看 当前所在的 tag
[root@tracker_server01 fastdfs]# git describe --tags
  V5.11-25-g102c444


[root@tracker_server01 libfastcommon]# ./make.sh
[root@tracker_server01 libfastcommon]# ./make.sh install


// 安装 fastdfs
[root@tracker_server01 libfastcommon]# cd ~/download/
[root@tracker_server01 download]# git clone https://github.com/happyfish100/fastdfs.git
[root@tracker_server01 download]# ls
      fastdfs  libfastcommon

[root@tracker_server01 download]# cd fastdfs/
[root@tracker_server01 fastdfs]# ls
      client  common  conf  COPYING-3_0.txt  docker  fastdfs.spec  HISTORY  init.d  INSTALL  make.sh  php_client  README.md  restart.sh  stop.sh  storage  test  tracker

[root@tracker_server01 fastdfs]# ./make.sh
[root@tracker_server01 fastdfs]# ./make.sh install


----------------------------------------------------------------------------------------------------
查看观察一下 相关的目录

[root@tracker_server01 ~]# ls /etc/fdfs/
      client.conf.sample  storage.conf.sample  storage_ids.conf.sample  tracker.conf.sample

[root@tracker_server01 ~]# ls /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README

[root@tracker_server01 ~]# ls -1 /usr/bin/fdfs_*
      /usr/bin/fdfs_appender_test
      /usr/bin/fdfs_appender_test1
      /usr/bin/fdfs_append_file
      /usr/bin/fdfs_crc32
      /usr/bin/fdfs_delete_file
      /usr/bin/fdfs_download_file
      /usr/bin/fdfs_file_info
      /usr/bin/fdfs_monitor
      /usr/bin/fdfs_storaged
      /usr/bin/fdfs_test
      /usr/bin/fdfs_test1
      /usr/bin/fdfs_trackerd
      /usr/bin/fdfs_upload_appender
      /usr/bin/fdfs_upload_file



----------------------------------------------------------------------------------------------------
设置 tracker_server01

[root@tracker_server01 ~]# cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf

[root@tracker_server01 ~]# vim /etc/fdfs/tracker.conf

      bind_addr=192.168.175.101
      base_path=/data/fastdfs/tracker

[root@tracker_server01 ~]# mkdir -pv /data/fastdfs/tracker
      mkdir: created directory ‘/data’
      mkdir: created directory ‘/data/fastdfs’
      mkdir: created directory ‘/data/fastdfs/tracker’


[root@tracker_server01 ~]# ls  /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README

// 查看一下 fdfs_trackerd 的 usage
[root@tracker_server01 ~]# /etc/init.d/fdfs_trackerd -h
      Usage: /etc/init.d/fdfs_trackerd {start|stop|status|restart|condrestart}

[root@tracker_server01 ~]# /etc/init.d/fdfs_trackerd start
      Reloading systemd:                                         [  OK  ]
      Starting fdfs_trackerd (via systemctl):                    [  OK  ]


[root@tracker_server01 ~]# /etc/init.d/fdfs_trackerd status
      ● fdfs_trackerd.service - LSB: FastDFS tracker server
         Loaded: loaded (/etc/rc.d/init.d/fdfs_trackerd; bad; vendor preset: disabled)
         Active: active (running) since Tue 2019-09-10 21:36:10 CST; 11min ago
           Docs: man:systemd-sysv-generator(8)
        Process: 1102 ExecStart=/etc/rc.d/init.d/fdfs_trackerd start (code=exited, status=0/SUCCESS)
         CGroup: /system.slice/fdfs_trackerd.service
                 └─1107 /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf

      Sep 10 21:36:10 tracker_server01 systemd[1]: Starting LSB: FastDFS tracker server...
      Sep 10 21:36:10 tracker_server01 fdfs_trackerd[1102]: Starting FastDFS tracker server:
      Sep 10 21:36:10 tracker_server01 systemd[1]: Started LSB: FastDFS tracker server.


[root@tracker_server01 ~]# netstat -anptu | grep fdfs
      tcp        0      0 192.168.175.101:22122   0.0.0.0:*               LISTEN      1107/fdfs_trackerd


// 查看一下 base_path 下的变化
[root@tracker_server01 ~]# tree /data/fastdfs/tracker/
        /data/fastdfs/tracker/
        ├── data
        │   ├── fdfs_trackerd.pid
        │   └── storage_changelog.dat
        └── logs
            └── trackerd.log



----------------------------------------------------------------------------------------------------
设置 tracker_server02

[root@tracker_server02 ~]# cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf

[root@tracker_server02 ~]# vim /etc/fdfs/tracker.conf

      bind_addr=192.168.175.102
      base_path=/data/fastdfs/tracker

[root@tracker_server02 ~]# mkdir -pv /data/fastdfs/tracker
      mkdir: created directory ‘/data’
      mkdir: created directory ‘/data/fastdfs’
      mkdir: created directory ‘/data/fastdfs/tracker’


[root@tracker_server02 ~]# ls  /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README

// 查看一下 fdfs_trackerd 的 usage
[root@tracker_server02 ~]# /etc/init.d/fdfs_trackerd -h
      Usage: /etc/init.d/fdfs_trackerd {start|stop|status|restart|condrestart}

[root@tracker_server02 ~]# /etc/init.d/fdfs_trackerd start
      Reloading systemd:                                         [  OK  ]
      Starting fdfs_trackerd (via systemctl):                    [  OK  ]


[root@tracker_server02 ~]# /etc/init.d/fdfs_trackerd status
      ● fdfs_trackerd.service - LSB: FastDFS tracker server
         Loaded: loaded (/etc/rc.d/init.d/fdfs_trackerd; bad; vendor preset: disabled)
         Active: active (running) since Tue 2019-09-10 21:44:28 CST; 46s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 1080 ExecStart=/etc/rc.d/init.d/fdfs_trackerd start (code=exited, status=0/SUCCESS)
         CGroup: /system.slice/fdfs_trackerd.service
                 └─1085 /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf

      Sep 10 21:44:28 tracker_server02 systemd[1]: Starting LSB: FastDFS tracker server...
      Sep 10 21:44:28 tracker_server02 fdfs_trackerd[1080]: Starting FastDFS tracker server:
      Sep 10 21:44:28 tracker_server02 systemd[1]: Started LSB: FastDFS tracker server.



[root@tracker_server02 ~]# netstat -anptu | grep fdfs_
        tcp        0      0 192.168.175.102:22122   0.0.0.0:*               LISTEN      1085/fdfs_trackerd


// 查看一下 base_path 下的变化
[root@tracker_server02 ~]# tree /data/fastdfs/tracker/
      /data/fastdfs/tracker/
      ├── data
      │   ├── fdfs_trackerd.pid
      │   └── storage_changelog.dat
      └── logs
          └── trackerd.log


----------------------------------------------------------------------------------------------------
设置 storage_server01


[root@storage_server01 ~]# ls /etc/fdfs/
      client.conf.sample  storage.conf.sample  storage_ids.conf.sample  tracker.conf.sample

[root@storage_server01 ~]# cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf

[root@storage_server01 ~]# vim /etc/fdfs/storage.conf

        group_name=group01
        bind_addr=192.168.175.111
        base_path=/data/fastdfs/storage

        store_path_count=1
        store_path0=/data/fastdfs/data

        tracker_server=192.168.175.101:22122
        tracker_server=192.168.175.102:22122



[root@storage_server01 ~]# mkdir -pv /data/fastdfs/storage
[root@storage_server01 ~]# mkdir -pv /data/fastdfs/data

[root@storage_server01 ~]# ls /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README


[root@storage_server01 ~]# /etc/init.d/fdfs_storaged -h
    Usage: /etc/init.d/fdfs_storaged {start|stop|status|restart|condrestart}

[root@storage_server01 ~]# /etc/init.d/fdfs_storaged start
    Starting fdfs_storaged (via systemctl):                    [  OK  ]

[root@storage_server01 ~]# /etc/init.d/fdfs_storaged status
      ● fdfs_storaged.service - LSB: FastDFS storage server
         Loaded: loaded (/etc/rc.d/init.d/fdfs_storaged; bad; vendor preset: disabled)
         Active: active (running) since Tue 2019-09-10 22:09:03 CST; 32s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 1123 ExecStart=/etc/rc.d/init.d/fdfs_storaged start (code=exited, status=0/SUCCESS)
         CGroup: /system.slice/fdfs_storaged.service
                 └─1128 /usr/bin/fdfs_storaged /etc/fdfs/storage.conf

      Sep 10 22:09:03 storage_server01 systemd[1]: Starting LSB: FastDFS storage server...
      Sep 10 22:09:03 storage_server01 fdfs_storaged[1123]: Starting FastDFS storage server:
      Sep 10 22:09:03 storage_server01 systemd[1]: Started LSB: FastDFS storage server.


[root@storage_server01 ~]# netstat -anptu | grep fdfs
      tcp        0      0 192.168.175.111:23000   0.0.0.0:*               LISTEN      1128/fdfs_storaged  <------
      tcp        0      0 192.168.175.111:38819   192.168.175.101:22122   ESTABLISHED 1128/fdfs_storaged  <------
      tcp        0      0 192.168.175.111:43394   192.168.175.102:22122   ESTABLISHED 1128/fdfs_storaged  <------


// 查看一下 base_path 下的变化
[root@storage_server01 ~]# tree /data/fastdfs/storage/
      /data/fastdfs/storage/
      ├── data
      │   ├── fdfs_storaged.pid
      │   ├── storage_stat.dat
      │   └── sync
      │       ├── binlog.000
      │       └── binlog.index
      └── logs
          └── storaged.log


// 在 tracker_server01 上查看一下 文件 storage_groups_new.dat 的内容
[root@tracker_server01 ~]# cat /data/fastdfs/tracker/data/storage_groups_new.dat
      # global section
      [Global]
        group_count=1

      # group: group01
      [Group001]
        group_name=group01
        storage_port=23000
        storage_http_port=8888
        store_path_count=1
        subdir_count_per_path=256
        current_trunk_file_id=0
        trunk_server=
        last_trunk_server=



// 查看一下 store_path0 目录下的变化
[root@storage_server01 ~]# ls /data/fastdfs/data/
        data  <------- storage_server01 上自动生成的目录

// 查看 在 store_path0 目录下 data 目录下 自动生成的 256 个第一级子目录
[root@storage_server01 ~]# ls /data/fastdfs/data/data/

      00  09  12  1B  24  2D  36  3F  48  51  5A  63  6C  75  7E  87  90  99  A2  AB  B4  BD  C6  CF  D8  E1  EA  F3  FC
      01  0A  13  1C  25  2E  37  40  49  52  5B  64  6D  76  7F  88  91  9A  A3  AC  B5  BE  C7  D0  D9  E2  EB  F4  FD
      02  0B  14  1D  26  2F  38  41  4A  53  5C  65  6E  77  80  89  92  9B  A4  AD  B6  BF  C8  D1  DA  E3  EC  F5  FE
      03  0C  15  1E  27  30  39  42  4B  54  5D  66  6F  78  81  8A  93  9C  A5  AE  B7  C0  C9  D2  DB  E4  ED  F6  FF
      04  0D  16  1F  28  31  3A  43  4C  55  5E  67  70  79  82  8B  94  9D  A6  AF  B8  C1  CA  D3  DC  E5  EE  F7
      05  0E  17  20  29  32  3B  44  4D  56  5F  68  71  7A  83  8C  95  9E  A7  B0  B9  C2  CB  D4  DD  E6  EF  F8
      06  0F  18  21  2A  33  3C  45  4E  57  60  69  72  7B  84  8D  96  9F  A8  B1  BA  C3  CC  D5  DE  E7  F0  F9
      07  10  19  22  2B  34  3D  46  4F  58  61  6A  73  7C  85  8E  97  A0  A9  B2  BB  C4  CD  D6  DF  E8  F1  FA
      08  11  1A  23  2C  35  3E  47  50  59  62  6B  74  7D  86  8F  98  A1  AA  B3  BC  C5  CE  D7  E0  E9  F2  FB


// 查看 在 store_path0 目录下 data 目录下 自动生成的 256 个第一级子目录 中 第一个子目录 00 下的 256 个第二级子目录
// 注:   256*256=65536
[root@storage_server01 ~]# ls /data/fastdfs/data/data/00/

      00  09  12  1B  24  2D  36  3F  48  51  5A  63  6C  75  7E  87  90  99  A2  AB  B4  BD  C6  CF  D8  E1  EA  F3  FC
      01  0A  13  1C  25  2E  37  40  49  52  5B  64  6D  76  7F  88  91  9A  A3  AC  B5  BE  C7  D0  D9  E2  EB  F4  FD
      02  0B  14  1D  26  2F  38  41  4A  53  5C  65  6E  77  80  89  92  9B  A4  AD  B6  BF  C8  D1  DA  E3  EC  F5  FE
      03  0C  15  1E  27  30  39  42  4B  54  5D  66  6F  78  81  8A  93  9C  A5  AE  B7  C0  C9  D2  DB  E4  ED  F6  FF
      04  0D  16  1F  28  31  3A  43  4C  55  5E  67  70  79  82  8B  94  9D  A6  AF  B8  C1  CA  D3  DC  E5  EE  F7
      05  0E  17  20  29  32  3B  44  4D  56  5F  68  71  7A  83  8C  95  9E  A7  B0  B9  C2  CB  D4  DD  E6  EF  F8
      06  0F  18  21  2A  33  3C  45  4E  57  60  69  72  7B  84  8D  96  9F  A8  B1  BA  C3  CC  D5  DE  E7  F0  F9
      07  10  19  22  2B  34  3D  46  4F  58  61  6A  73  7C  85  8E  97  A0  A9  B2  BB  C4  CD  D6  DF  E8  F1  FA
      08  11  1A  23  2C  35  3E  47  50  59  62  6B  74  7D  86  8F  98  A1  AA  B3  BC  C5  CE  D7  E0  E9  F2  FB

----------------------------------------------------------------------------------------------------
设置 storage_server02


[root@storage_server02 ~]# ls /etc/fdfs/
      client.conf.sample  storage.conf.sample  storage_ids.conf.sample  tracker.conf.sample

[root@storage_server02 ~]# cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf

[root@storage_server02 ~]# vim /etc/fdfs/storage.conf

        group_name=group01
        bind_addr=192.168.175.112
        base_path=/data/fastdfs/storage

        store_path_count=1
        store_path0=/data/fastdfs/data

        tracker_server=192.168.175.101:22122
        tracker_server=192.168.175.102:22122



[root@storage_server02 ~]# mkdir -pv /data/fastdfs/storage
[root@storage_server02 ~]# mkdir -pv /data/fastdfs/data

[root@storage_server02 ~]# ls /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README


[root@storage_server02 ~]# /etc/init.d/fdfs_storaged -h
    Usage: /etc/init.d/fdfs_storaged {start|stop|status|restart|condrestart}

[root@storage_server02 ~]# /etc/init.d/fdfs_storaged start
    Starting fdfs_storaged (via systemctl):                    [  OK  ]

[root@storage_server02 ~]# /etc/init.d/fdfs_storaged status
      ● fdfs_storaged.service - LSB: FastDFS storage server
         Loaded: loaded (/etc/rc.d/init.d/fdfs_storaged; bad; vendor preset: disabled)
         Active: active (running) since Tue 2019-09-10 22:32:42 CST; 19s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 1094 ExecStart=/etc/rc.d/init.d/fdfs_storaged start (code=exited, status=0/SUCCESS)
         CGroup: /system.slice/fdfs_storaged.service
                 └─1099 /usr/bin/fdfs_storaged /etc/fdfs/storage.conf

      Sep 10 22:32:42 storage_server02 systemd[1]: Starting LSB: FastDFS storage server...
      Sep 10 22:32:42 storage_server02 fdfs_storaged[1094]: Starting FastDFS storage server:
      Sep 10 22:32:42 storage_server02 systemd[1]: Started LSB: FastDFS storage server.


// 在 storage_server02 上查看 fdfs_storaged 进程 的 网络状态信息
[root@storage_server02 ~]# netstat -anptu | grep fdfs
        tcp        0      0 192.168.175.112:23000   0.0.0.0:*               LISTEN      1099/fdfs_storaged
        tcp        0      0 192.168.175.112:44232   192.168.175.102:22122   ESTABLISHED 1099/fdfs_storaged
        tcp        0      0 192.168.175.112:54759   192.168.175.111:23000   ESTABLISHED 1099/fdfs_storaged  <-----观察(用于同步)
        tcp        0      0 192.168.175.112:57571   192.168.175.101:22122   ESTABLISHED 1099/fdfs_storaged
        tcp        0      0 192.168.175.112:23000   192.168.175.111:45747   ESTABLISHED 1099/fdfs_storaged  <-----观察(用于同步)

// 在 storage_server01 上查看 fdfs_storaged 进程 的 网络状态信息
[root@storage_server01 ~]# netstat -anptu | grep fdfs
        tcp        0      0 192.168.175.111:23000   0.0.0.0:*               LISTEN      1128/fdfs_storaged
        tcp        0      0 192.168.175.111:38819   192.168.175.101:22122   ESTABLISHED 1128/fdfs_storaged
        tcp        0      0 192.168.175.111:45747   192.168.175.112:23000   ESTABLISHED 1128/fdfs_storaged  <-----观察
        tcp        0      0 192.168.175.111:43394   192.168.175.102:22122   ESTABLISHED 1128/fdfs_storaged
        tcp        0      0 192.168.175.111:23000   192.168.175.112:54759   ESTABLISHED 1128/fdfs_storaged  <-----观察





// 查看一下 base_path 下的变化
[root@storage_server02 ~]# tree /data/fastdfs/storage/
      /data/fastdfs/storage/
      ├── data
      │   ├── fdfs_storaged.pid
      │   ├── storage_stat.dat
      │   └── sync
      │       ├── 192.168.175.111_23000.mark
      │       ├── binlog.000
      │       └── binlog.index
      └── logs
          └── storaged.log

[root@storage_server01 ~]# tree /data/fastdfs/storage/
      /data/fastdfs/storage/
      ├── data
      │   ├── fdfs_storaged.pid
      │   ├── storage_stat.dat
      │   └── sync
      │       ├── 192.168.175.112_23000.mark
      │       ├── binlog.000
      │       └── binlog.index
      └── logs
          └── storaged.log



// 在 tracker_server01 上查看一下 文件 storage_groups_new.dat 的内容
[root@tracker_server01 ~]# cat /data/fastdfs/tracker/data/storage_groups_new.dat
      # global section
      [Global]
        group_count=1

      # group: group01
      [Group001]
        group_name=group01
        storage_port=23000
        storage_http_port=8888
        store_path_count=1
        subdir_count_per_path=256
        current_trunk_file_id=0
        trunk_server=
        last_trunk_server=

[root@tracker_server01 ~]# cat /data/fastdfs/tracker/data/storage_servers_new.dat  | less
      # storage 192.168.175.111:23000
      [Storage001]
              group_name=group01
              ip_addr=192.168.175.111
              status=7
              version=5.12
              join_time=1568124543
              storage_port=23000
              storage_http_port=8888

      略 略 略 略 略 略
      # storage 192.168.175.112:23000
      [Storage002]
              group_name=group01
              ip_addr=192.168.175.112
              status=1
              version=5.12
              join_time=1568125962
              storage_port=23000
              storage_http_port=8888
      略 略 略 略 略 略




// 查看一下 store_path0 目录下的变化
[root@storage_server02 ~]# ls /data/fastdfs/data/
        data  <------- storage_server02 上自动生成的目录

// 查看 在 store_path0 目录下 data 目录下 自动生成的 256 个第一级子目录
[root@storage_server02 ~]# ls /data/fastdfs/data/data/

      00  09  12  1B  24  2D  36  3F  48  51  5A  63  6C  75  7E  87  90  99  A2  AB  B4  BD  C6  CF  D8  E1  EA  F3  FC
      01  0A  13  1C  25  2E  37  40  49  52  5B  64  6D  76  7F  88  91  9A  A3  AC  B5  BE  C7  D0  D9  E2  EB  F4  FD
      02  0B  14  1D  26  2F  38  41  4A  53  5C  65  6E  77  80  89  92  9B  A4  AD  B6  BF  C8  D1  DA  E3  EC  F5  FE
      03  0C  15  1E  27  30  39  42  4B  54  5D  66  6F  78  81  8A  93  9C  A5  AE  B7  C0  C9  D2  DB  E4  ED  F6  FF
      04  0D  16  1F  28  31  3A  43  4C  55  5E  67  70  79  82  8B  94  9D  A6  AF  B8  C1  CA  D3  DC  E5  EE  F7
      05  0E  17  20  29  32  3B  44  4D  56  5F  68  71  7A  83  8C  95  9E  A7  B0  B9  C2  CB  D4  DD  E6  EF  F8
      06  0F  18  21  2A  33  3C  45  4E  57  60  69  72  7B  84  8D  96  9F  A8  B1  BA  C3  CC  D5  DE  E7  F0  F9
      07  10  19  22  2B  34  3D  46  4F  58  61  6A  73  7C  85  8E  97  A0  A9  B2  BB  C4  CD  D6  DF  E8  F1  FA
      08  11  1A  23  2C  35  3E  47  50  59  62  6B  74  7D  86  8F  98  A1  AA  B3  BC  C5  CE  D7  E0  E9  F2  FB


// 查看 在 store_path0 目录下 data 目录下 自动生成的 256 个第一级子目录 中 第一个子目录 00 下的 256 个第二级子目录
// 注:   256*256=65536
[root@storage_server02 ~]# ls /data/fastdfs/data/data/00/

      00  09  12  1B  24  2D  36  3F  48  51  5A  63  6C  75  7E  87  90  99  A2  AB  B4  BD  C6  CF  D8  E1  EA  F3  FC
      01  0A  13  1C  25  2E  37  40  49  52  5B  64  6D  76  7F  88  91  9A  A3  AC  B5  BE  C7  D0  D9  E2  EB  F4  FD
      02  0B  14  1D  26  2F  38  41  4A  53  5C  65  6E  77  80  89  92  9B  A4  AD  B6  BF  C8  D1  DA  E3  EC  F5  FE
      03  0C  15  1E  27  30  39  42  4B  54  5D  66  6F  78  81  8A  93  9C  A5  AE  B7  C0  C9  D2  DB  E4  ED  F6  FF
      04  0D  16  1F  28  31  3A  43  4C  55  5E  67  70  79  82  8B  94  9D  A6  AF  B8  C1  CA  D3  DC  E5  EE  F7
      05  0E  17  20  29  32  3B  44  4D  56  5F  68  71  7A  83  8C  95  9E  A7  B0  B9  C2  CB  D4  DD  E6  EF  F8
      06  0F  18  21  2A  33  3C  45  4E  57  60  69  72  7B  84  8D  96  9F  A8  B1  BA  C3  CC  D5  DE  E7  F0  F9
      07  10  19  22  2B  34  3D  46  4F  58  61  6A  73  7C  85  8E  97  A0  A9  B2  BB  C4  CD  D6  DF  E8  F1  FA
      08  11  1A  23  2C  35  3E  47  50  59  62  6B  74  7D  86  8F  98  A1  AA  B3  BC  C5  CE  D7  E0  E9  F2  FB







----------------------------------------------------------------------------------------------------
准备 测试用的 client


作为测试用的 client, 同样需要安装 fastdfs 软件
--------------------------------------------------
// 构建基础编译环境
[root@client ~]# yum -y install gcc gcc-c++ autoconf automake

[root@client ~]# mkdir download
[root@client ~]# cd download/

// 安装 fastdfs 依赖库 libfastcommon
[root@tracker_server01 download]# git clone https://github.com/happyfish100/libfastcommon.git
[root@tracker_server01 download]# ls
      libfastcommon

[root@tracker_server01 download]# cd libfastcommon/
[root@tracker_server01 libfastcommon]# ls
      doc  HISTORY  INSTALL  libfastcommon.spec  make.sh  php-fastcommon  README  src

[root@tracker_server01 libfastcommon]# ./make.sh
[root@tracker_server01 libfastcommon]# ./make.sh install


// 安装 fastdfs
[root@tracker_server01 libfastcommon]# cd ~/download/
[root@tracker_server01 download]# git clone https://github.com/happyfish100/fastdfs.git
[root@tracker_server01 download]# ls
      fastdfs  libfastcommon

[root@tracker_server01 download]# cd fastdfs/
[root@tracker_server01 fastdfs]# ls
      client  common  conf  COPYING-3_0.txt  docker  fastdfs.spec  HISTORY  init.d  INSTALL  make.sh  php_client  README.md  restart.sh  stop.sh  storage  test  tracker

[root@tracker_server01 fastdfs]# ./make.sh
[root@tracker_server01 fastdfs]# ./make.sh install


--------------------------------------------------
配置客户端测试数据读写


[root@client ~]# cp /etc/fdfs/client.conf.sample  /etc/fdfs/client.conf
[root@client ~]# vim /etc/fdfs/client.conf

      base_path=/data/fastdfs/client
      tracker_server=192.168.175.101:22122
      tracker_server=192.168.175.102:22122


[root@client ~]# mkdir -pv /data/fastdfs/client
    mkdir: created directory ‘/data’
    mkdir: created directory ‘/data/fastdfs’
    mkdir: created directory ‘/data/fastdfs/client’


[root@client ~]# echo 'hello fdfs' > /tmp/1.txt

// 查看一下 相关命令
[root@client ~]# ls -1 /usr/bin/fdfs_*

      /usr/bin/fdfs_appender_test
      /usr/bin/fdfs_appender_test1
      /usr/bin/fdfs_append_file
      /usr/bin/fdfs_crc32
      /usr/bin/fdfs_delete_file
      /usr/bin/fdfs_download_file
      /usr/bin/fdfs_file_info
      /usr/bin/fdfs_monitor
      /usr/bin/fdfs_storaged
      /usr/bin/fdfs_test
      /usr/bin/fdfs_test1
      /usr/bin/fdfs_trackerd
      /usr/bin/fdfs_upload_appender
      /usr/bin/fdfs_upload_file

// 查看一下命令 fdfs_upload_file 的 usage
[root@client ~]# fdfs_upload_file -h
      Usage: fdfs_upload_file <config_file> <local_filename> [storage_ip:port] [store_path_index]

[root@client ~]# fdfs_upload_file /etc/fdfs/client.conf /tmp/1.txt
    group01/M00/00/00/wKivb114XC2ARIVaAAAAC_u0Yds557.txt   <---------记住该 file_id



// 查看一下命令 fdfs_file_info 的 usage
[root@client ~]# fdfs_file_info -h
      Usage: fdfs_file_info <config_file> <file_id>

// 查看 指定  file_id 对应的 存储信息
[root@client ~]# fdfs_file_info /etc/fdfs/client.conf  group01/M00/00/00/wKivb114XC2ARIVaAAAAC_u0Yds557.txt
      source storage id: 0
      source ip address: 192.168.175.111
      file create timestamp: 2019-09-11 10:30:05
      file size: 11
      file crc32: 4222902747 (0xFBB461DB)


// 在 storage_server01 上查看文件
[root@storage_server01 ~]# ls /data/fastdfs/data/data/00/00/
      wKivb114XC2ARIVaAAAAC_u0Yds557.txt

// 在 storage_server02 上查看文件 (两个 storage_server 上都存在该文件, 则证明已经同步该文件)
[root@storage_server02 ~]# ls /data/fastdfs/data/data/00/00/
      wKivb114XC2ARIVaAAAAC_u0Yds557.txt


[root@storage_server02 ~]# fdfs_download_file -h
      Usage: fdfs_download_file <config_file> <file_id> [local_filename] [<download_offset> <download_bytes>]

[root@client ~]# fdfs_download_file /etc/fdfs/client.conf group01/M00/00/00/wKivb114XC2ARIVaAAAAC_u0Yds557.txt

[root@client ~]# cat wKivb114XC2ARIVaAAAAC_u0Yds557.txt
      hello fdfs


// 使用 fdfs_monitor 显示 观察信息
[root@client ~]# fdfs_monitor /etc/fdfs/client.conf | less

            server_count=2, server_index=1

            tracker server is 192.168.175.102:22122

            group count: 1

            Group 1:
            group name = group01
            disk total space = 18218 MB
            disk free space = 16157 MB
            trunk free space = 0 MB
            storage server count = 2
            active server count = 2
            storage server port = 23000
            storage HTTP port = 8888
            store path count = 1
            subdir count per path = 256
            current write server index = 0
            current trunk file id = 0

                    Storage 1:
                            id = 192.168.175.111
                            ip_addr = 192.168.175.111  ACTIVE
                            http domain =
                            version = 5.12
                            join time = 2019-09-10 22:09:03
            略 略 略 略 略 略












----------------------------------------------------------------------------------------------------
FastDFS+Nginx实现文件服务器

版本对应关系: 来自
    https://blog.csdn.net/qq_34301871/article/details/80060235

      fastdfs 5.11版本对照：Version 5.11对应的fastdfs-nginx-module的Version 1.20
      fastdfs  5.10版本对照：Version 5.10对应的fastdfs-nginx-module的Version 1.19


在所有storage节点上安装nginx及fastdfs-nginx-module模块

如下以 storage_server01 上的 安装为例:


[root@storage_server01 download]# git clone https://github.com/happyfish100/fastdfs-nginx-module.git
[root@storage_server01 download]# cd fastdfs-nginx-module/

// 查看一下 所有版本
[root@storage_server01 fastdfs-nginx-module]# git tag
      V1.20

// 查看 当前 所在版本
[root@storage_server01 fastdfs-nginx-module]# git describe --tags
    V1.20-2-g8796a7d


// 安装 nginx 相关相关依赖
[root@storage_server01 ~]# yum install -y pcre-devel zlib-devel openssl-devel

[root@storage_server01 ~]# cd download/
[root@storage_server01 download]# wget http://nginx.org/download/nginx-1.14.2.tar.gz

[root@storage_server01 download]# tar -xvf nginx-1.14.2.tar.gz
[root@storage_server01 download]# ls
      fastdfs  fastdfs-nginx-module  libfastcommon  nginx-1.14.2  nginx-1.14.2.tar.gz

[root@storage_server01 download]# cd nginx-1.14.2/
[root@storage_server01 nginx-1.14.2]# ./configure --prefix=/app/nginx --add-module=/root/download/fastdfs-nginx-module/src

[root@storage_server01 nginx-1.14.2]# make
[root@storage_server01 nginx-1.14.2]# make install


// 复制fastdfs-nginx-module中的配置文件到/etc/fdfs目录
[root@storage_server01 nginx-1.14.2]# cd
[root@storage_server01 ~]# cp ~/download/fastdfs-nginx-module/src/mod_fastdfs.conf /etc/fdfs/

[root@storage_server01 ~]# vim /etc/fdfs/mod_fastdfs.conf

        tracker_server=192.168.175.101:22122
        tracker_server=192.168.175.102:22122

        group_name=group01
        url_have_group_name = true

        store_path_count=1
        store_path0=/data/fastdfs/data

        [group1]
        group_name=group01
        storage_server_port=23000
        store_path_count=1
        store_path0=/data/fastdfs/data


// 复制fdfs源码目录中的关于http的配置文件
[root@storage_server01 ~]# cp ~/download/fastdfs/conf/mime.types /etc/fdfs/
[root@storage_server01 ~]# cp ~/download/fastdfs/conf/http.conf /etc/fdfs/

// 创建数据存放目录的软链接
[root@storage_server01 ~]# ln -s /data/fastdfs/data/data  /data/fastdfs/data/M00
[root@storage_server01 ~]# ls -l /data/fastdfs/data/
      total 12
      drwxr-xr-x 258 root root 8192 Sep 10 22:09 data
      lrwxrwxrwx   1 root root   23 Sep 11 14:19 M00 -> /data/fastdfs/data/data


// 编辑nginx配置文件, 并启动
[root@storage_server01 ~]# vim /app/nginx/conf/nginx.conf

    server {
        # 注: 此处的端口号应该与文件 /etc/fdfs/storage.conf 中的 设置 'http.server_port=8888' 保持一致
        listen       8888;
        server_name  localhost;

        location ~ /group[0-9][0-9]/M00 {
            ngx_fastdfs_module;
        }

    }

[root@storage_server01 ~]# /app/nginx/sbin/nginx
    ngx_http_fastdfs_set pid=4708


[root@client ~]# curl http://192.168.175.111:8888/group01/M00/00/00/wKivb114XC2ARIVaAAAAC_u0Yds557.txt
      hello fdfs









----------------------------------------------------------------------------------------------------
在Tracker节点上安装nginx

      主要为了提供 http 访问的反向代理、负载均衡以及缓存服务。


// 安装nginx
[root@tracker_server01 ~]# yum install -y pcre-devel zlib-devel openssl-devel
[root@tracker_server01 ~]# cd download/
[root@tracker_server01 download]# wget http://nginx.org/download/nginx-1.14.2.tar.gz
[root@tracker_server01 download]# tar -xvf nginx-1.14.2.tar.gz
[root@tracker_server01 download]# ls
      fastdfs  libfastcommon  nginx-1.14.2  nginx-1.14.2.tar.gz

[root@tracker_server01 download]# cd nginx-1.14.2/
[root@tracker_server01 nginx-1.14.2]# ./configure --prefix=/app/nginx
[root@tracker_server01 nginx-1.14.2]# make
[root@tracker_server01 nginx-1.14.2]# make install


// 编辑nginx配置文件实现负载均衡
[root@tracker_server01 nginx-1.14.2]# vim /app/nginx/conf/nginx.conf

          upstream fdfs_group01 {
              server 192.168.175.111:8888 weight=1 max_fails=2 fail_timeout=2;
              server 192.168.175.112:8888 weight=1 max_fails=2 fail_timeout=2;
          }

          server {
              listen       8000;
              server_name  localhost;


              location /group01/M00 {
                  proxy_pass http://fdfs_group01;
              }
          }


[root@tracker_server01 nginx-1.14.2]# /app/nginx/sbin/nginx
[root@tracker_server01 nginx-1.14.2]# netstat -anptu | grep nginx
      tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      4474/nginx: master


// 测试通过tracker访问文件内容
[root@client ~]# curl http://192.168.175.101:8000/group01/M00/00/00/wKivb114XC2ARIVaAAAAC_u0Yds557.txt
      hello fdfs



















----------------------------------------------------------------------------------------------------
其他资料:

    https://github.com/happyfish100/fastdfs-client-java














