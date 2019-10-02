


https://www.docker.com/
https://docs.docker.com

----------------------------------------------------------------------------------------------------
https://docs.docker.com/get-started/


Images and containers
A container is launched by running an image. An image is an executable package that includes
everything needed to run an application--the code, a runtime, libraries, environment variables, and configuration files.
// A container 通过运行 an image 来启动, An image 是一个可执行包(an executable package), 其包含了
// 运行 an application 所需的 everything--the code, a runtime, libraries, environment variables, and configuration files.

A container is a runtime instance of an image--what the image becomes in memory when executed
(that is, an image with state, or a user process).
You can see a list of your running containers with the command, docker ps, just as you would in Linux.
//A container 是 an image 的 一个 运行时 实例(a runtime instance)



https://www.docker.com/resources/what-container





What is a Container?
  A standardized unit of software
  // 标准化的软件单元



                    containerized applications:

                  +----------------------------+
                  | appA | appB | appC | appD  |
                  |----------------------------|
                  |          Docker            |
                  |----------------------------|
                  |   Host Operating System    |
                  |----------------------------|
                  |      Infrastructure        |
                  +----------------------------+


    Package Software into Standardized Units for Development, Shipment and Deployment
    // 将 Software 打包 进 标准单元 中 以用于 Development, Shipment and Deployment

    A container is a standard unit of software that packages up code and all its dependencies
    so the application runs quickly and reliably from one computing environment to another.
    A Docker container image is a lightweight, standalone, executable package of software
    that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.
    // A container 是 一个 标准的 软件单元, 其对 code 和 其所有 依赖(dependencies)进行了打包.
    // 因此 the application 可以 快速 并 可靠 地 从 one computing environment 跑/运行(runs) 到 另一个计算环境.
    // A Docker container image 是一个 lightweight, standalone, 可执行的 软件包,
    // 其包含了 run an application 所需要的 everything: code, runtime, system tools, system libraries and settings.


    Container images become containers at runtime and in the case of Docker containers-
    images become containers when they run on Docker Engine. Available for both Linux
    and Windows-based applications, containerized software will always run the same,
    regardless of the infrastructure. Containers isolate software from its environment
    and ensure that it works uniformly despite differences for instance between development and staging.
    // Container images 在 运行时成为 containers, 而 对于 Docker containers 来说,
    // images 会在 其 运行在 Docker Engine 上是 成为 containers. 不管 infrastructure 如何,
    // containerized software 对于 基于 Linux 和 Windows 的 applications 都是可用的, 其总是运行相同(一致),
    // Containers 将 software 与其 environment 隔离(isolate) 开来, 并 确保 其 一致地运行 而 无视
    // differences for instance between development and staging.


Docker containers that run on Docker Engine:

    - Standard: Docker created the industry standard for containers, so they could be portable anywhere

    - Lightweight: Containers share the machine’s OS system kernel and therefore do not require an OS per application,
                   driving higher server efficiencies and reducing server and licensing costs

    - Secure: Applications are safer in containers and Docker provides the strongest default isolation capabilities in the industry


Comparing Containers and Virtual Machines(Containers 和 Virtual Machines 的比较)

    Containers and virtual machines have similar resource isolation and allocation benefits,
    but function differently because containers virtualize the operating system instead of hardware.
    Containers are more portable and efficient.
    // Containers 和 virtual machines 具有相似的 资源隔离 和 分配优势,
    // 但 功能(function)不同, 因为 containers 是 虚拟化 the operating system 而非 hardware.
    // Containers are more portable and efficient.

        containerized applications         +----VM-----+----VM-----+----VM------+
      +----------------------------+       |           |           |            |
      | appA | appB | appC | appD  |       |  appA     |   appB    |    appC    |
      |----------------------------|       | --------  | --------  |  --------  |
      |          Docker            |       | Guest OS  | Guest OS  |  Guest OS  |
      |----------------------------|       |------------------------------------|
      |   Host Operating System    |       |            Hypervisor              |
      |----------------------------|       |------------------------------------|
      |      Infrastructure        |       |          Infrastructure            |
      +----------------------------+       +------------------------------------+


Containers
    Containers are an abstraction at the app layer that packages code and dependencies together.
    Multiple containers can run on the same machine and share the OS kernel with other containers,
    each running as isolated processes in user space. Containers take up less space than VMs
    (container images are typically tens of MBs in size),
    can handle more applications and require fewer VMs and Operating systems.

Virtual Machines
    Virtual machines (VMs) are an abstraction of physical hardware turning one server into many servers.
    The hypervisor allows multiple VMs to run on a single machine. Each VM includes a full copy
    of an operating system, the application, necessary binaries
    and libraries - taking up tens of GBs. VMs can also be slow to boot.


