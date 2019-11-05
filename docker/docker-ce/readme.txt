
docker 是使用 go 语言实现的

编写 Dockerfiles 的最佳实践:
https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

https://docs.docker.com/

https://hub.docker.com/


https://docs.docker.com/reference/


docker 国内加速地址
  https://www.jianshu.com/p/b5006ebf1522


docker 概览:
  https://docs.docker.com/engine/docker-overview/

docker 架构:
  https://docs.docker.com/engine/docker-overview/#docker-architecture


Docker - 从入门到实践
    https://yeasy.gitbooks.io/docker_practice/



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
示例: 让 容器 'centos7_02' 去 使用 另一个容器 'centos7_01' 的 network stack
      即 容器 'centos7_02' 共享 'centos7_01' 的 网络名称空间


https://docs.docker.com/engine/reference/run/#network-settings
https://forums.docker.com/t/shared-network-namespaces-using-net-container/16697
https://stackoverflow.com/questions/55399695/attaching-a-docker-container-to-another-containers-network-with-net-container

[root@node01 ~]# docker container run -dit --name centos7_01 centos:7
    5c87327b1c9edc9d9b3c003e901a473db38eabc0c7f1b2aa0ef87a4c5062ecd2

[root@node01 ~]# docker container run -dit --name centos7_02 --network=container:centos7_01  centos:7  #容器'centos7_02' 使用容器 'centos7_01' 的 network stack



[root@node01 ~]# docker container inspect centos7_02

            "NetworkMode": "container:5c87327b1c9edc9d9b3c003e901a473db38eabc0c7f1b2aa0ef87a4c5062ecd2",



[root@node01 ~]# docker container exec -it centos7_01 bash    #在容器 'centos7_01' 中 执行如下操作

      [root@5c87327b1c9e /]# yum -y install net-tools

      [root@5c87327b1c9e /]# ifconfig eth0
      eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
              inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
              ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
              RX packets 1466  bytes 10026523 (9.5 MiB)
              RX errors 0  dropped 0  overruns 0  frame 0
              TX packets 1324  bytes 75238 (73.4 KiB)
              TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

      [root@5c87327b1c9e /]# yum -y install httpd
      [root@5c87327b1c9e /]# httpd -k start
      [root@5c87327b1c9e /]# netstat -anptu
      Active Internet connections (servers and established)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
      tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      105/httpd




[root@node01 ~]# docker container exec -it centos7_02 bash   #在容器 'centos7_02' 中 执行如下操作
      [root@5c87327b1c9e /]# yum -y install net-tools

      [root@5c87327b1c9e /]# ifconfig eth0
      eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
              inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
              ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
              RX packets 2855  bytes 20047967 (19.1 MiB)
              RX errors 0  dropped 0  overruns 0  frame 0
              TX packets 2506  bytes 143388 (140.0 KiB)
              TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

      [root@5c87327b1c9e /]# curl -I http://localhost    #通过 localhost 访问 容器 'centos7_01' httpd 服务
          HTTP/1.1 403 Forbidden
          Date: Mon, 04 Nov 2019 09:57:37 GMT
          Server: Apache/2.4.6 (CentOS)
          Last-Modified: Thu, 16 Oct 2014 13:20:58 GMT
          ETag: "1321-5058a1e728280"
          Accept-Ranges: bytes
          Content-Length: 4897
          Content-Type: text/html; charset=UTF-8



// 关闭容器 'centos7_01'
[root@node01 ~]# docker container stop centos7_01
centos7_01
[root@node01 ~]# docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
786405fef4a5        centos:7            "/bin/bash"         27 minutes ago      Up 27 minutes                           centos7_02

