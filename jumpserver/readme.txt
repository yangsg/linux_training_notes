

官网: http://www.jumpserver.org
在线体验: https://demo.jumpserver.org/auth/login/
文档: https://jumpserver.readthedocs.io/zh/master/

------------------------------------------------------------------------------------------
1.4.8 版本:
    https://docs.jumpserver.org/zh/1.4.8/setup_by_centos7.html
    https://docs.jumpserver.org/zh/1.4.8/setup_by_prod.html#id2

组件说明
    - Jumpserver 为管理后台, 管理员可以通过 Web 页面进行资产管理、用户管理、资产授权等操作, 用户可以通过 Web 页面进行资产登录, 文件管理等操作
    - Coco 为 SSH Server 和 Web Terminal Server 。用户可以使用自己的账户通过 SSH 或者 Web Terminal 访问 SSH 协议和 Telnet 协议资产
    - Luna 为 Web Terminal Server 前端页面, 用户使用 Web Terminal 方式登录所需要的组件
    - Guacamole 为 RDP 协议和 VNC 协议资产组件, 用户可以通过 Web Terminal 来连接 RDP 协议和 VNC 协议资产 (暂时只能通过 Web Terminal 来访问)

端口说明
    - Jumpserver 默认端口为 8080/tcp 配置文件 jumpserver/config.yml
    - Coco 默认 SSH 端口为 2222/tcp, 默认 Web Terminal 端口为 5000/tcp 配置文件在 coco/config.yml
    - Guacamole 默认端口为 8081/tcp, 配置文件 /config/tomcat8/conf/server.xml
    - Nginx 默认端口为 80/tcp
    - Redis 默认端口为 6379/tcp
    - Mysql 默认端口为 3306/tcp


------------------------------------------------------------------------------------------
1.5.3版本:

组件说明: https://jumpserver.readthedocs.io/zh/master/setup_by_prod.html#id3

    - Jumpserver 为管理后台, 管理员可以通过 Web 页面进行资产管理、用户管理、资产授权等操作, 用户可以通过 Web 页面进行资产登录, 文件管理等操作
    - koko 为 SSH Server 和 Web Terminal Server 。用户可以使用自己的账户通过 SSH 或者 Web Terminal 访问 SSH 协议和 Telnet 协议资产
    - Luna 为 Web Terminal Server 前端页面, 用户使用 Web Terminal 方式登录所需要的组件
    - Guacamole 为 RDP 协议和 VNC 协议资产组件, 用户可以通过 Web Terminal 来连接 RDP 协议和 VNC 协议资产 (暂时只能通过 Web Terminal 来访问)

端口说明: https://jumpserver.readthedocs.io/zh/master/setup_by_prod.html#id4

    - Jumpserver 默认 Web 端口为 8080/tcp, 默认 WS 端口为 8070/tcp, 配置文件 jumpserver/config.yml
    - koko 默认 SSH 端口为 2222/tcp, 默认 Web Terminal 端口为 5000/tcp 配置文件在 koko/config.yml
    - Guacamole 默认端口为 8081/tcp, 配置文件 /config/tomcat9/conf/server.xml
    - Nginx 默认端口为 80/tcp
    - Redis 默认端口为 6379/tcp
    - Mysql 默认端口为 3306/tcp

------------------------------------------------------------------------------------------


Docs » 安装文档 » 一站式、分布式安装文档 » CentOS 7 安装文档
      https://jumpserver.readthedocs.io/zh/master/setup_by_centos7.html


生产环境建议使用 1.4.8 版本

Jumpserver 环境要求：

硬件配置: 2个CPU核心, 4G 内存, 50G 硬盘（最低）
操作系统: Linux 发行版 x86_64
Python = 3.6.x
Mysql Server ≥ 5.6
Mariadb Server ≥ 5.5.56
Redis




----------------------------------------------------------------------------------------------------
// 安装 epel 源(我的试验环境已有 epel 源, 此处略过)
[root@jump_server ~]# yum -y install epel-release


安装 python3.6 解释器
[root@jump_server ~]# yum -y install wget sqlite-devel xz gcc automake zlib-devel openssl-devel git