Containers and Virtual Machines Together
    Containers and VMs used together provide a great deal of flexibility in deploying and managing app





----------------------------------------------------------------------------------------------------
[root@node01 ~]# yum -y install docker

[root@node01 ~]# systemctl start docker
[root@node01 ~]# systemctl enable docker


[root@node01 ~]# docker version

    Client:
     Version:         1.13.1
     API version:     1.26
     Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
     Go version:      go1.10.3
     Git commit:      7f2769b/1.13.1
     Built:           Sun Sep 15 14:06:47 2019
     OS/Arch:         linux/amd64

    Server:
     Version:         1.13.1
     API version:     1.26 (minimum version 1.12)
     Package version: docker-1.13.1-103.git7f2769b.el7.centos.x86_64
     Go version:      go1.10.3
     Git commit:      7f2769b/1.13.1
     Built:           Sun Sep 15 14:06:47 2019
     OS/Arch:         linux/amd64
     Experimental:    false


[root@node01 ~]# ip a
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever
      2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
          link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
          inet 192.168.175.139/24 brd 192.168.175.255 scope global dynamic ens33
             valid_lft 1351sec preferred_lft 1351sec
          inet6 fe80::20c:29ff:fe52:8e39/64 scope link
             valid_lft forever preferred_lft forever
      3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN  <-----观察
          link/ether 02:42:0f:0d:77:2f brd ff:ff:ff:ff:ff:ff
          inet 172.17.0.1/16 scope global docker0
             valid_lft forever preferred_lft forever

[root@node01 ~]# cat /proc/sys/net/ipv4/ip_forward
    1

[root@node01 ~]# iptables -t nat -nL
    Chain PREROUTING (policy ACCEPT)
    target     prot opt source               destination
    DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

    Chain INPUT (policy ACCEPT)
    target     prot opt source               destination

    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination
    DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

    Chain POSTROUTING (policy ACCEPT)
    target     prot opt source               destination
    MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0   <---- 观察

    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0



----------------------------------------------------------------------------------------------------



// 查看一下 docker 命令的简要帮助
[root@node01 ~]# docker --help

    Usage:  docker COMMAND

    A self-sufficient runtime for containers

    Options:
          --config string      Location of client config files (default "/root/.docker")
      -D, --debug              Enable debug mode
          --help               Print usage
      -H, --host list          Daemon socket(s) to connect to (default [])
      -l, --log-level string   Set the logging level ("debug", "info", "warn", "error", "fatal") (default "info")
          --tls                Use TLS; implied by --tlsverify
          --tlscacert string   Trust certs signed only by this CA (default "/root/.docker/ca.pem")
          --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
          --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
          --tlsverify          Use TLS and verify the remote
      -v, --version            Print version information and quit

    Management Commands:
      container   Manage containers
      image       Manage images
      network     Manage networks
      node        Manage Swarm nodes
      plugin      Manage plugins
      secret      Manage Docker secrets
      service     Manage services
      stack       Manage Docker stacks
      swarm       Manage Swarm
      system      Manage Docker
      volume      Manage volumes

    Commands:
      attach      Attach to a running container
      build       Build an image from a Dockerfile
      commit      Create a new image from a container's changes
      cp          Copy files/folders between a container and the local filesystem
      create      Create a new container
      diff        Inspect changes on a container's filesystem
      events      Get real time events from the server
      exec        Run a command in a running container
      export      Export a container's filesystem as a tar archive
      history     Show the history of an image
      images      List images
      import      Import the contents from a tarball to create a filesystem image
      info        Display system-wide information
      inspect     Return low-level information on Docker objects
      kill        Kill one or more running containers
      load        Load an image from a tar archive or STDIN
      login       Log in to a Docker registry
      logout      Log out from a Docker registry
      logs        Fetch the logs of a container
      pause       Pause all processes within one or more containers
      port        List port mappings or a specific mapping for the container
      ps          List containers
      pull        Pull an image or a repository from a registry
      push        Push an image or a repository to a registry
      rename      Rename a container
      restart     Restart one or more containers
      rm          Remove one or more containers
      rmi         Remove one or more images
      run         Run a command in a new container
      save        Save one or more images to a tar archive (streamed to STDOUT by default)
      search      Search the Docker Hub for images
      start       Start one or more stopped containers
      stats       Display a live stream of container(s) resource usage statistics
      stop        Stop one or more running containers
      tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
      top         Display the running processes of a container
      unpause     Unpause all processes within one or more containers
      update      Update configuration of one or more containers
      version     Show the Docker version information
      wait        Block until one or more containers stop, then print their exit codes

    Run 'docker COMMAND --help' for more information on a command.



