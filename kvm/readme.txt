

https://en.wikipedia.org/wiki/Virtualization
https://en.wikipedia.org/wiki/Protection_ring


virtualization

相关术语 或 概念(见 wiki):  https://en.wikipedia.org/wiki/Virtualization

---------------------------------------------------------------------------------------------------
Hardware virtualization (或 platform virtualization)

    host machine
    guest machine

    host
    guest

    hypervisor or virtual machine monitor: The software or firmware that creates a virtual machine on the host hardware is called a hypervisor or virtual machine monitor.

        ----------------------------------------------------------------------
        https://en.wikipedia.org/wiki/Hypervisor

            The term hypervisor is a variant of supervisor, a traditional term for the kernel of an operating system:
            the hypervisor is the supervisor of the supervisor,[1] with hyper- used as a stronger variant of super-.[a]
            The term dates to circa 1970;[2] in the earlier CP/CMS (1967) system the term Control Program was used instead.

        hypervisors 的分类:
              Type-1, native or bare-metal hypervisors
                                            |------------------|
                                            |         os       |
                                            |------------------|
                                            |     hypervisor   |
                                            |------------------|
                                            |     hardware     |
                                            |------------------|

                  These hypervisors run directly on the host's hardware to control the hardware and to manage guest operating systems.
                  For this reason, they are sometimes called bare metal hypervisors. The first hypervisors, which IBM developed in the 1960s,
                  were native hypervisors.[4] These included the test software SIMMON and the CP/CMS operating system
                  (the predecessor of IBM's z/VM). Modern equivalents include AntsleOs[5],
                  Xen, XCP-ng, Oracle VM Server for SPARC, Oracle VM Server for x86,
                  Microsoft Hyper-V, Xbox One system software, and VMware ESX/ESXi.
                        ------------------------------------------------------------


              Type-2 or hosted hypervisors

                                            |------------------|
                                            |         os       |
                                            |------------------|
                                            |     hypervisor   |
                                            |------------------|
                                            |         os       |
                                            |------------------|
                                            |     hardware     |
                                            |------------------|

                  These hypervisors run on a conventional operating system (OS) just as other computer programs do.
                  A guest operating system runs as a process on the host. Type-2 hypervisors abstract guest operating systems
                  from the host operating system. VMware Workstation, VMware Player, VirtualBox,
                  Parallels Desktop for Mac and QEMU are examples of type-2 hypervisors.


          这两种类型的区分并不总是 清晰 的:
              The distinction between these two types is not always clear. For instance, Linux's Kernel-based
              Virtual Machine (KVM) and FreeBSD's bhyve are kernel modules[6] that effectively convert
              the host operating system to a type-1 hypervisor.[7] At the same time, since Linux distributions
              and FreeBSD are still general-purpose operating systems, with applications competing with
              each other for VM resources, KVM and bhyve can also be categorized as type-2 hypervisors.[8]

        ----------------------------------------------------------------------

    Different types of hardware virtualization include:
        - Full virtualization – almost complete simulation of the actual hardware to allow a software environments,
                                including a guest operating system and its apps, to run unmodified.
        - Paravirtualization – the guest apps are executed in their own isolated domains, as if they are running on a separate system,
                               but a hardware environment is not simulated. Guest programs need to be specifically modified to run in this environment.

                https://en.wikipedia.org/wiki/Full_virtualization
                https://en.wikipedia.org/wiki/Paravirtualization



    Snapshots
        创建 snapshots 的 工作方式 与 增量备份(incremental backup)的 机制类似.

    Migration
    Failover

    Nested virtualization
        Nested virtualization refers to the ability of running a virtual machine within another,
        having this general concept extendable to an arbitrary depth. In other words,
        nested virtualization refers to running one or more hypervisors inside another hypervisor.


---------------------------------------------------------------------------------------------------
Desktop virtualization

    Desktop virtualization is the concept of separating the logical desktop from the physical machine.

        client -------> data center servers

---------------------------------------------------------------------------------------------------
Containerization

        https://en.wikipedia.org/wiki/OS-level_virtualisation

    Operating-system-level virtualization, also known as containerization, refers to an operating system feature
    in which the kernel allows the existence of multiple isolated user-space instances(多个隔离的用户空间实例).
    Such instances, called containers,[17] partitions, virtual environments (VEs) or jails (FreeBSD jail or chroot jail),
    may look like real computers from the point of view of programs running in them. A computer program
    running on an ordinary operating system can see all resources (connected devices, files and folders, network shares,
    CPU power, quantifiable hardware capabilities) of that computer. However, programs running inside
    a container can only see the container's contents and devices assigned to the container.

---------------------------------------------------------------------------------------------------
Other types  见 wiki

---------------------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------------------
https://en.wikipedia.org/wiki/Hardware-assisted_virtualization

Hardware-assisted virtualization

      In computing, hardware-assisted virtualization is a platform virtualization approach that
      enables efficient full virtualization using help from hardware capabilities,
      primarily from the host processors. Full virtualization is used to simulate
      a complete hardware environment, or virtual machine, in which an unmodified
      guest operating system (using the same instruction set as the host machine)
      effectively executes in complete isolation. Hardware-assisted virtualization
      was added to x86 processors (Intel VT-x or AMD-V) in 2005 and 2006 (respectively).

      Hardware-assisted virtualization is also known as accelerated virtualization;
      Xen calls it hardware virtual machine (HVM), and Virtual Iron calls it native virtualization.


---------------------------------------------------------------------------------------------------

https://en.wikipedia.org/wiki/X86_virtualization

x86 virtualization

Software-based virtualization
    特权指令问题:
      In protected mode the operating system kernel runs at a higher privilege such as ring 0,
      and applications at a lower privilege such as ring 3.[citation needed] In software-based virtualization,
      a host OS has direct access to hardware while the guest OSs have limited access to hardware,
      just like any other application of the host OS. One approach used in x86 software-based
      virtualization to overcome this limitation is called ring deprivileging,
      which involves running the guest OS at a ring higher (lesser privileged) than 0.



Hardware-assisted virtualization

第一代 x86 hardware virtualization 解决了 特权指令的问题.

    In 2005 and 2006, Intel and AMD (working independently) created new processor extensions to the x86 architecture.
    The first generation of x86 hardware virtualization addressed the issue of privileged instructions(特权指令).
    The issue of low performance of virtualized system memory was addressed
    with MMU virtualization that was added to the chipset later.

--------------------
AMD-V: AMD Virtualization

      AMD virtualization (AMD-V):

          AMD developed its first generation virtualization extensions under the code name "Pacifica",
          and initially published them as AMD Secure Virtual Machine (SVM),[16]
          but later marketed them under the trademark AMD Virtualization, abbreviated AMD-V.

          The CPU flag for AMD-V is "svm". This may be checked in BSD derivatives via dmesg or sysctl and in Linux via /proc/cpuinfo


--------------------
Intel (VT-x): VT-x represents Intel's technology for virtualization on the x86 platform.

      Intel virtualization (VT-x):

          Previously codenamed "Vanderpool", VT-x represents Intel's technology for virtualization on the x86 platform.
          On November 13, 2005, Intel released two models of Pentium 4 (Model 662 and 672) as the first
          Intel processors to support VT-x. The CPU flag for VT-x capability is "vmx"; in Linux,
          this can be checked via /proc/cpuinfo, or in macOS via sysctl machdep.cpu.features.[19]

          As of 2015, almost all newer server, desktop and mobile Intel processors support VT-x,
          with some of the Intel Atom processors as the primary exception.[21] With some motherboards,
          users must enable Intel's VT-x feature in the BIOS setup before applications can make use of it.[22]


---------------------------------------------------------------------------------------------------




---------------------------------------------------------------------------------------------------








---------------------------------------------------------------------------------------------------
kvm

本例是 在 VMware® Workstation 15 Pro 上的 以 minimal 方式安装的 centos7.4 上安装 kvm

https://www.linuxtechi.com/install-kvm-hypervisor-on-centos-7-and-rhel-7/

// 启用 vmware 的 virtual matchine 中的 cpu 的 虚拟化支持功能:
右键 该 centos7.4 对应的虚拟主机 -> [设置...] -> [处理器] -> 勾选上[虚拟化 Intel VT-x/EPT 或 AMD-V/RVI(V)]




// 查看主机信息
[root@host ~]# uname -a
Linux host 3.10.0-693.el7.x86_64 #1 SMP Tue Aug 22 21:09:27 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

[root@host ~]# cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core)


// 查看 CPU 是否支持 Hardware Virtualization
[root@host ~]# grep -E '(vmx|svm)' /proc/cpuinfo

// 或 使用如下方式查看 (此例仅针对 intel 的 cpu)
[root@host ~]# lscpu | grep VT-x
    Virtualization:        VT-x


// 安装 kvm 相关的 packages
[root@host ~]# yum -y install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install virt-viewer bridge-utils


[root@host ~]# systemctl start libvirtd
[root@host ~]# systemctl enable libvirtd
[root@host ~]# systemctl status libvirtd

        ● libvirtd.service - Virtualization daemon
           Loaded: loaded (/usr/lib/systemd/system/libvirtd.service; enabled; vendor preset: enabled)
           Active: active (running) since Wed 2019-08-14 00:48:59 CST; 4min 2s ago
             Docs: man:libvirtd(8)
                   https://libvirt.org
         Main PID: 2184 (libvirtd)
           CGroup: /system.slice/libvirtd.service
                   ├─2184 /usr/sbin/libvirtd
                   ├─2286 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/usr/libexec/libvirt_leaseshelper
                   └─2287 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/usr/libexec/libvirt_leaseshelper

        Aug 14 00:48:59 host systemd[1]: Started Virtualization daemon.
        Aug 14 00:49:00 host dnsmasq[2286]: started, version 2.76 cachesize 150
        Aug 14 00:49:00 host dnsmasq[2286]: compile time options: IPv6 GNU-getopt DBus no-i18n IDN DHCP DHCPv6 no-Lua TFTP no-conntrack ipset auth no-DNSSEC loop-detect inotify
        Aug 14 00:49:00 host dnsmasq-dhcp[2286]: DHCP, IP range 192.168.122.2 -- 192.168.122.254, lease time 1h
        Aug 14 00:49:00 host dnsmasq-dhcp[2286]: DHCP, sockets bound exclusively to interface virbr0
        Aug 14 00:49:00 host dnsmasq[2286]: reading /etc/resolv.conf
        Aug 14 00:49:00 host dnsmasq[2286]: using nameserver 192.168.175.2#53
        Aug 14 00:49:00 host dnsmasq[2286]: read /etc/hosts - 2 addresses
        Aug 14 00:49:00 host dnsmasq[2286]: read /var/lib/libvirt/dnsmasq/default.addnhosts - 0 addresses
        Aug 14 00:49:00 host dnsmasq-dhcp[2286]: read /var/lib/libvirt/dnsmasq/default.hostsfile


// 查看模块是否被 loaded
[root@host ~]# lsmod | grep kvm

      kvm_intel             170086  0
      kvm                   566340  1 kvm_intel
      irqbypass              13503  1 kvm

// In Case you have Minimal CentOS 7 and RHEL 7 installation , then virt-manger will not start for that you need to install x-window package.
[root@host ~]# yum -y install "@X Window System" xorg-x11-xauth xorg-x11-fonts-* xorg-x11-utils


// 通过 xshell 远程登录 到 host 主机, 再执行 命令 virt-manager 可打开其 图形管理终端
      不过需要先配置 xshell 支持 x11 forwarding 功能:  [文件] -> [属性] -> [连接] -> [ssh] -> [隧道] -> 分别选中 [转发X11连接到] 和 [Xmanager]
[c:\~]$ ssh root@192.168.175.30
[root@host ~]# virt-manager




---------------------------------------------------------------------------------------------------

[root@host ~]# ip a
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever
      2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
          link/ether 00:0c:29:ba:d6:a5 brd ff:ff:ff:ff:ff:ff
          inet 192.168.175.30/24 brd 192.168.175.255 scope global ens33
             valid_lft forever preferred_lft forever
          inet6 fe80::20c:29ff:feba:d6a5/64 scope link
             valid_lft forever preferred_lft forever
      3: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN qlen 1000
          link/ether 52:54:00:4e:4b:68 brd ff:ff:ff:ff:ff:ff
          inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
             valid_lft forever preferred_lft forever
      4: virbr0-nic: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast master virbr0 state DOWN qlen 1000
          link/ether 52:54:00:4e:4b:68 brd ff:ff:ff:ff:ff:ff



[root@host ~]# cat /proc/sys/net/ipv4/ip_forward
    1


[root@host ~]# iptables -t nat -nL
        Chain PREROUTING (policy ACCEPT)
        target     prot opt source               destination

        Chain INPUT (policy ACCEPT)
        target     prot opt source               destination

        Chain OUTPUT (policy ACCEPT)
        target     prot opt source               destination

        Chain POSTROUTING (policy ACCEPT)
        target     prot opt source               destination
        RETURN     all  --  192.168.122.0/24     224.0.0.0/24
        RETURN     all  --  192.168.122.0/24     255.255.255.255
        MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
        MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
        MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24


---------------------------------------------------------------------------------------------------
使用 命令 virt-install

// 可以查阅 更多 详细信息
[root@host ~]# man virt-install

// 通过 --option=? 的形式可以查看 对应 argument 的  sub options
[root@host ~]# virt-install --disk=?

// 在 kvm 上 安装 一个 centos7.4 操作系统
[root@host ~]# virt-install \
  --name vm01-centos7.4-64 \
  --graphics vnc,listen=0.0.0.0,port=5920,keymap=en_us \
  --memory 512,maxmemory=1024 \
  --vcpus 1,maxvcpus=2 \
  --disk path=/var/lib/libvirt/images/vm01-centos7.4-64.img,size=8,format=qcow2 \
  --network bridge=virbr0 \
  --cdrom /tmp/CentOS-7.4-x86_64-Everything-1708.iso



安装完成后重启, 查看相关进程:
[root@host ~]# ps -elf | grep qemu-kvm
        6 S qemu       2600      1  2  80   0 - 462041 poll_s 13:36 ?       00:01:48 /usr/libexec/qemu-kvm -name vm01-centos7.4-64 -S -machine pc-i440fx-rhel7.0.0,accel=kvm,usb=off,dump-guest-core=off -cpu Broadwell-IBRS,-hle,-rtm -m 1024 -realtime mlock=off -smp 1,maxcpus=2,sockets=2,cores=1,threads=1 -uuid b06b39da-30ca-4905-be1c-e3db5783bed8 -no-user-config -nodefaults -chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/domain-5-vm01-centos7.4-64/monitor.sock,server,nowait -mon chardev=charmonitor,id=monitor,mode=control -rtc base=utc,driftfix=slew -global kvm-pit.lost_tick_policy=delay -no-hpet -no-shutdown -global PIIX4_PM.disable_s3=1 -global PIIX4_PM.disable_s4=1 -boot strict=on -device ich9-usb-ehci1,id=usb,bus=pci.0,addr=0x4.0x7 -device ich9-usb-uhci1,masterbus=usb.0,firstport=0,bus=pci.0,multifunction=on,addr=0x4 -device ich9-usb-uhci2,masterbus=usb.0,firstport=2,bus=pci.0,addr=0x4.0x1 -device ich9-usb-uhci3,masterbus=usb.0,firstport=4,bus=pci.0,addr=0x4.0x2 -device virtio-serial-pci,id=virtio-serial0,bus=pci.0,addr=0x5 -drive file=/var/lib/libvirt/images/vm01-centos7.4-64.img,format=qcow2,if=none,id=drive-virtio-disk0 -device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x6,drive=drive-virtio-disk0,id=virtio-disk0,bootindex=1 -drive if=none,id=drive-ide0-0-0,readonly=on -device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0 -netdev tap,fd=26,id=hostnet0,vhost=on,vhostfd=28 -device virtio-net-pci,netdev=hostnet0,id=net0,mac=52:54:00:ad:ce:4e,bus=pci.0,addr=0x3 -chardev pty,id=charserial0 -device isa-serial,chardev=charserial0,id=serial0 -chardev socket,id=charchannel0,path=/var/lib/libvirt/qemu/channel/target/domain-5-vm01-centos7.4-64/org.qemu.guest_agent.0,server,nowait -device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=org.qemu.guest_agent.0 -device usb-tablet,id=input0,bus=usb.0,port=1 -vnc 0.0.0.0:20 -k en-us -vga cirrus -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x7 -object rng-random,id=objrng0,filename=/dev/urandom -device virtio-rng-pci,rng=objrng0,id=rng0,bus=pci.0,addr=0x8 -msg timestamp=on


---------------------------------------------------------------------------------------------------

[root@host ~]# man virsh   # Virtual Shell

[root@host ~]# virsh list    #list domains
 Id    Name                           State
 ----------------------------------------------------
  5     vm01-centos7.4-64              running

[root@host ~]# virsh list --all   #list inactive & active domains
 Id    Name                           State
----------------------------------------------------
 5     vm01-centos7.4-64              running


// 如果直接 键入 virsh, 可以进入 virsh 的 交互模式
[root@host ~]# virsh
        Welcome to virsh, the virtualization interactive terminal.

        Type:  'help' for help with commands
               'quit' to quit

        virsh # help list
          NAME
            list - list domains

--------------------------------------------------
如下是连接 GuestOS 的 各种方式 (注: 通过 console 连接方式的配置针对 centos6 和 centos7 略有不同, 因为其采用的Grub的版本不同)


      ------------------------------
      连接方式 1): 通过 virt-manager, 然后加 图形界面选中对应的 Guest Machine, 并 点击 Open 工具按钮
      [root@host ~]# virt-manager


      ------------------------------
      连接方式 2): 通过 virt-viewer
      [root@host ~]# virt-viewer vm01-centos7.4-64

      ------------------------------
      连接方式 3): 通过 vncviewer

      [root@host ~]# yum provides '*bin/vncviewer'
      [root@host ~]# yum -y install tigervnc
      [root@host ~]# man vncviewer

      [root@host ~]# ps -elf | grep qemu-kvm | grep -E -o -- '-vnc[[:space:]]+[[:digit:]\.]+:[[:digit:]]+'
            -vnc 0.0.0.0:20

      [root@host ~]# netstat -anptu | grep qemu-kvm
            tcp        0      0 0.0.0.0:5920            0.0.0.0:*               LISTEN      6021/qemu-kvm

      // 使用 vncviewer 连接 GuestOS
      [root@host ~]# vncviewer 192.168.175.30:5920

                  按 F8 可以 显示 the context menu

          当然, 通过 windows 操作系统 上的 'VNC Viewer' 客户端软件也是可以连接的


      ------------------------------
      连接方式 4): 通过 console 方式 连接 kvm 安装的 centos7 (此例仅正对 centos7, 因centos7 采用grub2)

      // 编辑 grub 的参数配置文件
      [root@localhost ~]# vim /etc/sysconfig/grub
            GRUB_CMDLINE_LINUX="rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet console=ttyS0"

      // 重做(remake) grub2的配置文件
      [root@localhost ~]# grub2-mkconfig -o /boot/grub2/grub.cfg
      [root@localhost ~]# reboot


      [root@host ~]# virsh console vm01-centos7.4-64

              Connected to domain vm01-centos7.4-64
              Escape character is ^]
                  <======================= 直接回车
              CentOS Linux 7 (Core)
              Kernel 3.10.0-693.el7.x86_64 on an x86_64

              localhost login: root
              Password:
              Last login: Wed Aug 14 17:03:19 on ttyS0
              [root@localhost ~]# exit
              logout

              CentOS Linux 7 (Core)
              Kernel 3.10.0-693.el7.x86_64 on an x86_64

              localhost login: <======================= 按 Ctrl + ] 返回到 HostOS



