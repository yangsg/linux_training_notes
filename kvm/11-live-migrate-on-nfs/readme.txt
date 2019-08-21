
----------------------------------------------------------------------------------------------------
准备 一台独立的 nfs server 用于共享存储


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

----------------------------------------------------------------------------------------------------
准备 两台 安装了 kvm 的 host 主机

--------------------------------------------------
// 准备 主机 kvm_src_host

        参考 https://github.com/yangsg/linux_training_notes/tree/master/kvm


本例是 在 VMware® Workstation 15 Pro 上的 以 minimal 方式安装的 centos7.4 上安装 kvm

https://www.linuxtechi.com/install-kvm-hypervisor-on-centos-7-and-rhel-7/

// 启用 vmware 的 virtual matchine 中的 cpu 的 虚拟化支持功能:
右键 该 centos7.4 对应的虚拟主机 -> [设置...] -> [处理器] -> 勾选上[虚拟化 Intel VT-x/EPT 或 AMD-V/RVI(V)]


// 查看主机信息
[root@kvm_src_host ~]# uname -a
    Linux kvm_src_host 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

[root@kvm_src_host ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)

// 查看 CPU 是否支持 Hardware Virtualization
[root@kvm_src_host ~]# grep -E '(vmx|svm)' /proc/cpuinfo

// 或 使用如下方式查看 (此例仅针对 intel 的 cpu)
[root@kvm_src_host ~]# lscpu | grep VT-x
    Virtualization:        VT-x



https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-installing_the_virtualization_packages-installing_virtualization_packages_on_an_existing_red_hat_enterprise_linux_system

// 安装 kvm 相关的 packages
[root@kvm_src_host ~]# yum -y install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install virt-viewer bridge-utils libguestfs-tools

注: libguestfs-tools 包 中包含工具如 guestfish 等 可以
    在 Guest虚拟机处于 shutdown 状态时直接修改 Guest虚拟机的文件系统中的文件,对于自动化配置IP时很有用.

[root@kvm_src_host ~]# systemctl start libvirtd
[root@kvm_src_host ~]# systemctl enable libvirtd
[root@kvm_src_host ~]# systemctl status libvirtd

// 查看模块是否被 loaded
[root@kvm_src_host ~]# lsmod | grep kvm
    kvm_intel             170086  0
    kvm                   566340  1 kvm_intel
    irqbypass              13503  1 kvm


// In Case you have Minimal CentOS 7 and RHEL 7 installation , then virt-manger will not start for that you need to install x-window package.
[root@kvm_src_host ~]# yum -y install "@X Window System" xorg-x11-xauth xorg-x11-fonts-* xorg-x11-utils

// 重新启动 host
[root@kvm_src_host ~]# reboot

// 通过 xshell 远程登录 到 host 主机, 再执行 命令 virt-manager 可打开其 图形管理终端
      不过需要先配置 xshell 支持 x11 forwarding 功能:  [文件] -> [属性] -> [连接] -> [ssh] -> [隧道] -> 分别选中 [转发X11连接到] 和 [Xmanager]
[c:\~]$ ssh root@192.168.175.40
[root@kvm_src_host ~]# virt-manager


--------------------------------------------------
按类似如上相同的方式 准备主机 kvm_dst_host




--------------------------------------------------
在主机 kvm_src_host 上 准备基于 nfs 的 storage pool 及 其他相应环境

// 创建挂载点(注意 主机 kvm_src_host 和 kvm_dst_host 的挂载点路径要保持一致)
[root@kvm_src_host ~]# mkdir /opt/kvm

[root@kvm_src_host ~]# showmount -e 192.168.175.111
    Export list for 192.168.175.111:
    /kvm_images 192.168.175.50,192.168.175.40

[root@kvm_src_host ~]# vim /etc/libvirt/storage/my_nfs_shared_storage_pool.xml

    <pool type='netfs'>
      <name>my_nfs_shared_storage_pool</name>
      <uuid>cfb1dac9-396d-40b2-aae2-3c05daa7153c</uuid>
      <capacity unit='bytes'>0</capacity>
      <allocation unit='bytes'>0</allocation>
      <available unit='bytes'>0</available>
      <source>
        <host name='192.168.175.111'/>
        <dir path='/kvm_images'/>
        <format type='auto'/>
      </source>
      <target>
        <path>/opt/kvm</path>
      </target>
    </pool>

[root@kvm_src_host ~]# virsh pool-define /etc/libvirt/storage/my_nfs_shared_storage_pool.xml
[root@kvm_src_host ~]# virsh pool-start my_nfs_shared_storage_pool
[root@kvm_src_host ~]# virsh pool-autostart my_nfs_shared_storage_pool