[root@jump_server download]# tar -xvf Python-3.6.8.tgz
[root@jump_server download]# cd Python-3.6.8/
[root@jump_server Python-3.6.8]# ./configure
[root@jump_server Python-3.6.8]# make
[root@jump_server Python-3.6.8]# make install

[root@jump_server Python-3.6.8]# python3.6 -V
    Python 3.6.8


// 安装 Redis, Jumpserver 使用 Redis 做 cache 和 celery broke
[root@jump_server ~]# yum -y install redis
[root@jump_server ~]# rpm -q redis
    redis-3.2.12-2.el7.x86_64


[root@jump_server ~]# systemctl start redis
[root@jump_server ~]# systemctl enable redis
      Created symlink from /etc/systemd/system/multi-user.target.wants/redis.service to /usr/lib/systemd/system/redis.service.

[root@jump_server ~]# systemctl status redis
    ● redis.service - Redis persistent key-value database
       Loaded: loaded (/usr/lib/systemd/system/redis.service; enabled; vendor preset: disabled)
      Drop-In: /etc/systemd/system/redis.service.d
               └─limit.conf
       Active: active (running) since Sat 2019-10-12 10:21:54 CST; 11s ago
     Main PID: 15553 (redis-server)
       CGroup: /system.slice/redis.service
               └─15553 /usr/bin/redis-server 127.0.0.1:6379

    Oct 12 10:21:54 jump_server systemd[1]: Starting Redis persistent key-value database...
    Oct 12 10:21:54 jump_server systemd[1]: Started Redis persistent key-value database.



// 注: 如下 使用 curl 下载的 mariadb 的官方仓库 实在是太慢了, 所以改为使用国内的 mariadb 镜像仓库
//    [root@jump_server ~]# curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
// 参考:
//    https://lug.ustc.edu.cn/wiki/mirrors/help/mariadb
//    https://downloads.mariadb.org/mariadb/repositories/#distro=CentOS&distro_release=centos7-amd64--centos7&mirror=guzel&version=10.4
[root@jump_server ~]# vim /etc/yum.repos.d/mariadb.repo

    # MariaDB 10.4 CentOS repository list - created 2019-10-12 02:33 UTC
    # http://downloads.mariadb.org/mariadb/repositories/
    [mariadb]
    name = MariaDB
    baseurl = https://mirrors.ustc.edu.cn/mariadb/yum/10.4/centos7-amd64
    gpgkey=https://mirrors.ustc.edu.cn/mariadb/yum/RPM-GPG-KEY-MariaDB
    gpgcheck=1



[root@jump_server ~]# yum -y install  MariaDB-client MariaDB-server MariaDB-devel MariaDB-shared
[root@jump_server ~]# rpm -q  MariaDB-client MariaDB-server MariaDB-devel MariaDB-shared
    MariaDB-client-10.4.8-1.el7.centos.x86_64
    MariaDB-server-10.4.8-1.el7.centos.x86_64
    MariaDB-devel-10.4.8-1.el7.centos.x86_64
    MariaDB-shared-10.4.8-1.el7.centos.x86_64



