
docker 是使用 go 语言实现的

https://docs.docker.com/

https://hub.docker.com/


docker 国内加速地址
  https://www.jianshu.com/p/b5006ebf1522


docker 概览:
  https://docs.docker.com/engine/docker-overview/

docker 架构:
  https://docs.docker.com/engine/docker-overview/#docker-architecture



----------------------------------------------------------------------------------------------------
docker 概览:
    https://docs.docker.com/engine/docker-overview/


Docker Engine (docker 容器引擎)

    Docker Engine is a client-server application with these major components:
    // 即 Docker Engine 是一个 C/S 架构的应用

                         Docker REST API
      client(docker) ---------------------> server(dockerd)


    The daemon creates and manages Docker objects, such as images, containers, networks, and volumes.


Docker architecture (docker 架构)


    |client            |           docker_host              |    registry            |
    |------------------|------------------------------------|------------------------|
    |docker build      |           docker daemon            |     repo_01            |
    |docker pull       |                                    |       img_01 img02     |
    |docker run        |          containers   images       |                        |
    |                  |           c1           img_01      |     repo_02            |
    |                  |           c2           img_01      |       img_001  img_002 |
    |                  |           c3                       |                        |
    |                  |           c4                       |                        |
    |                  |           c5                       |                        |
    |                  |                                    |                        |


    文档中出现的缩略语:
        DDC: Docker Datacenter
        DTR: Docker Trusted Registry


Docker objects (Docker 对象)

- images

    An image is a read-only template with instructions for creating a Docker container.
    Often, an image is based on another image, with some additional customization.

      Each instruction in a Dockerfile creates a layer in the image.
      When you change the Dockerfile and rebuild the image, only those layers which have changed are rebuilt.

- containers

执行 命令 `docker run -i -t ubuntu /bin/bash` 背后所发生的事情:

    1) If you do not have the ubuntu image locally, Docker pulls it from
       your configured registry, as though you had run docker pull ubuntu manually.

    2) Docker creates a new container, as though you had run a docker container create command manually.

    3) Docker allocates a read-write filesystem to the container, as its final layer.
       This allows a running container to create or modify files and directories in its local filesystem.
       // 分配(创建) 可 读写层

    4) Docker creates a network interface to connect the container to the default network,
       since you did not specify any networking options. This includes assigning an
       IP address to the container. By default, containers can connect to external
       networks using the host machine’s network connection.
      // 创建 网卡

    5) Docker starts the container and executes /bin/bash. Because the container is
       running interactively and attached to your terminal (due to the -i and -t flags),
       you can provide input using your keyboard while the output is logged to your terminal.

    6) When you type exit to terminate the /bin/bash command,
       the container stops but is not removed. You can start it again or remove it.

- services

The underlying technology (底层技术)

Namespaces (名称空间)

  Docker uses a technology called namespaces to provide the isolated workspace called the container.
  When you run a container, Docker creates a set of namespaces for that container.

  These namespaces provide a layer of isolation. Each aspect of a container
  runs in a separate namespace and its access is limited to that namespace.


Docker Engine uses namespaces such as the following on Linux:

    - The pid namespace: Process isolation (PID: Process ID).
    - The net namespace: Managing network interfaces (NET: Networking).
    - The ipc namespace: Managing access to IPC resources (IPC: InterProcess Communication).
    - The mnt namespace: Managing filesystem mount points (MNT: Mount).
    - The uts namespace: Isolating kernel and version identifiers. (UTS: Unix Timesharing System).


- Control groups

    Docker Engine on Linux also relies on another technology called control groups (cgroups).
    A cgroup limits an application to a specific set of resources. Control groups allow
    Docker Engine to share available hardware resources to containers and optionally enforce
    limits and constraints. For example, you can limit the memory available to a specific container.


- Union file systems

    Union file systems, or UnionFS, are file systems that operate by creating layers,
    making them very lightweight and fast. Docker Engine uses UnionFS to provide the building
    blocks for containers. Docker Engine can use multiple UnionFS variants,
    including AUFS, btrfs, vfs, and DeviceMapper.

- Container format

    Docker Engine combines the namespaces, control groups, and UnionFS into a wrapper called a container format.
    The default container format is libcontainer. In the future, Docker may support other container
    formats by integrating with technologies such as BSD Jails or Solaris Zones.





----------------------------------------------------------------------------------------------------
安装 docker-ce:

      https://docs.docker.com/install/linux/docker-ce/centos/
      https://opsx.alibaba.com/mirror
      https://yq.aliyun.com/articles/110806



docker-ce 对 OS 的要求:
    1) a maintained version of CentOS 7
    2) yum 仓库 centos-extras 处于启动状态(默认已经处于 启动状态)
    3) 推荐 storage driver: overlay2


[root@node01 ~]# yum repolist  | grep -E extras
      Repodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast
       * extras: mirrors.aliyun.com
      !extras/7/x86_64      CentOS-7 - Extras - mirrors.aliyun.com                 321



// Uninstall old versions (卸载旧版本的 docker(名叫 docker 或 docker-engine) 及其 依赖)
[root@node01 ~]# yum remove docker \
                     docker-client \
                     docker-client-latest \
                     docker-common \
                     docker-latest \
                     docker-latest-logrotate \
                     docker-logrotate \
                     docker-engine


  注: The contents of /var/lib/docker/, including images, containers, volumes, and networks, are preserved.

// 设置 docker-ce 相关的 yum 仓库 (本示例采用国内 阿里的 镜像源):
// 安装必须的 package
// 注: yum-utils 提供了 yum-config-manager 工具,
//     而 device-mapper-persistent-data 和 lvm2 是 devicemapper 存储驱动(storage driver) 所必需的
[root@node01 ~]# yum install -y yum-utils device-mapper-persistent-data lvm2


// 添加 稳定版本的 docker-ce 的 yum 源
[root@node01 ~]# yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
      Loaded plugins: fastestmirror
      adding repo from: http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
      grabbing file http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
      repo saved to /etc/yum.repos.d/docker-ce.repo

// 更新 repo
[root@node01 ~]# yum makecache fast
[root@node01 ~]# yum repolist  | grep docker-ce
    docker-ce-stable/x86_64  Docker CE Stable - x86_64                            61