---------------------------------------------------------------------------------------------------

kvm 中,
从动态的角度看, 活动的 virtual machine 对应于 一个 qemu-kvm 进程,
从静态的角度看, virtual machine = 配置文件 + 磁盘文件


[root@host ~]# ls /var/lib/libvirt/images/
    vm01-centos7.4-64.img

[root@host ~]# ls -l /var/lib/libvirt/images/
    -rw------- 1 qemu qemu 8591507456 Aug 14 18:03 vm01-centos7.4-64.img

[root@host ~]# tree -L 1 /var/lib/libvirt/

          /var/lib/libvirt/
          ├── boot
          ├── dnsmasq
          ├── filesystems
          ├── images  <----------
          ├── lxc
          ├── network
          ├── qemu      (Quick Emulator)
          └── swtpm


[root@host ~]# tree -L 1 /etc/libvirt/
          /etc/libvirt/
          ├── libvirt-admin.conf
          ├── libvirt.conf
          ├── libvirtd.conf
          ├── lxc.conf
          ├── nwfilter
          ├── qemu     <----------
          ├── qemu.conf
          ├── qemu-lockd.conf
          ├── secrets
          ├── storage  <----------
          ├── virtlockd.conf
          └── virtlogd.conf

[root@host ~]# ls /etc/libvirt/qemu
      networks  vm01-centos7.4-64.xml  <--- 这里的 xml 文件为现有的 虚拟机的 配置文件
               注: 如果需要修改配置,不要手动直接修改(如用vim)这些配置文件, 而应通过 virsh edit <domain> 这种方式来修改


    --------------------------------------------------------------------------------
    |设置开机自启的语法:   virsh autostart [--disable] domain
    |                       Configure a domain to be automatically started at boot.
    |
    |                       The option --disable disables autostarting.
    --------------------------------------------------------------------------------


