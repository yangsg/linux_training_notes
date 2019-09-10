

网上资料:
    fastdfs 的安装部署:
        https://www.cnblogs.com/Yin-BloodMage/p/5480608.html
        https://www.jianshu.com/p/1de9b0383bb9
        https://www.iteye.com/blog/liuyieyer-2065562



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


tracker_server01    192.168.175.101
tracker_server02    192.168.175.102
storage_server01    192.168.175.111
storage_server02    192.168.175.112


----------------------------------------------------------------------------------------------------
在所有节点安装fastdfs软件, 即在如下 4 台 servers 上分别安装 fastdfs 软件
          tracker_server01
          tracker_server02
          storage_server01
          storage_server02


// 此处以 tracker_server01 上安装 fastdfs 为例
// 构建基础编译环境
[root@tracker_server01 ~]# yum -y install gcc gcc-c++ autoconf automak

[root@tracker_server01 ~]# mkdir download
[root@tracker_server01 ~]# cd download/

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


----------------------------------------------------------------------------------------------------
查看观察一下 相关的目录

[root@tracker_server01 ~]# ls /etc/fdfs/
      client.conf.sample  storage.conf.sample  storage_ids.conf.sample  tracker.conf.sample

[root@tracker_server01 ~]# ls /etc/init.d/
      fdfs_storaged  fdfs_trackerd  functions  netconsole  network  README


----------------------------------------------------------------------------------------------------
设置 tracker_server01

[root@tracker_server01 ~]# cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf



