[root@node01 ~]# yum install -y docker-ce docker-ce-cli containerd.io   #//注:如果没指定 docker-ce-cli containerd.io, 其也会作为 docker-ce 的依赖 被自动安装
[root@node01 ~]# rpm -q docker-ce docker-ce-cli containerd.io
      docker-ce-19.03.4-3.el7.x86_64
      docker-ce-cli-19.03.4-3.el7.x86_64
      containerd.io-1.2.10-3.2.el7.x86_64

// The docker group is created, but no users are added to the group.
[root@node01 ~]# cat /etc/group | grep docker
    docker:x:995:

// 启动 docker 容器引擎 并 设置为 开机自启
[root@node01 ~]# systemctl start docker
[root@node01 ~]# systemctl enable docker
      Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.


[root@node01 ~]# systemctl status docker
    ● docker.service - Docker Application Container Engine
       Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
       Active: active (running) since Sun 2019-10-27 10:24:53 CST; 1min 6s ago
         Docs: https://docs.docker.com
     Main PID: 17156 (dockerd)
       CGroup: /system.slice/docker.service
               └─17156 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock

    Oct 27 10:24:52 node01 dockerd[17156]: time="2019-10-27T10:24:52.925768367+08:00" level=info msg="scheme \"unix\" not registered, fallback to default scheme" module=grpc
    Oct 27 10:24:52 node01 dockerd[17156]: time="2019-10-27T10:24:52.925783109+08:00" level=info msg="ccResolverWrapper: sending update to cc: {[{unix:///run/containerd/containe... module=grpc
    Oct 27 10:24:52 node01 dockerd[17156]: time="2019-10-27T10:24:52.925790805+08:00" level=info msg="ClientConn switching balancer to \"pick_first\"" module=grpc
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.007325226+08:00" level=info msg="Loading containers: start."
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.432995995+08:00" level=info msg="Default bridge (docker0) is assigned with an IP address 172.17.0.0/16. Daem... IP address"
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.593997165+08:00" level=info msg="Loading containers: done."
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.746971067+08:00" level=info msg="Docker daemon" commit=9013bf583a graphdriver(s)=overlay2 version=19.03.4
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.761559442+08:00" level=info msg="Daemon has completed initialization"
    Oct 27 10:24:53 node01 systemd[1]: Started Docker Application Container Engine.
    Oct 27 10:24:53 node01 dockerd[17156]: time="2019-10-27T10:24:53.851596790+08:00" level=info msg="API listen on /var/run/docker.sock"
    Hint: Some lines were ellipsized, use -l to show in full.





      --------------------------------------------------
      安装指定 版本 docker-ce 的方式
          [root@localhost ~]# yum list docker-ce --showduplicates | sort -r  #// 列出 所有可用版本的 docker-ce

                ......
                docker-ce.x86_64            3:19.03.1-3.el7                     docker-ce-stable
                docker-ce.x86_64            3:19.03.0-3.el7                     docker-ce-stable
                docker-ce.x86_64            3:18.09.9-3.el7                     docker-ce-stable  <----以该版本为例
                docker-ce.x86_64            3:18.09.8-3.el7                     docker-ce-stable
                ......

          [root@localhost ~]# yum install -y docker-ce-18.09.9-3.el7 docker-ce-cli-18.09.9-3.el7 containerd.io
          [root@localhost ~]# rpm -q docker-ce docker-ce-cli containerd.io
              docker-ce-18.09.9-3.el7.x86_64
              docker-ce-cli-18.09.9-3.el7.x86_64
              containerd.io-1.2.10-3.2.el7.x86_64
      --------------------------------------------------

// 观察: 添加了虚拟网卡 docker0
[root@node01 ~]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.100/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe52:8e39/64 scope link
           valid_lft forever preferred_lft forever
    3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN  <---观察: 添加了 docker0 虚拟网卡为容器提供 nat bridge 功能
        link/ether 02:42:d3:c1:3b:24 brd ff:ff:ff:ff:ff:ff
        inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0   <-----作为 网段 172.17.0.0/16 的桥
           valid_lft forever preferred_lft forever

//  观察: 启用了 路由转发 功能
[root@node01 ~]# cat /proc/sys/net/ipv4/ip_forward
1


// 观察 iptables 的 nat 表
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
    MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0 <---观察: 通过 docker0 (nat bridge) 为容器提供 snat 功能

    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0