[root@host ~]# virsh help

[root@host ~]# virsh list
 Id    Name                           State
----------------------------------------------------
 7     vm01-centos7.4-64              running

// 设置 虚拟客户机(即 Domain) 开机 自动启动 (其实就是在 /etc/libvirt/qemu/autostart/ 目录下为 指定的虚拟机建立配置文件的软连接文件)
[root@host ~]# virsh autostart vm01-centos7.4-64
      Domain vm01-centos7.4-64 marked as autostarted

[root@host ~]# ls -l /etc/libvirt/qemu/autostart/
    lrwxrwxrwx 1 root root 39 Aug 14 19:35 vm01-centos7.4-64.xml -> /etc/libvirt/qemu/vm01-centos7.4-64.xml




---------------------------------------------------------------------------------------------------

[root@host ~]# virsh help | grep list
    domblklist                     list all domain blocks
    domiflist                      list all domain virtual interfaces
    list                           list domains
    iface-list                     list physical host interfaces
    nwfilter-list                  list network filters
    nwfilter-binding-list          list network filter bindings
    net-list                       list networks
    nodedev-list                   enumerate devices on this host
    secret-list                    list secrets
    snapshot-list                  List snapshots for a domain
    pool-list                      list pools
    vol-list                       list vols

[root@host libvirt]# virsh help | grep edit
    edit                           edit XML configuration for a domain
    managedsave-edit               edit XML for a domain's managed save state file
    save-image-edit                edit XML for a domain's saved state file
    iface-edit                     edit XML configuration for a physical host interface
    nwfilter-edit                  edit XML configuration for a network filter
    net-edit                       edit XML configuration for a network
    snapshot-edit                  edit XML for a snapshot
    pool-edit                      edit XML configuration for a storage pool