[root@node01 ~]# docker container exec -it centos7_02 bash    #在容器 'centos7_02' 中 执行如下操作
    [root@5c87327b1c9e /]# ifconfig      #可以观察到, 容器 centos7_02 去使用 centos7_01 的 network stack 时, 如果关闭了 centos7_01, 则 centos7_02 也就失去了 network stack
    lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
            inet 127.0.0.1  netmask 255.0.0.0
            loop  txqueuelen 1  (Local Loopback)
            RX packets 74  bytes 21060 (20.5 KiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 74  bytes 21060 (20.5 KiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0



----------------------------------------------------------------------------------------------------
Manage data in Docker

    https://docs.docker.com/storage/


By default all files created inside a container are stored on a writable container layer. This means that:
// 默认在容器中创建的所有的文件 被 存储在 一个 可写的 容器层中, 这意味着:

    - The data doesn’t persist when that container no longer exists,
      and it can be difficult to get the data out of the container if another process needs it.
      //  data 无法在 容器不存在时 维持(如 容器一旦被删除, data 也就丢失了). 且 如果其他 process
      //  需要这些数据, 很难再 容器外部 获取 这些数据.

    - A container’s writable layer is tightly coupled to the host machine where the container is running.
      You can’t easily move the data somewhere else.
      // 容器的 可写层 与 运行容器的 宿主机  耦合 紧密, 你无法轻松地将数据移动到 其他地方.

    - Writing into a container’s writable layer requires a storage driver to manage the filesystem.
      The storage driver provides a union filesystem, using the Linux kernel. This extra abstraction reduces performance
      as compared to using data volumes, which write directly to the host filesystem.
      // 向 容器的 writable layer 需要 a storage driver 来 管理 the filesystem.
      // 该 storage driver 使用 Linux kernel 提供了 a union filesystem (联合文件系统).
      // 该额外的 抽象 比起 使用 data volumes 降低了 性能, 因为 data volumes 是 直接写入 the host filesystem.

        考虑方面: 数据共享 及 持久存储，容器 和 数据 迁移 , 性能


          volumes  <---- 推荐 recommend
          bind mounts

      Linux 上还可使用 tmpfs mount


          +------host-------------------------------------------------------+
          |                              +------------+                     |
          |              +---------------|  container |------+              |
          |              |               +------------+      |              |
          |   bind mount |                       |           |              |
          |              V                       |volume     |              |
          |           +--------------------+     |           |tmpfs mount   |
          |           |                    |     |           |              |
          |           |  Filesystem        |     |           |              |
          |           |                    |     |           V              |
          |           |  +-------------+   |     |      +--------+          |
          |           |  |Docker area  |<--|-----+      | Memory |          |
          |           |  +-------------+   |            +--------+          |
          |           |                    |                                |
          |           +--------------------+                                |
          |                                                                 |
          +-----------------------------------------------------------------+


    - Volumes are stored in a part of the host filesystem which is managed by Docker (/var/lib/docker/volumes/ on Linux).
      Non-Docker processes should not modify this part of the filesystem. Volumes are the best way to persist data in Docker.

    - Bind mounts may be stored anywhere on the host system. They may even be important system files or directories.
      Non-Docker processes on the Docker host or a Docker container can modify them at any time.

    - tmpfs mounts are stored in the host system’s memory only, and are never written to the host system’s filesystem.


--------------------
https://docs.docker.com/storage/

  https://docs.docker.com/storage/volumes/

Volumes:
      Created and managed by Docker. You can create a volume explicitly using the docker volume create command,
      or Docker can create a volume during container or service creation.
      // 卷(Volumes) 由 Docker 创建并管理. 可以显示地使用命令 `docker volume create` 创建卷, 或在 container 或 service
      // 创建期间 创建 卷

      When you create a volume, it is stored within a directory on the Docker host.
      When you mount the volume into a container, this directory is what is mounted into the container.
      This is similar to the way that bind mounts work, except that volumes are managed
      by Docker and are isolated from the core functionality of the host machine.

      A given volume can be mounted into multiple containers simultaneously.
      When no running container is using a volume, the volume is still available to Docker
      and is not removed automatically. You can remove unused volumes using docker volume prune.
      // 一个 volume 可以同时(simultaneously) 被多个 containers 挂载. 当 没有运行着的 容器正在使用 卷时,
      // 该 volume 对 Docker 仍然 可用(available) 且 不会被 自动删除(removed), 你 可以使用
      // 命令 `docker volume prune` 来 remove 不再被使用的 volumes.

      When you mount a volume, it may be named or anonymous. Anonymous volumes are
      not given an explicit name when they are first mounted into a container,
      so Docker gives them a random name that is guaranteed to be unique within a given Docker host.
      Besides the name, named and anonymous volumes behave in the same ways.
      // 当 你挂载 a volume, 其可以被 命令(named) 或 是匿名的(anonymous)

      Volumes also support the use of volume drivers, which allow you to store
      your data on remote hosts or cloud providers, among other possibilities.


Bind mounts:

    Available since the early days of Docker. Bind mounts have limited functionality compared to volumes.
    When you use a bind mount, a file or directory on the host machine is mounted into a container.
    The file or directory is referenced by its full path on the host machine.
    The file or directory does not need to exist on the Docker host already.
    It is created on demand if it does not yet exist. Bind mounts are very performant,
    but they rely on the host machine’s filesystem having a specific directory structure available.
    If you are developing new Docker applications, consider using named volumes instead.
    You can’t use Docker CLI commands to directly manage bind mounts.
    // 如果你 正在 开发 新的 Docker applications, 应考虑使用 named volumes 而非 bind mounts.
    // 你无法 使用 Docker 命令行工具 来直接 管理 bind mounts.


  Bind mounts allow access to sensitive files (Bind mounts的一个副作用: 允许 访问敏感文件)
      One side effect of using bind mounts, for better or for worse,
      is that you can change the host filesystem via processes running in a container,
      including creating, modifying, or deleting important system files or directories.
      This is a powerful ability which can have security implications,
      including impacting non-Docker processes on the host system.


tmpfs mounts:
    A tmpfs mount is not persisted on disk, either on the Docker host or within a container.
    It can be used by a container during the lifetime of the container,
    to store non-persistent state or sensitive information. For instance, internally,
    swarm services use tmpfs mounts to mount secrets into a service’s containers.



Bind mounts and volumes can both be mounted into containers using the -v or --volume flag,
but the syntax for each is slightly different. For tmpfs mounts, you can use the --tmpfs flag.
However, in Docker 17.06 and higher, we recommend using the --mount flag for both containers and services,
for bind mounts, volumes, or tmpfs mounts, as the syntax is more clear.

------------------------------
Good use cases for volumes (卷 的 好的使用场景)

   作为首

Volumes are the preferred way to persist data in Docker containers and services. Some use cases for volumes include:
// Volumes 应 视为 Docker containers 和 services 的 数据持久化的 首选方式, 其一些使用场景包括:

    - Sharing data among multiple running containers. If you don’t explicitly create it,
      a volume is created the first time it is mounted into a container. When that container stops
      or is removed, the volume still exists. Multiple containers can mount the same volume simultaneously,
      either read-write or read-only. Volumes are only removed when you explicitly remove them.
      // 多个 运行的 容器之间 共享 数据

    - When the Docker host is not guaranteed to have a given directory or file structure.
      Volumes help you decouple the configuration of the Docker host from the container runtime.
      // 当 Docker host 不能保证 具有指定 目录 或 文件 结构的时候.
      // Volumes 能帮你 将 Docker host 的 the configuration  与 the container runtime 进行解耦.

    - When you want to store your container’s data on a remote host or a cloud provider, rather than locally.
      // 当 你想要 将 你的 container’s data 存储在 a remote host 或 a cloud provider 而非 本地时

    - When you need to back up, restore, or migrate data from one Docker host to another, volumes are a better choice.
      You can stop containers using the volume, then back up the volume’s directory (such as /var/lib/docker/volumes/<volume-name>).
      // 需要 在 不同宿主机上 进行 数据 备份, 还原 或 迁移 时, volumes 是更好的选择.




------------------------------
Good use cases for bind mounts (bind mounts 的 好的使用场景)

  In general, you should use volumes where possible. Bind mounts are appropriate for the following types of use case:

    - Sharing configuration files from the host machine to containers. This is how Docker provides
      DNS resolution to containers by default, by mounting /etc/resolv.conf from the host machine into each container.

    - Sharing source code or build artifacts between a development environment on the Docker host and a container.
      For instance, you may mount a Maven target/ directory into a container, and each time you build
      the Maven project on the Docker host, the container gets access to the rebuilt artifacts.

      If you use Docker for development this way, your production Dockerfile would copy the
      production-ready artifacts directly into the image, rather than relying on a bind mount.

    - When the file or directory structure of the Docker host is guaranteed to be consistent with the bind mounts the containers require.


------------------------------
Good use cases for tmpfs mounts

  tmpfs mounts are best used for cases when you do not want the data to persist either on
  the host machine or within the container. This may be for security reasons or to protect
  the performance of the container when your application needs to write a large volume of non-persistent state data.

------------------------------
提示, 使用 bind mounts 或 volumes 需要注意的一些地方

Tips for using bind mounts or volumes

  If you use either bind mounts or volumes, keep the following in mind:

      - If you mount an empty volume into a directory in the container in which files or directories exist,
        these files or directories are propagated (copied) into the volume. Similarly,
        if you start a container and specify a volume which does not already exist,
        an empty volume is created for you. This is a good way to pre-populate data that another container needs.
        // 挂载 空 卷到  容器中的某个 非空目录时, 该非空目录下的 文件 或 目录 会被 拷贝到 该 空卷中.
        // 类似地，如果启动了 一个容器 并制定了 一个 尚 不存在的 卷, 一个 空卷 会被 创建.
        // 这是 预填充(pre-populate) 另外的 容器 所需要的数据 的 好方法。

      - If you mount a bind mount or non-empty volume into a directory in the container in which some files or directories exist,
        these files or directories are obscured by the mount, just as if you saved files into /mnt on
        a Linux host and then mounted a USB drive into /mnt. The contents of /mnt would be obscured by
        the contents of the USB drive until the USB drive were unmounted. The obscured files are not removed or altered,
        but are not accessible while the bind mount or volume is mounted.
        // 如果你 挂载一个 bind mount 或 非空 卷 到  容器中的 一个 非空 目录, 则 该 非空目录下的 文件或目录
        // 会被  隐藏掩盖(obscured)起来

----------------------------------------------------------------------------------------------------
Use volumes  (使用卷)

    https://docs.docker.com/storage/volumes/

  Volumes use 'rprivate' bind propagation, and bind propagation is not configurable for volumes.


Choose the -v or --mount flag  (Docker 17.06 或 更高的版本推荐使用 --mount 选项. --mount 更加 明确 和 详细)

      New users should try --mount syntax which is simpler than --volume syntax.

  If you need to specify volume driver options, you must use --mount.
  // 如果需要 指定 volume driver 选项, 则 必须 使用 --mount


--mount: Consists of multiple key-value pairs, separated by commas(逗号) and each consisting of a <key>=<value> tuple.
         The --mount syntax is more verbose than -v or --volume, but the order of the keys is not significant,
         and the value of the flag is easier to understand.

      - The 'type' of the mount, which can be 'bind', 'volume', or 'tmpfs'.
        This topic discusses volumes, so the type is always 'volume'.

      - The 'source' of the mount. For named volumes, this is the name of the volume.
        For anonymous volumes, this field is omitted. May be specified as 'source' or 'src'.

      - The 'destination' takes as its value the path where the file or directory is
        mounted in the container. May be specified as 'destination', 'dst', or 'target'.

      - The 'readonly' option, if present, causes the bind mount to be mounted into the container as read-only.

      - The 'volume-opt' option, which can be specified more than once,
        takes a key-value pair consisting of the option name and its value.


  --------------------
  Escape values from outer CSV parser (关于转义)

      If your volume driver accepts a comma-separated list as an option,
      you must escape the value from the outer CSV parser. To escape a volume-opt,
      surround it with double quotes (") and surround the entire mount parameter with single quotes (').

      For example, the local driver accepts mount options as a comma-separated list in the o parameter.
      This example shows the correct way to escape the list.

    $ docker service create \
         --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>,volume-driver=local,volume-opt=type=nfs,volume-opt=device=<nfs-server>:<nfs-path>,"volume-opt=o=addr=<nfs-address>,vers=4,soft,timeo=180,bg,tcp,rw"'
        --name myservice \
        <IMAGE>
  --------------------


Create and manage volumes

    Unlike a bind mount, you can create and manage volumes outside the scope of any container.

// Create a volume(创建 卷):
[root@node01 ~]# docker volume create my-vol
    my-vol

// List volumes(列出 卷):
[root@node01 ~]# docker volume ls
    DRIVER              VOLUME NAME
    local               my-vol

// Inspect a volume(观察 卷详细信息):
[root@node01 ~]# docker volume inspect my-vol
    [
        {
            "CreatedAt": "2019-10-29T19:45:53+08:00",
            "Driver": "local",
            "Labels": {},
            "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
            "Name": "my-vol",
            "Options": {},
            "Scope": "local"
        }
    ]

// Remove a volume(移除 卷):
[root@node01 ~]# docker volume rm my-vol
    my-vol


// Start a container with a volume()

  If you start a container with a volume that does not yet exist, Docker creates the volume for you.
  The following example mounts the volume myvol2 into /app/ in the container.


[root@node01 ~]# docker run -d --name devtest --mount source=myvol2,target=/app  nginx:latest
    9983fc16bf55c3714a5a95aafea76e2141b43708f19ef3d6feb97d96623a7cdd


[root@node01 ~]# docker inspect devtest

    ......
        "Mounts": [
            {
                "Type": "volume",
                "Name": "myvol2",
                "Source": "/var/lib/docker/volumes/myvol2/_data",
                "Destination": "/app",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
    ......




// 删除 卷(volume) 'myvol2'

  1) 停止容器
  [root@node01 ~]# docker container stop devtest
      devtest

  2) 删除容器
  [root@node01 ~]# docker container rm devtest
      devtest

  3) 删除 卷 (volume) 'myvol2'
  [root@node01 ~]# docker volume rm myvol2
      myvol2



--------------------
Populate a volume using a container

    If you start a container which creates a new volume, as above, and the container has files
    or directories in the directory to be mounted (such as /app/ above), the directory’s
    contents are copied into the volume. The container then mounts and uses the volume,
    and other containers which use the volume also have access to the pre-populated content.


  To illustrate this, this example starts an nginx container and populates the new volume nginx-vol
  with the contents of the container’s /usr/share/nginx/html directory,
  which is where Nginx stores its default HTML content.


// 使用 容器 填充 新的空卷 'nginx-vol'
// 注: 该命令中 volume 'nginx-vol' 不存在, 所以会自动被新建, 而同时卷所挂载到的 容器中的目录 /usr/share/nginx/html 为非空目录
//     所以 该容器目录 /usr/share/nginx/html 下的 内容(contents) 会被自动 copy 到 挂载卷中
[root@node01 ~]# docker run -d --name=nginxtest --mount source=nginx-vol,destination=/usr/share/nginx/html  nginx:latest
    5d4657d8354f7ac7a5fa252dfe93f316c7a4f12395e67fa72b875f95de486b12

// 观察一下卷 'nginx-vol' 的详细信息
[root@node01 ~]# docker volume inspect nginx-vol
    [
        {
            "CreatedAt": "2019-10-29T20:32:23+08:00",
            "Driver": "local",
            "Labels": null,
            "Mountpoint": "/var/lib/docker/volumes/nginx-vol/_data",  <----
            "Name": "nginx-vol",
            "Options": null,
            "Scope": "local"
        }
    ]


// 观察一下 容器 'nginxtest' 的详细信息(这里主要关注 卷 挂载信息)
[root@node01 ~]# docker container inspect nginxtest

    ......
        "Mounts": [
            {
                "Type": "volume",
                "Name": "nginx-vol",
                "Source": "/var/lib/docker/volumes/nginx-vol/_data", <----
                "Destination": "/usr/share/nginx/html",  <----
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
    ......


// 查看卷 在 宿主机上  对应的数据目录
[root@node01 ~]# ls /var/lib/docker/volumes/nginx-vol/_data
    50x.html  index.html  <----


// 删除卷 'nginx-vol'
[root@node01 ~]# docker container stop nginxtest #停止使用 卷'nginx-vol' 的容器 'nginxtest'
[root@node01 ~]# docker container rm nginxtest   #删除容器 'nginxtest'
[root@node01 ~]# docker volume rm nginx-vol      #删除卷


--------------------------------------------------
Use a read-only volume  (使用只读卷)

// 在挂载卷 选项中指定了 readonly 选项
[root@node01 ~]# docker run -d --name=nginxtest --mount source=nginx-vol,destination=/usr/share/nginx/html,readonly  nginx:latest
    b93d1210be881f3fbe431640df84c29b9dcffafcf38134f6fd4e8d07f25e09b3

[root@node01 ~]# docker container inspect nginxtest

    ......
        "Mounts": [
            {
                "Type": "volume",
                "Name": "nginx-vol",
                "Source": "/var/lib/docker/volumes/nginx-vol/_data",
                "Destination": "/usr/share/nginx/html",
                "Driver": "local",
                "Mode": "z",
                "RW": false,  <----观察
                "Propagation": ""
            }
        ],
    ......


// 尝试在 容器中 通过 卷的挂载目录 向 该只读卷中写入数据 (可以发现写入操作失败, 这和 readonly 卷的预期效果相符)
[root@node01 ~]# docker container exec -it nginxtest bash
    root@b93d1210be88:/# ls /usr/share/nginx/html/
      50x.html  index.html
    root@b93d1210be88:/# echo 'hello' > /usr/share/nginx/html/hello.html
      bash: /usr/share/nginx/html/hello.html: Read-only file system  <----观察, 写入失败
    root@b93d1210be88:/# exit
      exit

// 删除卷 'nginx-vol'
[root@node01 ~]# docker container stop nginxtest
[root@node01 ~]# docker container rm nginxtest
[root@node01 ~]# docker volume rm nginx-vol


--------------------------------------------------
Share data among machines
Use a volume driver

      见官方文档  https://docs.docker.com/storage/volumes/






--------------------------------------------------
Backup, restore, or migrate data volumes


--------------------
Backup a container (备份一个容器)

    Volumes 对于 backups, restores, 和 migrations 很有用. 使用 --volumes-from  选项 以 创建一个 挂载了指定 container(s) 中的 volumes 的新容器


[root@node01 ~]# docker container  run --help
      --volumes-from list              Mount volumes from the specified container(s)




[root@node01 ~]# docker container run --mount destination=/dbdata --name dbstore ubuntu /bin/bash

[root@node01 ~]# docker volume ls
    DRIVER              VOLUME NAME
    local               2a73973c277f0de4afed08d6e33f185b14ccd7f41df8de549125612c233d8bd6

[root@node01 ~]# docker container run --rm --volumes-from dbstore --mount type=bind,source=$(pwd),destination=/backup ubuntu tar cvf /backup/backup.tar /dbdata



--------------------
Restore container from backup(从备份中还原容器)

    With the backup just created, you can restore it to the same container, or another that you made elsewhere.


// 创建一个新容器 'dbstore2'
[root@node01 ~]# docker container run --mount destination=/dbdata --name dbstore2 ubuntu /bin/bash

[root@node01 ~]# docker container run --rm --volumes-from dbstore2 --mount type=bind,source=$(pwd),destination=/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"


You can use the techniques above to automate backup, migration and restore testing using your preferred tools.





--------------------
Remove volumes (删除卷)

A Docker data volume persists after a container is deleted. There are two types of volumes to consider:

    - Named volumes(命令卷) have a specific source from outside the container, for example awesome:/bar.
    - Anonymous volumes(匿名卷) have no specific source so when the container is deleted, instruct the Docker Engine daemon to remove them.


Remove anonymous volumes (自动删除匿名卷)

  To automatically remove anonymous volumes, use the --rm option. For example,
  this command creates an anonymous /foo volume. When the container is removed,
  the Docker Engine removes the /foo volume but not the awesome volume.


// 注: 此处的 选项 --rm  不仅会导致 容器退出(exited) 后该容器会被自动删除, 还会导致 其中的匿名卷(Anonymous volumes) 也会被自动删除
[root@node01 ~]# docker container run --rm --mount destination=/foo --mount source=awesome,destination=/bar busybox top


[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    549704d70d30        busybox             "top"               17 seconds ago      Up 16 seconds                           charming_engelbart

[root@node01 ~]# docker volume ls
    DRIVER              VOLUME NAME
    local               0e93e392c8d9f1efecd08a095a6b0f93aab00646fcb3c1bde00eeae7f359538e  <----观察该 匿名卷
    local               awesome


[root@node01 ~]# docker container stop 549704d70d30
    549704d70d30

[root@node01 ~]# docker container ls -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS                    NAMES
    7bf55b4d7744        bulletinboard:1.0   "npm start"         2 days ago          Exited (255) 26 hours ago   0.0.0.0:8000->8080/tcp   bb
    d30997a78cc3        hello-world         "/hello"            2 days ago          Exited (0) 2 days ago                                nervous_hugle


// 列出观察 卷, 发现 曾经的匿名卷 已经不见了(因其被删除了)
[root@node01 ~]# docker volume ls
    DRIVER              VOLUME NAME
    local               awesome



--------------------
Remove all volumes  (删除所有卷)

To remove all unused volumes and free up space:

[root@node01 ~]# docker volume prune  #删除所有没有被任何容器使用到的 local volumes
    WARNING! This will remove all local volumes not used by at least one container.
    Are you sure you want to continue? [y/N]






----------------------------------------------------------------------------------------------------
Use bind mounts  (使用 bind 挂载)

    https://docs.docker.com/storage/bind-mounts/

  注: 使用 bind mounts 之前，应优先考虑 named volumes 是否是 更好的选择


  When you use a bind mount, a file(文件) or directory(目录) on the host machine is mounted into a container.
  The file or directory is referenced by its full(全/绝对路径) or relative path(相对路径) on the host machine.

  The file or directory does not need to exist on the Docker host already. It is created on demand(按需) if it does not yet exist.
  // 这里的按需 创建 是指 使用 -v 选项的时候(即是 -v 的行为), 而 --mount 选项不会按需创建, 如果不存在，则 --mount 会生成 an error.


Choose the -v or --mount flag (推荐 --mount 选项, 因 --mount 选项清晰，详细, 可读性更好)


--mount: Consists of multiple key-value pairs, separated by commas(逗号) and each consisting of a <key>=<value> tuple.
         The --mount syntax is more verbose than -v or --volume, but the order of the keys is not significant,
         and the value of the flag is easier to understand.

      - The 'type' of the mount, which can be 'bind', 'volume', or 'tmpfs'.
        This topic discusses bind mounts, so the type is always 'bind'.

      - The 'source' of the mount. For bind mounts, this is the path to
        the file or directory on the Docker daemon host. May be specified as 'source' or 'src'.

      - The 'destination' takes as its value the path where the file or directory is mounted in the container.
        May be specified as 'destination', 'dst', or 'target'.

      - The 'readonly' option, if present, causes the bind mount to be mounted into the container as read-only.

      - The 'bind-propagation' option, if present, changes the bind propagation.
        May be one of 'rprivate', 'private', 'rshared', 'shared', 'rslave', 'slave'.

      - The 'consistency' option, if present, may be one of 'consistent', 'delegated', or 'cached'.
        This setting only applies to Docker Desktop for Mac, and is ignored on all other platforms.

      - The --mount flag does not support z or Z options for modifying selinux labels.

Differences between -v and --mount behavior (-v 和 --mount 行为上的一点不同)

  there is one behavior that is different between -v and --mount

    If you use -v or --volume to bind-mount a file or directory that does not yet exist on the Docker host,
    -v creates the endpoint for you. It is always created as a directory.
    // 使用 -v 时, 如果 file 或 directory 在 宿主机上 尚不 存在时, 会 以 directory 方式创建 该 endpoint

    If you use --mount to bind-mount a file or directory that does not yet exist on the Docker host,
    Docker does not automatically create it for you, but generates an error.
    // 使用 --mount 时不会自动创建 宿主机 上 尚不未在 的 a file or directory, 而是生成 an error.


--------------------------------------------------
示例: Start a container with a bind mount (启动容器时 指定 a bind mount)

    https://docs.docker.com/storage/bind-mounts/

// 先在 宿主机上创建 预 bind mounts 的 目录(因为 本示例打算使用 --mount 选项, 其不具备 -v 选项那种 按需创建 directory 的特性)
[root@node01 ~]# mkdir -p /tmp/source/target
[root@node01 ~]# cd /tmp/source/


// 运行容器的时候 指定将 宿主机上目录 /tmp/source/target 绑定挂载到 容器 中的 目录 /app
[root@node01 source]# docker container run -d -it --name devtest --mount type=bind,source="$(pwd)"/target,target=/app nginx:latest
    3d1ea6a888e99e8f9f26e1335bac3785ed902ddfc03a5280e82e0c611db9957e

[root@node01 source]# docker container ls
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    3d1ea6a888e9        nginx:latest        "nginx -g 'daemon of…"   25 seconds ago      Up 21 seconds       80/tcp              devtest


// 观察一下 容器 'devtest' 挂载 相关的信息
[root@node01 source]# docker container inspect devtest

    ......
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/tmp/source/target",
                "Destination": "/app",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }
        ],
    ......


[root@node01 ~]# docker container stop devtest   #停止容器 'devtest'
[root@node01 ~]# docker container rm devtest     #删除容器 'devtest'

--------------------------------------------------
示例: Mount into a non-empty directory on the container (bind 挂载 到 容器中的 一个 非空目录)
        注: 该示例中 bind 挂载之后, 容器中 原本 的 bind 挂载到的目标目录中的内容将被 隐藏掩盖(obscured)

    https://docs.docker.com/storage/bind-mounts/


  If you bind-mount into a non-empty directory on the container, the directory’s existing contents
  are obscured by the bind mount. This can be beneficial, such as when you want to test a new version
  of your application without building a new image. However, it can also be surprising and
  this behavior differs from that of docker volumes.


//注: 这个例子 仅作为演示效果, 其会导致 容器 无法正常工作(因为使用了宿主机 /tmp 下的内容隐藏/掩盖 了容器中 目录 /usr 下的内容)
//    所以该 容器 会被创建； 但却 无法 正常启动(start).
[root@node01 ~]# docker container run -d -it --name broken-container --mount type=bind,source=/tmp,target=/usr nginx:latest
    b5525f488fe78d94382dc2ce24f5465eefbd400284ea68d9af5da19ef2b8c1fc
    docker: Error response from daemon: OCI runtime create failed: container_linux.go:346: starting container process caused "exec: \"nginx\": executable file not found in $PATH": unknown.


[root@node01 ~]# docker container rm broken-container  #删除容器 'broken-container'





--------------------------------------------------
Use a read-only bind mount  (使用 只读 的 bind 挂载)

    https://docs.docker.com/storage/bind-mounts/

// 将 宿主机上的 目录 /tmp/source/target 以只读的方式 bind 挂载到 容器中的 目录 /app
[root@node01 source]# docker container run -d -it --name devtest --mount type=bind,source="$(pwd)"/target,target=/app,readonly  nginx:latest
    cc649f79d365d6d5c2bc6a0aec5316694411de216ba604a13ca815acaad2eedb

// 观察一下 容器 'devtest' 挂载相关的信息
[root@node01 source]# docker container inspect devtest

    ......
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/tmp/source/target",
                "Destination": "/app",
                "Mode": "",
                "RW": false,  <---观察
                "Propagation": "rprivate"
            }
        ],
    ......

[root@node01 source]# docker container exec -it devtest /bin/bash
    root@cc649f79d365:/# echo hello > /app/hello.html
      bash: /app/hello.html: Read-only file system  <---观察, 写入失败, 因为指定为了 只读的 bind 挂载
    root@cc649f79d365:/# ls /app/
    root@cc649f79d365:/# exit
      exit


// 停止 并 删除 容器 'devtest'
[root@node01 source]# docker container stop devtest
[root@node01 source]# docker container rm devtest





--------------------------------------------------
Configure bind propagation  (配置 bind 传播)

    https://docs.docker.com/storage/bind-mounts/


注: 在设置 bind-propagation 之前, 还需要确保 宿主机的 文件系统已经支持  bind propagation.
    见 https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt

  Bind propagation defaults to rprivate for both bind mounts and volumes. It is only configurable for bind mounts,
  and only on Linux host machines. Bind propagation is an advanced topic and many users never need to configure it.
  // Bind propagation 对于 bind mounts 和 volumes 的默认值都是 'rprivate'.
  // 且 仅针对于 bind mounts 其是可配置的(volumes 就是固定的 'rprivate', 无法配置), 且仅针对于 linux 宿主机.
  // Bind propagation 是一个 高级的 主题 且 许多 users 从不需要 配置它。

  更多信息见官网  https://docs.docker.com/storage/bind-mounts/






--------------------------------------------------
About storage drivers (关于 存储驱动)

      https://docs.docker.com/storage/storagedriver/

       docker image 的 分层构建、联合挂载

  存储驱动 overlay2(推荐): https://docs.docker.com/storage/storagedriver/overlayfs-driver/


To use storage drivers effectively, it’s important to know how Docker builds and stores images,
and how these images are used by containers. You can use this information to make informed
choices about the best way to persist data from your applications and avoid performance problems along the way.

Storage drivers allow you to create data in the writable layer of your container.
The files won’t be persisted after the container is deleted,
and both read and write speeds are lower than native file system performance.

// 读和写的操作在 速度上 native file system performance 更高效,
// 所以 卷(volumes) 不只是提供持久化能力, 还可以提升读写性能及其他等特性


A Docker image is built up from a series of layers. Each layer represents an instruction
in the image’s Dockerfile. Each layer except the very last one is read-only.
Consider the following Dockerfile:

      FROM ubuntu:18.04
      COPY . /app
      RUN make /app
      CMD python /app/app.py


  This Dockerfile contains four commands, each of which creates a layer(每个指令都创建了一个层).
  The `FROM` statement starts out by creating a layer from the 'ubuntu:18.04' image.
  The `COPY` command adds some files from your Docker client’s current directory.
  The `RUN` command builds your application using the 'make' command. Finally,
  the last layer specifies what command to run within the container.

  Each layer is only a set of differences from the layer before it. The layers are stacked on top of each other.
  When you create a new container, you add a new writable layer(新的可写层) on top of the underlying layers.
  This layer is often called the “container layer”(容器层). All changes made to the running container,
  such as writing new files, modifying existing files, and deleting files, are written to this
  thin writable container layer(可写的容器层). The diagram below shows a container based on the Ubuntu 18.04 image.


        +-------------------------------------------------+
        |              Thin R/W layer                     |  <------Container layer (可读可写层)
        +-------------------------------------------------+
             Λ         Λ         Λ          Λ         Λ
             |         |         |          |         |
             V         V         V          V         V
        |+------------------------------------------------+-----------------------------
        |                                                 |                     Λ
        |   +------------------------------------+        |                     |
CMD     |   | 5a1ee5e7e5a2                    0 B|        |                     |
        |   +------------------------------------+        |                     |
        |                                                 |                     |
        |   +------------------------------------+        |                     |
RUN     |   | e27aefd94cc8               1.895 KB|        |                     |
        |   +------------------------------------+        |                     |
        |                                            (locked/readonly)          |image layers (readonly)
        |   +------------------------------------+        |                     |
COPY    |   | c7b462a3a162               194.5 KB|        |                     |
        |   +------------------------------------+        |                     |
        |                                                 |                     |
        |   +------------------------------------+        |                     |
FROM    |   | 273fc2106a02               188.1 MB|        |                     |
        |   +------------------------------------+        |                     |
        |                                                 |                     |
        |        ubuntu:18.04                             |                     V
        +-------------------------------------------------+-----------------------------
              Container (Base on ubuntu:18.04 image)


storage driver 的作用: 处理 各 layer 与 layer 之间 交互 的细节
    A storage driver handles the details about the way these layers interact with each other.
    Different storage drivers are available, which have advantages and disadvantages in different situations.


--------------------------------------------------
Container and layers

  每个容器 都有自己的 可写层(即 容器层), 且多个 容器 可以 共享 底层 的 image layers.

    The major difference between a container and an image is the top writable layer.
    All writes to the container that add new or modify existing data are stored in this writable layer.
    When the container is deleted, the writable layer is also deleted.
    The underlying image remains unchanged.

    Because each container has its own writable container layer, and all changes are stored in this container layer,
    multiple containers can share access to the same underlying image and yet have their own data state.
    The diagram below shows multiple containers sharing the same Ubuntu 18.04 image.




            Container_01      Container_02         Container_03
                  |                  |               |
                  |                  |               |
       Thin_R/W_layer_01   Thin_R/W_layer_02   Thin_R/W_layer_03
                  Λ                  Λ               Λ
                  |                  |               |
                  V                  V               V
          |+------------------------------------------------+
          |                                                 |
          |   +------------------------------------+        |
          |   | 5a1ee5e7e5a2                    0 B|        |
          |   +------------------------------------+        |
          |                                                 |
          |   +------------------------------------+        |
          |   | e27aefd94cc8               1.895 KB|        |
          |   +------------------------------------+        |
          |                                                 |
          |   +------------------------------------+        |
          |   | c7b462a3a162               194.5 KB|        |
          |   +------------------------------------+        |
          |                                                 |
          |   +------------------------------------+        |
          |   | 273fc2106a02               188.1 MB|        |
          |   +------------------------------------+        |
          |                                                 |
          |        ubuntu:18.04                             |
          +-------------------------------------------------+
                Container (Base on ubuntu:18.04 image)



Note: If you need multiple images to have shared access to the exact same data,
      store this data in a Docker volume and mount it into your containers.
      // 如果你 需要 多个 images 共享访问 完全相同的 data, 可以 把 该 data
      // 存储 在 a Docker volume 中 并 将其 挂载到 你的 containers 中.

Docker uses storage drivers to manage the contents of the image layers and the writable container layer.
Each storage driver handles the implementation differently,
but all drivers use stackable image layers and the copy-on-write (CoW) strategy.
  // 所有的 驱动 使用了  stackable image layers 和 写时复制 策略.


--------------------------------------------------
Container size on disk (容器的磁盘大小)

      https://docs.docker.com/storage/storagedriver/


[root@node01 ~]# docker container run --rm -d --name nginx_test  nginx:latest
    60c72edef8f58b7c6c5f4e54e4a4b14634b5c64502d56933062dbdc61c682bad

// 使用命令 `docker ps -s` 查看 容器的 'size' 和 'virtual size'
[root@node01 ~]# docker ps -s
    CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES               SIZE
    60c72edef8f5        nginx:latest        "nginx -g 'daemon of…"   About a minute ago   Up About a minute   80/tcp              nginx_test          2B (virtual 126MB)


[root@node01 ~]# docker container stop nginx_test



To view the approximate size of a running container, you can use the `docker ps -s` command. Two different columns relate to size.

  - 'size':         the amount of data (on disk) that is used for the writable layer(可写层) of each container.
  - 'virtual size': the amount of data used for the read-only image data(只读的镜像数据) used by the container plus(加上) the container’s
                    writable layer(可写层) size. Multiple containers may share some or all read-only image data.
                    Two containers started from the same image share 100% of the read-only data,
                    while two containers with different images which have layers in common share those common layers.
                    Therefore, you can’t just total the virtual sizes. This over-estimates the total
                    disk usage by a potentially non-trivial amount.

  The total disk space used by all of the running containers on disk is some combination of each container’s
  'size' and the 'virtual size' values. If multiple containers started from the same exact image,
  the total size on disk for these containers would be SUM ('size' of containers) plus one image size ('virtual size'- 'size').

This also does not count the following additional ways a container can take up disk space:

    - Disk space used for log files if you use the json-file logging driver.
      This can be non-trivial if your container generates a large amount of logging data and log rotation is not configured.

    - Volumes and bind mounts used by the container.

    - Disk space used for the container’s configuration files, which are typically small.

    - Memory written to disk (if swapping is enabled).

    - Checkpoints, if you’re using the experimental checkpoint/restore feature.







--------------------------------------------------
The copy-on-write (CoW) strategy  (写时复制策略)

      https://docs.docker.com/storage/storagedriver/

    Copy-on-write is a strategy of sharing and copying files for maximum efficiency. If a file or
    directory exists in a lower layer within the image, and another layer (including the writable layer)
    needs read access to it, it just uses the existing file. The first time another layer needs
    to modify the file (when building the image or running the container)(注: 写时复制可以发生在 image的构建或容器的运行时),
    the file is copied into that layer and modified. This minimizes I/O and the size
    of each of the subsequent layers. These advantages are explained in more depth below.


Sharing promotes smaller images (共享可以促成更小的 images)


  When you use docker pull to pull down an image from a repository, or when you create a container
  from an image that does not yet exist locally, each layer is pulled down separately,
  and stored in Docker’s local storage area, which is usually
  /var/lib/docker/ on Linux hosts. You can see these layers being pulled in this example:


// 拉取 下载 镜像 'ubuntu:18.04'
[root@node01 ~]# docker image pull ubuntu:18.04
    18.04: Pulling from library/ubuntu
    22e816666fd6: Pull complete    <----- 下载 layer
    079b6d2a1e53: Pull complete    <----- 下载 layer
    11048ebae908: Pull complete    <----- 下载 layer
    c58094023a2e: Pull complete    <----- 下载 layer
    Digest: sha256:a7b8b7b33e44b123d7f997bd4d3d0a59fafc63e203d17efedf09ff3f6f516152
    Status: Downloaded newer image for ubuntu:18.04
    docker.io/library/ubuntu:18.04

Each of these layers is stored in its own directory inside the Docker host’s local storage area.
To examine the layers on the filesystem, list the contents of
/var/lib/docker/<storage-driver>. This example uses the overlay2 storage driver:

[root@node01 ~]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ubuntu              18.04               cf0f3ca922e0        11 days ago         64.2MB

[root@node01 ~]# ls -1 /var/lib/docker/overlay2
    5b5f526af60283dfb6255ac475550f2fb51ca0384e2be67f2d5389012ef5c7d6
    6eb211802c02aeb97c1b70c3ca746dbd46324576c8cd929ec804d40d0743e5bd
    b26b24f202724f10e6b92c44f77b991d33b72b847eb47b66364802dc42c640f0
    backingFsBlockDev
    cf59eb7d3a0197a7012f135459525e48c038aca5e63ed01d30e3b5f46fb82c46
    l

    The directory names do not correspond to the layer IDs (this has been true since Docker 1.10).
    // 目录名 和 层的 IDs 并不对应


// 1) Make a new directory cow-test/ and change into it.

[root@node01 ~]# mkdir cow-test/
[root@node01 ~]# cd cow-test/
[root@node01 cow-test]#

// 2) Within cow-test/, create a new file called hello.sh with the following contents:
[root@node01 cow-test]# vim hello.sh

    #!/bin/sh
    echo "Hello world"

// Save the file, and make it executable:
[root@node01 cow-test]# chmod +x hello.sh
[root@node01 cow-test]# ls -l hello.sh
    -rwxr-xr-x 1 root root 29 Oct 30 23:39 hello.sh

// 3) Copy the contents of the first Dockerfile above into a new file called Dockerfile.base
[root@node01 cow-test]# vim Dockerfile.base

    FROM ubuntu:18.04
    COPY . /app

// 4) Copy the contents of the second Dockerfile above into a new file called Dockerfile
[root@node01 cow-test]# vim Dockerfile

    FROM acme/my-base-image:1.0
    CMD /app/hello.sh


// 5) Within the cow-test/ directory, build the first image. Don’t forget to include the final '.' in the command.
      That sets the PATH, which tells Docker where to look for any files that need to be added to the image.

[root@node01 cow-test]# docker image build -t acme/my-base-image:1.0 -f Dockerfile.base .
    Sending build context to Docker daemon  4.096kB
    Step 1/2 : FROM ubuntu:18.04
     ---> cf0f3ca922e0
    Step 2/2 : COPY . /app
     ---> 4045fd4cc6a2
    Successfully built 4045fd4cc6a2
    Successfully tagged acme/my-base-image:1.0


// 6) Build the second image

[root@node01 cow-test]# docker image build -t acme/my-final-image:1.0 -f Dockerfile .
    Sending build context to Docker daemon  4.096kB
    Step 1/2 : FROM acme/my-base-image:1.0
     ---> 4045fd4cc6a2
    Step 2/2 : CMD /app/hello.sh
     ---> Running in 882b9941ca09
    Removing intermediate container 882b9941ca09
     ---> daca8e3b9294
    Successfully built daca8e3b9294
    Successfully tagged acme/my-final-image:1.0


// 7) Check out the sizes of the images:
[root@node01 cow-test]# docker image ls
    REPOSITORY            TAG                 IMAGE ID            CREATED              SIZE
    acme/my-final-image   1.0                 daca8e3b9294        About a minute ago   64.2MB
    acme/my-base-image    1.0                 4045fd4cc6a2        3 minutes ago        64.2MB
    ubuntu                18.04               cf0f3ca922e0        11 days ago          64.2MB


// 8) Check out the layers that comprise each image:

[root@node01 cow-test]# docker image history 4045fd4cc6a2
    IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
    4045fd4cc6a2        7 minutes ago       /bin/sh -c #(nop) COPY dir:60e6768edfda1227e…   105B
    cf0f3ca922e0        11 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>           11 days ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
    <missing>           11 days ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
    <missing>           11 days ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
    <missing>           11 days ago         /bin/sh -c #(nop) ADD file:d13b09e8b3cc98bf0…   63.2MB


[root@node01 cow-test]# docker image history daca8e3b9294
    IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
    daca8e3b9294        6 minutes ago       /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "/app…   0B    <----观察
    4045fd4cc6a2        8 minutes ago       /bin/sh -c #(nop) COPY dir:60e6768edfda1227e…   105B
    cf0f3ca922e0        11 days ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>           11 days ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
    <missing>           11 days ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
    <missing>           11 days ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
    <missing>           11 days ago         /bin/sh -c #(nop) ADD file:d13b09e8b3cc98bf0…   63.2MB


Notice that all the layers are identical except the top layer of the second image.
All the other layers are shared between the two images, and are only stored once in /var/lib/docker/.
The new layer actually doesn’t take any room at all,
because it is not changing any files, but only running a command.

Note: The <missing> lines in the `docker history` output indicate that those layers
were built on another system and are not available locally. This can be ignored.


----------------------------------------------------------------------------------------------------
Copying makes containers efficient (复制使 容器高效)


    https://docs.docker.com/storage/storagedriver/

When you start a container, a thin writable container layer is added on top of the other layers.
Any changes the container makes to the filesystem are stored here. Any files the container
does not change do not get copied to this writable layer. This means that the writable layer is as small as possible.
// 容器做的 所有的文件系统修改 都被存储在 该 可写的 container layer.


When an existing file in a container is modified, the storage driver performs a copy-on-write operation.
The specifics steps involved depend on the specific storage driver. For the aufs,
overlay, and overlay2 drivers, the copy-on-write operation follows this rough sequence:
// 存储驱动 aufs, overlay 和 overlay2 的  copy-on-write 操作的大体步骤:

    - Search through the image layers for the file to update. The process starts at the newest layer
      and works down to the base layer one layer at a time. When results are found,
      they are added to a cache to speed future operations.
      // 在 image layers 上从上往下搜索预修改的文件, 如果找到 便 将其 加入 cache 中以 加速 将来的操作.

    - Perform a copy_up operation on the first copy of the file that is found, to copy the file to the container’s writable layer.
      // 执行 向上复制(copy_up) 操作, 将 找到的 file 的 first copy 复制到 容器的 可写层.

    - Any modifications are made to this copy of the file, and the container cannot see
      the read-only copy of the file that exists in the lower layer.
      // 任何修改 都在 该 file 的 copy 副本上 执行, 容器无法再看到 底层(lower layer) 存在的 该 file 的 只读副本(read-only).
      // 即 file 的 上层副本 会 掩盖隐藏 下层的 副本.


Btrfs, ZFS, and other drivers handle the copy-on-write differently.
You can read more about the methods of these drivers later in their detailed descriptions.
// Btrfs, ZFS 和 其他 drivers 以 不同的方式 处理 copy-on-write

Containers that write a lot of data consume more space than containers that do not.
This is because most write operations consume new space in the container’s thin writable top layer.


Note: for write-heavy applications, you should not store the data in the container.
Instead, use Docker volumes, which are independent of the running container and
are designed to be efficient for I/O. In addition, volumes can be shared
among containers and do not increase the size of your container’s writable layer.
// 注: 对于大量写入的 applications, 你应该使用 Docker volumes, 即使用 native file system 以
//     获取高效的 I/O 性能。另外, volumes 可以在 多个 containers 之间共享 且 不会 增加
//     容器 可写层的 size.


A copy_up operation can incur a noticeable performance overhead.
This overhead is different depending on which storage driver(存储驱动) is in use.
Large files(大文件), lots of layers(大量层), and deep directory trees(深的目录树) can make the impact more noticeable.
This is mitigated by the fact that each copy_up operation only occurs the first time a given file is modified.


示例:
To verify the way that copy-on-write works, the following procedures spins up 5 containers
based on the acme/my-final-image:1.0 image we built earlier and examines how much room they take up.

    Note: This procedure doesn’t work on Docker Desktop for Mac or Docker Desktop for Windows.

1) From a terminal on your Docker host, run the following docker run commands. The strings at the end are the IDs of each container.