// 观察路由表信息
[root@node01 ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0  <---观察
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


// 设置 docker 使用国内 镜像加速  (注: 本示例中使用的是 虚构的地址, 应该修改为自己正确的地址)
//    https://www.jianshu.com/p/b5006ebf1522
//    https://help.aliyun.com/product/60716.html?spm=a2c4g.750001.list.6.256b7b13BTtnr3
[root@node01 ~]# vim /etc/docker/daemon.json

    {
      "registry-mirrors": ["https://fqhy0m47.mirror.aliyuncs.com"]
    }

// 重启 docker, 使如上的配置修改 生效
[root@node01 ~]# systemctl restart docker


// 验证 Docker Engine - Community 是否安装正确(通过运行 镜像 hello-world:latest 对应的容量).
[root@node01 ~]# docker run hello-world

      Unable to find image 'hello-world:latest' locally
      latest: Pulling from library/hello-world
      1b930d010525: Pull complete
      Digest: sha256:c3b4ada4687bbaa170745b3e4dd8ac3f194ca95b2d0518b417fb47e5879d9b5f
      Status: Downloaded newer image for hello-world:latest

      Hello from Docker!  <----- 观察
      This message shows that your installation appears to be working correctly.

      ......



安装完成后 一些 可选的 后安装步骤:

    https://docs.docker.com/install/linux/linux-postinstall/


----------------------------------------------------------------------------------------------------
示例:
卸载 docker-ce 的方法:

[root@node01 ~]# systemctl stop docker
// 卸载 docker-ce 软件包
[root@node01 ~]# yum remove docker-ce
// 手动删除 all images, containers, and volumes:
[root@node01 ~]# rm -rf /var/lib/docker

     注: 其他 编辑的 配置文件 也需要 手动删除

此时 docker0 虚拟网卡 和 iptables 中 docker 相关的规则依然存在, 此时可以简单地重启(reboot)一下主机






----------------------------------------------------------------------------------------------------
示例:  容器化 一个 nodejs 的 web 应用程序 (即 构建该 web app 的 docker image)

    https://docs.docker.com/get-started/part2/


[root@node01 ~]# git clone -b v1 https://github.com/docker-training/node-bulletin-board
[root@node01 ~]# cd node-bulletin-board/bulletin-board-app

[root@node01 bulletin-board-app]# cat Dockerfile

    #Dockerfile reference 见 https://docs.docker.com/engine/reference/builder/

    # 指定作为基础架构 image
    FROM node:6.11.5

    # 指定 image 文件系统中的工作目录, 所有后续操作 都应该 基于 此目录
    WORKDIR /usr/src/app
    # 将 package.json 复制到 image 中的当前工作目录 (即复制后最终 image 中路径为 /usr/src/app/package.json)
    COPY package.json .
    # 在 image filesystem 中执行命令 `npm install`, 安装 该 nodejs 项目的 依赖 modules.
    # 注:  指令(instruction) RUN 指定的内容(命令和/或命令参数) 是在 docker构建(build) image 时 被执行
    RUN npm install
    # 复制 app 中 其余的 源代码 到 image 文件系统中 的 当前工作目录中(即 /usr/src/app/ 中)
    COPY . .

    # 注: 指令 CMD 指定的 内容(命令和/或命令参数) 是在 docker 启动(start)容器时 被执行的
    CMD [ "npm", "start" ]




// 构建 image

// 观察当前 目录信息, 以确保 指定 build 命令时 处于 工程目录中
[root@node01 bulletin-board-app]# pwd
    /root/node-bulletin-board/bulletin-board-app
[root@node01 bulletin-board-app]# ls
    app.js  backend  Dockerfile  fonts  index.html  LICENSE  package.json  readme.md  server.js  site.css

// 构建 工程 的 docker image 文件
//   参考  `man docker-image-build`  或 `docker image build --help`
[root@node01 bulletin-board-app]# docker image build -t bulletinboard:1.0 .

        ......

        Successfully built 1a81106c60ff
        Successfully tagged bulletinboard:1.0


// 列出 查看本机上的 images
[root@node01 ~]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    bulletinboard       1.0                 1a81106c60ff        4 minutes ago       681MB   <-----构建生成的 工程目标 image
    hello-world         latest              fce289e99eb9        9 months ago        1.84kB
    node                6.11.5              852391892b9f        23 months ago       662MB   <-----构建时作为 基础 image 被 pull 下载下来的


// 观察一下 image 'bulletinboard:1.0' 的一些详细信息
[root@node01 ~]# docker image inspect bulletinboard:1.0

// 运行容器(即创建并运行 image 'bulletinboard:1.0' 的容器实例), 并将 容器中的 端口 8080 发布到宿主机的端口 8000 上
// (因为该容器使用 bridge 网络类型, 所以是通过 dnat 方式发布)
[root@node01 ~]# docker container run --publish 8000:8080 --detach --name bb bulletinboard:1.0
    7bf55b4d774477e5eb2fa4ee637a84b59f1b3cde34ff8a4e5dd17ad315f87bb6

此时可以使用浏览器访问 http://192.168.175.100:8000/
或执行如下命令访问:
    wget -O - -q 192.168.175.100:8000 | less

// 列出 观察 正运行的容器
[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
    7bf55b4d7744        bulletinboard:1.0   "npm start"         17 minutes ago      Up 17 minutes       0.0.0.0:8000->8080/tcp   bb

[root@node01 ~]# docker container ls --no-trunc  #通过选项 --no-trunc 可显示完整的容器 ID
    CONTAINER ID                                                       IMAGE               COMMAND             CREATED             STATUS              PORTS                    NAMES
    7bf55b4d774477e5eb2fa4ee637a84b59f1b3cde34ff8a4e5dd17ad315f87bb6   bulletinboard:1.0   "npm start"         41 minutes ago      Up 41 minutes       0.0.0.0:8000->8080/tcp   bb

// 观察 容器 的详细信息
[root@node01 ~]# docker container  inspect 7bf55b4d7744
[root@node01 ~]# docker container  inspect bb



// 在 运行着 的容器中 执行某些指令 以观察某些 容器内部信息
[root@node01 ~]# docker container exec -it bb /bin/bash
    root@7bf55b4d7744:/usr/src/app# hostname
    7bf55b4d7744  <-----观察, 容器中 hostname 为 容器的 ID
    root@7bf55b4d7744:/usr/src/app# ip a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
            inet 127.0.0.1/8 scope host lo
               valid_lft forever preferred_lft forever
        8: eth0@if9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default <----观察
            link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
            inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0  <-----观察,当前容器中 ip 地址为 172.17.0.2/16
               valid_lft forever preferred_lft forever
    root@7bf55b4d7744:/usr/src/app# ps -elf
        F S UID         PID   PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
        4 S root          1      0  0  80   0 - 265674 ep_pol 10:36 ?       00:00:00 npm  <-----观察, 1号(pid为1) 进程 执行的 CMD 为 npm
        4 S root         15      1  0  80   0 -  1082 wait   10:36 ?        00:00:00 sh -c node server.js
        4 S root         16     15  0  80   0 - 221109 ep_pol 10:36 ?       00:00:00 node server.js
        4 S root         61      0  0  80   0 -  5059 wait   10:59 pts/0    00:00:00 /bin/bash
        0 R root         68     61  0  80   0 -  4373 -      11:00 pts/0    00:00:00 ps -elf
    root@7bf55b4d7744:/usr/src/app# ss -lntu
        Netid  State      Recv-Q Send-Q        Local Address:Port     Peer Address:Port
        tcp    LISTEN     0      128                      :::8080               :::*


// 观察 宿主机 上 网卡的变化: 启动容器时 在 宿主机上 新增了 一块 虚拟网卡
[root@node01 ~]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.100/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe52:8e39/64 scope link
           valid_lft forever preferred_lft forever
    3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
        link/ether 02:42:82:6d:e2:1a brd ff:ff:ff:ff:ff:ff
        inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
           valid_lft forever preferred_lft forever
        inet6 fe80::42:82ff:fe6d:e21a/64 scope link
           valid_lft forever preferred_lft forever
    9: vethf8ab950@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP  <----观察
        link/ether 76:c7:ef:63:0d:62 brd ff:ff:ff:ff:ff:ff link-netnsid 0
        inet6 fe80::74c7:efff:fe63:d62/64 scope link
           valid_lft forever preferred_lft forever

//  观察 发布端口 8080 到 宿主机端口 8000 时 宿主机上 iptables 的 nat 表中生成的 相应规则
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
    MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0
    MASQUERADE  tcp  --  172.17.0.2           172.17.0.2           tcp dpt:8080  <---观察

    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0
    DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:8000 to:172.17.0.2:8080  <---观察


[root@node01 ~]# docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    8f2c05ab4d03        bridge              bridge              local
    b95038e2394a        host                host                local
    28e6958b6080        none                null                local


[root@node01 ~]# docker network inspect 8f2c05ab4d03
[root@node01 ~]# docker network inspect bridge
    [
        {
            "Name": "bridge",
            "Id": "8f2c05ab4d03601ce7f04117ac015f07e7c448086816a9353da57234c48791b9",
            "Created": "2019-10-27T17:31:51.965220005+08:00",
            "Scope": "local",
            "Driver": "bridge", <----
            "EnableIPv6": false,
            "IPAM": {
                "Driver": "default",
                "Options": null,
                "Config": [
                    {
                        "Subnet": "172.17.0.0/16",
                        "Gateway": "172.17.0.1"  <-----观察，这正是 宿主机 的虚拟网卡 docker0 的 ip
                    }
                ]
            },
            "Internal": false,
            "Attachable": false,
            "Ingress": false,
            "ConfigFrom": {
                "Network": ""
            },
            "ConfigOnly": false,
            "Containers": {
                "7bf55b4d774477e5eb2fa4ee637a84b59f1b3cde34ff8a4e5dd17ad315f87bb6": {
                    "Name": "bb",
                    "EndpointID": "73a8e0a5a8e4f78b0c96fc11431ed96fb68aa1f2d138f2d6fdec9607c7d1bae1",
                    "MacAddress": "02:42:ac:11:00:02",
                    "IPv4Address": "172.17.0.2/16",  <----观察, 这正是本示例中 启动的 容器的 ip
                    "IPv6Address": ""
                }
            },
            "Options": {
                "com.docker.network.bridge.default_bridge": "true",
                "com.docker.network.bridge.enable_icc": "true",
                "com.docker.network.bridge.enable_ip_masquerade": "true",
                "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
                "com.docker.network.bridge.name": "docker0",  <----观察, docker0 被用作 docker 网络中 bridge 网络的 桥(交换机)
                "com.docker.network.driver.mtu": "1500"
            },
            "Labels": {}
        }
    ]



----------------------------------------------------------------------------------------------------
docker 网络

https://docs.docker.com/network/


https://docs.docker.com/network/iptables/
https://success.docker.com/article/networking


Network drivers (网络驱动)

    - bridge  默认的网络驱动
    - host    直接使用宿主机的网络
    - overlay
    - macvlan
    - none
    - Network plugins


Network driver summary (网络驱动总结)

    - User-defined bridge networks are best when you need multiple containers to communicate on the same Docker host.
      // 适用于 相同 宿主机 上的 多个容器 需要彼此通信时

    - Host networks are best when the network stack should not be isolated from the Docker host,
      but you want other aspects of the container to be isolated.
      // 适用于 仅让 容器的网络 与 宿主机的 网络 不被隔离的情况(容器共享宿主机的网络,其他资源隔离).

    - Overlay networks are best when you need containers running on different Docker hosts to communicate,
      or when multiple applications work together using swarm services.
      // 适用于 多个 不同的 宿主机 上的 容器 需要彼此 通信的情况

    - Macvlan networks are best when you are migrating from a VM setup or need your containers
      to look like physical hosts on your network, each with a unique MAC address.

    - Third-party network plugins allow you to integrate Docker with specialized network stacks.





----------------------------------------------------------------------------------------------------
Use bridge networks

    https://docs.docker.com/network/bridge/


  When you start Docker, a default bridge network (also called bridge) is created automatically,
  and newly-started containers connect to it unless otherwise specified.

  选择使用 bridge 网络时, 生产环境中推荐使用 User-defined bridge networks


----------
Differences between user-defined bridges and the default bridge (用户定义的 bridges 与 默认 bridge 的区别)

  1) User-defined bridges provide better isolation and interoperability between containerized applications.
     // User-defined bridges 提供 更好的 隔离 和 互操作性

      Containers connected to the same user-defined bridge network automatically expose all ports to each other,
      and no ports to the outside world. This allows containerized applications to communicate
      with each other easily, without accidentally opening access to the outside world.
      // 连接到 相同 user-defined bridge network 的 Containers 向彼此 暴露(导出) 所有端口(expose all ports),
      // 但是 没有端口 会被暴露(导出) 到 the outside world. 这允许容器之间 很容易 做到 彼此访问, 而不会意外的
      // 向 the outside world 开放 访问权限.

      如 某个应用 由 一个 web 前端 和 一个 database 后端 组成，The outside world 仅需 访问 web 前端(如 80 端口),
      当 仅 后端本身 需要访问 the database host and port, 使用 a user-defined bridge, 仅需对外开放 web 端口(如 80 端口),
      而 database 应用程序 不需要 对外 开放 任何端口, 因为 web 前端 可以通过 the user-defined bridge 访问到该 database.

      而 如果你在 the default bridge network 中 使用相同的 应用栈(application stack),
      你需要同时 通过 -p 或 --publish 选项 来开放 该 web 端口 和 该 database 端口, 这意味着
      Docker host 需要依靠 其他方式 来 阻止对 该 database 端口的 访问.

    2) User-defined bridges provide automatic DNS resolution between containers.

      在 the default bridge network 中的 Containers 仅能通过 ip 地址来访问彼此, 除非使用 遗留(legacy)的 --link 选项,
      而在 user-defined bridge network 中, containers 可以通过 name 或 alias 来 解析(resolve)彼此.

      比如在 user-defined bridge network 中, web 前端 和 database 后端应用 所在的 containers 分别 叫做 'web' 和 'db',
      该 web 容器可以 connect 到 处于 'db' 处的 db 容器, 而 不管 该 application stack 运行于 哪个 Docker host.

      而 如果你在 the default bridge network 中跑 相同的 application stack, 你需要使用 遗留(legacy)的 --link 选项 在
      the containers 之间 手动创建 links, 这些 links 需要被 双向创建(即在 两个方向上 都被创建), 因此 你会看到
      在多于 2 个以上的 containers 之间 需要彼此通信时 情况会变得 复杂.
      另一种替代 方式是 修改 the containers 中的 /etc/hosts 文件, 但这会产生 难以 调试(debug) 的 problems.

    3) Containers can be attached and detached from user-defined networks on the fly.
      // 容器 可以 从 user-defined networks 中 动态地(on the fly) 被 attached 和 detached.

      During a container’s lifetime, you can connect or disconnect it from user-defined networks on the fly.
      To remove a container from the default bridge network,
      you need to stop the container and recreate it with different network options.
      // 在 container 的 生命期间, 你 可以动态的(on the fly) 与 user-defined networks 建立连接(connect) 或 断开连接(disconnect).
      // 而为了 从 the default bridge network 中 移除 一个 容器, 你需要 停止(stop) 该容器 并 使用 不同的 network 选项 来对其重新创建.

    4) Each user-defined network creates a configurable bridge.

      如果你的容器 使用了 the default bridge network, 你可以 对其 进行配置, 但是
      所有的 containers 将使用 相同的 settings, 如 MTU 和 iptables rules.
      另外, configuring the default bridge network happens outside of Docker itself,
      且 必须 重启(restart) Docker.

      User-defined bridge networks are created and configured using docker network create.
      If different groups of applications have different network requirements,
      you can configure each user-defined bridge separately, as you create it.
      // User-defined bridge networks 通过 使用命令 `docker network create` 被 创建(created) 和 配置(configured)
      // 如果 不同 组的 applications 要求 不同的 network 需求(requirements), 你可以 对每个 user-defined bridge
      // 分别配置, 就如同其被你创建时一样。

    5) Linked containers on the default bridge network share environment variables.

        Originally, the only way to share environment variables between two containers was
        to link them using the --link flag. This type of variable sharing is not possible
        with user-defined networks. However, there are superior ways(更高级的方法)
        to share environment variables. A few ideas:

      - Multiple containers can mount a file or directory containing the shared information, using a Docker volume.
        // 使用 Docker 卷(volume)

      - Multiple containers can be started together using docker-compose and the compose file can define the shared variables.

      - You can use swarm services instead of standalone containers, and take advantage of shared secrets and configs.


    Containers connected to the same user-defined bridge network effectively expose all ports to each other.
    For a port to be accessible to containers or non-Docker hosts on different networks,
    that port must be published using the -p or --publish flag.
    // 对外开放的 容器端口 必须使用通过 -p 或 --publish 选项 来 发布.