------------------------------
// 查看 网络 相关 信息 和 配置文件
[root@host ~]# virsh net-list
     Name                 State      Autostart     Persistent
    ----------------------------------------------------------
     default              active     yes           yes

[root@host ~]# ls /etc/libvirt/qemu/networks/
      autostart  default.xml <--- 该 xml 为网络的配置文件

[root@host ~]# ls -l /etc/libvirt/qemu/networks/autostart/
      lrwxrwxrwx 1 root root 14 Aug 14 00:40 default.xml -> ../default.xml



------------------------------
// 查看 存储(storage) 相关 信息 和 配置文件
[root@host ~]# virsh pool-list   #查看存储(storage)池

     Name                 State      Autostart
    -------------------------------------------
     default              active     yes
     root                 active     yes
     tmp                  active     yes


[root@host ~]# ls /etc/libvirt/storage/
      autostart  default.xml  root.xml  tmp.xml

[root@host ~]# ls -l /etc/libvirt/storage/autostart/

      lrwxrwxrwx 1 root root 32 Aug 14 01:00 default.xml -> /etc/libvirt/storage/default.xml
      lrwxrwxrwx 1 root root 29 Aug 14 12:59 root.xml -> /etc/libvirt/storage/root.xml
      lrwxrwxrwx 1 root root 28 Aug 14 13:11 tmp.xml -> /etc/libvirt/storage/tmp.xml





