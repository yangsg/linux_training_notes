

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


https://www.linuxtechi.com/install-kvm-hypervisor-on-centos-7-and-rhel-7/



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


virt-install

[root@host ~]# man virt-install

// 通过 --option=? 的形式可以查看 对应 argument 的  sub options
[root@host ~]# virt-install --disk=?









---------------------------------------------------------------------------------------------------
学习过程中 遇到的问题:

      https://communities.vmware.com/thread/541258
      https://www.centos.org/forums/viewtopic.php?t=49229