----------
Manage a user-defined bridge (管理用户自定义网络)

// 查看命令 `docker network` 简要帮助
[root@node01 ~]# docker network --help

        Usage:  docker network COMMAND

        Manage networks

        Commands:
          connect     Connect a container to a network
          create      Create a network
          disconnect  Disconnect a container from a network
          inspect     Display detailed information on one or more networks
          ls          List networks
          prune       Remove all unused networks
          rm          Remove one or more networks

        Run 'docker network COMMAND --help' for more information on a command.


// 查看命令 `docker network create` 简要帮助, 更多详细帮助见 `man docker-network-create`
[root@node01 ~]# docker network create --help

        Usage:  docker network create [OPTIONS] NETWORK

        Create a network

        Options:
              --attachable           Enable manual container attachment
              --aux-address map      Auxiliary IPv4 or IPv6 addresses used by Network driver (default map[])
              --config-from string   The network from which copying the configuration
              --config-only          Create a configuration only network
          -d, --driver string        Driver to manage the Network (default "bridge")  <----默认为 bridge
              --gateway strings      IPv4 or IPv6 Gateway for the master subnet
              --ingress              Create swarm routing-mesh network
              --internal             Restrict external access to the network
              --ip-range strings     Allocate container ip from a sub-range
              --ipam-driver string   IP Address Management Driver (default "default")
              --ipam-opt map         Set IPAM driver specific options (default map[])
              --ipv6                 Enable IPv6 networking
              --label list           Set metadata on a network
          -o, --opt map              Set driver specific options (default map[])
              --scope string         Control the network's scope
              --subnet strings       Subnet in CIDR format that represents a network segment