------------------------------
[root@host ~]# virsh domblklist vm01-centos7.4-64   # Get device block stats for a running domain.
      Target     Source
      ------------------------------------------------
      vda        /var/lib/libvirt/images/vm01-centos7.4-64.img
      hda        -



---------------------------------------------------------------------------------------------------
kvm cpu 热添加: 动态调整(添加) cpu 个数

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-managing_guest_virtual_machines_with_virsh-displaying_per_guest_virtual_machine_information#sect-Displaying_per_guest_virtual_machine_information-Configuring_virtual_CPU_count


    注: 如果要添加 cpu, 最稳妥的做法还是在 关机的时候 静态添加

  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-managing_guest_virtual_machines_with_virsh-displaying_per_guest_virtual_machine_information#sect-Displaying_per_guest_virtual_machine_information-Configuring_virtual_CPU_count
  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/7.0_release_notes/chap-red_hat_enterprise_linux-7.0_release_notes-virtualization

  https://serverfault.com/questions/457250/kvm-and-libvirt-how-do-i-hotplug-a-new-virtio-disk/457259
  https://www.unixarena.com/2015/12/linux-kvm-how-to-add-remove-vcpu-to-guest-on-fly.html/


前提: 设置 cpu 最大个数
      仅针对 centos7 以上的系统

        重要提示: Hot unplugging vCPUs is not supported on Red Hat Enterprise Linux 7.