// 将 mysql 字符集设置为 utf8mb4 (即真正意义上的 utf8)
// https://blog.csdn.net/zhnxin_163/article/details/82879586
// https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/006-mha4mysql-semi-sync-gtid-utf8mb4-rpm
[root@jump_server ~]# vim /etc/my.cnf

    [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
    loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

    [mysql]
    default-character-set = utf8mb4

    [mysqlbinlog]
    set_charset=utf8mb4

    [mysqld]
    # 设置 mysql 字符集为 utf8mb4
    character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
    character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
    collation-server = utf8mb4_unicode_ci

    innodb_large_prefix=ON
    innodb_file_format=barracuda
    innodb_file_per_table=ON
    innodb_default_row_format='dynamic'


[root@jump_server ~]# systemctl start mariadb
[root@jump_server ~]# systemctl enable mariadb

[root@jump_server ~]# systemctl status mariadb
    ● mariadb.service - MariaDB 10.4.8 database server
       Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
      Drop-In: /etc/systemd/system/mariadb.service.d
               └─migrated-from-my.cnf-settings.conf
       Active: active (running) since Sat 2019-10-12 10:50:52 CST; 14s ago
         Docs: man:mysqld(8)
               https://mariadb.com/kb/en/library/systemd/
     Main PID: 16080 (mysqld)
       Status: "Taking your SQL requests now..."
       CGroup: /system.slice/mariadb.service
               └─16080 /usr/sbin/mysqld

    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] InnoDB: 10.4.8 started; log sequence number 139827; transaction id 21
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] InnoDB: Loading buffer pool(s) from /var/lib/mysql/ib_buffer_pool
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] InnoDB: Buffer pool(s) load completed at 191012 10:50:52
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] Plugin 'FEEDBACK' is disabled.
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] Server socket created on IP: '::'.
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] Reading of all Master_info entries succeeded
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] Added new Master_info '' to hash table
    Oct 12 10:50:52 jump_server mysqld[16080]: 2019-10-12 10:50:52 0 [Note] /usr/sbin/mysqld: ready for connections.
    Oct 12 10:50:52 jump_server mysqld[16080]: Version: '10.4.8-MariaDB'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MariaDB Server
    Oct 12 10:50:52 jump_server systemd[1]: Started MariaDB 10.4.8 database server.



[root@jump_server ~]# mysql_secure_installation

    Enter current password for root (enter for none):   <=========直接按 enter 键

    Switch to unix_socket authentication [Y/n] y  <======键入y

    Change the root password? [Y/n] y  <=====键入 y
    New password:    <========键入 root 的新密码, 此处我使用简单密码 'redhat'
    Re-enter new password:  <========重复键入 root 的新密码


[root@jump_server ~]# mysql -u root -p
    Enter password:

    // 查看字符集信息
    MariaDB [(none)]> SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';
    +--------------------------+----------------------------+
    | Variable_name            | Value                      |
    +--------------------------+----------------------------+
    | character_set_client     | utf8mb4                    |
    | character_set_connection | utf8mb4                    |
    | character_set_database   | utf8mb4                    |
    | character_set_filesystem | binary                     |
    | character_set_results    | utf8mb4                    |
    | character_set_server     | utf8mb4                    |
    | character_set_system     | utf8                       |
    | character_sets_dir       | /usr/share/mysql/charsets/ |
    | collation_connection     | utf8mb4_unicode_ci         |
    | collation_database       | utf8mb4_unicode_ci         |
    | collation_server         | utf8mb4_unicode_ci         |
    +--------------------------+----------------------------+


   变量 character_set_system : The character set used by the server for storing identifiers. The value is always utf8.

    // 创建数据库 Jumpserver 并授权
    MariaDB [(none)]> create database jumpserver charset utf8mb4;
    MariaDB [(none)]> grant all on jumpserver.* to 'jumpserver'@'127.0.0.1' identified by 'redhat';
    MariaDB [(none)]> flush privileges;


// 安装 Nginx, 用作代理服务器整合 Jumpserver 与各个组件
[root@jump_server ~]# yum -y install nginx
[root@jump_server ~]# rpm -q nginx
    nginx-1.12.2-3.el7.x86_64




// 创建 py3 虚拟环境
[root@jump_server ~]# python3.6 -m venv /opt/py3


// 载入 py3 虚拟环境
// 注: 每次操作 jumpserver 都需要使用下面的命令载入 py3 虚拟环境
[root@jump_server ~]# source /opt/py3/bin/activate
(py3) [root@jump_server ~]#

// 获取 jumpserver 代码 (因为官网推荐 "生产环境建议使用 1.4.8 版本", 且我的学习环境网速太慢,所以这里仅 clone 版本 1.4.8 的 jumpserver)
(py3) [root@jump_server ~]# cd /opt
(py3) [root@jump_server opt]# git clone --depth=1 --branch 1.4.8  https://github.com/jumpserver/jumpserver.git
(py3) [root@jump_server opt]# cd jumpserver/
(py3) [root@jump_server jumpserver]# git checkout -b version_1.4.8
          Switched to a new branch 'version_1.4.8'