[root@node01 ~]# docker container run -dit --name my_container_1 acme/my-final-image:1.0 bash \
                   && docker container run -dit --name my_container_2 acme/my-final-image:1.0 bash \
                   && docker container run -dit --name my_container_3 acme/my-final-image:1.0 bash \
                   && docker container run -dit --name my_container_4 acme/my-final-image:1.0 bash \
                   && docker container run -dit --name my_container_5 acme/my-final-image:1.0 bash

    f370efe43d83b2ec48b7dddb2e7a2ba39182269c5bb5a547d67eb6eb0b60e575
    a5304d12704c5a7cc5dc12c6877dc0eb2467ce9eea57e23a2bb62ccd24b99970
    0a8d9f3d982bd29c82c89bfeafebf61b2f48ed9b092079049d2a3cdcf5e8ab9f
    c74bd1ab157244575df75c3310a11db0af8c9d53de489a42834db35110ca213f
    447a604aa52bf2e3b7595a6bba6716cf954989578da7e67a974400d74bc3c86b

2) Run the docker ps command to verify the 5 containers are running.

[root@node01 ~]# docker ps    #注: 命令 `docker ps` 是 命令 `docker container ls` 的别名
  CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS              PORTS               NAMES
  447a604aa52b        acme/my-final-image:1.0   "bash"              2 minutes ago       Up 2 minutes                            my_container_5
  c74bd1ab1572        acme/my-final-image:1.0   "bash"              2 minutes ago       Up 2 minutes                            my_container_4
  0a8d9f3d982b        acme/my-final-image:1.0   "bash"              2 minutes ago       Up 2 minutes                            my_container_3
  a5304d12704c        acme/my-final-image:1.0   "bash"              2 minutes ago       Up 2 minutes                            my_container_2
  f370efe43d83        acme/my-final-image:1.0   "bash"              2 minutes ago       Up 2 minutes                            my_container_1

[root@node01 ~]# docker container ls
  CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS              PORTS               NAMES
  447a604aa52b        acme/my-final-image:1.0   "bash"              4 minutes ago       Up 4 minutes                            my_container_5
  c74bd1ab1572        acme/my-final-image:1.0   "bash"              4 minutes ago       Up 4 minutes                            my_container_4
  0a8d9f3d982b        acme/my-final-image:1.0   "bash"              4 minutes ago       Up 4 minutes                            my_container_3
  a5304d12704c        acme/my-final-image:1.0   "bash"              4 minutes ago       Up 4 minutes                            my_container_2
  f370efe43d83        acme/my-final-image:1.0   "bash"              4 minutes ago       Up 4 minutes                            my_container_1


3) List the contents of the local storage area.

[root@node01 ~]# ls -1 /var/lib/docker/containers
    0a8d9f3d982bd29c82c89bfeafebf61b2f48ed9b092079049d2a3cdcf5e8ab9f
    447a604aa52bf2e3b7595a6bba6716cf954989578da7e67a974400d74bc3c86b
    a5304d12704c5a7cc5dc12c6877dc0eb2467ce9eea57e23a2bb62ccd24b99970
    c74bd1ab157244575df75c3310a11db0af8c9d53de489a42834db35110ca213f
    f370efe43d83b2ec48b7dddb2e7a2ba39182269c5bb5a547d67eb6eb0b60e575

4) Now check out their sizes:

[root@node01 ~]# du -sh /var/lib/docker/containers/*
    24K /var/lib/docker/containers/0a8d9f3d982bd29c82c89bfeafebf61b2f48ed9b092079049d2a3cdcf5e8ab9f
    24K /var/lib/docker/containers/447a604aa52bf2e3b7595a6bba6716cf954989578da7e67a974400d74bc3c86b
    24K /var/lib/docker/containers/a5304d12704c5a7cc5dc12c6877dc0eb2467ce9eea57e23a2bb62ccd24b99970
    24K /var/lib/docker/containers/c74bd1ab157244575df75c3310a11db0af8c9d53de489a42834db35110ca213f
    24K /var/lib/docker/containers/f370efe43d83b2ec48b7dddb2e7a2ba39182269c5bb5a547d67eb6eb0b60e575


  Each of these containers only takes up 24K of space on the filesystem.

  Not only does copy-on-write save space, but it also reduces start-up time.
  When you start a container (or multiple containers from the same image), Docker only needs to create the thin writable container layer.

  If Docker had to make an entire copy of the underlying image stack each time it started a new container,
  container start times and disk space used would be significantly increased.
  This would be similar to the way that virtual machines work, with one or more virtual disks per virtual machine.







----------------------------------------------------------------------------------------------------
select storage driver  (选择 存储引擎)

Docker storage drivers

    https://docs.docker.com/storage/storagedriver/select-storage-driver/

      推荐: overlay2, 如果使用其他存储驱动, 可能需要自己承担一些风险

Ideally, very little data is written to a container’s writable layer, and you use Docker volumes to write data.
However, some workloads require you to be able to write to the container’s writable layer.
This is where storage drivers come in.
// 理想的情况下, 很少的 data 被 写入到 容器的可写层, 同时 使用 Docker volumes 来 写入数据

Docker supports several different storage drivers, using a pluggable architecture.
The storage driver controls how images and containers are stored and managed on your Docker host.
// storage driver 控制着 images 和 containers 在 宿主机上 被 存储 和 管理的方式


After you have read the storage driver overview, the next step is to choose the best storage driver for your workloads.
In making this decision, there are three high-level factors to consider:

If multiple storage drivers are supported in your kernel, Docker has a prioritized list
of which storage driver to use if no storage driver is explicitly configured, assuming that the storage driver meets the prerequisites.

Use the storage driver with the best overall performance and stability in the most usual scenarios.
// 在 大多数情况下，应使用 具有最佳 整体性能 和 稳定性 的 storage driver

Docker supports the following storage drivers:
// Docker 支持 如下 的 storage drivers:

  - 'overlay2' is the preferred storage driver, for all currently supported Linux distributions, and requires no extra configuration.
    // 'overlay2' 是 首选的 storage driver (对于当前所有被支持的 Linux distributions), 且 不需要 额外的配置.

  - 'aufs' is the preferred storage driver for Docker 18.06 and older, when running on Ubuntu 14.04 on kernel 3.13 which has no support for overlay2.

  - 'devicemapper' is supported, but requires direct-lvm for production environments, because loopback-lvm,
    while zero-configuration, has very poor performance(很低的性能). devicemapper was the recommended storage driver for CentOS and RHEL,
    as their kernel version did not support overlay2.  However, current versions of CentOS and RHEL now have support for overlay2, which is now the recommended driver.
    // 注: 当前版本的 CentOS 和 RHEL 已经支持 overlay2, 所以 推荐 overlay2

  - The 'btrfs' and 'zfs' storage drivers are used if they are
    the backing filesystem (the filesystem of the host on which Docker is installed).
    These filesystems allow for advanced options, such as creating “snapshots”,
    but require more maintenance and setup. Each of these relies on the backing filesystem being configured correctly.


  - The 'vfs' storage driver is intended for testing purposes(测试目的), and for situations where no copy-on-write filesystem can be used.
    Performance of this storage driver is poor, and is not generally recommended for production use.
    // 'vfs' 用于测试目的, 即 不能使用 写时复制的 场景。其性能 很差, 通过不建议在 生产环境中 使用.

NOTE: Your choice may be limited by your Docker edition(Docker 版本), operating system(操作系统), and distribution(发行版).
      For instance, aufs is only supported on Ubuntu and Debian, and may require extra packages to be installed,
      while btrfs is only supported on SLES, which is only supported with Docker Enterprise.
      See Support storage drivers per Linux distribution for more information.


--------------------------------------------------
Supported storage drivers per Linux distribution

    https://docs.docker.com/storage/storagedriver/select-storage-driver/

  At a high level, the storage drivers you can use is partially determined by the Docker edition you use.

  In addition, Docker does not recommend any configuration that requires you to disable security
  features of your operating system, such as the need to disable selinux if you use the 'overlay' or 'overlay2' driver on CentOS.


--------------------------------------------------
Docker Engine - Community

For Docker Engine - Community, only some configurations are tested,
and your operatingsystem’s kernel may not support every storage driver.
In general,the following configurations work on recent versions of the Linux distribution:


------------------------------------|--------------------------------------------------------------------|-----------------------------------
Linux distribution                  | Recommended storage drivers                                        |  Alternative drivers
------------------------------------|--------------------------------------------------------------------|-----------------------------------
Docker Engine - Community on Ubuntu |  overlay2 or aufs (for Ubuntu 14.04 running on kernel 3.13)        |  overlay¹, devicemapper², zfs, vfs
------------------------------------|--------------------------------------------------------------------|-----------------------------------
Docker Engine - Community on Debian |  overlay2 (Debian Stretch), aufs or devicemapper (older versions)  |   overlay¹, vfs
------------------------------------|--------------------------------------------------------------------|-----------------------------------
Docker Engine - Community on CentOS |  overlay2                                                          |   overlay¹, devicemapper², zfs, vfs
------------------------------------|--------------------------------------------------------------------|-----------------------------------
Docker Engine - Community on Fedora |  overlay2                                                          |   overlay¹, devicemapper², zfs, vfs
------------------------------------|--------------------------------------------------------------------|-----------------------------------


The overlay storage driver is deprecated in Docker Engine - Enterprise 18.09, and will be removed in a future release.
It is recommended that users of the overlay storage driver migrate to overlay2.
// overlay 存储驱动 在 Docker Engine - Enterprise 18.09 中 已经过时了, 且在未来版本中 其会被删除
// 所以建议 使用 overlay 存储驱动的用户 迁移到 overlay2


The devicemapper storage driver is deprecated in Docker Engine 18.09, and will be removed in a future release.
It is recommended that users of the devicemapper storage driver migrate to overlay2.
// devicemapper 存储驱动在 Docker Engine 18.09 中已经过时了, 且在未来版本中 其会被删除
// 所以建议 使用 devicemapper 存储驱动的用户 迁移到 overlay2

When possible, overlay2 is the recommended storage driver. When installing Docker for the first time,
overlay2 is used by default. Previously, aufs was used by default when available,
but this is no longer the case. If you want to use aufs on new installations going forward,
you need to explicitly configure it, and you may need to install extra packages, such as linux-image-extra. See aufs.
// 只要有可能, overlay2 就是 被推荐的 存储引擎, 首次安装 Docker 时, overlay2 就是默认被使用的.


    Expectations for non-recommended storage drivers: Commercial support is not available for Docker Engine - Community,
    and you can technically use any storage driver that is available for your platform. For instance,
    you can use btrfs with Docker Engine - Community, even though it is not recommended
    on any platform for Docker Engine - Community, and you do so at your own risk.

    The recommendations in the table above are based on automated regression testing and the configurations
    that are known to work for a large number of users. If you use a recommended configuration
    and find a reproducible issue, it is likely to be fixed very quickly. If the driver that you
    want to use is not recommended according to this table, you can run it at your own risk.
    You can and should still report any issues you run into. However,
    such issues have a lower priority than issues encountered when using a recommended configuration.
    // 使用 非推荐 的 存储驱动， 你可以要自己承担运行风险


--------------------------------------------------
Supported backing filesystems

  https://docs.docker.com/storage/storagedriver/select-storage-driver/

With regard to Docker, the backing filesystem is the filesystem where
/var/lib/docker/ is located. Some storage drivers only work with specific backing filesystems.


      ----------------------+----------------------------------
      Storage driver        |   Supported backing filesystems
      ----------------------|----------------------------------
        overlay2, overlay   |   xfs with ftype=1, ext4
      ----------------------|----------------------------------
        aufs                |   xfs, ext4
      ----------------------|----------------------------------
        devicemapper        |   direct-lvm
      ----------------------|----------------------------------
        btrfs               |   btrfs
      ----------------------|----------------------------------
        zfs                 |   zfs
      ----------------------|----------------------------------
        vfs                 |   any filesystem
      ----------------------+----------------------------------


--------------------------------------------------
Other considerations (其他注意事项)

    https://docs.docker.com/storage/storagedriver/select-storage-driver/

----------
Suitability for your workload


  Among other things, each storage driver has its own performance characteristics that
  make it more or less suitable for different workloads. Consider the following generalizations:

      - overlay2, aufs, and overlay all operate at the file level rather than the block level.
        This uses memory more efficiently, but the container’s writable layer may grow quite large in write-heavy workloads.

      - Block-level storage drivers such as devicemapper, btrfs, and zfs perform better for write-heavy workloads (though not as well as Docker volumes).

      - For lots of small writes or containers with many layers or deep filesystems, overlay may perform better than overlay2,
        but consumes more inodes, which can lead to inode exhaustion.

      - btrfs and zfs require a lot of memory.

      - zfs is a good choice for high-density workloads such as PaaS.

  More information about performance, suitability, and best practices is available in the documentation for each storage driver.


----------
Shared storage systems and the storage driver

  If your enterprise uses SAN, NAS, hardware RAID, or other shared storage systems, they may provide high availability,
  increased performance, thin provisioning, deduplication, and compression. In many cases,
  Docker can work on top of these storage systems, but Docker does not closely integrate with them.

  Each Docker storage driver is based on a Linux filesystem or volume manager. Be sure to follow existing
  best practices for operating your storage driver (filesystem or volume manager) on top of
  your shared storage system. For example, if using the ZFS storage driver on top of a shared storage system,
  be sure to follow best practices for operating ZFS filesystems on top of that specific shared storage system.


----------
Stability

  For some users, stability is more important than performance. Though Docker considers all of the storage drivers
  mentioned here to be stable, some are newer and are still under active development.
  In general, 'overlay2', aufs, overlay, and devicemapper are the choices with the highest stability.


----------
Test with your own workloads

  You can test Docker’s performance when running your own workloads on different storage drivers.
  Make sure to use equivalent hardware and workloads to match production conditions,
  so you can see which storage driver offers the best overall performance.



--------------------------------------------------
Check your current storage driver

    https://docs.docker.com/storage/storagedriver/select-storage-driver/

The detailed documentation for each individual storage driver details all of the set-up steps to use a given storage driver.

To see what storage driver Docker is currently using, use docker info and look for the Storage Driver line:

[root@node01 ~]# docker info  #在命令 `docker info` 的输出结果中可以查看到 当前使用的 Storage Driver
    Client:
     Debug Mode: false

    Server:
     Containers: 5
      Running: 5
      Paused: 0
      Stopped: 0
     Images: 3
     Server Version: 19.03.4
     Storage Driver: overlay2  <----观察, 当前使用的存储驱动
      Backing Filesystem: xfs
      Supports d_type: true
      Native Overlay Diff: true
     Logging Driver: json-file
     Cgroup Driver: cgroupfs
     Plugins:
      Volume: local
      Network: bridge host ipvlan macvlan null overlay
      Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
     Swarm: inactive
     Runtimes: runc
     Default Runtime: runc
     Init Binary: docker-init
     containerd version: b34a5c8af56e510852c35414db4c1f4fa6172339
     runc version: 3e425f80a8c931f88e6d94a8c831b9d5aa481657
     init version: fec3683
     Security Options:
      seccomp
       Profile: default
     Kernel Version: 3.10.0-693.el7.x86_64
     Operating System: CentOS Linux 7 (Core)
     OSType: linux
     Architecture: x86_64
     CPUs: 1
     Total Memory: 976.3MiB
     Name: node01
     ID: O75Q:DJJA:5HHT:R4M6:YZPH:4SDH:FHMV:RYRW:5MIR:CWFO:SAFW:GNEB
     Docker Root Dir: /var/lib/docker
     Debug Mode: false
     Registry: https://index.docker.io/v1/
     Labels:
     Experimental: false
     Insecure Registries:
      127.0.0.0/8
     Registry Mirrors:
      https://xxxxxxxxxxxxxxxx.mirror.aliyuncs.com/
     Live Restore Enabled: false


To change the storage driver, see the specific instructions for the new storage driver.
Some drivers require additional configuration, including configuration to physical or logical disks on the Docker host.


Important(重要): When you change the storage driver, any existing images and containers become inaccessible.
                 This is because their layers cannot be used by the new storage driver. If you revert your changes,
                 you can access the old images and containers again,
                 but any that you pulled or created using the new driver are then inaccessible.
// 重要: 当你 修改了 storage driver, 任何现有的 images 和 containers  将变得不可访问,
         这时因为 它们的 layers 无法被 新的 storage driver 所使用, 如果你还原你的修改,
         你可以再一次访问 旧的 images 和 containers, 但是 任何 你 通过 新的 驱动来 pulled 和 created 的 images 和 containers
         会变得不可访问

更多 关于 overlay2 的信息, 见:   https://docs.docker.com/storage/storagedriver/overlayfs-driver/





----------------------------------------------------------------------------------------------------
Use the OverlayFS storage driver  (使用 overlay2 存储驱动)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

OverlayFS is a modern union filesystem that is similar to AUFS, but faster and with a simpler implementation.
Docker provides two storage drivers for OverlayFS: the original overlay, and the newer and more stable overlay2.
// OverlayFS 是类似于 AUFS 的现代 联合文件系统, 但其 更加 快速 且 实现更加简单.
// Docker 针对 OverlayFS 提供了 2 个 storage drivers: 原始的 overlay, 即其 更新 和 更稳定的 overlay2.

This topic refers to the Linux kernel driver as 'OverlayFS' and to the Docker storage driver as 'overlay' or 'overlay2'.
// 本主题 将 Linux kernel driver 称为 'OverlayFS', 而将 Docker storage driver 称为 'overlay' 或 'overlay2'.



Note: If you use OverlayFS, use the overlay2 driver rather than the overlay driver,
      because it is more efficient in terms of inode utilization. To use the new driver,
      you need version 4.0 or higher of the Linux kernel, or RHEL or CentOS using version 3.10.0-514 and above.
// 使用 overlay2 的版本要求: Linux kernel 为 4.0 或 以上版本, 或者 RHEL 或 CentOS 使用的 3.10.0-514 或 以上的版本

[root@node01 ~]# uname -r
    3.10.0-693.el7.x86_64

[root@node01 ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)

--------------------
Prerequisites (先决条件)

OverlayFS is supported if you meet the following prerequisites:

    - The overlay2 driver is supported on Docker Engine - Community, and Docker EE 17.06.02-ee5 and up, and is the recommended storage driver.

    - Version 4.0 or higher of the Linux kernel, or RHEL or CentOS using version 3.10.0-514 of the kernel or higher.
      If you use an older kernel, you need to use the overlay driver, which is not recommended.

    - The overlay and overlay2 drivers are supported on xfs backing filesystems, but only with d_type=true enabled.
      // xfs backing filesystems 支持 overlay 和 overlay2 drivers, 但仅在 d_type=true 被 启动的情况下.
      [root@node01 ~]# docker info | grep d_type
        Supports d_type: true


    - Use xfs_info to verify that the ftype option is set to 1. To format an xfs filesystem correctly, use the flag -n ftype=1.

        [root@node01 ~]# xfs_info /
            meta-data=/dev/mapper/centos-root isize=512    agcount=4, agsize=1166592 blks
                     =                       sectsz=512   attr=2, projid32bit=1
                     =                       crc=1        finobt=0 spinodes=0
            data     =                       bsize=4096   blocks=4666368, imaxpct=25
                     =                       sunit=0      swidth=0 blks
            naming   =version 2              bsize=4096   ascii-ci=0 ftype=1  <---观察 ftype=1
            log      =internal               bsize=4096   blocks=2560, version=2
                     =                       sectsz=512   sunit=0 blks, lazy-count=1
            realtime =none                   extsz=4096   blocks=0, rtextents=0

         警告:
         Warning: Running on XFS without d_type support now causes Docker to skip the attempt to use the overlay or overlay2 driver.
                   Existing installs will continue to run, but produce an error. This is to allow users to migrate their data.
                   In a future version, this will be a fatal error, which will prevent Docker from starting.

    - Changing the storage driver makes existing containers and images inaccessible on the local system.
      Use `docker save` to save any images you have built or push them to Docker Hub or a private registry
      before changing the storage driver, so that you do not need to re-create them later.


--------------------------------------------------
Configure Docker with the overlay or overlay2 storage driver (配置 overlay2 存储驱动)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

It is highly recommended that you use the overlay2 driver if possible,
rather than the overlay driver. The overlay driver is not supported for Docker EE.
// 只要有可能, 就推荐使用 overlay2

The steps below outline how to configure the overlay2 storage driver.
// 如下的 步骤 概述 了如何配置 overlay2 storage driver:

1) Stop Docker

[root@node01 ~]# systemctl stop docker

2) Copy the contents of /var/lib/docker to a temporary location.

[root@node01 ~]# cp -au /var/lib/docker /var/lib/docker.bk

3) If you want to use a separate backing filesystem from the one used by /var/lib/,
   format the filesystem and mount it into /var/lib/docker. Make sure add this mount to /etc/fstab to make it permanent.

4) Edit /etc/docker/daemon.json. If it does not yet exist, create it. Assuming that the file was empty, add the following contents.

[root@node01 ~]# vim /etc/docker/daemon.json

    {
      "storage-driver": "overlay2"
    }

  Docker does not start if the daemon.json file contains badly-formed JSON.

5) Start Docker.

[root@node01 ~]# systemctl start docker

6) Verify that the daemon is using the overlay2 storage driver.
   Use the `docker info` command and look for Storage Driver and Backing filesystem.

[root@node01 ~]# docker info

  ......
     Server Version: 19.03.4
     Storage Driver: overlay2  <-----
      Backing Filesystem: xfs  <-----
      Supports d_type: true
      Native Overlay Diff: true
  ......

  Docker is now using the overlay2 storage driver and has automatically
  created the overlay mount with the required 'lowerdir', 'upperdir', 'merged', and 'workdir' constructs.



--------------------------------------------------
How the overlay2 driver works (overlay2 的工作方式)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

OverlayFS layers two directories on a single Linux host and presents them as a single directory.
These directories are called layers and the unification process is referred to as a union mount(联合挂载).
OverlayFS refers to the lower directory as 'lowerdir' and the upper directory a 'upperdir'.
The unified view is exposed through its own directory called 'merged'.

The overlay2 driver natively supports up to 128 lower OverlayFS layers.
This capability provides better performance for layer-related Docker commands
such as `docker build` and `docker commit`, and consumes fewer inodes on the backing filesystem.


--------------------
Image and container layers on-disk

After downloading a five-layer image using docker pull ubuntu, you can see six directories under /var/lib/docker/overlay2.

  Warning: Do not directly manipulate any files or directories within /var/lib/docker/. These files and directories are managed by Docker.
  // 警告: 不要直接 操作 /var/lib/docker/ 下的任何 文件 或 目录, 这些 文件 和 目录 是由 Docker 来管理的

  $ ls -l /var/lib/docker/overlay2

    total 24
    drwx------ 5 root root 4096 Jun 20 07:36 223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7
    drwx------ 3 root root 4096 Jun 20 07:36 3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b
    drwx------ 5 root root 4096 Jun 20 07:36 4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1
    drwx------ 5 root root 4096 Jun 20 07:36 e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5
    drwx------ 5 root root 4096 Jun 20 07:36 eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed
    drwx------ 2 root root 4096 Jun 20 07:36 l  <----目录 l(links), 其中包含了 layers 的 符号链接, 只不过符号链接的标识符字符串更短小

The new l (lowercase L) directory contains shortened layer identifiers as symbolic links.
These identifiers are used to avoid hitting the page size limitation on arguments to the mount command.
// 新的 l(小写 L) 目录 包含了 layer 的简短标识符(以 符号链接的方式),
// 这些标识符被用于 避免 在 mount 命令的 arguments 上 达到 页面大小(page size) 限制。

  $ ls -l /var/lib/docker/overlay2/l

    total 20
    lrwxrwxrwx 1 root root 72 Jun 20 07:36 6Y5IM2XC7TSNIJZZFLJCS6I4I4 -> ../3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff
    lrwxrwxrwx 1 root root 72 Jun 20 07:36 B3WWEFKBG3PLLV737KZFIASSW7 -> ../4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1/diff
    lrwxrwxrwx 1 root root 72 Jun 20 07:36 JEYMODZYFCZFYSDABYXD5MF6YO -> ../eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed/diff
    lrwxrwxrwx 1 root root 72 Jun 20 07:36 NFYKDW6APBCCUCTOUSYDH4DXAT -> ../223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff
    lrwxrwxrwx 1 root root 72 Jun 20 07:36 UL2MW33MSE3Q5VYIKBRN4ZAGQP -> ../e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5/diff


The lowest layer contains a file called link, which contains the name of the shortened identifier,
and a directory called diff which contains the layer’s contents.

    $ ls /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/

        diff  link  <----  目录 diff  和 文件 link

    $ cat /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/link

        6Y5IM2XC7TSNIJZZFLJCS6I4I4  <---  文件 link 包含 shortened identifier 的 名字

    $ ls  /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff

        bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
      // 目录  diff 包含 layer contents