[root@host ~]# virsh help | grep info
    domfsinfo                      Get information of domain's mounted filesystems.
    domjobinfo                     domain job information
    dumpxml                        domain information in XML
    iothreadinfo                   view domain IOThreads
    managedsave-dumpxml            Domain information of managed save state file in XML
    save-image-dumpxml             saved state domain information in XML
    schedinfo                      show/set scheduler parameters
    vcpuinfo                       detailed domain vcpu information
    domblkinfo                     domain block device size information
    dominfo                        domain information
    nodeinfo                       node information
    sysinfo                        print the hypervisor sysinfo
    iface-dumpxml                  interface information in XML
    nwfilter-dumpxml               network filter information in XML
    nwfilter-binding-dumpxml       network filter information in XML
    net-dhcp-leases                print lease info for a given network
    net-dumpxml                    network information in XML
    net-info                       network information
    snapshot-info                  snapshot information
    pool-dumpxml                   pool information in XML
    pool-info                      storage pool information
    vol-dumpxml                    vol information in XML
    vol-info                       storage vol information


[root@host ~]# virsh dumpxml vm01-centos7.4-64  | grep -in vcpu
      6:  <vcpu placement='static' current='1'>2</vcpu>   <---- 当前虚拟 cpu 个数为 1, 最大个数为 2


[root@host ~]# virsh dominfo vm01-centos7.4-64
    Id:             1
    Name:           vm01-centos7.4-64
    UUID:           b06b39da-30ca-4905-be1c-e3db5783bed8
    OS Type:        hvm
    State:          running
    CPU(s):         1      <---- 当前 vcpu 个数
    CPU time:       33.0s
    Max memory:     1048576 KiB
    Used memory:    524288 KiB
    Persistent:     yes
    Autostart:      enable
    Managed save:   no
    Security model: none
    Security DOI:   0


子命令 setvcpus 的语法格式:  virsh setvcpus {domain-name, domain-id or domain-uuid} count [[--config] [--live] | [--current]] [--maximum] [--guest]

选项说明:
    --config: If the --config flag is specified, the change is made to the stored XML configuration
              for the guest virtual machine, and will only take effect when the guest is started.

    --live: If --live is specified, the guest virtual machine must be active, and the change takes place immediately.
            This option will allow hot plugging of a vCPU.
            Both the --config and --live flags may be specified together if supported by the hypervisor.

    --current: If --current is specified, the flag affects the current guest virtual machine state.

        When no flags are specified, the --live flag is assumed. The command will fail if
        the guest virtual machine is not active. In addition, if no flags are specified,
        it is up to the hypervisor whether the --config flag is also assumed.
        This determines whether the XML configuration is adjusted to make the change persistent.

    --maximum: The --maximum flag controls the maximum number of virtual CPUs that can be hot-plugged
               the next time the guest virtual machine is booted. Therefore,
               it can only be used with the --config flag, not with the --live flag.

        Note that count cannot exceed the number of CPUs assigned to the guest virtual machine.

    --guest: If --guest is specified, the flag modifies the CPU state in the current guest virtual machine.


// 热添加 vcpu 个数 为 2
[root@host ~]# virsh setvcpus vm01-centos7.4-64 2 --live

[root@host ~]# virsh dominfo vm01-centos7.4-64
    Id:             1
    Name:           vm01-centos7.4-64
    UUID:           b06b39da-30ca-4905-be1c-e3db5783bed8
    OS Type:        hvm
    State:          running
    CPU(s):         2      <---- 当前 vcpu 个数 (注: 实际是否真实生效最好还是在 GuestOS 中执行 lscpu 命令实际确认一下)
    CPU time:       38.1s
    Max memory:     1048576 KiB
    Used memory:    524288 KiB
    Persistent:     yes
    Autostart:      enable
    Managed save:   no
    Security model: none
    Security DOI:   0

// 显示 vcpu 信息
[root@host ~]# virsh vcpuinfo vm01-centos7.4-64
      VCPU:           0
      CPU:            1
      State:          running
      CPU time:       33.5s
      CPU Affinity:   yy

      VCPU:           1
      CPU:            1
      State:          running
      CPU time:       1.1s
      CPU Affinity:   yy


---------------------------------------------------------------------------------------------------
kvm 内存气球技术:  在线调整内存大小

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-manipulating_the_domain_xml-devices#sect-Devices-Memory_balloon_device
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-managing_guest_virtual_machines_with_virsh-displaying_per_guest_virtual_machine_information#sect-Displaying_per_guest_virtual_machine_information-Configuring_virtual_CPU_count


    前提: 最大内存量

// 确认虚拟机支持内存气球的驱动
[root@host ~]# virsh dumpxml vm01-centos7.4-64  | grep -C 2 memballoon

      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>  <------- 观察这里
      <alias name='balloon0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </memballoon>
    <rng model='virtio'>
      <backend model='random'>/dev/urandom</backend>