// 观察一下现在的 本地仓库 信息
(py3) [root@jump_server jumpserver]# git branch
        * version_1.4.8
(py3) [root@jump_server jumpserver]# git describe --tags
        1.4.8
(py3) [root@jump_server jumpserver]# git log
          commit 232674b1c1e4d4609227d8f761108d0e8bcbbd1a
          Author: 老广 <ibuler@qq.com>
          Date:   Fri Feb 22 17:10:05 2019 +0800

              Merge pull request #2423 from jumpserver/dev

              Dev


    git clone 指定 branch 或 tag 的相关资料:
        https://stackoverflow.com/questions/3489173/how-to-clone-git-repository-with-specific-revision-changeset
        https://stackoverflow.com/questions/45241502/how-to-git-clone-a-specific-release



// 安装依赖
(py3) [root@jump_server jumpserver]# cd /opt/jumpserver/requirements
(py3) [root@jump_server requirements]# ls
          alpine_requirements.txt  deb_requirements.txt  issues.txt  mac_requirements.txt  requirements.txt  rpm_requirements.txt


// 安装依赖 RPM 包
(py3) [root@jump_server requirements]# yum install -y $(cat rpm_requirements.txt)

// 设置国内 pip 镜像源
// 参考:
//    https://blog.csdn.net/dss875914213/article/details/86500146
//    https://opsx.alibaba.com/mirror
//    https://pip.pypa.io/en/stable/user_guide/
//    https://www.cnblogs.com/zhzhlong/p/11445667.html
//    https://wiki.python.org/moin/PyPISimple
//    https://www.cnblogs.com/zzhaolei/p/11063255.html

(py3) [root@jump_server requirements]# mkdir ~/.pip
(py3) [root@jump_server requirements]# vim ~/.pip/pip.conf

              [global]
              index-url = https://mirrors.aliyun.com/pypi/simple

              [install]
              trusted-host = mirrors.aliyun.com



// 安装 依赖的 python modules 之前先升级一下 pip 和 setuptools 工具
(py3) [root@jump_server requirements]# pip install --upgrade pip setuptools


// 安装 依赖的 python modules
(py3) [root@jump_server requirements]# pip install -r requirements.txt


----------------------------------------
// 当如上的命令 进行到 安装 python-gssapi-0.6.4 时 出现如下错误(网络不可达):
//     注: 实际试验时发现, 在 较快速的网络环境中做试验时, 没有出现 Network is unreachable 的问题

    distutils.errors.DistutilsError: Download error for https://files.pythonhosted.org/packages/5f/bf/6aa1925384c23ffeb579e97a5569eb9abce41b6310b329352b8252cee1c3/cffi-1.12.3-cp36-cp36m-manylinux1_x86_64.whl#sha256=59b4dc008f98fc6ee2bb4fd7fc786a8d70000d058c2bbe2698275bc53a8d3fa7: [Errno 101] Network is unreachable

// 解决办法 一: 手动下载 python-gssapi-0.6.4.tar.gz 并在 本地执行安装
//   https://stackoverflow.com/questions/36014334/how-to-install-python-packages-from-the-tar-gz-file-without-using-pip-install
//   https://stackoverflow.com/questions/43419975/installing-downloaded-tar-gz-files-with-pip?noredirect=1
//   https://pypi.org/project/python-gssapi/
//   https://github.com/sigmaris/python-gssapi/releases
//   https://github.com/pythongssapi/python-gssapi

(py3) [root@jump_server requirements]# wget -O /root/download/python-gssapi-0.6.4.tar.gz  https://github.com/sigmaris/python-gssapi/archive/0.6.4.tar.gz

(py3) [root@jump_server requirements]# pip install /root/download/python-gssapi-0.6.4.tar.gz     #注: 如果中间有失败, 可以多尝试几次


// 解决办法 二: 直接单独安装执行 pip 命令安装 python-gssapi==0.6.4, 该方式有时要卡很长一会儿才能成功
(py3) [root@jump_server requirements]# pip install python-gssapi==0.6.4