// 使用命令 `docker network create` 创建 a user-defined bridge network
[root@node01 ~]# docker network create my-net
    f359161e8488e2428b588b89e724bfbc95f06b2e0216457f05b0c0d2456523b1

[root@node01 ~]# docker network ls
      NETWORK ID          NAME                DRIVER              SCOPE
      3e3e7e11ec22        bridge              bridge              local
      b95038e2394a        host                host                local
      f359161e8488        my-net              bridge              local <-----
      28e6958b6080        none                null                local

[root@node01 ~]# docker network inspect my-net
    [
        {
            "Name": "my-net",
            "Id": "f359161e8488e2428b588b89e724bfbc95f06b2e0216457f05b0c0d2456523b1",
            "Created": "2019-10-29T07:46:26.872317567+08:00",
            "Scope": "local",
            "Driver": "bridge",
            "EnableIPv6": false,
            "IPAM": {
                "Driver": "default",
                "Options": {},
                "Config": [
                    {
                        "Subnet": "172.18.0.0/16", <----
                        "Gateway": "172.18.0.1"    <----观察,此为宿主机上虚拟网卡 br-f359161e8488 的地址
                    }
                ]
            },
            "Internal": false,
            "Attachable": false,
            "Ingress": false,
            "ConfigFrom": {
                "Network": ""
            },
            "ConfigOnly": false,
            "Containers": {},
            "Options": {},
            "Labels": {}
        }
    ]


// 观察 宿主机 网卡信息变化: 新增了 一块新的虚拟网卡 'br-f359161e8488'
[root@node01 ~]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.100/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe52:8e39/64 scope link
           valid_lft forever preferred_lft forever
    3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
        link/ether 02:42:61:d4:59:bf brd ff:ff:ff:ff:ff:ff
        inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
           valid_lft forever preferred_lft forever
    4: br-f359161e8488: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN   <-----观察
        link/ether 02:42:32:cb:04:a6 brd ff:ff:ff:ff:ff:ff
        inet 172.18.0.1/16 brd 172.18.255.255 scope global br-f359161e8488
           valid_lft forever preferred_lft forever



