
---------------------------------------------------------------------------------------------------
构建 最基本的 local yum repo 服务

// 创建 用于 local yum repo 的 目录
[root@localyumrepo ~]# mkdir  /var/www/html/local_yum_repo_dir

// 先下载 httpd 和 createrepo 相关的 rpm 包 到 /var/www/html/local_yum_repo_dir
[root@localyumrepo ~]# yum install httpd createrepo --downloadonly   --downloaddir=/var/www/html/local_yum_repo_dir

// 正式 安装软件 httpd 和 createrepo
[root@localyumrepo ~]# yum -y install httpd
[root@localyumrepo html]# yum -y install createrepo

// 启动 用于 local yum repo 的 httpd server
[root@localyumrepo ~]# systemctl start httpd
[root@localyumrepo ~]# systemctl enable httpd
      Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.

// 将 local_yum_repo_dir 构建为 仓库目录(即 创建相关的 metadata 目录 和 文件)
[root@localyumrepo ~]# createrepo /var/www/html/local_yum_repo_dir/

至此, 一个最基本的 local yum repo 就准备完成了
---------------------------------------------------------------------------------------------------
示例: 向本地仓库 添加 mysql 的 相关 rpm 包

[root@localyumrepo ~]# mkdir download && cd download
[root@localyumrepo download]# wget --no-check-certificate https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@localyumrepo download]# yum -y install mysql80-community-release-el7-2.noarch.rpm

[root@localyumrepo download]# ls /etc/yum.repos.d/ | grep mysql
    mysql-community.repo
    mysql-community-source.repo

[root@localyumrepo download]# vim /etc/yum.repos.d/mysql-community.repo

      # Enable to use MySQL 5.7
      [mysql57-community]
      name=MySQL 5.7 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
      #// enabled=1 表示启用仓库
      enabled=1
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

      [mysql80-community]
      name=MySQL 8.0 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/7/$basearch/
      #// enabled=0 表示禁用仓库
      enabled=0
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

[root@localyumrepo ~]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                 108
      mysql-tools-community/x86_64      MySQL Tools Community                       90
      mysql57-community/x86_64          MySQL 5.7 Community Server                 347

[root@localyumrepo ~]# yum -y install mysql-community-server --downloadonly --downloaddir=/var/www/html/local_yum_repo_dir/
[root@localyumrepo ~]# createrepo /var/www/html/local_yum_repo_dir/   # 注: 其实 createrepo 是一个执行 python 程序的 shell script

---------------------------------------------------------------------------------------------------
client 端:

[root@client ~]# vim /etc/yum.repos.d/local-yum.repo
        [local-yum]
        name=local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0

[root@client ~]# yum repolist | grep local-yum
      local-yum             local-yum                                                6

[root@client ~]# yum -y install mysql-community-server

---------------------------------------------------------------------------------------------------
client 端: (另一种使用方式, 为 local yum repo 配置高优先级, update 时低优先级repo的 packages 无法覆盖 高优先级 repo 的 packages)

[root@localyumrepo ~]# yum -y install yum-plugin-priorities --downloadonly   --downloaddir=/var/www/html/local_yum_repo_dir
[root@localyumrepo ~]# createrepo /var/www/html/local_yum_repo_dir

// 查看 yum 的 plugins 功能 以确保其被启用
[root@client ~]# grep -E '^plugins=1' /etc/yum.conf
        plugins=1   <----- 为 1 表示 已经其被 enabled

[root@client ~]# yum install yum-plugin-priorities

// 查看一下 安装 yum-plugin-priorities 的 相关文件
[root@client ~]# rpm -ql yum-plugin-priorities
        /etc/yum/pluginconf.d/priorities.conf   <------
        /usr/lib/yum-plugins/priorities.py
        /usr/lib/yum-plugins/priorities.pyc
        /usr/lib/yum-plugins/priorities.pyo
        /usr/share/doc/yum-plugin-priorities-1.1.31
        /usr/share/doc/yum-plugin-priorities-1.1.31/COPYING

// 查看 插件 yum-plugin-priorities 的配置文件确保其被启用
[root@client ~]# cat /etc/yum/pluginconf.d/priorities.conf
      [main]
      enabled = 1

[root@client ~]# vim /etc/yum.repos.d/local-yum.repo
        [local-yum]
        name=local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0
        #  priority=N 用于指定优先级, N 是 1 到 99 范围的 整数, 数字越小, 优先级越高, 默认值为 99
        #  见 https://wiki.centos.org/PackageManagement/Yum/Priorities
        priority=1

---------------------------------------------------------------------------------------------------
网上资料:
https://serverfault.com/questions/503083/how-does-yum-know-which-repository-to-use-for-installation-if-the-same-applicati

https://wiki.centos.org/PackageManagement/Yum/Priorities
https://wiki.centos.org/PackageManagement/Yum

https://wiki.centos.org/TipsAndTricks/YumAndRPM





