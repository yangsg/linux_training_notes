

https://docs.docker.com/

https://hub.docker.com/


docker 国内加速地址
  https://www.jianshu.com/p/b5006ebf1522


docker 架构:
  https://docs.docker.com/engine/docker-overview/#docker-architecture



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



