// 观察 iptables 中 nat 表相关规则
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
    MASQUERADE  all  --  172.18.0.0/16        0.0.0.0/0           <----
    MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0

    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0            <----
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0

// 观察路由表信息
[root@node01 ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
    172.18.0.0      0.0.0.0         255.255.0.0     U     0      0        0 br-f359161e8488 <----
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33



----------
Connect a container to a user-defined bridge (见容器 连接到 用户自定义网络)


    When you create a new container, you can specify one or more --network flags.

// 查看一下 命令 `docker container create` 简要帮助
[root@node01 ~]# docker container create --help     #更多详细帮助见 `man docker-container-create`

      Usage:  docker container create [OPTIONS] IMAGE [COMMAND] [ARG...]

      Create a new container

      Options:
            --add-host list                  Add a custom host-to-IP mapping (host:ip)
        -a, --attach list                    Attach to STDIN, STDOUT or STDERR
            --blkio-weight uint16            Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)
            --blkio-weight-device list       Block IO weight (relative device weight) (default [])
            --cap-add list                   Add Linux capabilities
            --cap-drop list                  Drop Linux capabilities
            --cgroup-parent string           Optional parent cgroup for the container
            --cidfile string                 Write the container ID to the file
            --cpu-period int                 Limit CPU CFS (Completely Fair Scheduler) period
            --cpu-quota int                  Limit CPU CFS (Completely Fair Scheduler) quota
            --cpu-rt-period int              Limit CPU real-time period in microseconds
            --cpu-rt-runtime int             Limit CPU real-time runtime in microseconds
        -c, --cpu-shares int                 CPU shares (relative weight)
            --cpus decimal                   Number of CPUs
            --cpuset-cpus string             CPUs in which to allow execution (0-3, 0,1)
            --cpuset-mems string             MEMs in which to allow execution (0-3, 0,1)
            --device list                    Add a host device to the container
            --device-cgroup-rule list        Add a rule to the cgroup allowed devices list
            --device-read-bps list           Limit read rate (bytes per second) from a device (default [])
            --device-read-iops list          Limit read rate (IO per second) from a device (default [])
            --device-write-bps list          Limit write rate (bytes per second) to a device (default [])
            --device-write-iops list         Limit write rate (IO per second) to a device (default [])
            --disable-content-trust          Skip image verification (default true)
            --dns list                       Set custom DNS servers
            --dns-option list                Set DNS options
            --dns-search list                Set custom DNS search domains
            --domainname string              Container NIS domain name
            --entrypoint string              Overwrite the default ENTRYPOINT of the image
        -e, --env list                       Set environment variables
            --env-file list                  Read in a file of environment variables
            --expose list                    Expose a port or a range of ports
            --gpus gpu-request               GPU devices to add to the container ('all' to pass all GPUs)
            --group-add list                 Add additional groups to join
            --health-cmd string              Command to run to check health
            --health-interval duration       Time between running the check (ms|s|m|h) (default 0s)
            --health-retries int             Consecutive failures needed to report unhealthy
            --health-start-period duration   Start period for the container to initialize before starting health-retries countdown (ms|s|m|h) (default 0s)
            --health-timeout duration        Maximum time to allow one check to run (ms|s|m|h) (default 0s)
            --help                           Print usage
        -h, --hostname string                Container host name
            --init                           Run an init inside the container that forwards signals and reaps processes
        -i, --interactive                    Keep STDIN open even if not attached
            --ip string                      IPv4 address (e.g., 172.30.100.104)
            --ip6 string                     IPv6 address (e.g., 2001:db8::33)
            --ipc string                     IPC mode to use
            --isolation string               Container isolation technology
            --kernel-memory bytes            Kernel memory limit
        -l, --label list                     Set meta data on a container
            --label-file list                Read in a line delimited file of labels
            --link list                      Add link to another container
            --link-local-ip list             Container IPv4/IPv6 link-local addresses
            --log-driver string              Logging driver for the container
            --log-opt list                   Log driver options
            --mac-address string             Container MAC address (e.g., 92:d0:c6:0a:29:33)
        -m, --memory bytes                   Memory limit
            --memory-reservation bytes       Memory soft limit
            --memory-swap bytes              Swap limit equal to memory plus swap: '-1' to enable unlimited swap
            --memory-swappiness int          Tune container memory swappiness (0 to 100) (default -1)
            --mount mount                    Attach a filesystem mount to the container
            --name string                    Assign a name to the container
            --network network                Connect a container to a network  <---注: 选项 --network 可以指定多次
            --network-alias list             Add network-scoped alias for the container
            --no-healthcheck                 Disable any container-specified HEALTHCHECK
            --oom-kill-disable               Disable OOM Killer
            --oom-score-adj int              Tune host's OOM preferences (-1000 to 1000)
            --pid string                     PID namespace to use
            --pids-limit int                 Tune container pids limit (set -1 for unlimited)
            --privileged                     Give extended privileges to this container
        -p, --publish list                   Publish a container's port(s) to the host
        -P, --publish-all                    Publish all exposed ports to random ports
            --read-only                      Mount the container's root filesystem as read only
            --restart string                 Restart policy to apply when a container exits (default "no")
            --rm                             Automatically remove the container when it exits
            --runtime string                 Runtime to use for this container
            --security-opt list              Security Options
            --shm-size bytes                 Size of /dev/shm
            --stop-signal string             Signal to stop a container (default "SIGTERM")
            --stop-timeout int               Timeout (in seconds) to stop a container
            --storage-opt list               Storage driver options for the container
            --sysctl map                     Sysctl options (default map[])
            --tmpfs list                     Mount a tmpfs directory
        -t, --tty                            Allocate a pseudo-TTY
            --ulimit ulimit                  Ulimit options (default [])
        -u, --user string                    Username or UID (format: <name|uid>[:<group|gid>])
            --userns string                  User namespace to use
            --uts string                     UTS namespace to use
        -v, --volume list                    Bind mount a volume
            --volume-driver string           Optional volume driver for the container
            --volumes-from list              Mount volumes from the specified container(s)
        -w, --workdir string                 Working directory inside the container