The second-lowest layer, and each higher layer, contain a file called 'lower', which denotes its parent,
and a directory called 'diff' which contains its contents. It also contains a 'merged' directory,
which contains the unified contents of its parent layer and itself,
and a 'work' directory which is used internally by OverlayFS.

  $ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7

      diff  link  lower  merged  work

    文件 lower: denotes its parent (即指明其 父层)
    目录 diff:  contains its contents (即 包含层的内容)
    目录 merged: contains the unified contents of its parent layer and itself(即包含 联合/合并 后的内容)
    目录 work: used internally by OverlayFS (即由 OverlayFS 内部使用,被视为 工作目录)

  $ cat /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/lower

      l/6Y5IM2XC7TSNIJZZFLJCS6I4I4  <---  parent layer

  $ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff/

      etc  sbin  usr  var <---- layer's contents


To view the mounts which exist when you use the overlay storage driver with Docker, use the mount command. The output below is truncated for readability.

$ mount | grep overlay

  overlay on /var/lib/docker/overlay2/9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/merged
  type overlay (rw,relatime, <----此处的 rw 表示该 overlay mount 是 读写挂载
  lowerdir=l/DJA75GUWHWG7EWICFYX54FIOVT:l/B3WWEFKBG3PLLV737KZFIASSW7:l/JEYMODZYFCZFYSDABYXD5MF6YO:l/UL2MW33MSE3Q5VYIKBRN4ZAGQP:l/NFYKDW6APBCCUCTOUSYDH4DXAT:l/6Y5IM2XC7TSNIJZZFLJCS6I4I4,
  upperdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/diff,
  workdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/work)

The rw on the second line shows that the overlay mount is read-write.






--------------------------------------------------
How the overlay driver works (此处介绍的是 overlay 存储驱动的工作方式 而非 overlay 存储驱动的工作方式)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/#how-the-overlay-driver-works


--------------------------------------------------
How container reads and writes work with overlay or overlay2

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

------------------------------
Reading files

  Consider three scenarios where a container opens a file for read access with overlay.

      - The file does not exist in the container layer:
            If a container opens a file for read access and the file does not
            already exist in the container (upperdir) it is read from the image
            (lowerdir). This incurs very little performance overhead.

      - The file only exists in the container layer:
            If a container opens a file for read access and the file exists in the container
            (upperdir) and not in the image (lowerdir), it is read directly from the container.

      - The file exists in both the container layer and the image layer:
            If a container opens a file for read access and the file exists in the image layer and the container layer,
            the file’s version in the container layer is read. Files in the container layer (upperdir)
            obscure files with the same name in the image layer (lowerdir).


------------------------------
Modifying files or directories

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

Consider some scenarios where files in a container are modified.

- Writing to a file for the first time:
    The first time a container writes to an existing file,
    that file does not exist in the container (upperdir).
    The overlay/overlay2 driver performs a copy_up operation to copy the file
    from the image (lowerdir) to the container (upperdir).
    The container then writes the changes to the new copy of the file in the container layer.

    However, OverlayFS works at the file level rather than the block level.
    This means that all OverlayFS copy_up operations copy the entire file,
    even if the file is very large and only a small part of it is being modified.
    This can have a noticeable impact on container write performance. However, two things are worth noting:


        - The copy_up operation only occurs the first time a given file is written to.
          Subsequent writes to the same file operate against the copy of the file already copied up to the container.

        - OverlayFS only works with two layers. This means that performance should be better than AUFS,
          which can suffer noticeable latencies when searching for files in images with many layers.
          This advantage applies to both overlay and overlay2 drivers. overlayfs2 is slightly less performant
          than overlayfs on initial read, because it must look through more layers, but it caches the results so this is only a small penalty


- Deleting files and directories:
    - When a file is deleted within a container, a whiteout file is created in the container (upperdir).
      The version of the file in the image layer (lowerdir) is not deleted
      (because the lowerdir is read-only). However, the whiteout file prevents it from being available to the container.

    - When a directory is deleted within a container, an opaque directory is created within
      the container (upperdir). This works in the same way as a whiteout file and effectively
      prevents the directory from being accessed, even though it still exists in the image (lowerdir).


- Renaming directories:
    Calling rename(2) for a directory is allowed only when both the source and the destination path
    are on the top layer. Otherwise, it returns EXDEV error (“cross-device link not permitted”).
    Your application needs to be designed to handle EXDEV and fall back to a “copy and unlink” strategy.



--------------------------------------------------
OverlayFS and Docker Performance

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

Both overlay2 and overlay drivers are more performant than aufs and devicemapper.
In certain circumstances, overlay2 may perform better than btrfs as well.
However, be aware of the following details.

    - Page Caching. OverlayFS supports page cache sharing. Multiple containers accessing the same
                    file share a single page cache entry for that file. This makes the overlay and
                    overlay2 drivers efficient with memory and a good option for high-density use cases such as PaaS.

    - copy_up. As with AUFS, OverlayFS performs copy-up operations whenever a container writes to
               a file for the first time. This can add latency into the write operation, especially for large files.
               However, once the file has been copied up, all subsequent writes to that file occur in the upper layer,
               without the need for further copy-up operations.

        The OverlayFS copy_up operation is faster than the same operation with AUFS, because
        AUFS supports more layers than OverlayFS and it is possible to incur far larger
        latencies if searching through many AUFS layers. overlay2 supports multiple layers
        as well, but mitigates any performance hit with caching.

    - Inode limits. Use of the legacy overlay storage driver can cause excessive inode consumption.
                    This is especially true in the presence of a large number of images and containers
                    on the Docker host. The only way to increase the number of inodes available to
                    a filesystem is to reformat it. To avoid running into this issue,
                    it is highly recommended that you use overlay2 if at all possible.


--------------------------------------------------
Performance best practices (性能最佳实践)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

The following generic performance best practices also apply to OverlayFS.

    - Use fast storage: Solid-state drives (SSDs) provide faster reads and writes than spinning disks.
      // 使用快速 存储: 固态硬盘

    - Use volumes for write-heavy workloads: Volumes provide the best and most predictable performance
      for write-heavy workloads. This is because they bypass the storage driver and do not incur any
      of the potential overheads introduced by thin provisioning and copy-on-write.
      Volumes have other benefits, such as allowing you to share data among containers
      and persisting your data even if no running container is using them.
      // 将 卷(volumes) 用于 write-heavy workloads


--------------------------------------------------
Limitations on OverlayFS compatibility (OverlayFS 的兼容限制)

    https://docs.docker.com/storage/storagedriver/overlayfs-driver/

    - open(2): OverlayFS only implements a subset of the POSIX standards. This can result in certain
               OverlayFS operations breaking POSIX standards. One such operation is the copy-up operation.
               Suppose that your application calls fd1=open("foo", O_RDONLY) and then fd2=open("foo", O_RDWR).
               In this case, your application expects fd1 and fd2 to refer to the same file. However,
               due to a copy-up operation that occurs after the second calling to open(2),
               the descriptors refer to different files. The fd1 continues to reference the file
               in the image (lowerdir) and the fd2 references the file in the container (upperdir).
               A workaround for this is to touch the files which causes the copy-up operation to happen.
               All subsequent open(2) operations regardless of read-only or read-write
               access mode reference the file in the container (upperdir).

              yum is known to be affected unless the yum-plugin-ovl package is installed.
              If the yum-plugin-ovl package is not available in your distribution such as
              RHEL/CentOS prior to 6.8 or 7.2, you may need to run touch /var/lib/rpm/* before
              running yum install. This package implements the touch workaround referenced above for yum.

    - rename(2): OverlayFS does not fully support the rename(2) system call.
                 Your application needs to detect its failure and fall back to a “copy and unlink” strategy.



----------------------------------------------------------------------------------------------------
Docker object labels  (docker 对象标签)

    https://docs.docker.com/config/labels-custom-metadata/



----------------------------------------------------------------------------------------------------
Prune unused Docker objects  (修剪  未被使用的对象)

    https://docs.docker.com/config/pruning/

Docker takes a conservative approach to cleaning up unused objects (often referred to as “garbage collection”),
such as images, containers, volumes, and networks: these objects are generally not removed unless you explicitly
ask Docker to do so. This can cause Docker to use extra disk space. For each type of object,
Docker provides a `prune` command. In addition, you can use
`docker system prune` to clean up multiple types of objects at once.
This topic shows how to use these `prune` commands.
// Docker 采用 一种保守的方式来 清理 未被使用的对象(通常被称为 "垃圾收集")

--------------------------------------------------
Prune images (修剪 images)

    https://docs.docker.com/config/pruning/
    https://docs.docker.com/engine/reference/commandline/image_prune/



[root@node01 ~]# docker image prune --help

    Usage:  docker image prune [OPTIONS]

    Remove unused images

    Options:
      -a, --all             Remove all unused images, not just dangling ones
          --filter filter   Provide filter values (e.g. 'until=<timestamp>')
      -f, --force           Do not prompt for confirmation



The `docker image prune` command allows you to clean up unused images. By default,
`docker image prune` only cleans up dangling images. A dangling image is one that
is not tagged and is not referenced by any container. To remove dangling images:

// 命令 `docker image prune` 允许你 清理 未被使用的 images.
// 默认, `docker image prune` 仅 清理 dangling images.
// A dangling image 是那些 未被标记(tagged) 和 没有被 任何 container 引用的 image.

    $ docker image prune

    WARNING! This will remove all dangling images.
    Are you sure you want to continue? [y/N] y


To remove all images which are not used by existing containers, use the -a flag:

    $ docker image prune -a

    WARNING! This will remove all images without at least one container associated to them.
    Are you sure you want to continue? [y/N] y

By default, you are prompted to continue. To bypass the prompt, use the -f or --force flag.

You can limit which images are pruned using filtering expressions with the --filter flag.
For example, to only consider images created more than 24 hours ago:

    $ docker image prune -a --filter "until=24h"


更多 filtering expressions 见 https://docs.docker.com/engine/reference/commandline/image_prune/


--------------------------------------------------
Prune containers (修剪 containers)

    https://docs.docker.com/config/pruning/
    https://docs.docker.com/engine/reference/commandline/container_prune/


        [root@node01 ~]# docker container prune  --help

        Usage:  docker container prune [OPTIONS]

        Remove all stopped containers

        Options:
              --filter filter   Provide filter values (e.g. 'until=<timestamp>')
          -f, --force           Do not prompt for confirmation




When you stop a container, it is not automatically removed unless you started it with the --rm flag.
To see all containers on the Docker host, including stopped containers,
use docker ps -a. You may be surprised how many containers exist, especially on a development system!
A stopped container’s writable layers still take up disk space. To clean this up,
you can use the `docker container prune` command.

// 停止(stop) 一个容器时, 该容器 并不会被自动删除(除非你在启动该容器时指定了 --rm 选项)

    $ docker container prune

    WARNING! This will remove all stopped containers.
    Are you sure you want to continue? [y/N] y

By default, you are prompted to continue. To bypass the prompt, use the -f or --force flag.

By default, all stopped containers are removed. You can limit the scope using the --filter flag.
For instance, the following command only removes stopped containers older than 24 hours:

      $ docker container prune --filter "until=24h"


  更多 filtering expressions 见 https://docs.docker.com/engine/reference/commandline/container_prune/



--------------------------------------------------
Prune volumes  (修剪 volumes)

  https://docs.docker.com/config/pruning/
  https://docs.docker.com/engine/reference/commandline/volume_prune/

注: 即使 volumes 暂时 没有被任何容器使用, 也不一定就意味着 该 volumes 中的内容就不需要了。
    所以删除 volumes 之前一定要 慎重考虑，以免造成 数据丢失.


[root@node01 ~]# docker volume prune --help

    Usage:  docker volume prune [OPTIONS]

    Remove all unused local volumes

    Options:
          --filter filter   Provide filter values (e.g. 'label=<label>')
      -f, --force           Do not prompt for confirmation


Volumes can be used by one or more containers, and take up space on the Docker host.
Volumes are never removed automatically, because to do so could destroy data.


        $ docker volume prune

        WARNING! This will remove all volumes not used by at least one container.
        Are you sure you want to continue? [y/N] y


By default, you are prompted to continue. To bypass the prompt, use the -f or --force flag.

By default, all unused volumes are removed. You can limit the scope using the --filter flag.
For instance, the following command only removes volumes which are not labelled with the keep label:

    $ docker volume prune --filter "label!=keep"

  更多 filtering expressions 见 https://docs.docker.com/engine/reference/commandline/volume_prune/



--------------------------------------------------
Prune networks  (修剪 networks)

    https://docs.docker.com/config/pruning/

        [root@node01 ~]# docker network prune --help

        Usage:  docker network prune [OPTIONS]

        Remove all unused networks

        Options:
              --filter filter   Provide filter values (e.g. 'until=<timestamp>')
          -f, --force           Do not prompt for confirmation


Docker networks don’t take up much disk space, but they do create iptables rules,
bridge network devices, and routing table entries. To clean these things up,
you can use `docker network prune` to clean up networks which aren’t used by any containers.

    $ docker network prune

    WARNING! This will remove all networks not used by at least one container.
    Are you sure you want to continue? [y/N] y


By default, you are prompted to continue. To bypass the prompt, use the -f or --force flag.

By default, all unused networks are removed. You can limit the scope using the --filter flag.
For instance, the following command only removes networks older than 24 hours:

    $ docker network prune --filter "until=24h"

  更多 filtering expressions 见  https://docs.docker.com/engine/reference/commandline/network_prune/





--------------------------------------------------
Prune everything (修剪 everything)


    https://docs.docker.com/config/pruning/


      [root@node01 ~]# docker system prune --help

      Usage:  docker system prune [OPTIONS]

      Remove unused data

      Options:
        -a, --all             Remove all unused images not just dangling ones
            --filter filter   Provide filter values (e.g. 'label=<key>=<value>')
        -f, --force           Do not prompt for confirmation
            --volumes         Prune volumes



The docker system prune command is a shortcut that prunes images, containers, and networks.
In Docker 17.06.0 and earlier, volumes are also pruned. In Docker 17.06.1 and higher,
you must specify the --volumes flag for docker system prune to prune volumes.
// 命令 `docker system prune` 是 修剪 images, containers, 和 networks 的快捷方式.
//  在早期 Docker 17.06.0 及 以前 版本中, volumes 也会被 修剪. 而在 后来的 Docker 17.06.1
//  即更高的版本中, 你必须指定 --volumes 选项来 明确告诉 命令 `docker system prune` 还要
//  修剪 volumes (这其实也是出于数据安全性的考虑, 以免无意中造成数据丢失)

      $ docker system prune

      WARNING! This will remove:
              - all stopped containers
              - all networks not used by at least one container
              - all dangling images
              - all build cache
      Are you sure you want to continue? [y/N] y

If you are on Docker 17.06.1 or higher and want to also prune volumes, add the --volumes flag:

      $ docker system prune --volumes

      WARNING! This will remove:
              - all stopped containers
              - all networks not used by at least one container
              - all volumes not used by at least one container
              - all dangling images
              - all build cache
      Are you sure you want to continue? [y/N] y
      By default, you are prompted to continue. To bypass the prompt, use the -f or --force flag.






----------------------------------------------------------------------------------------------------
Format command and log output


    https://docs.docker.com/config/formatting/

    Go templates(需要翻墙): https://golang.org/pkg/text/template/

Docker uses Go templates which you can use to manipulate the output format of certain commands and log drivers.

Docker provides a set of basic functions to manipulate template elements.
All of these examples use the docker inspect command, but many other CLI
commands have a --format flag, and many of the CLI command
references include examples of customizing the output format.

[root@node01 ~]# docker container run --rm -d --name nginx_c01 nginx:latest
    678370437e5b8c93ef33e3a911e0ca6318f9edfec413f5346992c32abc866a48


-  join
      join concatenates a list of strings to create a single string. It puts a separator between each element in the list.

[root@node01 ~]# docker inspect --format '{{join .Args " , "}}' nginx_c01
    -g , daemon off;

-  json
      json encodes an element as a json string.

[root@node01 ~]# docker container run --rm -dit --mount destination=/dbdata --name centos7_c01 centos:7
[root@node01 ~]# docker container inspect --format '{{json .Mounts}}' centos7_c01
      [{"Type":"volume","Name":"8b74e8c86a888883027834d8f6492785a3b9e003247d228c76d028ce17ec4f06","Source":"/var/lib/docker/volumes/8b74e8c86a888883027834d8f6492785a3b9e003247d228c76d028ce17ec4f06/_data","Destination":"/dbdata","Driver":"local","Mode":"z","RW":true,"Propagation":""}]



-  lower
      lower transforms a string into its lowercase representation.

[root@node01 ~]# docker container inspect --format "{{lower .Name}}" centos7_c01
    /centos7_c01


-  upper
      upper transforms a string into its uppercase representation.

[root@node01 ~]# docker container inspect --format "{{upper .Name}}" centos7_c01
    /CENTOS7_C01



-  split
      split slices a string into a list of strings separated by a separator.

[root@node01 ~]# docker container inspect --format '{{split .Image ":"}}' centos7_c01
    [sha256 67fa590cfc1c207c30b837528373f819f6262c884b7e69118d060a0c04d70ab8]



-  title
      title capitalizes the first character of a string.

[root@node01 ~]# docker container inspect --format "{{title .Name}}" centos7_c01
    /Centos7_c01


-  println
      println prints each value on a new line.

[root@node01 ~]# docker container inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' centos7_c01
    172.17.0.2


Hint (提示)
      To find out what data can be printed, show all content as json:

[root@node01 ~]# docker container ls --format='{{json .}}'
    {"Command":"\"/bin/bash\"","CreatedAt":"2019-11-01 14:27:00 +0800 CST","ID":"5c1db6025050","Image":"centos:7","Labels":"org.label-schema.vendor=CentOS,org.label-schema.build-date=20190801,org.label-schema.license=GPLv2,org.label-schema.name=CentOS Base Image,org.label-schema.schema-version=1.0","LocalVolumes":"1","Mounts":"8b74e8c86a8888…","Names":"centos7_c01","Networks":"bridge","Ports":"","RunningFor":"19 minutes ago","Size":"0B","Status":"Up 19 minutes"}









----------------------------------------------------------------------------------------------------
Dockerfile reference  (Dockerfile 参考)

    https://docs.docker.com/engine/reference/builder/
    https://docs.docker.com/reference/
    https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

  关于 Dockerfile 的作用, 可以类比一下 Makefile


            [root@node01 ~]# docker build --help

            Usage:  docker build [OPTIONS] PATH | URL | -

            Build an image from a Dockerfile

            Options:
                  --add-host list           Add a custom host-to-IP mapping (host:ip)
                  --build-arg list          Set build-time variables
                  --cache-from strings      Images to consider as cache sources
                  --cgroup-parent string    Optional parent cgroup for the container
                  --compress                Compress the build context using gzip
                  --cpu-period int          Limit the CPU CFS (Completely Fair Scheduler) period
                  --cpu-quota int           Limit the CPU CFS (Completely Fair Scheduler) quota
              -c, --cpu-shares int          CPU shares (relative weight)
                  --cpuset-cpus string      CPUs in which to allow execution (0-3, 0,1)
                  --cpuset-mems string      MEMs in which to allow execution (0-3, 0,1)
                  --disable-content-trust   Skip image verification (default true)
              -f, --file string             Name of the Dockerfile (Default is 'PATH/Dockerfile')
                  --force-rm                Always remove intermediate containers
                  --iidfile string          Write the image ID to the file
                  --isolation string        Container isolation technology
                  --label list              Set metadata for an image
              -m, --memory bytes            Memory limit
                  --memory-swap bytes       Swap limit equal to memory plus swap: '-1' to enable unlimited swap
                  --network string          Set the networking mode for the RUN instructions during build (default "default")
                  --no-cache                Do not use cache when building the image
                  --pull                    Always attempt to pull a newer version of the image
              -q, --quiet                   Suppress the build output and print image ID on success
                  --rm                      Remove intermediate containers after a successful build (default true)
                  --security-opt strings    Security options
                  --shm-size bytes          Size of /dev/shm
              -t, --tag list                Name and optionally a tag in the 'name:tag' format
                  --target string           Set the target build stage to build.
                  --ulimit ulimit           Ulimit options (default [])





Docker can build images automatically by reading the instructions from a Dockerfile.
A Dockerfile is a text document that contains all the commands a user could call on
the command line to assemble an image. Using docker build users can create an
automated build that executes several command-line instructions in succession.

This page describes the commands you can use in a Dockerfile. When you
are done reading this page, refer to the Dockerfile Best Practices for a tip-oriented guide.

  Dockerfile 的最佳实践 见: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/


Usage (用法)

The `docker build` command builds an image from a `Dockerfile` and a context.
The build’s context is the set of files at a specified location 'PATH' or 'URL'.
The PATH is a directory on your local filesystem. The URL is a Git repository location.
// 构建上下文(build’s context) 是 位于 'PATH' 或 'URL' 处的 文件集.

A context is processed recursively. So, a PATH includes any subdirectories and
the URL includes the repository and its submodules.
This example shows a build command that uses the current directory as context:
// A context 是 被 递归地处理的, 因此, a PATH 包含 其任意 子目录 且 the URL 包含 其 仓库和其 submodules.

      $ docker build .
      Sending build context to Docker daemon  6.51 MB
      ...

The build is run by the Docker daemon, not by the CLI. The first thing a build process does
is send the entire context (recursively) to the daemon. In most cases, it’s best to start
with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.
// build 是通过 Docker 守护进程 执行的, 不是可通过 CLI. build 过程做的 第一件 事情 就是将
// 整个上下文(recursively) 发送给 Docker daemon. 大多数情况下, 最好 开始时 以 一个 空目录 作为 context
// 并将 Dockerfile 放入其中。 而后仅添加 构建 Dockerfile 所需要的 files.


    Warning(警告): Do not use your root directory, /, as the PATH as it causes the build to
             transfer the entire contents of your hard drive to the Docker daemon.


To use a file in the build context, the Dockerfile refers to the file specified in an instruction,
for example, a `COPY` instruction. To increase the build’s performance, exclude files and directories
by adding a '.dockerignore'(类比 '.gitignore' 文件) file to the context directory.
For information about how to create a '.dockerignore' file see the documentation on this page.


Traditionally, the Dockerfile is called Dockerfile and located in the root of the context.
You use the -f flag with docker build to point to a Dockerfile anywhere in your file system.
// 习惯地, Dockerfile 被命名为 Dockerfile 并置于 context 的 root 下.
// 可以使用 `docker build` 的 -f 选项 来指定 文件系统中 任意位置的 a Dockerfile

      $ docker build -f /path/to/a/Dockerfile .   #注意: 此处的 点 '.' 表示当前目录作为 PATH(即 context 的 root)


You can specify a repository and tag at which to save the new image if the build succeeds:

      $ docker build -t shykes/myapp .  #使用 -t 选项指定 build 成功后 该 new image 所 save 到的 repository 和 tag

To tag the image into multiple repositories after the build, add multiple -t parameters when you run the build command:

      $ docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .   #选项 -t 可重复多次 以指定 多个仓库(repositories)


Before the Docker daemon runs the instructions in the Dockerfile,
it performs a preliminary validation of the Dockerfile and returns an error if the syntax is incorrect:
// 在 Docker daemon 执行 Dockerfile 中的 指令(instructions) 之前, Docker daemon 会初步地 检查验证 Dockerfile,
// 如果 Dockerfile 存在语法错误, 其会 返回 an error

      $ docker build -t test/myapp .
      Sending build context to Docker daemon 2.048 kB
      Error response from daemon: Unknown instruction: RUNCMD

The Docker daemon runs the instructions in the Dockerfile one-by-one, committing the result of
each instruction to a new image if necessary, before finally outputting the ID of your new image.
The Docker daemon will automatically clean up the context you sent.
// Docker daemon 会逐一运行  Dockerfile 中的 instructions, 在 最终 输出 生成的 new image 的 ID 之间,
// 会根据需要 把 每个 instruction 的 结果 提交到 a new image.


Note that each instruction is run independently, and causes a new image
to be created - so RUN cd /tmp will not have any effect on the next instructions.
// 注意: 每个 instruction 是 独立运行的, 并导致 一个新的 image 被创建.
//       因此, 指令 'RUN cd /tmp' 对于 下一条指定 不会起到任何作用

Whenever possible, Docker will re-use the intermediate images (cache),
to accelerate the docker build process significantly. This is indicated
by the 'Using cache' message in the console output. (For more information,
see the Build cache section in the Dockerfile best practices guide):
// 只要有可能, Docker 就会 重用 中间过程中的 images (cache),
// 以 显著地 加速 docker build 过程. 这在 console output 中 通过 'Using cache' 消息给出了指示.

$ docker build -t svendowideit/ambassador .
    Sending build context to Docker daemon 15.36 kB
    Step 1/4 : FROM alpine:3.2
     ---> 31f630c65071
    Step 2/4 : MAINTAINER SvenDowideit@home.org.au
     ---> Using cache  <----观察 'Using cache' 指示
     ---> 2a1c91448f5f
    Step 3/4 : RUN apk update &&      apk add socat &&        rm -r /var/cache/
     ---> Using cache
     ---> 21ed6e7fbb73
    Step 4/4 : CMD env | grep _TCP= | (sed 's/.*_PORT_\([0-9]*\)_TCP=tcp:\/\/\(.*\):\(.*\)/socat -t 100000000 TCP4-LISTEN:\1,fork,reuseaddr TCP4:\2:\3 \&/' && echo wait) | sh
     ---> Using cache
     ---> 7ea8aef582cc
    Successfully built 7ea8aef582cc


Build cache is only used from images that have a local parent chain. This means that these images
were created by previous builds or the whole chain of images was loaded with docker load.
If you wish to use build cache of a specific image you can specify it with '--cache-from' option.
Images specified with '--cache-from' do not need to have a parent chain and may be pulled from other registries.


When you’re done with your build, you’re ready to look into Pushing a repository to its registry.




--------------------------------------------------
BuildKit


    https://docs.docker.com/engine/reference/builder/
    https://github.com/moby/buildkit

BuildKit has been integrated to docker build since Docker 18.06 .
//从 Docker 18.09 开始, BuildKit 已经被 集成到了 docker build 中


Starting with version 18.09, Docker supports a new backend for executing your builds that is provided by the moby/buildkit project.
The BuildKit backend provides many benefits compared to the old implementation. For example, BuildKit can:

    - Detect and skip executing unused build stages
    - Parallelize building independent build stages
    - Incrementally transfer only the changed files in your build context between builds
    - Detect and skip transferring unused files in your build context
    - Use external Dockerfile implementations with many new features
    - Avoid side-effects with rest of the API (intermediate images and containers)
    - Prioritize your build cache for automatic pruning

To use the BuildKit backend, you need to set an environment variable DOCKER_BUILDKIT=1 on the CLI before invoking docker build.
// 为了使用 BuildKit backend, 你需要在调用命令 `docker build` 之前 在 命令行(CLI) 上设置 环境变量  `DOCKER_BUILDKIT=1`

To learn about the experimental Dockerfile syntax available to BuildKit-based builds refer to the documentation in the BuildKit repository.
        https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/experimental.md


--------------------------------------------------
Format

    https://docs.docker.com/engine/reference/builder/

Here is the format of the Dockerfile:

      # Comment
      INSTRUCTION arguments

The instruction is not case-sensitive. However, convention is for them to be UPPERCASE to distinguish them from arguments more easily.
// instruction 大小写不敏感, 但是, 约定 使用 大写 以 使其 更容易与 指令的 arguments 进行区分.

Docker runs instructions in a Dockerfile in order. A Dockerfile must begin with a `FROM` instruction.
This may be after parser directives, comments, and globally scoped ARGs.
The FROM instruction specifies the Parent Image from which you are building.
FROM may only be preceded by one or more ARG instructions,
which declare arguments that are used in FROM lines in the Dockerfile.
// Docker 按顺序执行 Dockerfile 中的 instructions. 一个 Dockerfile 必须以 一个 `FROM` instruction 开始.
// 不过该 `FROM` instruction 可以位于 parser directives, comments, 和 globally scoped ARGs 之后,
// FROM 指令 指定了 你 正在构建 做 基于的 父镜像(the Parent Image).
// FROM 仅能 前面 有 一个 或 多个 ARG instructions, 其声明了 在 Dockerfile 中 FROM lines 中所使用的 arguments.

Docker treats lines that begin with # as a comment, unless the line is a valid parser directive.
A # marker anywhere else in a line is treated as an argument. This allows statements like:
// Docker 视 以 # 起始的行 为注释, 除非 该行是一个 有效的 解析器指令(parser directive)

      # Comment
      RUN echo 'we are running some # of cool things'

Line continuation characters are not supported in comments.
// comments 中 不支持 续行字符





--------------------------------------------------
Parser directives

    https://docs.docker.com/engine/reference/builder/

Parser directives are optional, and affect the way in which subsequent lines in a Dockerfile are handled.
Parser directives do not add layers to the build, and will not be shown as a build step.
Parser directives are written as a special type of comment in the form # directive=value.
A single directive may only be used once.


Once a comment, empty line or builder instruction has been processed, Docker no longer looks for parser directives.
Instead it treats anything formatted as a parser directive as a comment and does not attempt to validate
if it might be a parser directive. Therefore, all parser directives must be at the very top of a Dockerfile.
// 所有的 parser directives 必须位于 Dockerfile 文件中的 最上面/最顶上(包括 注释 和 空行).
// 因为 一旦 a comment, empty line 或 builder instruction 被处理了, Docker 就不会再查找 parser directives.
// 而会将 所有 遇到的 形如 parser directives 的内容 视为 注释(comment)

Parser directives are not case-sensitive. However, convention is for them to be lowercase.
Convention is also to include a blank line following any parser directives.
Line continuation characters are not supported in parser directives.
// Parser directives 大小写 不敏感. 但是, 约定 其 使用小写.
// 约定 还 包括在 任意 多个 parser directives 之后 再 跟随一个空白行(a blank line)
// parser directives 不支持 续行符


Due to these rules, the following examples are all invalid:
// 根据这些规则, 如下的示例 都是 无效的:

Invalid due to line continuation:

      # direc \   <----非法(invalid), 因为 Parser directives 不支持 续行符
      tive=value


Invalid due to appearing twice:

    # directive=value1
    # directive=value2 <------非法(invalid),因为 单个 指令仅被使用一次

    FROM ImageName


Treated as a comment due to appearing after a builder instruction:

    FROM ImageName
    # directive=value  <-----非法(invalid),因为 parser directives 必须出现在 Dockerfile 的最上面(包括注释和空行), 否则其会被视为注释(comment)

Treated as a comment due to appearing after a comment which is not a parser directive:

    # About my dockerfile
    # directive=value  <-----非法(invalid),因为 parser directives 必须出现在 Dockerfile 的最上面(包括注释和空行), 否则其会被视为注释(comment)
    FROM ImageName


The unknown directive is treated as a comment due to not being recognized.
In addition, the known directive is treated as a comment due to appearing after a comment which is not a parser directive.

      # unknowndirective=value  <-----非法(invalid),因为 未知的(unknown) directive 被视为 注释, 所以该错误还会导致 后面的 所有 Parser directives  被视为注释(comment)
      # knowndirective=value



Non line-breaking whitespace is permitted in a parser directive. Hence, the following lines are all treated identically(等价):

            #directive=value
            # directive =value
            # directive= value
            # directive = value
            #   dIrEcTiVe=value




The following parser directives are supported:

        syntax
        escape




--------------------------------------------------
syntax

    https://docs.docker.com/engine/reference/builder/

语法: syntax=[remote image reference]

For example:

      示例:  syntax=docker/dockerfile
      示例:  syntax=docker/dockerfile:1.0
      示例:  syntax=docker.io/docker/dockerfile:1
      示例:  syntax=docker/dockerfile:1.0.0-experimental
      示例:  syntax=example.com/user/repo:tag@sha256:abcdef...


This feature is only enabled if the BuildKit backend is used.
// 该 特性 仅在 使用 BuildKit backend 时 被启用(enabled)

The syntax directive defines the location of the Dockerfile builder that is used for building the current Dockerfile.
The BuildKit backend allows to seamlessly use external implementations of builders that are distributed
as Docker images and execute inside a container sandbox environment.
// syntax 指令定义了 用于构建 当前 Dockerfile 的 Dockerfile builder 的 location.
// BuildKit backend 允许 无缝地 使用 builders 的 外部实现.  其 作为 Docker images 被 发布 且 在 容器的 沙箱环境中执行.


Custom Dockerfile implementation allows you to:
// 自定义 Dockerfile 实现的 好处:

    - Automatically get bugfixes without updating the daemon
      // 自动 获取 bugfixes 而 无需 更新 daemon

    - Make sure all users are using the same implementation to build your Dockerfile
      // 确保 所有的 users 正在 使用 相同的 实现 来 构建 你的 Dockerfile

    - Use the latest features without updating the daemon
    - Try out new experimental or third-party features



Official releases

Docker distributes official versions of the images that can be used for building Dockerfiles
under docker/dockerfile repository on Docker Hub.
There are two channels where new images are released: stable and experimental.
// Docker 在 Docker Hub 上的 docker/dockerfile 仓库中  分发 官方版本的 可被用于构建 Dockerfiles 的 the images.

      https://hub.docker.com/r/docker/dockerfile
      https://hub.docker.com/r/docker/dockerfile/tags


Stable channel follows semantic versioning. For example:

    - docker/dockerfile:1.0.0 - only allow immutable version 1.0.0
    - docker/dockerfile:1.0 - allow versions 1.0.*
    - docker/dockerfile:1 - allow versions 1..
    - docker/dockerfile:latest - latest release on stable channel

The experimental channel uses incremental versioning with the major and minor component from the stable channel on the time of the release. For example:

    - docker/dockerfile:1.0.1-experimental - only allow immutable version 1.0.1-experimental
    - docker/dockerfile:1.0-experimental - latest experimental releases after 1.0
    - docker/dockerfile:experimental - latest release on experimental channel


You should choose a channel that best fits your needs. If you only want bugfixes,
you should use docker/dockerfile:1.0. If you want to benefit from experimental features,
you should use the experimental channel. If you are using the experimental channel,
newer releases may not be backwards compatible, so it is recommended to use an immutable full version variant.
// 建议使用 不可变的 full version variant, 如 'docker/dockerfile:1.0.0'


For master builds and nightly feature releases refer to the description in the source repository.
          https://github.com/moby/buildkit/blob/master/README.md




--------------------------------------------------
escape

    https://docs.docker.com/engine/reference/builder/

语法: escape=\ (backslash)

Or

语法: escape=` (backtick)


The escape directive sets the character used to escape characters in a Dockerfile. If not specified, the default escape character is \.
// escape directive 设置 Dockerfile 中 使用的 转义字符, 如果 没有指定, 默认的 转移字符 是 \.


The escape character is used both to escape characters in a line, and to escape a newline.
This allows a Dockerfile instruction to span multiple lines. Note that regardless of whether
the escape parser directive is included in a Dockerfile, escaping is not performed in a RUN command, except at the end of a line.
// 注: 不管 Dockerfile 中 是否包含了 escape 解析器指令,  转移 不会 在 a RUN command 中 被执行, 除了 at the end of a line.


Setting the escape character to ` is especially useful on Windows,
where \ is the directory path separator. ` is consistent with Windows PowerShell.
// 将 转移字符 设置为 ` 在 Windows 系统上 很有用


关于 windows 上 的 Dockerfile 的转义字符 更多讨论见 https://docs.docker.com/engine/reference/builder/






--------------------------------------------------
Environment replacement

    https://docs.docker.com/engine/reference/builder/

Environment variables (declared with the `ENV` statement) can also be used in certain instructions as variables
to be interpreted by the Dockerfile. Escapes are also handled for including variable-like syntax into a statement literally.

Environment variables are notated in the Dockerfile either with $variable_name or ${variable_name}.
They are treated equivalently and the brace syntax is typically used to address issues with variable names with no whitespace, like ${foo}_bar.
// 注: Dockerfile 中 环境变量的引用 方式 类似于 bash shell 中对变量的 引用方式, 即 $variable_name 或 ${variable_name}


The ${variable_name} syntax also supports a few of the standard bash modifiers as specified below:

      - ${variable:-word} indicates that if variable is set then the result will be that value. If variable is not set then word will be the result.
      - ${variable:+word} indicates that if variable is set then word will be the result, otherwise the result is the empty string.

In all cases, word can be any string, including additional environment variables.

Escaping is possible by adding a \ before the variable: \$foo or \${foo}, for example, will translate to $foo and ${foo} literals respectively.


Example (parsed representation is displayed after the #):
//示例

        FROM busybox
        ENV foo /bar
        WORKDIR ${foo}   # WORKDIR /bar
        ADD . $foo       # ADD . /bar
        COPY \$foo /quux # COPY $foo /quux


Environment variables are supported by the following list of instructions in the Dockerfile:
// 如下 Dockerfile 中的指令 支持 环境变量:

          -  ADD
          -  COPY
          -  ENV
          -  EXPOSE
          -  FROM
          -  LABEL
          -  STOPSIGNAL
          -  USER
          -  VOLUME
          -  WORKDIR

as well as(以及):

          -  ONBUILD (when combined with one of the supported instructions above)

Note(注): prior to 1.4, ONBUILD instructions did NOT support environment variable, even when combined with any of the instructions listed above.


Environment variable substitution will use the same value for each variable throughout the entire instruction. In other words, in this example:
// 环境变量 替换 在 entire instruction 中 将使用 每个变量的 相同的值, 如下示例:

        ENV abc=hello
        ENV abc=bye def=$abc   <---注: 该指令执行后 def 的 value 为  hello
        ENV ghi=$abc           <---注: 该指令执行后 ghi 的 value 为  bye

will result in def having a value of hello, not bye. However, ghi will have a value of bye because it is not part of the same instruction that set abc to bye.








--------------------------------------------------
.dockerignore file


    https://docs.docker.com/engine/reference/builder/


    类比 .gitignore 文件


Before the docker CLI sends the context to the docker daemon, it looks for a file named .dockerignore
in the root directory of the context. If this file exists, the CLI modifies the context to
exclude files and directories that match patterns in it. This helps to avoid unnecessarily
sending large or sensitive files and directories to the daemon and potentially adding them to images using ADD or COPY.
// 在 docker CLI 发送 context 到 docker daemon 之前, 其 会在 context 的 root 目录中 查找 文件 .dockerignore .
// 如果该文件存在, CLI 会 修改 该 context 以 将 匹配 该 .dockerignore 文件中的 patterns 的那些文件 或 目录 排除在外.


The CLI interprets the .dockerignore file as a newline-separated list of patterns similar
to the file globs of Unix shells. For the purposes of matching, the root of the context is
considered to be both the working and the root directory. For example,
the patterns /foo/bar and foo/bar both exclude a file or directory named bar in
the foo subdirectory of PATH or in the root of the git repository located at URL. Neither excludes anything else.
// .dockerignore 中的 patterns 与 Unix shells 中的 the file globs 类似(见 `man 7 glob`).
// 匹配的时候, context 的 根目录 会被同时 视为 the working and the root directory.

If a line in .dockerignore file starts with # in column 1, then this line
is considered as a comment and is ignored before interpreted by the CLI.


Here is an example .dockerignore file:
// .dockerignore 示例文件

        # comment
        */temp*   <---匹配 root 的直接子目录下的 name 以 'temp' 开始的 文件和目录 并 排除, 如文件 /somedir/temporary.txt 或 /somedir/temp
        */*/temp* <---匹配 root 的二级子目录下的 name 以 'temp' 开始的 文件和目录 并 排除, 如文件 /somedir/subdir/temporary.txt
        temp?     <---匹配 root 下的 name 以 'temp' 开始 且以 一个字符结束 的 文件和目录并排除, 如 /tempa 和 /tempb

This file causes the following build behavior:
-----------+----------------------------------------------------------------------------------------
Rule       |    Behavior
-----------|----------------------------------------------------------------------------------------
# comment  |    Ignored.
-----------|----------------------------------------------------------------------------------------
*/temp*    |    Exclude files and directories whose names start with temp in any immediate subdirectory of the root.
           |    For example, the plain file /somedir/temporary.txt is excluded, as is the directory /somedir/temp.