----------------------------------------
// 当如上的命令 进行到 安装 python-gssapi-0.6.4 时 出现如下错误(网络不可达):

// 解决了如上问题后, 重新执行 如下命令 继续安装相关  依赖的 python 模块
(py3) [root@jump_server requirements]# pip install -r requirements.txt

----------------------------------------

(py3) [root@jump_server requirements]# cd /opt/jumpserver
(py3) [root@jump_server jumpserver]# vim apps/jumpserver/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE),
            'NAME': CONFIG.DB_NAME,
            'HOST': CONFIG.DB_HOST,
            'PORT': CONFIG.DB_PORT,
            'USER': CONFIG.DB_USER,
            'PASSWORD': CONFIG.DB_PASSWORD,
            'ATOMIC_REQUESTS': True,
            # 添加 与 utf8mb4 相关的设置
            'OPTIONS': {
                'use_unicode': True,
                'charset': 'utf8mb4',
            }
        }
    }




// 修改配置文件
(py3) [root@jump_server jumpserver]# cp config_example.yml config.yml


(py3) [root@jump_server jumpserver]# vim config.yml
    # SECURITY WARNING: keep the secret key used in production secret!
    # 加密秘钥 生产环境中请修改为随机字符串，请勿外泄, 可使用命令生成
    # 注: 生成随机SECRET_KEY 的命令: `cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 50`
    SECRET_KEY: kDfhgOq0LXoN9waJewc8BHl2GGFc1rK2t8ygJwVaBNelelMPtP

    # SECURITY WARNING: keep the bootstrap token used in production secret!
    # 预共享Token coco和guacamole用来注册服务账号，不在使用原来的注册接受机制
    # 注: 生成 生成随机BOOTSTRAP_TOKEN 的命令:`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 16`
    BOOTSTRAP_TOKEN: dMyXJCBLKpayNUbb

    # Development env open this, when error occur display the full process track, Production disable it
    # DEBUG 模式 开启DEBUG后遇到错误时可以看到更多日志
    DEBUG: false

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    # 日志级别
    LOG_LEVEL: ERROR
    # LOG_DIR:

    # Session expiration setting, Default 24 hour, Also set expired on on browser close
    # 浏览器Session过期时间，默认24小时, 也可以设置浏览器关闭则过期
    # SESSION_COOKIE_AGE: 86400
    SESSION_EXPIRE_AT_BROWSER_CLOSE: true


    # MySQL or postgres setting like
    # 使用Mysql作为数据库
    DB_ENGINE: mysql
    DB_HOST: 127.0.0.1
    DB_PORT: 3306
    DB_USER: jumpserver
    DB_PASSWORD: redhat
    DB_NAME: jumpserver



    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # 运行时绑定端口
    HTTP_BIND_HOST: 0.0.0.0
    HTTP_LISTEN_PORT: 8080

    # Use Redis as broker for celery and web socket
    # Redis配置
    REDIS_HOST: 127.0.0.1
    REDIS_PORT: 6379
    # REDIS_PASSWORD:
    REDIS_DB_CELERY: 3
    REDIS_DB_CACHE: 4



// 运行 Jumpserver
// 新版本更新了运行脚本, 使用方式./jms start|stop|status all  后台运行请添加 -d 参数
(py3) [root@jump_server jumpserver]# ./jms start -d  # 后台运行使用 -d 参数./jms start -d

      Sat Oct 12 11:22:09 2019
      Jumpserver version 1.4.8, more see https://www.jumpserver.org

      - Start Gunicorn WSGI HTTP Server
      Check database connection ...


// 下载 jumpserver 的 systemd 的 service unit 文件
(py3) [root@jump_server jumpserver]# wget -O /usr/lib/systemd/system/jms.service https://demo.jumpserver.org/download/shell/centos/jms.service