一、镜像管理指令

// 查看一下 docker image 管理指令的简要帮助
[root@node01 ~]# docker image --help

    Usage:  docker image COMMAND

    Manage images

    Options:
          --help   Print usage

    Commands:
      build       Build an image from a Dockerfile
      history     Show the history of an image
      import      Import the contents from a tarball to create a filesystem image
      inspect     Display detailed information on one or more images
      load        Load an image from a tar archive or STDIN
      ls          List images
      prune       Remove unused images
      pull        Pull an image or a repository from a registry
      push        Push an image or a repository to a registry
      rm          Remove one or more images
      save        Save one or more images to a tar archive (streamed to STDOUT by default)
      tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE

    Run 'docker image COMMAND --help' for more information on a command.



[root@node01 ~]# docker image ls
      REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE



[root@node01 ~]# docker search centos   #搜素 name 中带有 字符串 'centos' 的镜像
      INDEX       NAME                                         DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
      docker.io   docker.io/centos                             The official build of CentOS.                   5592      [OK]
      docker.io   docker.io/ansible/centos7-ansible            Ansible on Centos7                              123                  [OK]
      docker.io   docker.io/jdeathe/centos-ssh                 OpenSSH / Supervisor / EPEL/IUS/SCL Repos ...   112                  [OK]
      docker.io   docker.io/consol/centos-xfce-vnc             Centos container with "headless" VNC sessi...   99                   [OK]
      docker.io   docker.io/centos/mysql-57-centos7            MySQL 5.7 SQL database server                   63
      docker.io   docker.io/imagine10255/centos6-lnmp-php56    centos6-lnmp-php56                              57                   [OK]
      docker.io   docker.io/tutum/centos                       Simple CentOS docker image with SSH access      45
      docker.io   docker.io/centos/postgresql-96-centos7       PostgreSQL is an advanced Object-Relationa...   39
      docker.io   docker.io/kinogmt/centos-ssh                 CentOS with SSH                                 29                   [OK]
      docker.io   docker.io/centos/php-56-centos7              Platform for building and running PHP 5.6 ...   22
      docker.io   docker.io/pivotaldata/centos-gpdb-dev        CentOS image for GPDB development. Tag nam...   10
      docker.io   docker.io/nathonfowlie/centos-jre            Latest CentOS image with the JRE pre-insta...   8                    [OK]
      docker.io   docker.io/drecom/centos-ruby                 centos ruby                                     6                    [OK]
      docker.io   docker.io/darksheer/centos                   Base Centos Image -- Updated hourly             3                    [OK]
      docker.io   docker.io/mamohr/centos-java                 Oracle Java 8 Docker image based on Centos 7    3                    [OK]
      docker.io   docker.io/pivotaldata/centos                 Base centos, freshened up a little with a ...   3
      docker.io   docker.io/miko2u/centos6                     CentOS6 日本語環境                                   2                    [OK]
      docker.io   docker.io/pivotaldata/centos-gcc-toolchain   CentOS with a toolchain, but unaffiliated ...   2
      docker.io   docker.io/pivotaldata/centos-mingw           Using the mingw toolchain to cross-compile...   2
      docker.io   docker.io/blacklabelops/centos               CentOS Base Image! Built and Updates Daily!     1                    [OK]
      docker.io   docker.io/indigo/centos-maven                Vanilla CentOS 7 with Oracle Java Developm...   1                    [OK]
      docker.io   docker.io/mcnaughton/centos-base             centos base image                               1                    [OK]
      docker.io   docker.io/pivotaldata/centos6.8-dev          CentosOS 6.8 image for GPDB development         0
      docker.io   docker.io/pivotaldata/centos7-dev            CentosOS 7 image for GPDB development           0
      docker.io   docker.io/smartentry/centos                  centos with smartentry                          0                    [OK]



[root@node01 ~]# docker image pull docker.io/centos   # 拉取 或 下载 指定 image
      Using default tag: latest
      Trying to pull repository docker.io/library/centos ...
      latest: Pulling from docker.io/library/centos
      d8d02d457314: Pull complete
      Digest: sha256:307835c385f656ec2e2fec602cf093224173c51119bbebd602c53c3653a3d6eb
      Status: Downloaded newer image for docker.io/centos:latest


[root@node01 ~]# docker image ls
      REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
      docker.io/centos    latest              67fa590cfc1c        5 weeks ago         202 MB