// 基于 image 'nginx:latest' 创建 名为 'my-nginx' 的容器, 并将其连接到 'my-net' 网络, 且将容器中的 80 端口发布到 宿主机上的 8080 端口
// 注: 此处的 create 和 run 的区别是 子命令 create 创建容器 但 不会 自动启动运行容器
[root@node01 ~]# docker container create --name my-nginx --network my-net --publish 8080:80 nginx:latest

      Unable to find image 'nginx:latest' locally
      latest: Pulling from library/nginx
      8d691f585fa8: Pull complete
      5b07f4e08ad0: Pull complete
      abc291867bca: Pull complete
      Digest: sha256:922c815aa4df050d4df476e92daed4231f466acc8ee90e0e774951b0fd7195a4
      Status: Downloaded newer image for nginx:latest
      e86279a2b8d6f9c226b3a09767e96cbbf93e74d78c099e47e3c4cd5265acd618

// 查看 运行着的 容器
[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
// 查看 所有的 容器
[root@node01 ~]# docker container ls -a   #注: 可以使用 --no-trunc 查看 非截断的信息
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS                    NAMES
    e86279a2b8d6        nginx:latest        "nginx -g 'daemon of…"   8 minutes ago       Created                                              my-nginx <----
    7bf55b4d7744        bulletinboard:1.0   "npm start"              38 hours ago        Exited (255) 11 hours ago   0.0.0.0:8000->8080/tcp   bb
    d30997a78cc3        hello-world         "/hello"                 39 hours ago        Exited (0) 39 hours ago                              nervous_hugle


[root@node01 ~]# docker container inspect  my-nginx
[
    {
        "Id": "e86279a2b8d6f9c226b3a09767e96cbbf93e74d78c099e47e3c4cd5265acd618",
        "Created": "2019-10-29T00:13:39.413127247Z",
        "Path": "nginx",
        "Args": [
            "-g",
            "daemon off;"
        ],

      ......
            "NetworkMode": "my-net",
            "PortBindings": {
                "80/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "8080"
                    }
                ]
            },
      ......
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {},
            "SandboxKey": "",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "my-net": { <---
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "",
                    "EndpointID": "",
                    "Gateway": "",
                    "IPAddress": "",
                    "IPPrefixLen": 0,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "",
                    "DriverOpts": null
                }
            }

[root@node01 ~]# docker container start my-nginx
    my-nginx