// 观察一下是否适合当前环境
(py3) [root@jump_server jumpserver]# cat /usr/lib/systemd/system/jms.service

    [Unit]
    Description=jms
    After=network.target mariadb.service redis.service docker.service
    Wants=mariadb.service redis.service docker.service

    [Service]
    Type=forking
    TimeoutStartSec=0
    WorkingDirectory=/opt/jumpserver
    Environment="PATH=/opt/py3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
    ExecStart=/opt/jumpserver/jms start all -d
    ExecReload=
    ExecStop=/opt/jumpserver/jms stop

    [Install]
    WantedBy=multi-user.target


(py3) [root@jump_server jumpserver]# chmod 755 /usr/lib/systemd/system/jms.service

// 配置为开机自启
(py3) [root@jump_server jumpserver]# systemctl enable jms
    Created symlink from /etc/systemd/system/multi-user.target.wants/jms.service to /usr/lib/systemd/system/jms.service.








// 使用 chrome 浏览器访问一下 http://192.168.175.100:8080
// 浏览器会自动 重定向到 jumpserver 的登录页面, 但页面有点丑陋, 因为很多 css 和 js 文件没有被成功 loaded.
// 此时, 先简单配置一下 nginx 以解决 css 和 js 等资源文件的加载问题:
[root@jump_server ~]# vim /etc/nginx/conf.d/jumpserver.conf

      server {
          listen 80;

          location /static/ {
              root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
          }
          location / {
              proxy_pass http://localhost:8080;  # 如果jumpserver安装在别的服务器，请填写它的ip
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header Host $host;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
      }

[root@jump_server ~]# vim /etc/nginx/nginx.conf    # 注释掉如下内容

    ##    server {
    ##        listen       80 default_server;
    ##        listen       [::]:80 default_server;
    ##        server_name  _;
    ##        root         /usr/share/nginx/html;
    ##
    ##        # Load configuration files for the default server block.
    ##        include /etc/nginx/default.d/*.conf;
    ##
    ##        location / {
    ##        }
    ##
    ##        error_page 404 /404.html;
    ##            location = /40x.html {
    ##        }
    ##
    ##        error_page 500 502 503 504 /50x.html;
    ##            location = /50x.html {
    ##        }
    ##    }


[root@jump_server ~]# systemctl start nginx
[root@jump_server ~]# systemctl enable nginx
    Created symlink from /etc/systemd/system/multi-user.target.wants/nginx.service to /usr/lib/systemd/system/nginx.service.

[root@jump_server ~]# systemctl status nginx
    ● nginx.service - The nginx HTTP and reverse proxy server
       Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
       Active: active (running) since Sat 2019-10-12 11:40:50 CST; 34s ago
     Main PID: 54176 (nginx)
       CGroup: /system.slice/nginx.service
               ├─54176 nginx: master process /usr/sbin/nginx
               └─54177 nginx: worker process

    Oct 12 11:40:50 jump_server systemd[1]: Starting The nginx HTTP and reverse proxy server...
    Oct 12 11:40:50 jump_server nginx[54170]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    Oct 12 11:40:50 jump_server nginx[54170]: nginx: configuration file /etc/nginx/nginx.conf test is successful
    Oct 12 11:40:50 jump_server systemd[1]: Failed to read PID from file /run/nginx.pid: Invalid argument
    Oct 12 11:40:50 jump_server systemd[1]: Started The nginx HTTP and reverse proxy server.


此时在用 chrome 浏览器访问一下 http://192.168.175.100 地址(即通过 nginx 来访问 jumpserver服务),
可以发现, 此时的 jumpserver 的登录界面 美观了不少.

此时可以 输入默认的登录信息进去看一下:
    default username: admin
    default password: admin






----------------------------------------------------------------------------------------------------
// 安装 docker 部署 koko 与 guacamole
[root@jump_server ~]# yum install -y yum-utils device-mapper-persistent-data lvm2
[root@jump_server ~]# yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
[root@jump_server ~]# yum makecache fast
[root@jump_server ~]# rpm --import https://mirrors.aliyun.com/docker-ce/linux/centos/gpg

[root@jump_server ~]# yum -y install docker-ce
[root@jump_server ~]# systemctl enable docker
    Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.

[root@jump_server ~]# curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://f1361db2.m.daocloud.io
[root@jump_server ~]# systemctl restart docker

// http://<Jumpserver_url> 指向 jumpserver 的服务端口, 如 http://192.168.175.100:8080
// BOOTSTRAP_TOKEN 为 Jumpserver/config.yml 里面的 BOOTSTRAP_TOKEN
// 警告: 这里 BOOTSTRAP_TOKEN 本来应该保密, 所以不应该这么指定, 但这里我就暂时偷懒了, 注意生产环境中不要这么干
[root@jump_server ~]# docker run --name jms_coco -d -p 2222:2222 -p 5000:5000 \
                             -e CORE_HOST=http://192.168.175.100:8080 \
                             -e BOOTSTRAP_TOKEN='kDfhgOq0LXoN9waJewc8BHl2GGFc1rK2t8ygJwVaBNelelMPtP' \
                             jumpserver/jms_coco:1.4.8


// 警告: 这里 BOOTSTRAP_TOKEN 本来应该保密, 所以不应该这么指定, 但这里我就暂时偷懒了, 注意生产环境中不要这么干
[root@jump_server ~]# docker run --name jms_guacamole -d -p 8081:8081 \
                             -e CORE_HOST=http://192.168.175.100:8080 \
                             -e BOOTSTRAP_TOKEN='kDfhgOq0LXoN9waJewc8BHl2GGFc1rK2t8ygJwVaBNelelMPtP' \
                             jumpserver/jms_guacamole:1.4.8


// 安装 Web Terminal 前端: Luna  需要 Nginx 来运行访问 访问(https://github.com/jumpserver/luna/releases)下载对应版本的 release 包, 直接解压, 不需要编译
[root@jump_server ~]# cd /opt
[root@jump_server opt]# wget https://github.com/jumpserver/luna/releases/download/1.4.8/luna.tar.gz

[root@jump_server opt]# tar -xvf luna.tar.gz
[root@jump_server opt]# chown -R root:root luna


[root@jump_server ~]# vim /etc/nginx/conf.d/jumpserver.conf

        server {
            listen 80;

            client_max_body_size 100m;  # 录像及文件上传大小限制

            location /luna/ {
                try_files $uri / /index.html;
                alias /opt/luna/;  # luna 路径, 如果修改安装目录, 此处需要修改
            }

            location /media/ {
                add_header Content-Encoding gzip;
                root /opt/jumpserver/data/;  # 录像位置, 如果修改安装目录, 此处需要修改
            }

            location /static/ {
                root /opt/jumpserver/data/;  # 静态资源, 如果修改安装目录, 此处需要修改
            }

            location /socket.io/ {
                proxy_pass       http://localhost:5000/socket.io/;
                proxy_buffering off;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                access_log off;
            }

            location /coco/ {
                proxy_pass       http://localhost:5000/coco/;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                access_log off;
            }

            location /guacamole/ {
                proxy_pass       http://localhost:8081/;
                proxy_buffering off;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection $http_connection;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                access_log off;
            }

            location / {
                proxy_pass http://localhost:8080;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
        }


[root@jump_server ~]# systemctl reload nginx






----------------------------------------------------------------------------------------------------


https://stackoverflow.com/questions/35847015/mysql-change-innodb-large-prefix
http://www.voidcn.com/article/p-uoferwcl-bwa.html
https://dev.mysql.com/doc/refman/5.5/en/innodb-parameters.html#sysvar_innodb_large_prefix
https://mariadb.com/kb/en/library/innodb-system-variables/
https://mariadb.com/kb/en/library/innodb-dynamic-row-format/
https://mariadb.com/kb/en/library/innodb-system-variables/#innodb_default_row_format
https://docs.moodle.org/37/en/MySQL_full_unicode_support


    innodb_large_prefix=ON
    innodb_file_format=barracuda
    innodb_file_per_table=ON
    innodb_default_row_format='dynamic'

mariadb 下载(MariaDB 10.4 is the current stable (GA) series of MariaDB.):

      https://downloads.mariadb.org/


      https://downloads.mariadb.org/mariadb/10.4.8/
      https://mariadb.com/kb/en/library/yum/



