[root@kvm_src_host ~]# virsh pool-list

     Name                 State      Autostart
    -------------------------------------------
     default              active     yes
     my_nfs_shared_storage_pool active     yes  <------


[root@kvm_src_host ~]# df -hT | grep '/opt/kvm'

    192.168.175.111:/kvm_images nfs4       18G  1.9G   16G  11% /opt/kvm


// (可选) 测试一下 nfs 共享目录是否可以正常写入
[root@kvm_src_host ~]# touch /opt/kvm/a.txt
[root@kvm_src_host ~]# rm /opt/kvm/a.txt
      rm: remove regular empty file ‘/opt/kvm/a.txt’? y

// 将 待迁移的 Guest 虚拟机安装到 共享存储目录
[root@kvm_src_host ~]# virt-install \
  --name vm01-centos7.4-64 \
  --graphics vnc,listen=0.0.0.0,port=5920,keymap=en_us \
  --memory 512,maxmemory=1024 \
  --vcpus 1,maxvcpus=2 \
  --disk path=/opt/kvm/vm01-centos7.4-64.img,size=8,format=qcow2 \
  --network bridge=virbr0 \
  --cdrom /tmp/CentOS-7.4-x86_64-Everything-1708.iso

[root@kvm_src_host ~]# virsh start vm01-centos7.4-64
    Domain vm01-centos7.4-64 started


// 添加主机名解析
[root@kvm_src_host ~]# vim /etc/hosts
    192.168.175.40  kvm_src_host
    192.168.175.50  kvm_dst_host



----------------------------------------------------------------------------------------------------
准备 kvm_dst_host 相应环境


// 添加主机名解析
[root@kvm_dst_host ~]# vim /etc/hosts
    192.168.175.40  kvm_src_host
    192.168.175.50  kvm_dst_host

// 创建挂载点(注意 主机 kvm_src_host 和 kvm_dst_host 的挂载点路径要保持一致)
[root@kvm_dst_host ~]# mkdir /opt/kvm

[root@kvm_dst_host ~]# showmount -e 192.168.175.111
    Export list for 192.168.175.111:
    /kvm_images 192.168.175.50,192.168.175.40

[root@kvm_dst_host ~]# mount -t nfs 192.168.175.111:/kvm_images /opt/kvm
[root@kvm_dst_host ~]# ls /opt/kvm/
    vm01-centos7.4-64.img


[root@kvm_dst_host ~]# vim /etc/fstab

    192.168.175.111:/kvm_images /opt/kvm            nfs     defaults  0 0


[root@kvm_dst_host ~]# umount /opt/kvm/
[root@kvm_dst_host ~]# mount -a
[root@kvm_dst_host ~]# ls /opt/kvm/
      vm01-centos7.4-64.img




----------------------------------------------------------------------------------------------------
执行 在线迁移操作:

// 先看一下 是否 可以远程连接
[root@kvm_src_host ~]# virsh --connect qemu+ssh://192.168.175.50/system list


// 执行在线迁移
[root@kvm_src_host ~]# virsh migrate --live vm01-centos7.4-64 qemu+ssh://192.168.175.50/system --unsafe

注: 如上命令加 选项 --unsafe  是为了避免如下错误:
      error: Unsafe migration: Migration may lead to data corruption if disks use cache != none or cache != directsync

    对应什么时候需要加 --unsafe 使之强制迁移 可参考如下文字(见 man virsh):
           In some cases libvirt may refuse to migrate the domain because doing so may lead to potential
           problems such as data corruption, and thus the migration is considered unsafe. For QEMU domain, this
           may happen if the domain uses disks without explicitly setting cache mode to "none". Migrating such
           domains is unsafe unless the disk images are stored on coherent clustered filesystem, such as GFS2 or
           GPFS. If you are sure the migration is safe or you just do not care, use --unsafe to force the
           migration.


// 在 kvm_dst_host 上查看  Guest 虚拟机
[root@kvm_dst_host ~]# virsh list --all

       Id    Name                           State
      ----------------------------------------------------
       1     vm01-centos7.4-64              running


// 在 kvm_src_host 上查看  Guest 虚拟机
[root@kvm_src_host ~]# virsh list --all

     Id    Name                           State
    ----------------------------------------------------
     -     vm01-centos7.4-64              shut off


----------------------------------------------------------------------------------------------------

网上资料:

    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-kvm_live_migration-shared_storage_example_nfs_for_a_simple_migration
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-kvm_live_migration-live_kvm_migration_with_virsh
    https://www.server-world.info/en/note?os=Ubuntu_16.04&p=kvm&f=6
    https://www.jb51.net/article/99937.htm

