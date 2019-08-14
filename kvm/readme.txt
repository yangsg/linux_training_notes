

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

      ------------------------------

--------------------------------------------------

---------------------------------------------------------------------------------------------------
学习过程中 遇到的问题:

      https://communities.vmware.com/thread/541258
      https://www.centos.org/forums/viewtopic.php?t=49229








