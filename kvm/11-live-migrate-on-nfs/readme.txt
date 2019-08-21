

[root@nfs_server ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
192.168.175.111/24

// 安装 nfs-utils
[root@nfs_server ~]# yum -y install nfs-utils


// 启动并设置开机自启
[root@nfs_server ~]# systemctl start nfs-server
[root@nfs_server ~]# systemctl enable nfs-server

[root@nfs_server ~]# netstat -anptu | grep 2049
[root@nfs_server ~]# netstat -aptu  | grep nfs


// 准备目录并导出
[root@nfs_server ~]# mkdir /kvm_images
[root@nfs_server ~]# chmod o+w /kvm_images


[root@nfs_server ~]# vim /etc/exports

      # man 5 exports   #/EXAMPLE
      # exportfs -rav   #man exportfs  #/EXAMPLES

      # 示例demo: 注意给目录 /nfs4_share/data/ 合适的权限,包括mount磁盘时提供合适的options
      # /nfs4_share/data/  192.168.175.10(rw,sync,no_root_squash)  192.168.2.0/24(rw,root_squash,anonuid=150,anongid=100)

      # 使用 NFS storage 时 导出时必须加 sync 参数
      #    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-kvm_live_migration-shared_storage_example_nfs_for_a_simple_migration
      # it is required that the synch parameter is enabled. This is required for proper export of the NFS storage.
      /kvm_images 192.168.175.40(rw,no_root_squash,sync) 192.168.175.50(rw,no_root_squash,sync)


// 重新导出 配置中的 所有 文件系统
[root@nfs_server ~]# exportfs -rav
    exporting 192.168.175.40:/kvm_images
    exporting 192.168.175.50:/kvm_images


      # 注: 如果要关闭 导出的 配置中的所有文件系统, 可以使用命令 `exportfs -auv`