-----------|----------------------------------------------------------------------------------------
*/*/temp*  |    Exclude files and directories starting with temp from any subdirectory that is two levels below the root.
           |    For example, /somedir/subdir/temporary.txt is excluded.
-----------|----------------------------------------------------------------------------------------
temp?      |    Exclude files and directories in the root directory whose names are a one-character extension of temp.
           |    For example, /tempa and /tempb are excluded.
-----------+----------------------------------------------------------------------------------------

Matching is done using Go’s filepath.Match rules. A preprocessing step removes leading
and trailing whitespace and eliminates . and .. elements using Go’s filepath.Clean.
Lines that are blank after preprocessing are ignored.
// 匹配时 通过 Go 语言的  filepath.Match 规则完成的, 一个 预处理步骤 会 移除 leading
// and trailing whitespace 并 使用 Go 语言的 filepath.Clean 计算出 . 和 .. 元素.
// blank 行 在 云处理之后 会被 ignored.

Beyond Go’s filepath.Match rules, Docker also supports a special wildcard string ** that matches
any number of directories (including zero). For example, **/*.go will exclude all files
that end with .go that are found in all directories, including the root of the build context.
// 除了 Go 的 filepath.Match 规则之外, Docker 还 支持特殊的 通配字符串 ** 以 匹配 任意
// 数量的 directories(包括 zero).


Lines starting with ! (exclamation mark) can be used to make exceptions to exclusions.
The following is an example .dockerignore file that uses this mechanism:
// 感叹号 ! 用于指定 例外

      *.md
      !README.md  <---这两行表示 排除  context的root 下的 所有 以 .md 结尾的文件或目录, 但 README.md 例外

The placement of ! exception rules influences the behavior: the last line of the .dockerignore that
matches a particular file determines whether it is included or excluded. Consider the following example:
// ! exception rules 的 位置 会 影响 其 行为: .dockerignore 中 匹配 特定 文件的 的 最后那行(the last line)
// 将确定 其是 被 包含还是 被 排除.

    *.md
    !README*.md
    README-secret.md  <---这3行的效果是: 排除所有的 *.md 和 README-secret.md, 但其他的 README*.md 除外.

No markdown files are included in the context except README files other than README-secret.md.

Now consider this example:

    *.md
    README-secret.md
    !README*.md  <---这3行的效果是: 排除 所有的 *.md 但是 包含 所有的 README*.md, 即 第二行被 第3行的规则所覆盖了,所以不再起作用

All of the README files are included. The middle line has no effect because !README*.md matches README-secret.md and comes last.

You can even use the .dockerignore file to exclude the Dockerfile and .dockerignore files.
These files are still sent to the daemon because it needs them to do its job. But the ADD and COPY instructions do not copy them to the image.
// 你甚至 可以使用 .dockerignore 来排除 文件 Dockerfile 和 .dockerignore.
// 这些文件 仍然会被 发送给 docker daemon 因为 这些文件 是其 完成任务 所需要的.
// 但是 指令 ADD 和 COPY 则 不会将这些文件 复制到 image 中.

Finally, you may want to specify which files to include in the context, rather than which to exclude.
To achieve this, specify * as the first pattern, followed by one or more ! exception patterns.
// 一种实现类似 白名单 的 技巧: 先排除所有, 然后在 添加 例外.

Note: For historical reasons, the pattern . is ignored.
// 注: 因为历史原因，模式 . 会被忽略



--------------------------------------------------
FROM 指令

    https://docs.docker.com/engine/reference/builder/

      注: 指令 ARG 是 仅有的 在 Dockerfile 中 可以在 指令 ARG 之前的指令

语法: FROM <image> [AS <name>]     <---注: 如果忽略 [:<tag>] 或 [@<digest>], 则默认使用 tag 'latest', 如果找不到给tag, 则返回错误

Or

语法: FROM <image>[:<tag>] [AS <name>]
Or
语法: FROM <image>[@<digest>] [AS <name>]


The FROM instruction initializes a new build stage and sets the Base Image for subsequent instructions.
As such, a valid Dockerfile must start with a FROM instruction. The image can be
any valid image – it is especially easy to start by pulling an image from the Public Repositories.

  - ARG is the only instruction that may precede FROM in the Dockerfile. See Understand how ARG and FROM interact.
    // 指令 ARG 是 仅有的 在 Dockerfile 中 可以在 指令 ARG 之前的指令
          https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact

  - FROM can appear multiple times within a single Dockerfile to create multiple images or use one
    build stage as a dependency for another. Simply make a note of the last image ID output by
    the commit before each new FROM instruction. Each FROM instruction clears any state created by previous instructions.
    // 指令 FROM 在 单个 Dockerfile 中 可以出现 多次 以 创建多个 images 或 将 一个构件阶段(build stage) 作为 另一个构件阶段的依赖.

  - Optionally a name can be given to a new build stage by adding AS name to the FROM instruction.
    The name can be used in subsequent FROM and `COPY --from=<name|index>` instructions to refer to the image built in this stage.

  - The tag or digest values are optional. If you omit either of them, the builder assumes
    a latest tag by default. The builder returns an error if it cannot find the tag value.


----------
Understand how ARG and FROM interact  (理解 指令 ARG 和 FROM 的交互)

FROM instructions support variables that are declared by any ARG instructions that occur before the first FROM.
// 在 第一个 指令 FROM 之前 可以使用 任意多个 指令 ARG 来声明 变量(variables)

        ARG  CODE_VERSION=latest
        FROM base:${CODE_VERSION}
        CMD  /code/run-app

        FROM extras:${CODE_VERSION}
        CMD  /code/run-extras

An ARG declared before a FROM is outside of a build stage, so it can’t be used in any instruction after a FROM.
To use the default value of an ARG declared before the first FROM use an ARG instruction without a value inside of a build stage:
// 在 a FROM 之前 声明的 的 An ARG 在 构件阶段 之外(即超出了 build stage, 不属于构件阶段内),
// 因此其 无法被 FROM 之后 的 任意 指令 使用.
// 要使用 the first FROM 之前的 指令 ARG 声明的 变量的 默认值, 在以在 a build stage 内部 使用 不带 value 的 ARG 指令

      ARG VERSION=latest
      FROM busybox:$VERSION
      ARG VERSION  <----注:为了使用第一行变量的默认值,这里在 FROM 指令初始化的 build stage 内 使用了不带 value 的 ARG 指令
      RUN echo $VERSION > image_version




--------------------------------------------------
RUN

    https://docs.docker.com/engine/reference/builder/


                                     RUN                                CMD
      Dockerfile(with context) --------------------->  new image  ---------------------> container
                                 docker build                         docker run

RUN has 2 forms:

- RUN <command> (shell form, the command is run in a shell, which by default is /bin/sh -c on Linux or cmd /S /C on Windows)
  // RUN <command> 为 shell 的形式, 该 command 在 shell 中被执行, Linux 上默认为 `/bin/sh -c` 或 Windows 上默认为 `cmd /S /C`

- RUN ["executable", "param1", "param2"] (exec form)  <---注:exec form 中是作为 a JSON array来解析,所以只能使用双引号不能使用单引号

The RUN instruction will execute any commands in a new layer on top of the current image and commit the results.
The resulting committed image will be used for the next step in the Dockerfile.
// 指令 RUN 会在 当前 image 顶部 的  一个 新层(a new layer) 中 执行 任意 commands 并 提交结果.
// 该 结果提交后 产生的 image 会被用于 该 Dockerfile 的 下一步中.


Layering RUN instructions and generating commits conforms to the core concepts of Docker
where commits are cheap and containers can be created from any point in an image’s history, much like source control.


The exec form makes it possible to avoid shell string munging, and to RUN commands
using a base image that does not contain the specified shell executable.
// exec form 能够避免 shell 的 字符串整理(string munging). 并 使用 不包含 特定 shell 可执行程序
// 的 base image 来 RUN commands

The default shell for the shell form can be changed using the SHELL command.
// shell form 中的 默认 shell 可以通过 命令 SHELL 来修改

In the shell form you can use a \ (backslash) to continue a single RUN instruction onto the next line.
For example, consider these two lines:
// 在 shell form 中 可以使用 \ (backslash) 来 将 a single RUN instruction 延续到 下一行, 如:

      RUN /bin/bash -c 'source $HOME/.bashrc; \
      echo $HOME'

Together they are equivalent to this single line(等价于):

      RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'

Note: To use a different shell, other than ‘/bin/sh’, use the exec form passing in the desired shell.
For example, RUN ["/bin/bash", "-c", "echo hello"]
// 注: RUN ["/bin/bash", "-c", "echo hello"] 中以 exec form 的方式来使用 bash 运行命令 echo

Note: The exec form is parsed as a JSON array, which means that you must use double-quotes (“) around words not single-quotes (‘).
// 注:exec form 中是作为 a JSON array来解析,所以只能使用双引号不能使用单引号


Note: Unlike the shell form, the exec form does not invoke a command shell.
      This means that normal shell processing does not happen.
      For example, RUN [ "echo", "$HOME" ] will not do variable substitution on $HOME.
      If you want shell processing then either use the shell form or execute a shell directly,
      for example: RUN [ "sh", "-c", "echo $HOME" ]. When using the exec form and executing a shell directly,
      as in the case for the shell form, it is the shell that is doing the environment variable expansion, not docker.
//注: 不同于 shell form, exec form 不会 调用 shell 命令.
//    这意味着 不会执行 shell 处理(shell processing).
//    例如, RUN [ "echo", "$HOME" ] 不会 执行 $HOME 的 变量替换.
//    如果你 需要 shell processing, 则即可以使用 shell form, 也可以 直接执行 shell,
//    例如: RUN [ "sh", "-c", "echo $HOME" ]. 当 使用 exec form 并 执行执行 一个 shell 时,
//    与 shell form 一样, 是由 shell 来 完成 environment variable expansion 而非 docker.


