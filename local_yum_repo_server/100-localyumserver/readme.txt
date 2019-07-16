
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

//注: 这里 加了前缀 '000-', 其实其并不会影响下载顺序, 只是为了在 使用如 `yum repolist` 这样的命令时其能第一个显示出来
[root@client ~]# vim /etc/yum.repos.d/000-local-yum.repo
        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0

[root@client ~]# yum repolist | grep local-yum
      local-yum             local-yum                                                6

[root@client ~]# yum clean metadata   # force yum to download all the metadata the next time it is run.
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

[root@client ~]# vim /etc/yum.repos.d/000-local-yum.repo
        [local-yum]
        name=local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0
        #  priority=N 用于指定优先级, N 是 1 到 99 范围的 整数, 数字越小, 优先级越高, 默认值为 99
        #  见 https://wiki.centos.org/PackageManagement/Yum/Priorities
        priority=1

[root@client ~]# yum clean metadata
[root@client ~]# yum list mysql-community-server


---------------------------------------------------------------------------------------------------
网上资料:
https://serverfault.com/questions/503083/how-does-yum-know-which-repository-to-use-for-installation-if-the-same-applicati

https://wiki.centos.org/PackageManagement/Yum/Priorities
https://wiki.centos.org/PackageManagement/Yum
https://docs.fedoraproject.org/en-US/Fedora/14/html/Musicians_Guide/sect-Musicians_Guide-CCRMA_Repository_Priorities.html
http://www.linuxe.cn/post-300.html

https://superuser.com/questions/333542/how-do-i-get-yum-to-see-updates-to-a-local-repo-without-cleaning-cache

https://wiki.centos.org/TipsAndTricks/YumAndRPM

https://stackoverflow.com/questions/635869/can-yum-tell-me-which-of-my-repositories-provide-a-particular-package

其他搭建 local yum repo 的资料:

      https://www.howtoforge.com/creating_a_local_yum_repository_centos
      https://phoenixnap.com/kb/create-local-yum-repository-centos
      https://www.itzgeek.com/how-tos/linux/centos-how-tos/create-local-yum-repository-on-centos-7-rhel-7-using-dvd.html
      https://www.cloudera.com/documentation/enterprise/5-5-x/topics/cdh_ig_yumrepo_local_create.html