[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
    e86279a2b8d6        nginx:latest        "nginx -g 'daemon of…"   23 minutes ago      Up 5 seconds        0.0.0.0:8080->80/tcp   my-nginx



[root@node01 ~]# docker container inspect  my-nginx

              "Networks": {
                  "my-net": { <----
                      "IPAMConfig": null,
                      "Links": null,
                      "Aliases": [
                          "e86279a2b8d6"
                      ],
                      "NetworkID": "f359161e8488e2428b588b89e724bfbc95f06b2e0216457f05b0c0d2456523b1",
                      "EndpointID": "e4a32139454a493bf83f5a3337d984dbcdd0d74117362d0dff0a63af6686f2ee",
                      "Gateway": "172.18.0.1",   <----
                      "IPAddress": "172.18.0.2", <----
                      "IPPrefixLen": 16,
                      "IPv6Gateway": "",
                      "GlobalIPv6Address": "",
                      "GlobalIPv6PrefixLen": 0,
                      "MacAddress": "02:42:ac:12:00:02",
                      "DriverOpts": null
                  }
              }


[root@node01 ~]# docker network inspect my-net
[
    {
        "Name": "my-net",
        "Id": "f359161e8488e2428b588b89e724bfbc95f06b2e0216457f05b0c0d2456523b1",
        "Created": "2019-10-29T07:46:26.872317567+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },

    ... ...
        "Containers": {
            "e86279a2b8d6f9c226b3a09767e96cbbf93e74d78c099e47e3c4cd5265acd618": {
                "Name": "my-nginx",  <-----
                "EndpointID": "e4a32139454a493bf83f5a3337d984dbcdd0d74117362d0dff0a63af6686f2ee",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",  <-----
                "IPv6Address": ""
            }
        },



// 将运行着的 容器 'my-nginx' 与 用户自定义的 bridge 网络 ‘my-net’ 断开连接
[root@node01 ~]# docker network disconnect my-net my-nginx

[root@node01 ~]# docker network inspect my-net

        "Containers": {},

[root@node01 ~]# docker container inspect my-nginx

  ......
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "1cd8bd90bbeeabb58201e551e78e318b41d25a3dee3adc01379639209c71fcde",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {},
            "SandboxKey": "/var/run/docker/netns/1cd8bd90bbee",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {}
        }
  ......


// 将 运行着的 容器 'my-nginx' 与 用户自定义的 bridge 网络 'my-net' 建立连接
[root@node01 ~]# docker network connect my-net my-nginx

[root@node01 ~]# docker network inspect my-net

    ......
        "Containers": {
            "e86279a2b8d6f9c226b3a09767e96cbbf93e74d78c099e47e3c4cd5265acd618": {
                "Name": "my-nginx",
                "EndpointID": "e92d5fed1c4fe390dad5d4bb6ebd7ac30d723257346205cc277eff6393f580be",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            }
    ......


// 使用命令 `docker network rm` 移除 a user-defined bridge network, 注: remove 前需要将当前连接到 该network 的 container 断开连接
[root@node01 ~]# docker network disconnect my-net my-nginx   #断开容器 'my-nginx' 与网络 'my-net' 的连接
[root@node01 ~]# docker network rm my-net      #删除(remove)网络 'my-net'
    my-net

[root@node01 ~]# docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    3e3e7e11ec22        bridge              bridge              local
    b95038e2394a        host                host                local
    28e6958b6080        none                null                local

      --------------------
      // 启用 ipv6 的支持
            https://docs.docker.com/config/daemon/ipv6/
            https://docs.docker.com/network/bridge/
            https://github.com/moby/moby/issues/36954
            https://docs.docker.com/v17.09/engine/userguide/networking/default_network/ipv6/
        中文:
            https://blog.csdn.net/taiyangdao/article/details/83066009
            https://blog.csdn.net/bleatingsheep/article/details/80534153

      --------------------


      --------------------
      // Enable forwarding from Docker containers to the outside world (为 the default bridge network 中的 容器提供 路由转发功能)

      1) Configure the Linux kernel to allow IP forwarding.

            $ sysctl net.ipv4.conf.all.forwarding=1

      2) Change the policy for the iptables FORWARD policy from DROP to ACCEPT.

            $ sudo iptables -P FORWARD ACCEPT

      These settings do not persist across a reboot, so you may need to add them to a start-up script.
      --------------------


  ------------------------------
  Use the default bridge network (使用默认的 bridge 网络) (不推荐)

      the default bridge network 被认为是 Docker 的遗留过时的 detail 且不建议在 生产环境(production)中使用.
      配置它 需要手动操作, 且 其 存在 技术缺陷(technical shortcomings)

  - Connect a container to the default bridge network

      If you do not specify a network using the --network flag, and you do specify a network driver,
      your container is connected to the default 'bridge' network by default.
      Containers connected to the default 'bridge' network can communicate,
      but only by IP address, unless they are linked using the legacy --link flag.

  - Configure the default bridge network (/etc/docker/daemon.json)

        {
          "bip": "192.168.1.5/24",
          "fixed-cidr": "192.168.1.5/25",
          "fixed-cidr-v6": "2001:db8::/64",
          "mtu": 1500,
          "default-gateway": "10.20.1.1",
          "default-gateway-v6": "2001:db8:abcd::89",
          "dns": ["10.20.1.2","10.20.1.3"]
        }

      核心选项为bip，即bridge ip之意，用于指定docker0桥自身的IP地址；其它选项可通过此地址计算得出。

      配置后 需要重启 docker
  ------------------------------





----------------------------------------------------------------------------------------------------
Use host networking   注: host 网络驱动仅工作在 Linux hosts 上

    https://docs.docker.com/network/host/
    https://docs.docker.com/network/network-tutorial-host/

  container 和 宿主机 共享 网络名称空间, container 不会单独分配其自己的 ip 地址, 例如,
  如果 你 运行一个 bind 到 80 号端口的容器 且使用的是 host networking, 则 该 容器的 application
  在 宿主机的 ip 上的 80 号端口是 可用的.

    ----------
    Note: Given that the container does not have its own IP-address when using host mode networking,
          port-mapping does not take effect, and the -p, --publish, -P, and --publish-all
          option are ignored, producing a warning instead:

          WARNING: Published ports are discarded when using host network mode
    ----------

  Host mode networking can be useful to optimize performance, and in situations where
  a container needs to handle a large range of ports, as it does not require network address translation (NAT),
  and no “userland-proxy” is created for each port.

  The host networking driver only works on Linux hosts, and is not supported on Docker Desktop for Mac,
  Docker Desktop for Windows, or Docker EE for Windows Server.
  //  host 网络驱动仅工作在 Linux hosts 上.


Networking using the host network
    https://docs.docker.com/network/network-tutorial-host/


示例: 将 nginx 通过 host 网络的方式 直接绑定到 Docker 上的 80 端口,
      从网络的角度来看, 这就好像是 nginx 进程 直接运行于 Docker 宿主机上 而非 容器中。
      但是，在其他方面，例如 storage, process namespace, 和 user namespace,  nginx 和 宿主机 是 隔离的.



[root@node01 ~]# docker container run --rm -d --network host --name my_nginx nginx    #注: 选项 --rm 用于在 容器 exits 时自动删除容器
    09bc947045398fef4a0a36bb0a355156941a8c757119c0122549f3bbea18096c

浏览器访问  http://192.168.175.100/

[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
    09bc94704539        nginx               "nginx -g 'daemon of…"   About a minute ago   Up About a minute                       my_nginx


// 观察一下 宿主机 网卡信息: 发现并没有 新的网卡被 创建添加
[root@node01 ~]# ip addr show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.100/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe52:8e39/64 scope link
           valid_lft forever preferred_lft forever
    3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
        link/ether 02:42:37:15:02:c3 brd ff:ff:ff:ff:ff:ff
        inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
           valid_lft forever preferred_lft forever

// 查看端口信息
[root@node01 ~]# netstat -tulpn | grep :80
    tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2126/nginx: master



[root@node01 ~]# docker container inspect my_nginx

    ......
            "Networks": {
                "host": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "b95038e2394a7ec3e54af5e677d7be7f837445b2ed59645e9ddab8387ea9a812",
                    "EndpointID": "39e04209ade2815dec9739a0ecbedafe5dc8d40dd6177058e8304303059385b9",
                    "Gateway": "",
                    "IPAddress": "",
                    "IPPrefixLen": 0,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "",
                    "DriverOpts": null
                }
            }
    ......

[root@node01 ~]# docker network ls
    NETWORK ID          NAME                DRIVER              SCOPE
    8e384223d2e1        bridge              bridge              local
    b95038e2394a        host                host                local <-----
    28e6958b6080        none                null                local

[root@node01 ~]# docker network inspect host

    [
        {
            "Name": "host",
            "Id": "b95038e2394a7ec3e54af5e677d7be7f837445b2ed59645e9ddab8387ea9a812",
            "Created": "2019-10-27T17:29:40.887513119+08:00",
            "Scope": "local",
            "Driver": "host",  <----
            "EnableIPv6": false,
            "IPAM": {
                "Driver": "default",
                "Options": null,
                "Config": []
            },
            "Internal": false,
            "Attachable": false,
            "Ingress": false,
            "ConfigFrom": {
                "Network": ""
            },
            "ConfigOnly": false,
            "Containers": {
                "09bc947045398fef4a0a36bb0a355156941a8c757119c0122549f3bbea18096c": {
                    "Name": "my_nginx", <-----
                    "EndpointID": "39e04209ade2815dec9739a0ecbedafe5dc8d40dd6177058e8304303059385b9",
                    "MacAddress": "",
                    "IPv4Address": "",
                    "IPv6Address": ""
                }
            },
            "Options": {},
            "Labels": {}
        }
    ]


// 停止(stop)  容器 'my_nginx'
[root@node01 ~]# docker container stop my_nginx
    my_nginx

[root@node01 ~]# docker container ls -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS                    NAMES
    7bf55b4d7744        bulletinboard:1.0   "npm start"         45 hours ago        Exited (255) 18 hours ago   0.0.0.0:8000->8080/tcp   bb
    d30997a78cc3        hello-world         "/hello"            46 hours ago        Exited (0) 46 hours ago                              nervous_hugle




----------------------------------------------------------------------------------------------------