Note: In the JSON form, it is necessary to escape backslashes. This is particularly relevant on Windows
where the backslash is the path separator. The following line would otherwise be treated as shell form
due to not being valid JSON, and fail in an unexpected way: RUN ["c:\windows\system32\tasklist.exe"]
The correct syntax for this example is: RUN ["c:\\windows\\system32\\tasklist.exe"]
// 注: 在 JSON form 中, 需要对 反斜线('\') 进行转义.  很重要的第一点是 在 Windows 系统上
// backslash('\') 是 路径分隔符.
// 错误形式: RUN ["c:\windows\system32\tasklist.exe"]
// 正确形式: RUN ["c:\\windows\\system32\\tasklist.exe"]


The cache for RUN instructions isn’t invalidated automatically during the next build.
The cache for an instruction like RUN apt-get dist-upgrade -y will be reused during the next build.
The cache for RUN instructions can be invalidated by using the --no-cache flag, for example docker build --no-cache.
// RUN 指令的 缓存(cache) 在 下一个 build 期间 不会 自动地 被 invalidated.
// 像 `RUN apt-get dist-upgrade -y` 这样的指令的 cache 会在 下一个 build 期间 被 重用(reused).
// 指令 RUN  的 cache 可以 通过 --no-cache 选项来使其 invalidated.  例如 `docker build --no-cache`


See the Dockerfile Best Practices guide for more information.
      https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

The cache for RUN instructions can be invalidated by ADD instructions. See below for details.
      https://docs.docker.com/engine/reference/builder/#add

    ------------------------------
    Known issues (RUN) (该 issues 与使用 AUFS 文件系统有关)
        Issue 783 is about file permissions problems that can occur when using the AUFS file system.
        You might notice it during an attempt to rm a file, for example.

        For systems that have recent aufs version (i.e., dirperm1 mount option can be set),
        docker will attempt to fix the issue automatically by mounting the layers with dirperm1 option.
        More details on dirperm1 option can be found at aufs man page

        If your system doesn’t have support for dirperm1, the issue describes a workaround.
    ------------------------------






--------------------------------------------------
CMD

    https://docs.docker.com/engine/reference/builder/


                                     RUN                                CMD
      Dockerfile(with context) --------------------->  new image  ---------------------> container
                                 docker build                         docker run


The CMD instruction has three forms:

    - CMD ["executable","param1","param2"] (exec form, this is the preferred form)
    - CMD ["param1","param2"] (as default parameters to ENTRYPOINT) <--默认参数意味着 其可以被运行 `docker run` 命令时指定的参数所覆盖
    - CMD command param1 param2 (shell form)`


There can only be one CMD instruction in a Dockerfile. If you list more than one CMD then only the last CMD will take effect.
// 一个 Dockerfile 中 仅能 有 一个 CMD 指令, 如果你 列出 多个 CMD 指令, 则 最后的 那个 CMD 将 起作用


The main purpose of a CMD is to provide defaults for an executing container.
These defaults can include an executable, or they can omit the executable,
in which case you must specify an ENTRYPOINT instruction as well.
// CMD 的主要目的 是为 执行中的 container 提供 defaults,
// 这些 defaults 可以包含 可执行程序(executable),  或 其 也 可以 忽略 可执行程序(executable),
// 在忽略 executable 的情况中, 你 还必须同时 指定 ENTRYPOINT 指令


Note: If CMD is used to provide default arguments for the ENTRYPOINT instruction,
both the CMD and ENTRYPOINT instructions should be specified with the JSON array format.
// 注:  如果 CMD 被用户 为 ENTRYPOINT 提供 默认的 arguments,
//      则 指令 CMD 和 指令 ENTRYPOINT 都应该 被 指定为 JSON array format.

Note: The exec form is parsed as a JSON array, which means that you must use double-quotes (“) around words not single-quotes (‘).
// 注: exec form 被 当做 a JSON array 来 解析, 这意味着 你必须使用 双引号(“) 而 不是 单引号(‘).

Note: Unlike the shell form, the exec form does not invoke a command shell.
      This means that normal shell processing does not happen.
      For example, CMD [ "echo", "$HOME" ] will not do variable substitution on $HOME.
      If you want shell processing then either use the shell form or execute a shell directly,
      for example: CMD [ "sh", "-c", "echo $HOME" ]. When using the exec form and executing a shell directly,
      as in the case for the shell form, it is the shell that is doing the environment variable expansion, not docker.


When used in the shell or exec formats, the CMD instruction sets the command to be executed when running the image.
// shell form  和 exec form 中, 指令 CMD 被用户指定 在 运行 image(即基于 image 运行容器) 时被执行的 command.


If you use the shell form of the CMD, then the <command> will execute in /bin/sh -c:
// 采用 shell form 的 CMD 指令时, <command> 是通过 /bin/sh -c 来执行的

    FROM ubuntu
    CMD echo "This is a test." | wc -

If you want to run your <command> without a shell then you must express the command as a JSON array
and give the full path to the executable. This array form is the preferred format of CMD.
Any additional parameters must be individually expressed as strings in the array:

      FROM ubuntu
      CMD ["/usr/bin/wc","--help"]   <----注: 这里命令 wc 必须使用 full path 指定, 因为这里 无法 使用 bash 等 shell 的一些特性

If you would like your container to run the same executable every time,
then you should consider using ENTRYPOINT in combination with CMD. See ENTRYPOINT.
// 如果你想让 你的容器 每次 都 执行相同的 executable, 则 你应该考虑  使用 ENTRYPOINT 与 CMD 结合的方式

            https://docs.docker.com/engine/reference/builder/#entrypoint

If the user specifies arguments to docker run then they will override the default specified in CMD.
// 如果 user 在 命令 `docker run` 中 指定 arguments,  则 这些 arguments  会 覆盖 指令 CMD 指定的 默认值(the default)

Note: Don’t confuse RUN with CMD. RUN actually runs a command and commits the result;
      CMD does not execute anything at build time, but specifies the intended command for the image.
// 注: 不要混淆 指令 RUN 和 指令 CMD. RUN 实际上 执行  a command 并 提交 the result;
//     而 CMD 不会在 构建时 执行任何操作, 而是为 the image 指定 与其 命令.


                                     RUN                                CMD
      Dockerfile(with context) --------------------->  new image  ---------------------> container
                                 docker build                         docker run





--------------------------------------------------
LABEL

    https://docs.docker.com/engine/reference/builder/

语法: LABEL <key>=<value> <key>=<value> <key>=<value> ...

The LABEL instruction adds metadata to an image. A LABEL is a key-value pair.
To include spaces within a LABEL value, use quotes and backslashes as you would in command-line parsing. A few usage examples:

        LABEL "com.example.vendor"="ACME Incorporated"
        LABEL com.example.label-with-value="foo"
        LABEL version="1.0"
        LABEL description="This text illustrates \
        that label-values can span multiple lines."

An image can have more than one label. You can specify multiple labels on a single line.
Prior to Docker 1.10, this decreased the size of the final image, but this is no longer the case.
You may still choose to specify multiple labels in a single instruction, in one of the following two ways:
// 在 Docker 1.10 之前, 在单行 上 指定 multiple labels 可以 减小 最终 image 的大小, 但是 现在情况不再如此.

    LABEL multi.label1="value1" multi.label2="value2" other="value3"

    LABEL multi.label1="value1" \
          multi.label2="value2" \
          other="value3"


Labels included in base or parent images (images in the FROM line) are inherited by your image.
If a label already exists but with a different value,
the most-recently-applied value overrides any previously-set value.
// base 或 parent images 中包含的 Labels 会被 你的 image 继承.
// 如果 一个 label 已经存在 但是 具有一个 不同的 value,
// 则 最近 被 应用的 value 会 覆盖掉 任何 之前 设置的 value.

To view an image’s labels, use the docker inspect command.
// 使用命令 `docker inspect` 可以查看 一个 image 的 labels

      "Labels": {
          "com.example.vendor": "ACME Incorporated"
          "com.example.label-with-value": "foo",
          "version": "1.0",
          "description": "This text illustrates that label-values can span multiple lines.",
          "multi.label1": "value1",
          "multi.label2": "value2",
          "other": "value3"
      },


--------------------------------------------------
MAINTAINER (deprecated)

    https://docs.docker.com/engine/reference/builder/

语法: MAINTAINER <name>   <---注: 指令 MAINTAINER 已经过时, 可以使用如 LABEL maintainer="SvenDowideit@home.org.au" 这样的 LABEL 指令替代


The MAINTAINER instruction sets the Author field of the generated images.
The LABEL instruction is a much more flexible version of this and you should use it instead,
as it enables setting any metadata you require, and can be viewed easily,
for example with docker inspect. To set a label corresponding to the MAINTAINER field you could use:


    LABEL maintainer="SvenDowideit@home.org.au"


This will then be visible from docker inspect with the other labels.


--------------------------------------------------
EXPOSE

    https://docs.docker.com/engine/reference/builder/

语法: EXPOSE <port> [<port>/<protocol>...]   <---注: protocol 默认为 TCP

The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
You can specify whether the port listens on TCP or UDP, and the default is TCP if the protocol is not specified.
// 指令 EXPOSE 告知 Docker 在运行的时候 容器 所 监听的 特定的 network ports.
// 你可以 指定 port 监听在 TCP 或 UDP 协议上, 默认协议为 TCP


The EXPOSE instruction does not actually publish the port. It functions as a type of documentation
between the person who builds the image and the person who runs the container,
about which ports are intended to be published. To actually publish the port
when running the container, use the -p flag on docker run to publish and map one or more ports,
or the -P flag to publish all exposed ports and map them to high-order ports.
// 指令 EXPOSE 不会 实际地 发布 port, 它的作用是 作为 builds the image 的人员 与 runs the container 的 人员
// 之间的 一种文档(documentation), 当 运行 容器时, 可以在命令 `docker run` 上使用 -p 选项 来 发布 和 映射 一个 one or more ports,
// 或使用 -P (即 大写 P) 选项 来发布 所有的 暴露 ports 并 将其  映射到 高阶端口(high-order ports).

By default, EXPOSE assumes TCP. You can also specify UDP:

    EXPOSE 80/udp

To expose on both TCP and UDP, include two lines:
// 同时 暴露 TCP 和 UDP 时 需要 2 行:

    EXPOSE 80/tcp
    EXPOSE 80/udp

In this case, if you use -P with docker run, the port will be exposed once for TCP and once for UDP.
Remember that -P uses an ephemeral high-ordered host port on the host, so the port will not be the same for TCP and UDP.
// 在这种情况下, 如果你使用指令 `docker run -P`, 则 port 对于 TCP 和 UDP 都会 暴露一次.
// 记住 -P 使用的是 临时的 high-ordered host port, 因此 该 port 对于 TCP 和 UDP 将 不会是相同的

Regardless of the EXPOSE settings, you can override them at runtime by using the -p flag. For example
// 不管 EXPOSE 的设置, 你可以 在 运行时 使用 -p 选项来 对其进行覆盖. 例如:

      docker run -p 80:80/tcp -p 80:80/udp ...

To set up port redirection on the host system, see using the -P flag. The docker network command supports
creating networks for communication among containers without the need to expose or publish specific ports,
because the containers connected to the network can communicate with each other over any port.
For detailed information, see the overview of this feature).

    https://docs.docker.com/engine/reference/run/#expose-incoming-ports
    https://docs.docker.com/network/




--------------------------------------------------
ENV

    https://docs.docker.com/engine/reference/builder/

语法: ENV <key> <value>
语法: ENV <key>=<value> ...


The ENV instruction sets the environment variable <key> to the value <value>.
This value will be in the environment for all subsequent instructions in the build stage and can be replaced inline in many as well.

The ENV instruction has two forms. The first form, ENV <key> <value>, will set a single variable to a value.
The entire string after the first space will be treated as the <value> - including whitespace characters.
The value will be interpreted for other environment variables, so quote characters will be removed if they are not escaped.

The second form, ENV <key>=<value> ..., allows for multiple variables to be set at one time.
Notice that the second form uses the equals sign (=) in the syntax, while the first form does not.
Like command line parsing, quotes and backslashes can be used to include spaces within values.

For example:

    ENV myName="John Doe" myDog=Rex\ The\ Dog \
        myCat=fluffy


and

    ENV myName John Doe
    ENV myDog Rex The Dog
    ENV myCat fluffy


will yield the same net results in the final image.

The environment variables set using ENV will persist when a container is run from the resulting image.
You can view the values using docker inspect, and change them using docker run --env <key>=<value>.
// 当 从 the resulting image 运行一个 容器时, 那些使用 ENV 设置的 环境变量 将会 继续存在.
// 可以使用 命令 `docker inspect` 观察 这些变量值, 和 使用命令 `docker run --env <key>=<value>` 对其 进行修改


Note: Environment persistence can cause unexpected side effects.
      For example, setting ENV DEBIAN_FRONTEND noninteractive may confuse apt-get users
      on a Debian-based image. To set a value for a single command, use RUN <key>=<value> <command>.

// 注: Environment 的持久存在 可能 导致 非预期的  副作用.
       例如, `ENV DEBIAN_FRONTEND noninteractive` 设置 可能会 对  基于 Debian 镜像上 的 apt-get users 造成迷惑.
       要为 单个 command 设置  a value, 可以使用  `RUN <key>=<value> <command>`





--------------------------------------------------
ADD

    https://docs.docker.com/engine/reference/builder/


ADD has two forms:

    语法: ADD [--chown=<user>:<group>] <src>... <dest>    <---注:<src> 路径 必须 位于 build 的 context 之内. <dest> 是 绝对路径 或  相对于 WORKDIR 的 的相对路径
    语法: ADD [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)

      注: 如果 <src> 为 a URL, 此时 <dest> 是否包含 a trailing slash 对于 下载文件后 该文件保存的路径有影响
      注: 如果 直接 或 通过 a wildcard 指定了 多个 <src> resources, 则 <dest> 必须是一个 目录 且 其必须 以 a slash / 结尾.
      注: 如果 <dest> 不以 a trailing slash 结尾, 其被 视为 a regular file 且 the contents of <src> 会被写在 <dest> 上。
      注: 如果 <dest> 实际不存在, 其 会与 其路径中 缺少的 directories 一起被创建.


Note: The --chown feature is only supported on Dockerfiles used to build Linux containers,
      and will not work on Windows containers. Since user and group ownership concepts do not
      translate between Linux and Windows, the use of /etc/passwd and /etc/group for translating
      user and group names to IDs restricts this feature to only be viable for Linux OS-based containers.
// 注: --chown 特性 仅在 构建 Linux containers 的 Dockerfiles 上 得到支持

The ADD instruction copies new files, directories or remote file URLs
from <src> and adds them to the filesystem of the image at the path <dest>.
//  指令 ADD 拷贝 <src> 指定的 new files, directories or remote file  并 将其
//  添加到 image 的文件系统中的  <dest> 指定的 路径位置

Multiple <src> resources may be specified but if they are files or directories,
their paths are interpreted as relative to the source of the context of the build.
// 可以指定 多个 <src> 资源 但是 如果 它们为 files 或 directories, 则
// 它们的 路径 被解释为 相对于 build 的 context 的 source


Each <src> may contain wildcards and matching will be done using Go’s filepath.Match rules. For example:
// 每个 <src> 可以包含 通配符 并 使用 Go 语言的 filepath.Match 规则进行匹配. 例如:

    ADD hom* /mydir/        # adds all files starting with "hom"
    ADD hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"

        http://golang.org/pkg/path/filepath#Match


The <dest> is an absolute path, or a path relative to WORKDIR, into which the source will be copied inside the destination container.
// <dest> 是 绝对路径 或  相对于 WORKDIR 的 的相对路径

      ADD test relativeDir/          # adds "test" to `WORKDIR`/relativeDir/
      ADD test /absoluteDir/         # adds "test" to /absoluteDir/


When adding files or directories that contain special characters (such as [ and ]),
you need to escape(转义) those paths following the Golang rules to prevent them from being treated as a matching pattern.
For example, to add a file named arr[0].txt, use the following;

      ADD arr[[]0].txt /mydir/    # copy a file named "arr[0].txt" to /mydir/

All new files and directories are created with a UID and GID of 0, unless the optional --chown flag
specifies a given username, groupname, or UID/GID combination to request specific ownership of
the content added. The format of the --chown flag allows for either username and groupname strings
or direct integer UID and GID in any combination. Providing a username without groupname
or a UID without GID will use the same numeric UID as the GID. If a username or groupname is provided,
the container’s root filesystem /etc/passwd and /etc/group files will be used to perform the translation
from name to integer UID or GID respectively. The following examples show valid definitions for the --chown flag:
// 所有的 new files and directories 使用 UID(0)  和 GID(0) 来创建, 除非 使用 可选的 --chown 选项
// 指定了 username, groupname, 或 UID/GID combination 来 要求 特定的 被添加内容的 所属关系.
// 如果 提供了 username 而没 提供 groupname, 或 提供了 UID 而每提供 GID, 则 GID 将使用 与 UID 相同的数值.
// 如果提供的是 username 或 groupname, 则 容器的 root filesystem 中的 /etc/passwd 和 /etc/group 文件
// 会被分别用于执行 name 到 整数的 UID 或 GID 之间的转换翻译。
// 如下是 一些 有效的 示例;

        ADD --chown=55:mygroup files* /somedir/
        ADD --chown=bin files* /somedir/
        ADD --chown=1 files* /somedir/
        ADD --chown=10:11 files* /somedir/


If the container root filesystem does not contain either /etc/passwd or /etc/group files and either user
or group names are used in the --chown flag, the build will fail on the ADD operation.
Using numeric IDs requires no lookup and will not depend on container root filesystem content.


In the case where <src> is a remote file URL, the destination will have permissions of 600.
If the remote file being retrieved has an HTTP Last-Modified header, the timestamp from that
header will be used to set the mtime on the destination file. However, like any other file
processed during an ADD, mtime will not be included in the determination of
whether or not the file has changed and the cache should be updated.


Note: If you build by passing a Dockerfile through STDIN (docker build - < somefile),
there is no build context, so the Dockerfile can only contain a URL based ADD instruction.
You can also pass a compressed archive through STDIN: (docker build - < archive.tar.gz),
the Dockerfile at the root of the archive and the rest of the archive will be used as the context of the build.

Note: If your URL files are protected using authentication, you will need to use RUN wget,
      RUN curl or use another tool from within the container as the ADD instruction does not support authentication.
      // 如果你的 URL files 使用了 authentication 来保护, 则你 需要使用 `RUN wget`, `RUN curl` 或 容器中的其他工具
      // 因为 指令 ADD 不支持 authentication.


Note: The first encountered ADD instruction will invalidate the cache for all following instructions
      from the Dockerfile if the contents of <src> have changed. This includes invalidating the
      cache for RUN instructions. See the Dockerfile Best Practices guide for more information.

            https://docs.docker.com/develop/develop-images/dockerfile_best-practices/


ADD obeys the following rules:
// 指令 ADD 遵循 如下 规则:

    - The <src> path must be inside the context of the build; you cannot ADD ../something /something,
      because the first step of a docker build is to send the context directory (and subdirectories) to the docker daemon.
      // <src> 路径 必须 位于 build 的 context 之内. 因为 `docker build` 的第一步 就是将 context 目录(和 子目录) 发送到 docker daemon.

    - If <src> is a URL and <dest> does not end with a trailing slash, then a file is downloaded from the URL and copied to <dest>.
      // 如果 <src> 为 URL 且 <dest> 不以 a trailing slash 结尾, 则 a file 会从 URL 下载 并 复制到 <dest>.

    - If <src> is a URL and <dest> does end with a trailing slash, then the filename is inferred from
      the URL and the file is downloaded to <dest>/<filename>. For instance,
      ADD http://example.com/foobar / would create the file /foobar. The URL must have
      a nontrivial path so that an appropriate filename can be discovered in this case (http://example.com will not work).
      // 如果 <src> 为 URL 且 <dest> 以 a trailing slash 结尾, 那么 filename 会从 该 URL 中被推断 出 且 该 file 被下载到
      // <dest>/<filename>. 例如, `ADD http://example.com/foobar /` 会创建 文件 /foobar.
      // URL 必须具有 a nontrivial path 从而 在 这种情况下 可以 发现 一个 适当的 filename(而 http://example.com 无法工作).

    - If <src> is a directory, the entire contents of the directory are copied, including filesystem metadata.
      // 如果 <src> 是 一个 目录, 则 整个 directory 的 内容都会被 copied, 包括 filesystem metadata.

        Note: The directory itself is not copied, just its contents.
        // 注: directory 本身 不会被 copied, 仅复制其 contents.

    - If <src> is a local tar archive in a recognized compression format (identity, gzip, bzip2 or xz) then
      it is unpacked as a directory. Resources from remote URLs are not decompressed.
      When a directory is copied or unpacked, it has the same behavior as tar -x, the result is the union of:
      // 如果 <src> 是一个本地的 其压缩格式 可被识别的 tar 归档文件(identity, gzip, bzip2 or xz),
      // 则 其会被 解包(unpacked) 为 一个 目录. Resources from remote URLs are not decompressed.
      // 当一个 directory 被 copied 或 unpacked 时, 其 行为与 命令 `tar -x` 行为相同, 结果如下:

            1. Whatever existed at the destination path and
            2. The contents of the source tree, with conflicts resolved in favor of “2.” on a file-by-file basis.

      Note: Whether a file is identified as a recognized compression format or not is done solely based
            on the contents of the file, not the name of the file. For example, if an empty file happens
            to end with .tar.gz this will not be recognized as a compressed file and will not generate any
            kind of decompression error message, rather the file will simply be copied to the destination.



    - If <src> is any other kind of file, it is copied individually along with its metadata. In this case,
      if <dest> ends with a trailing slash /, it will be considered a directory and the contents of <src> will be written at <dest>/base(<src>).


    - If multiple <src> resources are specified, either directly or due to the use of a wildcard,
      then <dest> must be a directory, and it must end with a slash /.
      // 如果 直接 或 通过 a wildcard 指定了 多个 <src> resources, 则 <dest> 必须是一个 目录 且 其必须 以 a slash / 结尾.

    - If <dest> does not end with a trailing slash, it will be considered a regular file and the contents of <src> will be written at <dest>.
      // 如果 <dest> 不以 a trailing slash 结尾, 其被 视为 a regular file 且 the contents of <src> 会被写在 <dest> 上。

    - If <dest> doesn’t exist, it is created along with all missing directories in its path.
      // 如果 <dest> 实际不存在, 其 会与 其路径中 缺少的 directories 一起被创建.






--------------------------------------------------
COPY

    https://docs.docker.com/engine/reference/builder/

COPY has two forms:

语法: COPY [--chown=<user>:<group>] <src>... <dest>
语法: COPY [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)


Note: The --chown feature is only supported on Dockerfiles used to build Linux containers,
      and will not work on Windows containers. Since user and group ownership concepts do not
      translate between Linux and Windows, the use of /etc/passwd and /etc/group for translating user
      and group names to IDs restricts this feature to only be viable for Linux OS-based containers.


The COPY instruction copies new files or directories from <src> and adds them to the filesystem of the container at the path <dest>.

Multiple <src> resources may be specified but the paths of files and directories will be interpreted as relative to the source of the context of the build.

Each <src> may contain wildcards and matching will be done using Go’s filepath.Match rules. For example:

    COPY hom* /mydir/        # adds all files starting with "hom"
    COPY hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"

The <dest> is an absolute path, or a path relative to WORKDIR, into which the source will be copied inside the destination container.

    COPY test relativeDir/   # adds "test" to `WORKDIR`/relativeDir/
    COPY test /absoluteDir/  # adds "test" to /absoluteDir/

When copying files or directories that contain special characters (such as [ and ]),
you need to escape those paths following the Golang rules to prevent them from being treated as
a matching pattern. For example, to copy a file named arr[0].txt, use the following;

    COPY arr[[]0].txt /mydir/    # copy a file named "arr[0].txt" to /mydir/

All new files and directories are created with a UID and GID of 0, unless the optional --chown flag specifies
a given username, groupname, or UID/GID combination to request specific ownership of the copied content.
The format of the --chown flag allows for either username and groupname strings or
direct integer UID and GID in any combination. Providing a username without groupname or a UID
without GID will use the same numeric UID as the GID. If a username or groupname is provided,
the container’s root filesystem /etc/passwd and /etc/group files will be used to perform the
translation from name to integer UID or GID respectively. The following examples show valid definitions for the --chown flag:

      COPY --chown=55:mygroup files* /somedir/
      COPY --chown=bin files* /somedir/
      COPY --chown=1 files* /somedir/
      COPY --chown=10:11 files* /somedir/