// 查看内存设置信息
[root@host ~]# virsh dumpxml vm01-centos7.4-64  | grep -in 'memory'
      4:  <memory unit='KiB'>1048576</memory>   <----- 最大内存, 可通过命令 virsh setmaxmem 修改
      5:  <currentMemory unit='KiB'>524288</currentMemory> <---- 当前内存, 可通过命令 virsh setmem 修改

    命令 virsh setmem 的用法见 `virsh help setmem` 或 `man virsh` 或 见:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-Managing_guest_virtual_machines_with_virsh-Displaying_per_guest_virtual_machine_information#sect-Displaying_per_guest_virtual_machine_information-Configuring_memory_allocation

    命令 virsh setmaxmem 的用法见 `virsh help setmaxmem` 或 `man virsh` 或 见:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-Managing_guest_virtual_machines_with_virsh-Displaying_per_guest_virtual_machine_information#sect-Displaying_per_guest_virtual_machine_information-Changing_the_memory_allocation_for_the_domain


          The following case-insensitive suffixes can be used to select a specific scale:
                单位:
                         b, byte  byte      1
                         KB       kilobyte  1,000
                         k, KiB   kibibyte  1,024
                         MB       megabyte  1,000,000
                         M, MiB   mebibyte  1,048,576
                         GB       gigabyte  1,000,000,000
                         G, GiB   gibibyte  1,073,741,824
                         TB       terabyte  1,000,000,000,000
                         T, TiB   tebibyte  1,099,511,627,776
                         PB       petabyte  1,000,000,000,000,000
                         P, PiB   pebibyte  1,125,899,906,842,624
                         EB       exabyte   1,000,000,000,000,000,000
                         E, EiB   exbibyte  1,152,921,504,606,846,976

              Note that all values will be rounded up to the nearest kibibyte by libvirt, and may be
              further rounded to the granularity supported by the hypervisor. Some hypervisors also
              enforce a minimum, such as 4000KiB (or 4000 x 210 or 4,096,000 bytes).
              The units for this value are determined by the optional attribute memory unit,
              which defaults to the kibibytes (KiB) as a unit of measure where
              the value given is multiplied by 210 or blocks of 1024 bytes.

            警告(Warning):
                If modifying the <currentMemory> value, make sure to leave sufficient memory for the guest OS to work properly.
                If the set value is too low, the guest may become unstable.


// 查看当前内存气球大小
[root@host ~]# virsh qemu-monitor-command vm01-centos7.4-64 --hmp info balloon
      balloon: actual=512

// 调整 内存 气球
[root@host ~]# virsh qemu-monitor-command vm01-centos7.4-64 --hmp balloon 1024
[root@host ~]# virsh qemu-monitor-command vm01-centos7.4-64 --hmp info balloon
      balloon: actual=1024

// 查看 balloon 相关信息
[root@host ~]# virsh domstats --balloon  vm01-centos7.4-64

      Domain: 'vm01-centos7.4-64'
        balloon.current=1048576
        balloon.maximum=1048576
        balloon.swap_in=0
        balloon.swap_out=0
        balloon.major_fault=179
        balloon.minor_fault=150424
        balloon.unused=933416
        balloon.available=1016104
        balloon.last-update=1565837755
        balloon.rss=412048

---------------------------------------------------------------------------------------------------
强制关机

// 执行 子命令 destroy 实现类似于 拔电源的 效果
// this does not delete any storage volumes used by the guest, and if the domain is persistent, it can be restarted later.
[root@host ~]# virsh destroy vm01-centos7.4-64    #直接终止虚拟机,没有给 domain OS任何反应机会, 效果相当于在 物理机上 直接拔掉电源线.

    Immediately terminate the domain domain.  This doesn't give the domain OS any chance to react, and it's the equivalent of ripping the power cord out on a physical machine.


---------------------------------------------------------------------------------------------------
取消 domain 的定义 (即删除 domain 的 配置(定义)文件)

// 删除 vm01-centos7.4-64 的配置文件 /etc/libvirt/qemu/vm01-centos7.4-64.xml, (注: 如果不加相应选项, 该命令不会删除其对应的 storage image 文件)
[root@host ~]# virsh undefine vm01-centos7.4-64


      Undefine a domain. If the domain is running, this converts it to a transient domain, without stopping it. If the domain is inactive, the domain configuration is removed.






---------------------------------------------------------------------------------------------------
kvm 网络管理

    --------------------------------------------------
    关于 virtio:

        https://wiki.libvirt.org/page/Virtio
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/virtualization_host_configuration_and_guest_installation_guide/chap-virtualization_host_configuration_and_guest_installation_guide-para_virtualized_drivers
        http://www.zeta.systems/blog/2018/07/03/Installing-Virtio-Drivers-In-Windows-On-KVM/

          virtio 是 kvm 的 virtual machine 的 半虚拟化设备驱动,
          半虚拟化驱动程序可提高计算机的性能，减少 I/O 延迟(可理解为绕过了虚拟的物理层)并将吞吐量提高到接近裸机级别。


    Virtio

        So-called "full virtualization" is a nice feature because it allows you to run any operating system virtualized.
        However, it's slow because the hypervisor has to emulate actual physical devices such as RTL8139 network cards .
        This emulation is both complicated and inefficient.

        Virtio is a virtualization standard for network and disk device drivers where just the guest's
        device driver "knows" it is running in a virtual environment, and cooperates with the hypervisor.
        This enables guests to get high performance network and disk operations,
        and gives most of the performance benefits of paravirtualization.

        Note that virtio is different, but architecturally similar to, Xen paravirtualized device drivers
        (such as the ones that you can install in a Windows guest to make it go faster under Xen).
        Also similar is VMWare's Guest Tools.
    --------------------------------------------------



--------------------------------------------------