// 通常创建容器 都用 run 命令, 很少使用 create 命令
[root@node01 ~]# docker run --help

      Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

      Run a command in a new container

Options: 常用选项

  -i, --interactive                           Keep STDIN open even if not attached
  -t, --tty                                   Allocate a pseudo-TTY
      --name string                           Assign a name to the container
  -d, --detach                                Run container in background and print container ID



[root@node01 ~]# docker run -i -t -d  docker.io/centos:latest  /bin/bash
    064e9713da0ab7451b8730c2f6f81f0e23f62639b86d1c79f1bacc56c56fe72a


[root@node01 ~]# docker ps


[root@node01 ~]# docker ps --all
CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS                     PORTS               NAMES
064e9713da0a        docker.io/centos:latest   "/bin/bash"         3 minutes ago       Up 3 minutes                                   vibrant_blackwell
49b3e4ea4067        docker.io/centos:latest   "/bin/bash"         4 minutes ago       Exited (0) 3 minutes ago                       mystifying_lamport
ad5d8b0cab2a        docker.io/centos:latest   "/bin/bash"         4 minutes ago       Exited (0) 4 minutes ago                       clever_montalcini


[root@node01 ~]# docker attach vibrant_blackwell
[root@064e9713da0a /]#

[root@064e9713da0a /]# hostname
064e9713da0a

[root@064e9713da0a /]# cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)


// 容器 和 物理机 共享内核
[root@064e9713da0a /]# uname -r
3.10.0-693.el7.x86_64


[root@node01 ~]# docker ps --all
CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS                      PORTS               NAMES
064e9713da0a        docker.io/centos:latest   "/bin/bash"         2 hours ago         Exited (0) 13 seconds ago                       vibrant_blackwell
49b3e4ea4067        docker.io/centos:latest   "/bin/bash"         2 hours ago         Exited (0) 2 hours ago                          mystifying_lamport
ad5d8b0cab2a        docker.io/centos:latest   "/bin/bash"         2 hours ago         Exited (0) 2 hours ago                          clever_montalcini

[root@node01 ~]# docker start vibrant_blackwell   #启动容器
vibrant_blackwell
[root@node01 ~]# docker ps --all
CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS                   PORTS               NAMES
064e9713da0a        docker.io/centos:latest   "/bin/bash"         2 hours ago         Up 3 seconds                                 vibrant_blackwell
49b3e4ea4067        docker.io/centos:latest   "/bin/bash"         2 hours ago         Exited (0) 2 hours ago                       mystifying_lamport
ad5d8b0cab2a        docker.io/centos:latest   "/bin/bash"         2 hours ago         Exited (0) 2 hours ago                       clever_montalcini


[root@node01 ~]# docker attach vibrant_blackwell   #连接容器
[root@064e9713da0a /]#

退出容器: Ctrl + p + q


----------------------------------------------------------------------------------------------------

[root@node01 ~]# docker attach vibrant_blackwell
[root@064e9713da0a /]# ip a
bash: ip: command not found
[root@064e9713da0a /]# yum -y install net-tools


[root@064e9713da0a /]# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 0.0.0.0
        inet6 fe80::42:acff:fe11:2  prefixlen 64  scopeid 0x20<link>
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
        RX packets 1055  bytes 8253124 (7.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 927  bytes 53631 (52.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

[root@064e9713da0a /]# route  -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.17.0.1      0.0.0.0         UG    0      0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 eth0

[root@node01 ~]# ifconfig docker0
docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 0.0.0.0
        inet6 fe80::42:dff:fe02:a7e8  prefixlen 64  scopeid 0x20<link>
        ether 02:42:0d:02:a7:e8  txqueuelen 0  (Ethernet)
        RX packets 946  bytes 41941 (40.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1048  bytes 8252566 (7.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


[root@064e9713da0a /]# ping www.baidu.com -c 2
      PING www.a.shifen.com (39.156.66.14) 56(84) bytes of data.
      64 bytes from 39.156.66.14 (39.156.66.14): icmp_seq=1 ttl=127 time=9.06 ms
      64 bytes from 39.156.66.14 (39.156.66.14): icmp_seq=2 ttl=127 time=9.25 ms

      --- www.a.shifen.com ping statistics ---
      2 packets transmitted, 2 received, 0% packet loss, time 1001ms
      rtt min/avg/max/mdev = 9.069/9.161/9.254/0.133 ms





[root@node01 ~]# docker run --help | less


      --restart string                        Restart policy to apply when a container exits (default "no")

  -p, --publish list                          Publish a container's port(s) to the host (default [])






