If the container root filesystem does not contain either /etc/passwd or /etc/group files and either
user or group names are used in the --chown flag, the build will fail on the COPY operation.
Using numeric IDs requires no lookup and will not depend on container root filesystem content.

Note: If you build using STDIN (docker build - < somefile), there is no build context, so COPY can’t be used.

Optionally COPY accepts a flag --from=<name|index> that can be used to set the source location to
a previous build stage (created with FROM .. AS <name>) that will be used instead of a build context
sent by the user. The flag also accepts a numeric index assigned for all previous build stages started
with FROM instruction. In case a build stage with a specified name can’t
be found an image with the same name is attempted to be used instead.
// 可选地, COPY 可 接受 --from=<name|index> 选项, 其能 被用于 将 source location 设置为  一个 先前的 build stage(created with FROM .. AS <name>)
// 以 代替 由 user 发送的 a build context. 该 选项 也 可以接受 从 FROM 指令开始的 所有先前 build stages 分配的 a numeric index.
// 如果 具有 指定 name 的 build stage 无法被找到, 则 替换为 使用 具有 相同 name 的 an image.

COPY obeys the following rules:
// COPY 遵循 如下的规则:

    - The <src> path must be inside the context of the build; you cannot COPY ../something /something,
      because the first step of a docker build is to send the context directory (and subdirectories) to the docker daemon.

    - If <src> is a directory, the entire contents of the directory are copied, including filesystem metadata.

    Note: The directory itself is not copied, just its contents.

    - If <src> is any other kind of file, it is copied individually along with its metadata. In this case,
      if <dest> ends with a trailing slash /, it will be considered a directory and the contents of <src> will be written at <dest>/base(<src>).

    - If multiple <src> resources are specified, either directly or due to the use of a wildcard,
      then <dest> must be a directory, and it must end with a slash /.

    - If <dest> does not end with a trailing slash, it will be considered a regular file and the contents of <src> will be written at <dest>.

    - If <dest> doesn’t exist, it is created along with all missing directories in its path.




--------------------------------------------------
ENTRYPOINT

    https://docs.docker.com/engine/reference/builder/

ENTRYPOINT has two forms:

语法: ENTRYPOINT ["executable", "param1", "param2"] (exec form, preferred)
语法: ENTRYPOINT command param1 param2 (shell form)

An ENTRYPOINT allows you to configure a container that will run as an executable.
// ENTRYPOINT 允许你 配置 作为 an executable 运行的 容器


For example, the following will start nginx with its default content, listening on port 80:

    docker run -i -t --rm -p 80:80 nginx

Command line arguments to docker run <image> will be appended after all elements in an exec form ENTRYPOINT,
and will override all elements specified using CMD. This allows arguments to be passed to the entry point,
i.e., docker run <image> -d will pass the -d argument to the entry point.
You can override the ENTRYPOINT instruction using the docker run --entrypoint flag.
// `docker run <image>` 的 命令行 arguments  将被 追加(appended) 所有 exec form ENTRYPOINT 的 元素(elements) 之后,
// 并 会 覆盖掉 由指令 CMD 指定 的 所有 elements. 这 运行了 将 arguments 传递给 the entry point.
// 例如, `docker run <image> -d`  会将 -d 参数 传递 给 the entry point.
// 你可以 使用 'docker run --entrypoint' 选项 来覆盖 ENTRYPOINT 指令.


The shell form prevents any CMD or run command line arguments from being used, but has the disadvantage
that your ENTRYPOINT will be started as a subcommand of /bin/sh -c, which does not pass signals.
This means that the executable will not be the container’s PID 1 - and will not
receive Unix signals - so your executable will not receive a SIGTERM from docker stop <container>.
// shell form 可防止 CMD 或 run 命令行参数 被使用, 但缺点是 ENTRYPOINT 被作为 命令 `/bin/sh -c` 的子命令启动.
// 而其 不会 传递信号(signals).
// 这意味着 该 executable 将不会成为  容器的 PID 1 且  无法接收到 Unix signals.
// 因此 你的 executable 无法 接收到 `docker stop <container>` 发送过来的 a SIGTERM 信号.

Only the last ENTRYPOINT instruction in the Dockerfile will have an effect.




--------------------
Exec form ENTRYPOINT example

    https://docs.docker.com/engine/reference/builder/

You can use the exec form of ENTRYPOINT to set fairly stable default commands and arguments
and then use either form of CMD to set additional defaults that are more likely to be changed.
// 你可以 使用 ENTRYPOINT 的 exec form 来 设置 相当 稳定的 default commands 和 arguments
// 并 使用 CMD 的 exec form 来 设置 额外的 很可能会被修改的 defaults

      FROM ubuntu
      ENTRYPOINT ["top", "-b"]
      CMD ["-c"]


When you run the container, you can see that top is the only process:

    $ docker run -it --rm --name test  top -H
    top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
    Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
    KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

      PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
        1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top


To examine the result further, you can use docker exec:

    $ docker exec -it test ps aux
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H  <---观察, CMD ["-c"]  指定的默认参数 "-c" 已经被 docker run 命令中的 -H 所覆盖了
    root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux


And you can gracefully request top to shut down using `docker stop test`.
// 使用 命令 `docker stop test` 停止 容器.


The following Dockerfile shows using the ENTRYPOINT to run Apache in the foreground (i.e., as PID 1):
// Apache 的 Dockerfile 简单示例:

      FROM debian:stable
      RUN apt-get update && apt-get install -y --force-yes apache2
      EXPOSE 80 443
      VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
      ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]


If you need to write a starter script for a single executable,
you can ensure that the final executable receives the Unix signals by using exec and gosu commands:
// 如果你 需要 为 a single executable 编写 启动脚本,
// 你 可以使用 命令 exec 和 命令 gosu 确保 最终的 executable  接收 Unix signals.

          #!/usr/bin/env bash
          set -e

          if [ "$1" = 'postgres' ]; then
              chown -R postgres "$PGDATA"

              if [ -z "$(ls -A "$PGDATA")" ]; then
                  gosu postgres initdb
              fi

              exec gosu postgres "$@"
          fi

          exec "$@"


关于 gosu:
    https://blog.csdn.net/boling_cavalry/article/details/93380447
    https://stackoverflow.com/questions/36781372/docker-using-gosu-vs-user
    https://hub.docker.com/r/gosu/centos


Lastly, if you need to do some extra cleanup (or communicate with other containers) on shutdown,
or are co-ordinating more than one executable, you may need to ensure that the ENTRYPOINT script
receives the Unix signals, passes them on, and then does some more work:


        #!/bin/sh
        # Note: I've written this using sh so it works in the busybox container too

        # USE the trap if you need to also do manual cleanup after the service is stopped,
        #     or need to start multiple services in the one container
        trap "echo TRAPed signal" HUP INT QUIT TERM

        # start service in background here
        /usr/sbin/apachectl start

        echo "[hit enter key to exit] or run 'docker stop <container>'"
        read

        # stop service and clean up here
        echo "stopping apache"
        /usr/sbin/apachectl stop

        echo "exited $0"


If you run this image with `docker run -it --rm -p 80:80 --name test apache`,
you can then examine the container’s processes with docker exec, or docker top, and then ask the script to stop Apache:

        $ docker exec -it test ps aux
        USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
        root         1  0.1  0.0   4448   692 ?        Ss+  00:42   0:00 /bin/sh /run.sh 123 cmd cmd2
        root        19  0.0  0.2  71304  4440 ?        Ss   00:42   0:00 /usr/sbin/apache2 -k start
        www-data    20  0.2  0.2 360468  6004 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
        www-data    21  0.2  0.2 360468  6000 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
        root        81  0.0  0.1  15572  2140 ?        R+   00:44   0:00 ps aux

        $ docker top test
        PID                 USER                COMMAND
        10035               root                {run.sh} /bin/sh /run.sh 123 cmd cmd2
        10054               root                /usr/sbin/apache2 -k start
        10055               33                  /usr/sbin/apache2 -k start
        10056               33                  /usr/sbin/apache2 -k start

        $ /usr/bin/time docker stop test
        test
        real  0m 0.27s
        user  0m 0.03s
        sys 0m 0.03s


Note: you can override the ENTRYPOINT setting using --entrypoint, but this can only set the binary to exec (no sh -c will be used).
// 注: 你可以 使用 --entrypoint 选项 来 覆盖 ENTRYPOINT 设置, 但是这仅能把 the binary 设置为 exec (`sh -c` 不会被使用)


Note: The exec form is parsed as a JSON array, which means that you must use double-quotes (“) around words not single-quotes (‘).

Note: Unlike the shell form, the exec form does not invoke a command shell. This means that normal
      shell processing does not happen. For example, ENTRYPOINT [ "echo", "$HOME" ] will not do variable
      substitution on $HOME. If you want shell processing then either use the shell form or execute
      a shell directly, for example: ENTRYPOINT [ "sh", "-c", "echo $HOME" ]. When using
      the exec form and executing a shell directly, as in the case for the shell form,
      it is the shell that is doing the environment variable expansion, not docker.





--------------------------------------------------
Shell form ENTRYPOINT example

    https://docs.docker.com/engine/reference/builder/

      注: 使用 Shell form 的 ENTRYPOINT 时, ENTRYPOINT 会 忽略 指令 CMD 和 `docker run` 命令指定的参数

You can specify a plain string for the ENTRYPOINT and it will execute in /bin/sh -c.
This form will use shell processing to substitute shell environment variables,
and will ignore any CMD or docker run command line arguments. To ensure that docker stop
will signal any long running ENTRYPOINT executable correctly, you need to remember to start it with exec:

    FROM ubuntu
    ENTRYPOINT exec top -b

When you run this image, you’ll see the single PID 1 process:

    $ docker run -it --rm --name test top
    Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
    CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
    Load average: 0.08 0.03 0.05 2/98 6
      PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
        1     0 root     R     3164   0%   0% top -b


Which will exit cleanly on docker stop:

    $ /usr/bin/time docker stop test
    test
    real  0m 0.20s
    user  0m 0.02s
    sys 0m 0.04s

If you forget to add exec to the beginning of your ENTRYPOINT:

    FROM ubuntu
    ENTRYPOINT top -b
    CMD --ignored-param1


You can then run it (giving it a name for the next step):

    $ docker run -it --name test top --ignored-param2
    Mem: 1704184K used, 352484K free, 0K shrd, 0K buff, 140621524238337K cached
    CPU:   9% usr   2% sys   0% nic  88% idle   0% io   0% irq   0% sirq
    Load average: 0.01 0.02 0.05 2/101 7
      PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
        1     0 root     S     3168   0%   0% /bin/sh -c top -b cmd cmd2
        7     1 root     R     3164   0%   0% top -b  <----观察, 没有使用 exec 时 其 command 的 pid 不为 1

You can see from the output of top that the specified ENTRYPOINT is not PID 1.

If you then run docker stop test, the container will not exit cleanly -
the stop command will be forced to send a SIGKILL after the timeout:

      $ docker exec -it test ps aux
      PID   USER     COMMAND
          1 root     /bin/sh -c top -b cmd cmd2
          7 root     top -b
          8 root     ps aux
      $ /usr/bin/time docker stop test
      test
      real  0m 10.19s
      user  0m 0.04s
      sys 0m 0.03s





--------------------------------------------------
Understand how CMD and ENTRYPOINT interact

    https://docs.docker.com/engine/reference/builder/


Both CMD and ENTRYPOINT instructions define what command gets executed when running a container.
There are few rules that describe their co-operation.

    1. Dockerfile should specify at least one of CMD or ENTRYPOINT commands.
    // Dockerfile 应该 指定 至少 一个 CMD 或 ENTRYPOINT commands.

    2. ENTRYPOINT should be defined when using the container as an executable.
    // 当将 container 作为 an executable 使用时 应该 定义 ENTRYPOINT.

    3. CMD should be used as a way of defining default arguments for an ENTRYPOINT command or for executing an ad-hoc command in a container.
    // CMD 应该被  用于作为 定义 an ENTRYPOINT command 的 default arguments 或 在容器中 执行 ad-hoc 命令的 的方式

    4. CMD will be overridden when running the container with alternative arguments.
    // 当使用 替代的 arguments 运行 容器时, CMD 将被 覆盖.


The table below shows what command is executed for different ENTRYPOINT / CMD combinations:

--------------------------+---------------------------+--------------------------------+---------------------------------------
                          | No ENTRYPOINT             | ENTRYPOINT exec_entry p1_entry |ENTRYPOINT [“exec_entry”, “p1_entry”]
--------------------------|---------------------------|--------------------------------|---------------------------------------
No CMD                    | error, not allowed        | /bin/sh -c exec_entry p1_entry |exec_entry p1_entry
--------------------------|---------------------------|--------------------------------|---------------------------------------
CMD [“exec_cmd”, “p1_cmd”]| exec_cmd p1_cmd           | /bin/sh -c exec_entry p1_entry |exec_entry p1_entry exec_cmd p1_cmd
--------------------------|---------------------------|--------------------------------|---------------------------------------
CMD [“p1_cmd”, “p2_cmd”]  | p1_cmd p2_cmd             | /bin/sh -c exec_entry p1_entry |exec_entry p1_entry p1_cmd p2_cmd
--------------------------|---------------------------|--------------------------------|---------------------------------------
CMD exec_cmd p1_cmd       |/bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry |exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd
--------------------------+---------------------------+--------------------------------+---------------------------------------


Note: If CMD is defined from the base image, setting ENTRYPOINT will reset CMD to an empty value.
      In this scenario, CMD must be defined in the current image to have a value.
// 注：如果 the base image 中定义了 CMD, 则设置 ENTRYPOINT 将 将 CMD 重置为 一个空值(empty value)
//     在 这种情况下,  在 当前的 image 中 必须定义 CMD 以 使其 拥有 a value.




--------------------------------------------------
VOLUME

      https://docs.docker.com/engine/reference/builder/

VOLUME ["/data"]


The VOLUME instruction creates a mount point with the specified name and marks it as holding
externally mounted volumes from native host or other containers. The value can be a JSON array,
VOLUME ["/var/log/"], or a plain string with multiple arguments, such as VOLUME /var/log or VOLUME /var/log /var/db.
For more information/examples and mounting instructions via the Docker client, refer to Share Directories via Volumes documentation.
// 指令 VOLUME 使用 指定的 name 创建一个  挂载点(mount point), 并将其 标记为 具有 来自
// native host 或 other containers 的 外部挂载卷. 该 value 可以是 a JSON array, VOLUME ["/var/log/"],
// 或普通的 具有 多个 arguments 的 字符串, 如 VOLUME /var/log 或 VOLUME /var/log /var/db.
// 更多 information/examples 和 通过  Docker client 挂载的指令 见 https://docs.docker.com/storage/volumes/



The docker run command initializes the newly created volume with any data that exists at the specified
location within the base image. For example, consider the following Dockerfile snippet:

      FROM ubuntu
      RUN mkdir /myvol
      RUN echo "hello world" > /myvol/greeting
      VOLUME /myvol

This Dockerfile results in an image that causes docker run to create
a new mount point at /myvol and copy the greeting file into the newly created volume.



Notes about specifying volumes