[root@host ~]# virsh --help | grep interface
    attach-interface               attach network interface   <---- 添加网卡
    detach-interface               detach network interface   <---- 删除网卡
    domif-setlink                  set link state of a virtual interface
    domiftune                      get/set parameters of a virtual interface
    domcontrol                     domain control interface state
    domif-getlink                  get link state of a virtual interface
    domifaddr                      Get network interfaces' addresses for a running domain
    domiflist                      list all domain virtual interfaces
    domifstat                      get network interface stats for a domain
 Interface (help keyword 'interface')
    iface-begin                    create a snapshot of current interfaces settings, which can be later committed (iface-commit) or restored (iface-rollback)
    iface-define                   define an inactive persistent physical host interface or modify an existing persistent one from an XML file
    iface-destroy                  destroy a physical host interface (disable it / "if-down")
    iface-dumpxml                  interface information in XML
    iface-edit                     edit XML configuration for a physical host interface
    iface-list                     list physical host interfaces
    iface-mac                      convert an interface name to interface MAC address
    iface-name                     convert an interface MAC address to interface name
    iface-start                    start a physical host interface (enable it / "if-up")
    iface-undefine                 undefine a physical host interface (remove it from configuration)



[root@host ~]# virsh attach-interface --help
          NAME
            attach-interface - attach network interface

          SYNOPSIS
            attach-interface <domain> <type> <source> [--target <string>] [--mac <string>] [--script <string>] [--model <string>] [--inbound <string>] [--outbound <string>] [--persistent] [--config] [--live] [--current] [--print-xml] [--managed]

          DESCRIPTION
            Attach new network interface.

          OPTIONS
            [--domain] <string>  domain name, id or uuid
            [--type] <string>  network interface type
            [--source] <string>  source of network interface
            --target <string>  target network name
            --mac <string>   MAC address
            --script <string>  script used to bridge network interface
            --model <string>  model type
            --inbound <string>  control domain's incoming traffics
            --outbound <string>  control domain's outgoing traffics
            --persistent     make live change persistent  (立即 + 永久)
            --config         affect next boot       (保存配置，重启生效)
            --live           affect running domain  (立刻生效,但不保存, 临时修改, 重启后所做修改会丢失)
            --current        affect current domain
            --print-xml      print XML document rather than attach the interface
            --managed        libvirt will automatically detach/attach the device from/to host


[root@host ~]# virsh help | grep dom

// 查看网卡
[root@host ~]# virsh domiflist vm01-centos7.4-64

      Interface  Type       Source     Model       MAC
      -------------------------------------------------------
      vnet0      bridge     virbr0     virtio      52:54:00:ad:ce:4e <---kvm虚拟机网卡的 mac 地址以 52:54:00 开始


// 通过 命令行 添加网卡
[root@host ~]# virsh attach-interface vm01-centos7.4-64 --type network --source default --model virtio --persistent
      Interface attached successfully

        注: type 为 network 时的 意思: network to indicate connection via a libvirt virtual network


[root@host ~]# virsh domiflist vm01-centos7.4-64
      Interface  Type       Source     Model       MAC
      -------------------------------------------------------
      vnet0      bridge     virbr0     virtio      52:54:00:ad:ce:4e
      vnet1      network    default    virtio      52:54:00:a3:19:8b


[root@host ~]# virsh detach-interface --help
    NAME
      detach-interface - detach network interface

    SYNOPSIS
      detach-interface <domain> <type> [--mac <string>] [--persistent] [--config] [--live] [--current]

    DESCRIPTION
      Detach network interface.

    OPTIONS
      [--domain] <string>  domain name, id or uuid
      [--type] <string>  network interface type
      --mac <string>   MAC address
      --persistent     make live change persistent
      --config         affect next boot
      --live           affect running domain
      --current        affect current domain


// 通过命令行删除网卡
[root@host ~]#  virsh detach-interface vm01-centos7.4-64 --type network --mac 52:54:00:a3:19:8b --persistent
    Interface detached successfully

[root@host ~]# virsh domiflist vm01-centos7.4-64

    Interface  Type       Source     Model       MAC
    -------------------------------------------------------
    vnet0      bridge     virbr0     virtio      52:54:00:ad:ce:4e


---------------------------------------------------------------------------------------------------
kvm 网络模式

1、NAT模式
2、桥接模式
3、隔离模式
4、路由模式



  1、NAT模式

      virtual machine 01 | <-----> default 交换机,自带dhcp, 192.168.122.0/24 <-----> virbr0 192.168.122.1 <----> 物理网卡 <---->
      virtual machine 02 |


[root@host ~]# cat /proc/sys/net/ipv4/ip_forward
    1

[root@host ~]# iptables -t nat -nL

      Chain POSTROUTING (policy ACCEPT)
      target     prot opt source               destination
      RETURN     all  --  192.168.122.0/24     224.0.0.0/24
      RETURN     all  --  192.168.122.0/24     255.255.255.255
      MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
      MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
      MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24


kvm 中 nat 模式 网络通信的 常规 3 个要点: (注: 网络故障排错一般根据 网络参考模型的 从下往上 排查, 好比建房子时从下往上盖)
   1) 虚拟机正确设置网关
   2) 物理机开启路由转发功能 (通过网卡 virbr0 才会转发数据包)
   3) 物理机启用 nat 功能 (通过物理网卡 以 snat 或 dnat 连通其他网络)




---------------------------------------------------------------------------------------------------
学习过程中 遇到的问题:

      https://communities.vmware.com/thread/541258
      https://www.centos.org/forums/viewtopic.php?t=49229