Keep the following things in mind about volumes in the Dockerfile.

  - Volumes on Windows-based containers: When using Windows-based containers, the destination of a volume inside the container must be one of:
        - a non-existing or empty directory
        - a drive other than C:

  - Changing the volume from within the Dockerfile: If any build steps change the data within
    the volume after it has been declared, those changes will be discarded.

  - JSON formatting: The list is parsed as a JSON array. You must enclose words with double quotes (") rather than single quotes (').

  - The host directory is declared at container run-time: The host directory (the mountpoint) is,
    by its nature, host-dependent. This is to preserve image portability, since a given host directory can’t
    be guaranteed to be available on all hosts. For this reason, you can’t mount a host directory
    from within the Dockerfile. The VOLUME instruction does not support specifying a host-dir parameter.
    You must specify the mountpoint when you create or run the container.






--------------------------------------------------
USER

    https://docs.docker.com/engine/reference/builder/

语法: USER <user>[:<group>] or
语法: USER <UID>[:<GID>]

The USER instruction sets the user name (or UID) and optionally the user group (or GID) to use when
running the image and for any RUN, CMD and ENTRYPOINT instructions that follow it in the Dockerfile.
// 指令 USER 设置 user name (或 UID) 和 可选的 user group (或 GID), 其被用于 运行 the image 和
// Dockerfile 中 随后的 任意RUN, CMD 和 ENTRYPOINT 指令.


Warning: When the user doesn’t have a primary group then the image (or the next instructions) will be run with the root group.
// 警告: 当 user 没有 a primary group 时, 该 the image (或 the next instructions) 将以 root group 运行.

On Windows, the user must be created first if it’s not a built-in account. This can be done with the net user command called as part of a Dockerfile.


    FROM microsoft/windowsservercore
    # Create Windows user in the container
    RUN net user /add patrick
    # Set it for subsequent commands
    USER patrick



--------------------------------------------------
WORKDIR

    https://docs.docker.com/engine/reference/builder/

语法: WORKDIR /path/to/workdir


The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that
follow it in the Dockerfile. If the WORKDIR doesn’t exist, it will be created even if it’s not used in any subsequent Dockerfile instruction.
// 指令 WORKDIR 为 Dockerfile 中随后的 指令 RUN, CMD, ENTRYPOINT, COPY and ADD 设置 工作目录(working directory).
// 如果 WORKDIR 不存在, 其将会被创建, 即使 其在 后续的 Dockerfile 指令中没有被使用.


The WORKDIR instruction can be used multiple times in a Dockerfile. If a relative path is provided,
it will be relative to the path of the previous WORKDIR instruction. For example:
// 指令 WORKDIR 在 a Dockerfile 中可以被 多次使用. 如果提供的是 相对路径,
// 则其 是相对于 先前 WORKDIR 指令 的 path, 例如:

        WORKDIR /a
        WORKDIR b
        WORKDIR c
        RUN pwd

The output of the final pwd command in this Dockerfile would be /a/b/c.


The WORKDIR instruction can resolve environment variables previously set using ENV.
You can only use environment variables explicitly set in the Dockerfile. For example:
// 指令 WORKDIR  可以 解析 先前 用 指令 ENV 设置的 环境变量,
// 你仅能 使用在 该 Dockerfile 中 显示设置的 环境变量. 例如:

      ENV DIRPATH /path
      WORKDIR $DIRPATH/$DIRNAME
      RUN pwd

The output of the final pwd command in this Dockerfile would be /path/$DIRNAME






--------------------------------------------------
ARG

    https://docs.docker.com/engine/reference/builder/

语法: ARG <name>[=<default value>]


The ARG instruction defines a variable that users can pass at build-time to the builder
with the docker build command using the --build-arg <varname>=<value> flag.
If a user specifies a build argument that was not defined in the Dockerfile, the build outputs a warning.
// 指令  ARG 定义 一个变量, users 可以 在 build-time 时 使用 `docker build` 命令的 `--build-arg <varname>=<value>`
// 选项 将其 传递给 builder. 如果 user 指定了 在  Dockerfile 中没有被定义的 build argument, 则 the build 会输出 警告:

    [Warning] One or more build-args [foo] were not consumed.

A Dockerfile may include one or more ARG instructions. For example, the following is a valid Dockerfile:
// Dockerfile 可以包含 一个 或 多个 ARG 指令. 例如:

          FROM busybox
          ARG user1
          ARG buildno
          ...

Warning: It is not recommended to use build-time variables for passing secrets like github keys,
         user credentials etc. Build-time variable values are visible to any user of the image with the docker history command.
// 警告: 不建议使用 build-time variables 来传递 保密的 信息(如 github keys, user credentials 等).
//       使用 命令 `docker history`, image 的任意 user  都可以看到 Build-time variable values.




Default values

An ARG instruction can optionally include a default value:
// 一个 ARG 指令 可以 可选择地 包含 一个 默认值:

        FROM busybox
        ARG user1=someuser
        ARG buildno=1
        ...

If an ARG instruction has a default value and if there is no value passed at build-time, the builder uses the default.



Scope

An ARG variable definition comes into effect from the line on which it is defined in the Dockerfile
not from the argument’s use on the command-line or elsewhere. For example, consider this Dockerfile:
// 一个 ARG variable definition 从 Dockerfile 中 其定义所在行 开始 起作用,
// 而非从 在 在 命令行中 使用该 argument 的时候 或 其他地方, 如下:


    1 FROM busybox
    2 USER ${user:-some_user}  <---注: 最终效果为 USER some_user , 因为 第 3 行才 定义 参数 user, 所以参数 user 从第 3 行开始其动作
    3 ARG user
    4 USER $user
    ...


A user builds this file by calling:

    $ docker build --build-arg user=what_user .

The USER at line 2 evaluates to some_user as the user variable is defined on the subsequent line 3.
The USER at line 4 evaluates to what_user as user is defined and the what_user value was passed on
the command line. Prior to its definition by an ARG instruction, any use of a variable results in an empty string.


An ARG instruction goes out of scope at the end of the build stage where it was defined.
To use an arg in multiple stages, each stage must include the ARG instruction.
// An ARG instruction 在 其 所 定义的 build stage 的 end 就 超出了 scope.
// 为了在 多个 stages 中 使用 an arg, 则每个 stage 必须包含 该 ARG instruction.

      FROM busybox
      ARG SETTINGS
      RUN ./run/setup $SETTINGS

      FROM busybox
      ARG SETTINGS
      RUN ./run/other $SETTINGS






Using ARG variables

You can use an ARG or an ENV instruction to specify variables that are available to the RUN instruction.
Environment variables defined using the ENV instruction always override an ARG instruction of the same name.
Consider this Dockerfile with an ENV and ARG instruction.
// 你可以使用 ARG 或 ENV 指令 指定 其 在 指令 RUN 中 可用的 variables.
// 使用 指令 ENV 定义的 环境变量 总是会 覆盖 由 指令 ARG 定义的 相同 name 的 变量.

        1 FROM ubuntu
        2 ARG CONT_IMG_VER
        3 ENV CONT_IMG_VER v1.0.0
        4 RUN echo $CONT_IMG_VER


Then, assume this image is built with this command:

    $ docker build --build-arg CONT_IMG_VER=v2.0.1 .

In this case, the RUN instruction uses v1.0.0 instead of the ARG setting passed by the user:v2.0.1
This behavior is similar to a shell script where a locally scoped variable overrides
the variables passed as arguments or inherited from environment, from its point of definition.


Using the example above but a different ENV specification you can create more useful interactions between ARG and ENV instructions:

        1 FROM ubuntu
        2 ARG CONT_IMG_VER
        3 ENV CONT_IMG_VER ${CONT_IMG_VER:-v1.0.0}
        4 RUN echo $CONT_IMG_VER


Unlike an ARG instruction, ENV values are always persisted in the built image. Consider a docker build without the --build-arg flag:

    $ docker build .


Using this Dockerfile example, CONT_IMG_VER is still persisted in the image but its value
would be v1.0.0 as it is the default set in line 3 by the ENV instruction.

The variable expansion technique in this example allows you to pass arguments from
the command line and persist them in the final image by leveraging the ENV instruction.
Variable expansion is only supported for a limited set of Dockerfile instructions.
      --------------------
      https://docs.docker.com/engine/reference/builder/#environment-replacement

        Environment variables are supported by the following list of instructions in the Dockerfile:

              - ADD
              - COPY
              - ENV
              - EXPOSE
              - FROM
              - LABEL
              - STOPSIGNAL
              - USER
              - VOLUME
              - WORKDIR
        as well as:

              - ONBUILD (when combined with one of the supported instructions above)
        --------------------



Predefined ARGs  (预定义的 ARGs: 使用时无需 对应的 ARG 指令)

Docker has a set of predefined ARG variables that you can use without a corresponding ARG instruction in the Dockerfile.

      - HTTP_PROXY
      - http_proxy
      - HTTPS_PROXY
      - https_proxy
      - FTP_PROXY
      - ftp_proxy
      - NO_PROXY
      - no_proxy


To use these, simply pass them on the command line using the flag:

    --build-arg <varname>=<value>



By default, these pre-defined variables are excluded from the output of docker history.
Excluding them reduces the risk of accidentally leaking sensitive authentication information in an HTTP_PROXY variable.
// 默认, 这些 预定义的 variables 是 被排除在 命令 `docker history` 的输出之外的,
// 排除它们 降低了 意外 泄露 HTTP_PROXY 变量中 敏感的 认证信息的 风险。

For example, consider building the following Dockerfile using --build-arg HTTP_PROXY=http://user:pass@proxy.lon.example.com

      FROM ubuntu
      RUN echo "Hello World"


In this case, the value of the HTTP_PROXY variable is not available in the docker history
and is not cached. If you were to change location, and your proxy server
changed to http://user:pass@proxy.sfo.example.com, a subsequent build does not result in a cache miss.


If you need to override this behaviour then you may do so by adding an ARG statement in the Dockerfile as follows:

    FROM ubuntu
    ARG HTTP_PROXY
    RUN echo "Hello World"

When building this Dockerfile, the HTTP_PROXY is preserved in the docker history, and changing its value invalidates the build cache.






--------------------
Automatic platform ARGs in the global scope

      https://docs.docker.com/engine/reference/builder/


This feature is only available when using the BuildKit backend.
// 该特性 仅在 使用  BuildKit backend 才有效.


Docker predefines a set of ARG variables with information on the platform of the node performing
the build (build platform) and on the platform of the resulting image (target platform).
The target platform can be specified with the --platform flag on docker build.


The following ARG variables are set automatically:

      - TARGETPLATFORM - platform of the build result. Eg linux/amd64, linux/arm/v7, windows/amd64.
      - TARGETOS - OS component of TARGETPLATFORM
      - TARGETARCH - architecture component of TARGETPLATFORM
      - TARGETVARIANT - variant component of TARGETPLATFORM
      - BUILDPLATFORM - platform of the node performing the build.
      - BUILDOS - OS component of BUILDPLATFORM
      - BUILDARCH - architecture component of BUILDPLATFORM
      - BUILDVARIANT - variant component of BUILDPLATFORM


These arguments are defined in the global scope so are not automatically available inside build stages
or for your RUN commands. To expose one of these arguments inside the build stage redefine it without value.
// 这些 arguments 被定义在 global scope 中, 因此不会再 build stages 或 RUN 命令 中 自动可用.
// 为了 导出 这些 其中的 某个变量 到 build stage 中 需要 通过 不加 value 的方式对于 重定义(redefine).


For example:

      FROM alpine
      ARG TARGETPLATFORM  <---注: redefine 全局变量 TARGETPLATFORM 是其被导入到 build stage 中
      RUN echo "I'm building for $TARGETPLATFORM"


Impact on build caching


ARG variables are not persisted into the built image as ENV variables are. However,
ARG variables do impact the build cache in similar ways. If a Dockerfile defines
an ARG variable whose value is different from a previous build, then a “cache miss”
occurs upon its first usage, not its definition. In particular,
all RUN instructions following an ARG instruction use the ARG variable implicitly (as an environment variable),
thus can cause a cache miss. All predefined ARG variables are exempt from caching unless there is a matching ARG statement in the Dockerfile.
// ARG variables 不会 像 ENV variables 那样 被 持久化 到 被构建的 image 中.
// 但是, ARG variables 会以 相似的方式 影响 build cache.
// 如果 Dockerfile 定义了一个 其值 与 先前 build  不同的 的 ARG variable,
// 那么在  其第一次 被使用时 会 发生 a “cache miss”, 而不是再其 definition 时.
// 特别地, 所有的 在 ARG 指令之后的 RUN 指令 都隐式的 使用 ARG variable(类似于 an environment variable)
// 因此 也会 导致 a cache miss.
// All predefined ARG variables are exempt from caching unless there is a matching ARG statement in the Dockerfile.


For example, consider these two Dockerfile:


      1 FROM ubuntu
      2 ARG CONT_IMG_VER
      3 RUN echo $CONT_IMG_VER


      1 FROM ubuntu
      2 ARG CONT_IMG_VER
      3 RUN echo hello


If you specify --build-arg CONT_IMG_VER=<value> on the command line, in both cases, the specification
on line 2 does not cause a cache miss; line 3 does cause a cache miss.ARG CONT_IMG_VER causes
the RUN line to be identified as the same as running CONT_IMG_VER=<value> echo hello,
so if the <value> changes, we get a cache miss.

Consider another example under the same command line:

      1 FROM ubuntu
      2 ARG CONT_IMG_VER
      3 ENV CONT_IMG_VER $CONT_IMG_VER
      4 RUN echo $CONT_IMG_VER


In this example, the cache miss occurs on line 3. The miss happens because the variable’s value
in the ENV references the ARG variable and that variable is changed through the command line.
In this example, the ENV command causes the image to include the value.

If an ENV instruction overrides an ARG instruction of the same name, like this Dockerfile:

      1 FROM ubuntu
      2 ARG CONT_IMG_VER
      3 ENV CONT_IMG_VER hello
      4 RUN echo $CONT_IMG_VER

Line 3 does not cause a cache miss because the value of CONT_IMG_VER is a constant (hello).
As a result, the environment variables and values used on the RUN (line 4) doesn’t change between builds.






--------------------------------------------------
ONBUILD

    https://docs.docker.com/engine/reference/builder/

语法: ONBUILD [INSTRUCTION]

The ONBUILD instruction adds to the image a trigger instruction to be executed at a later time,
when the image is used as the base for another build. The trigger will be executed in the context
of the downstream build, as if it had been inserted immediately after the FROM instruction in the downstream Dockerfile.
// 指令 ONBUILD 向 image 添加 a trigger instruction. 其在 以后的时间被 执行.
// 当 该 image 被 用作 another build 的 base 时. 该 trigger 在 下游构建的 context 中被执行,
// 就像是 其 被 直接 inserted 在 downstream Dockerfile 的 FROM 指令 之后一样.

Any build instruction can be registered as a trigger.
// 任何 构建指令 都能够被 注册为 a trigger.


This is useful if you are building an image which will be used as a base to build other images,
for example an application build environment or a daemon which may be customized with user-specific configuration.


For example, if your image is a reusable Python application builder, it will require
application source code to be added in a particular directory, and it might require
a build script to be called after that. You can’t just call ADD and RUN now,
because you don’t yet have access to the application source code,
and it will be different for each application build. You could simply provide application
developers with a boilerplate Dockerfile to copy-paste into their application,
but that is inefficient, error-prone and difficult to update because it mixes with application-specific code.

The solution is to use ONBUILD to register advance instructions to run later, during the next build stage.

Here’s how it works:
// 工作方式:

    - When it encounters an ONBUILD instruction, the builder adds a trigger to the metadata
      of the image being built. The instruction does not otherwise affect the current build.

    - At the end of the build, a list of all triggers is stored in the image manifest,
      under the key OnBuild. They can be inspected with the docker inspect command.

    - Later the image may be used as a base for a new build, using the FROM instruction.
      As part of processing the FROM instruction, the downstream builder looks for ONBUILD triggers,
      and executes them in the same order they were registered. If any of the triggers fail,
      the FROM instruction is aborted which in turn causes the build to fail. If all triggers succeed,
      the FROM instruction completes and the build continues as usual.

    - Triggers are cleared from the final image after being executed. In other words they are not inherited by “grand-children” builds.
      // Triggers 会从 其 被执行过的 最终的 image 中 清除. 换句话说 就是 它们不会被 继承到 “grand-children” builds 中。


For example you might add something like this:

    [...]
    ONBUILD ADD . /app/src
    ONBUILD RUN /usr/local/bin/python-build --dir /app/src
    [...]

Warning: Chaining ONBUILD instructions using ONBUILD ONBUILD isn’t allowed.
// 警告: ONBUILD ONBUILD 这种 链接 ONBUILD 指令是不被允许的

Warning: The ONBUILD instruction may not trigger FROM or MAINTAINER instructions.










--------------------------------------------------
STOPSIGNAL

  https://docs.docker.com/engine/reference/builder/

语法: STOPSIGNAL signal   <---注: signal 可以是有效的 unsigned number 或 形如 'SIGKILL' 这样的 signal name

The STOPSIGNAL instruction sets the system call signal that will be sent to the container to exit.
This signal can be a valid unsigned number that matches a position in the kernel’s syscall table,
for instance 9, or a signal name in the format SIGNAME, for instance SIGKILL.







--------------------------------------------------
HEALTHCHECK

    https://docs.docker.com/engine/reference/builder/


The HEALTHCHECK instruction has two forms:

语法: HEALTHCHECK [OPTIONS] CMD command (check container health by running a command inside the container)
语法: HEALTHCHECK NONE (disable any healthcheck inherited from the base image)

The HEALTHCHECK instruction tells Docker how to test a container to check that it is still working.
This can detect cases such as a web server that is stuck in an infinite loop and unable
to handle new connections, even though the server process is still running.

When a container has a healthcheck specified, it has a health status in addition to its normal status.
This status is initially 'starting'. Whenever a health check passes,
it becomes 'healthy' (whatever state it was previously in). After a certain number of consecutive failures, it becomes 'unhealthy'.


The options that can appear before CMD are:

        --interval=DURATION (default: 30s)
        --timeout=DURATION (default: 30s)
        --start-period=DURATION (default: 0s)
        --retries=N (default: 3)

The health check will first run interval seconds after the container is started, and then again interval seconds after each previous check completes.

If a single run of the check takes longer than timeout seconds then the check is considered to have failed.

It takes retries consecutive failures of the health check for the container to be considered unhealthy.

start period provides initialization time for containers that need time to bootstrap.
Probe failure during that period will not be counted towards the maximum number of retries.
However, if a health check succeeds during the start period, the container is considered started and
all consecutive failures will be counted towards the maximum number of retries.


There can only be one HEALTHCHECK instruction in a Dockerfile.
If you list more than one then only the last HEALTHCHECK will take effect.
// Dockerfile 中 仅能 有 一个 HEALTHCHECK 指令. 如果出现多个, 则最后一个 HEALTHCHECK 指令将其作用

The command after the CMD keyword can be either a shell command (e.g. HEALTHCHECK CMD /bin/check-running)
or an exec array (as with other Dockerfile commands; see e.g. ENTRYPOINT for details).

The command’s exit status indicates the health status of the container. The possible values are:

    0: success - the container is healthy and ready for use
    1: unhealthy - the container is not working correctly
    2: reserved - do not use this exit code

For example, to check every five minutes or so that a web-server is able to serve the site’s main page within three seconds:

      HEALTHCHECK --interval=5m --timeout=3s \
        CMD curl -f http://localhost/ || exit 1



To help debug failing probes, any output text (UTF-8 encoded) that the command writes on
stdout or stderr will be stored in the health status and can be queried with docker inspect.
Such output should be kept short (only the first 4096 bytes are stored currently).

When the health status of a container changes, a health_status event is generated with the new status.

The HEALTHCHECK feature was added in Docker 1.12.



--------------------------------------------------
SHELL

    https://docs.docker.com/engine/reference/builder/

语法: SHELL ["executable", "parameters"]   <--注: linux 上默认为 ["/bin/sh", "-c"]


The SHELL instruction allows the default shell used for the shell form of commands to be overridden.
The default shell on Linux is ["/bin/sh", "-c"], and on Windows is ["cmd", "/S", "/C"].
The SHELL instruction must be written in JSON form in a Dockerfile.

The SHELL instruction is particularly useful on Windows where there are two commonly used and
quite different native shells: cmd and powershell, as well as alternate shells available including sh.

The SHELL instruction can appear multiple times. Each SHELL instruction overrides
all previous SHELL instructions, and affects all subsequent instructions. For example:
// 指令 SHELL 可以出现 多次. 每个 SHELL 指令 都会 覆盖 先前的 SHELL instructions,
// 并对 所有 后续的指令其作用. 例如:

      FROM microsoft/windowsservercore

      # Executed as cmd /S /C echo default
      RUN echo default

      # Executed as cmd /S /C powershell -command Write-Host default
      RUN powershell -command Write-Host default

      # Executed as powershell -command Write-Host hello
      SHELL ["powershell", "-command"]
      RUN Write-Host hello

      # Executed as cmd /S /C echo hello
      SHELL ["cmd", "/S", "/C"]
      RUN echo hello


The following instructions can be affected by the SHELL instruction when
the shell form of them is used in a Dockerfile: RUN, CMD and ENTRYPOINT.

The following example is a common pattern found on Windows which can be streamlined by using the SHELL instruction:

    ...
    RUN powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
    ...

The command invoked by docker will be:

    cmd /S /C powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"


This is inefficient for two reasons. First, there is an un-necessary cmd.exe command processor (aka shell) being invoked.
Second, each RUN instruction in the shell form requires an extra powershell -command prefixing the command.

To make this more efficient, one of two mechanisms can be employed. One is to use the JSON form of the RUN command such as:

    ...
    RUN ["powershell", "-command", "Execute-MyCmdlet", "-param1 \"c:\\foo.txt\""]
    ...


While the JSON form is unambiguous and does not use the un-necessary cmd.exe, it does require more verbosity
through double-quoting and escaping. The alternate mechanism is to use the SHELL instruction and the shell form,
making a more natural syntax for Windows users, especially when combined with the escape parser directive:

      # escape=`

      FROM microsoft/nanoserver
      SHELL ["powershell","-command"]
      RUN New-Item -ItemType Directory C:\Example
      ADD Execute-MyCmdlet.ps1 c:\example\
      RUN c:\example\Execute-MyCmdlet -sample 'hello world'

The SHELL instruction could also be used to modify the way in which a shell operates. For example,
using SHELL cmd /S /C /V:ON|OFF on Windows, delayed environment variable expansion semantics could be modified.

The SHELL instruction can also be used on Linux should an alternate shell be required such as zsh, csh, tcsh and others.

The SHELL feature was added in Docker 1.12.






--------------------------------------------------
External implementation features

  https://docs.docker.com/engine/reference/builder/

This feature is only available when using the BuildKit backend.

Docker build supports experimental features like cache mounts, build secrets and ssh forwarding
that are enabled by using an external implementation of the builder with a syntax directive.
To learn about these features, refer to the documentation in BuildKit repository.

    https://docs.docker.com/engine/reference/builder/#buildkit
    https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/experimental.md





--------------------------------------------------
Dockerfile examples

    https://docs.docker.com/engine/reference/builder/
    https://docs.docker.com/engine/examples/

Below you can see some examples of Dockerfile syntax. If you’re interested in something more realistic,
take a look at the list of Dockerization examples.

------------------------------
      # Nginx
      #
      # VERSION               0.0.1

      FROM      ubuntu
      LABEL Description="This image is used to start the foobar executable" Vendor="ACME Products" Version="1.0"
      RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server


------------------------------
      # Firefox over VNC
      #
      # VERSION               0.3

      FROM ubuntu

      # Install vnc, xvfb in order to create a 'fake' display and firefox
      RUN apt-get update && apt-get install -y x11vnc xvfb firefox
      RUN mkdir ~/.vnc
      # Setup a password
      RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
      # Autostart firefox (might not be the best way, but it does the trick)
      RUN bash -c 'echo "firefox" >> /.bashrc'

      EXPOSE 5900
      CMD    ["x11vnc", "-forever", "-usepw", "-create"]


------------------------------
      # Multiple images example
      #
      # VERSION               0.1

      FROM ubuntu
      RUN echo foo > bar
      # Will output something like ===> 907ad6c2736f

      FROM ubuntu
      RUN echo moo > oink
      # Will output something like ===> 695d7793cbe4

      # You'll now have two images, 907ad6c2736f with /bar, and 695d7793cbe4 with
      # /oink.




----------------------------------------------------------------------------------------------------
Best practices for writing Dockerfiles  (编写 Dockerfiles 的 最佳实践)


    https://docs.docker.com/develop/develop-images/dockerfile_best-practices/




----------------------------------------------------------------------------------------------------
其他:

--------------------
// 优先使用 `docker container exec` 而非 `docker container attach`, 因为使用 attach 后 exit 会使容器退出, 而使用 exec 是 exit 后容器不会退出
[root@node01 ~]# docker container run -dit --name centos7_c1 centos:7
    2ed270039ffa3a950bf5367e5f6fee164fce7a626bd8417d03c96e9531149bea

[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    2ed270039ffa        centos:7            "/bin/bash"         19 seconds ago      Up 17 seconds                           centos7_c1

[root@node01 ~]# docker container exec -it centos7_c1 bash
[root@2ed270039ffa /]# cat /etc/redhat-release
    CentOS Linux release 7.6.1810 (Core)
[root@2ed270039ffa /]# exit
    exit

[root@node01 ~]# docker container ls
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    2ed270039ffa        centos:7            "/bin/bash"         3 minutes ago       Up 3 minutes                            centos7_c1 <--观察: 处于运行状态

[root@node01 ~]# docker container attach centos7_c1   #注:应优先使用 exec 子命令 而非 attach
[root@2ed270039ffa /]# exit
    exit
[root@node01 ~]# docker container ls -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
    2ed270039ffa        centos:7            "/bin/bash"         5 minutes ago       Exited (0) 4 seconds ago                       centos7_c1 <--观察: 处于退出状态


--------------------
// 导出 和 导入 容器

[root@node01 ~]# man docker-image-import
[root@node01 ~]# man docker-container-export



[root@node01 ~]# docker container export --help  #详细见  man docker-container-export

    Usage:  docker container export [OPTIONS] CONTAINER

    Export a container's filesystem as a tar archive

    Options:
      -o, --output string   Write to a file, instead of STDOUT

[root@node01 ~]# docker image import --help  #详细见 man docker-image-import

    Usage:  docker image import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]

    Import the contents from a tarball to create a filesystem image

    Options:
      -c, --change list      Apply Dockerfile instruction to the created image
      -m, --message string   Set commit message for imported image

[root@node01 ~]# docker container ls -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
    2ed270039ffa        centos:7            "/bin/bash"         14 minutes ago      Exited (0) 9 minutes ago                       centos7_c1


[root@node01 ~]# docker container export centos7_c1 -o /tmp/centos7_c1_export.tar   #导出容器快照

[root@node01 ~]# docker image import /tmp/centos7_c1_export.tar local/centos7_c1_export:v1.0  #将容器快照导入为镜像
    sha256:71fc55196c9e4bac94064208f9cec447a53be643c8a2473145f19937ce60d6b1

[root@node01 ~]# docker image ls local/centos7_c1_export
    REPOSITORY                TAG                 IMAGE ID            CREATED              SIZE
    local/centos7_c1_export   v1.0                71fc55196c9e        About a minute ago   202MB

[root@node01 ~]# docker image history local/centos7_c1_export:v1.0
    IMAGE               CREATED             CREATED BY          SIZE                COMMENT
    71fc55196c9e        2 minutes ago                           202MB               Imported from -


[root@node01 ~]# docker container export centos7_c1 | gzip > /tmp/centos7_c1_export.tar.gz

[root@node01 ~]# docker image import /tmp/centos7_c1_export.tar.gz local/centos7_c1_export:v2.0
    sha256:2e92070858bf4c2a1c36835cccf122080f3b31b53ff679052ea87b7132041aeb

[root@node01 ~]# docker image ls local/centos7_c1_export
    REPOSITORY                TAG                 IMAGE ID            CREATED              SIZE
    local/centos7_c1_export   v2.0                2e92070858bf        About a minute ago   202MB <---
    local/centos7_c1_export   v1.0                71fc55196c9e        About an hour ago    202MB




----------------------------------------------------------------------------------------------------
// 保存 和 加载 镜像  (注: 使用此方式前, 应考虑 是否应该 使用 registry 的方式)

[root@node01 ~]# docker image save --help

    Usage:  docker image save [OPTIONS] IMAGE [IMAGE...]

    Save one or more images to a tar archive (streamed to STDOUT by default)

    Options:
      -o, --output string   Write to a file, instead of STDOUT


[root@node01 ~]# docker image load --help

    Usage:  docker image load [OPTIONS]

    Load an image from a tar archive or STDIN

    Options:
      -i, --input string   Read from tar archive file, instead of STDIN
      -q, --quiet          Suppress the load output



[root@node01 ~]# docker image ls centos
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    centos              7                   67fa590cfc1c        2 months ago        202MB

[root@node01 ~]# docker image save centos:7 -o /tmp/centos_7_save.tar


[root@node01 ~]# docker image rm centos:7
[root@node01 ~]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE


[root@node01 ~]# docker image load -i /tmp/centos_7_save.tar
    877b494a9f30: Loading layer [==================================================>]  209.6MB/209.6MB
    Loaded image: centos:7

[root@node01 ~]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    centos              7                   67fa590cfc1c        2 months ago        202MB
[root@node01 ~]# docker image history centos:7
    IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
    67fa590cfc1c        2 months ago        /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
    <missing>           2 months ago        /bin/sh -c #(nop)  LABEL org.label-schema.sc…   0B
    <missing>           2 months ago        /bin/sh -c #(nop) ADD file:4e7247c06de9ad117…   202MB



[root@node01 ~]# docker image save centos:7 | gzip > /tmp/centos_7_save.tar.gz

[root@node01 ~]# docker image rm centos:7

[root@node01 ~]# docker image load -i /tmp/centos_7_save.tar.gz
    877b494a9f30: Loading layer [==================================================>]  209.6MB/209.6MB
    Loaded image: centos:7

[root@node01 ~]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    centos              7                   67fa590cfc1c        2 months ago        202MB


----------------------------------------------------------------------------------------------------
// 查看容器日志

[root@node01 ~]# docker container run -d --name c1 centos:7 bash -c 'for i in {1..100}; do echo $i; sleep 2; done'
    2a159b3affa4311a6696e1b7049e2f59ef682e6a34d46fda8b93648d728d8fc9


[root@node01 ~]# docker container logs -f c1   #获取查看 容器日志
1
2
3
4


----------------------------------------------------------------------------------------------------
Build your own bridge  (创建自定义网桥)



https://docs.docker.com/v17.09/engine/userguide/networking/default_network/build-bridges/
https://developer.ibm.com/recipes/tutorials/bridge-the-docker-containers-to-external-network/
https://unix.stackexchange.com/questions/255484/how-can-i-bridge-two-interfaces-with-ip-iproute2
https://www.baturin.org/docs/iproute2/#Overview%20of%20iproute2
https://www.lartc.org/howto/index.html
https://wiki.linuxfoundation.org/networking/iproute2

https://www.golinuxcloud.com/how-to-configure-network-bridge-nmtui-linux/
https://www.linuxsysadmins.com/how-to-create-a-linux-network-bridge/



[root@node01 ~]# yum -y install bridge-utils

[root@node01 ~]# ip link add name bridge0 type bridge
[root@node01 ~]# ip addr add 192.168.5.1/24 dev bridge0
[root@node01 ~]# ip link set dev bridge0 up

          --------------------------------------------------
          // 如果 要持久化 设置可采用如下方式
          [root@node01 ~]# vim /etc/sysconfig/network-scripts/ifcfg-bridge0
                DEVICE=bridge0
                NAME=bridge0
                ONBOOT=yes
                BOOTPROTO=none
                NM_CONTROLLED="no"
                STP=no
                TYPE=Bridge
                IPADDR=192.168.5.1
                PREFIX=24
          --------------------------------------------------


[root@node01 ~]# ip addr show bridge0
6: bridge0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 5e:42:be:9e:b3:7a brd ff:ff:ff:ff:ff:ff
    inet 192.168.5.1/24 scope global bridge0
       valid_lft forever preferred_lft forever
    inet6 fe80::5c42:beff:fe9e:b37a/64 scope link
       valid_lft forever preferred_lft forever


// 配置 docker 默认桥接到 "bridge0" 上
[root@node01 ~]# vim /etc/docker/daemon.json

    {
      "bridge": "bridge0"
    }

// 重启 是 配置修改生效
[root@node01 ~]# systemctl restart docker.service

[root@node01 ~]# iptables -t nat -L -n

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
    MASQUERADE  all  --  192.168.5.0/24       0.0.0.0/0           <----观察

    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  0.0.0.0/0            0.0.0.0/0


[root@node01 ~]# docker container run --rm -dit --name c1 centos:7
    36317afa164c9a468aa8b284b9adcacc1709956819b6bcf58303b260035416cd

[root@node01 ~]# docker container exec -it c1 bash
      [root@36317afa164c /]# yum -y install net-tools

      [root@36317afa164c /]# ifconfig
          eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
                  inet 192.168.5.2  netmask 255.255.255.0  broadcast 192.168.5.255
                  ether 02:42:c0:a8:05:02  txqueuelen 0  (Ethernet)
                  RX packets 1788  bytes 10043348 (9.5 MiB)
                  RX errors 0  dropped 0  overruns 0  frame 0
                  TX packets 1670  bytes 94455 (92.2 KiB)
                  TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

          lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
                  inet 127.0.0.1  netmask 255.0.0.0
                  loop  txqueuelen 1  (Local Loopback)
                  RX packets 0  bytes 0 (0.0 B)
                  RX errors 0  dropped 0  overruns 0  frame 0
                  TX packets 0  bytes 0 (0.0 B)
                  TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

      [root@36317afa164c /]# route  -n
          Kernel IP routing table
          Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
          0.0.0.0         192.168.5.1     0.0.0.0         UG    0      0        0 eth0
          192.168.5.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0

      [root@36317afa164c /]# ping www.baidu.com
      PING www.a.shifen.com (183.232.231.174) 56(84) bytes of data.
      64 bytes from 183.232.231.174 (183.232.231.174): icmp_seq=1 ttl=127 time=41.9 ms
      64 bytes from 183.232.231.174 (183.232.231.174): icmp_seq=2 ttl=127 time=50.4 ms




----------------------------------------------------------------------------------------------------







































