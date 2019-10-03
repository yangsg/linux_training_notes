
https://www.ansible.com/overview/how-ansible-works
https://docs.ansible.com/
https://docs.ansible.com/ansible/latest/index.html
https://docs.ansible.com/ansible/latest/user_guide/index.html



----------------------------------------------------------------------------------------------------
Linux Ansible  (自动化引擎 automation engine)

作用：

  ansible是新出现的自动化运维工具，基于Python开发，实现了批量系统配置、批量程序部署、批量运行命令等功能。


特性
    1.no agent: 不需要在被管控主机上安装任何软件
    2.no server: 无服务器端,使用时直接运行命令即可
    3.modules in any languages：基于模块工作，可使用任意语言开发模块,
    4.使用yaml语言定制剧本playbook
    5.ssh by default：基于SSH工作


优点
    (1)、轻量级，无需在客户端安装agent，更新时，只需在操作机上进行一次更新即可；
    (2)、批量任务执行可以写成脚本，而且不用分发到远程就可以执行；
    (3)、使用python编写，维护更简单，ruby语法过于复杂；


https://www.ansible.com/overview/how-ansible-works
efficient architecture (高效架构: 工作方式)

      Ansible works by connecting to your nodes and pushing out small programs,
      called "Ansible modules" to them. These programs are written to be resource
      models of the desired state of the system. Ansible then
      executes these modules (over SSH by default), and removes them when finished.



----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

安装

  Control Node Requirements(控制节点需求)
    Python 2 (version 2.7) or Python 3 (versions 3.5 and higher)
    Windows isn’t supported for the control node.

    警告: 请注意 某些 modules  和 plugins 需要额外的需求.

  Managed Node Requirements(被管理节点需求)
    On the managed nodes, you need a way to communicate, which is normally ssh. By default this uses sftp.
    If that’s not available, you can switch to scp in ansible.cfg.
    You also need Python 2 (version 2.6 or later) or Python 3 (version 3.5 or later).

    注: ansible 默认 定位查找 /usr/bin/python 来运行 其 modules.


// 在 控制节点上 安装 ansible
[root@control_node ~]# yum -y install ansible
[root@control_node ~]# rpm -q ansible
    ansible-2.8.5-1.el7.noarch


// 查看 ansible 自带的配置文件
[root@control_node ~]# rpm -qc ansible
    /etc/ansible/ansible.cfg
    /etc/ansible/hosts   <------主机清单Inventory文件


// 测试
[root@controller_node ~]# echo "127.0.0.1" > ~/ansible_hosts
[root@controller_node ~]# export ANSIBLE_INVENTORY=~/ansible_hosts  #指定自己的 inventory file 而非 /etc/ansible/hosts
[root@controller_node ~]# ansible all -m ping --ask-pass   #使用 ping 命令测试一下
    SSH password:  <===输入登录密码
    127.0.0.1 | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": false,
        "ping": "pong"
    }

    注:
      If using sudo features and when sudo requires a password,
      also supply --ask-become-pass (previously --ask-sudo-pass which has been deprecated).

[root@controller_node ~]# unset ANSIBLE_INVENTORY



----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html
https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings-locations

配置文件:

  --------------------------------------------------
  The configuration file
      https://docs.ansible.com/ansible/latest/reference_appendices/config.html#the-configuration-file

  Changes can be made and used in a configuration file which will be searched for in the following order:

      ANSIBLE_CONFIG (environment variable if set)
      ansible.cfg (in the current directory)
      ~/.ansible.cfg (in the home directory)
      /etc/ansible/ansible.cfg

  Ansible will process the above list and use the first file found, all others are ignored.

  注: 配置文件时 an INI format 的 一种变体, 整行注释 可使用 hash sign (#) 和 semicolon (;),
      但是内联(inline) 注释 仅允许使用 分号(;) 来引入, 如下:

        # some basic default values...
        inventory = /etc/ansible/hosts  ; This points to the file that lists your hosts
  --------------------------------------------------


  Avoiding security risks with ansible.cfg in the current directory (避免 当前目录下的 ansible.cfg 的安全风险)

      注: Ansible will not automatically load a config file from the current working directory if the directory is world-writable.


----------------------------------------------------------------------------------------------------

// 使用 命令 生成 非对称秘钥对
[root@controller_node ~]# ssh-keygen  #注: ssh-keygen 不带任何参数时, 默认生成 用于 SSH protocol 2 的 2048 bits 的 RSA key
      Generating public/private rsa key pair.
      Enter file in which to save the key (/root/.ssh/id_rsa): <=====直接 Enter
      Enter passphrase (empty for no passphrase):  <=====直接 Enter
      Enter same passphrase again:  <=====直接 Enter
      Your identification has been saved in /root/.ssh/id_rsa.
      Your public key has been saved in /root/.ssh/id_rsa.pub.
      The key fingerprint is:
      SHA256:5B2c3yTM9ma41WU0DH4xu3VXmxQ6FlAGC9wDDxr8TAM root@controller_node
      The key's randomart image is:
      +---[RSA 2048]----+
      |      .Eo+oo+=o*+|
      |       .o=+*+ +oO|
      |       .= =o*=.=*|
      |       o + +.*oo*|
      |        S . o *..|
      |             =   |
      |            .    |
      |                 |
      |                 |
      +----[SHA256]-----+


[root@controller_node ~]# ssh-copy-id root@192.168.175.101
[root@controller_node ~]# ssh-copy-id root@192.168.175.102
[root@controller_node ~]# ssh-copy-id root@192.168.175.103



[root@controller_node ~]# vim /etc/hosts

    192.168.175.101 node01.linux.com
    192.168.175.102 node02.linux.com
    192.168.175.103 node03.linux.com



       -i, --inventory, --inventory-file
          specify inventory host path or comma separated host list. --inventory-file is deprecated


// 将 managed node 添加到 清单文件(inventory file)中
// https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
[root@controller_node ~]# vim /etc/ansible/hosts

    # 注: 该清单文件中自带了 example
    192.168.175.101
    node02.linux.com


// 禁用(disable) Host Key Checking (注:编辑文件 /etc/ansible/ansible.cfg 或 ~/.ansible.cfg)
[root@controller_node ~]# vim /etc/ansible/ansible.cfg

      #Ansible has host key checking enabled by default.
      #If a host is reinstalled and has a different key in ‘known_hosts’,
      #this will result in an error message until corrected. If a host is not initially in ‘known_hosts’ this will
      #result in prompting for confirmation of the key, which results in an interactive
      #experience if using Ansible, from say, cron. You might not want this.
      # https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html#host-key-checking

      [defaults]
      host_key_checking = False
      # 注: 还可以通过 修改环境变量 `export ANSIBLE_HOST_KEY_CHECKING=False` 来禁用(disable) Host Key Checking



[root@controller_node ~]# ansible all -m ping           # 如果没有指定 -u 选项, 则默认使用当前用户名 远程连接 machines
[root@controller_node ~]# ansible all -m ping -u root   #以 root 用户 远程连接(remote connect) 到 machines
[root@controller_node ~]# ansible 192.168.175.101 -m ping -u root   #前提条件: 此处的 192.168.175.101  必须出现在 清单文件中
[root@controller_node ~]# ansible node02.linux.com -m ping -u root  #前提条件: 此处的 node02.linux.com 必须出现在 清单文件中


// 以 group 的方式在 清单文件中提供 managed nodes 的信息
[root@controller_node ~]# vim /etc/ansible/hosts

      [dbservers]
      192.168.175.101
      192.168.175.102
      192.168.175.103

[root@controller_node ~]# ansible dbservers -m ping -u root
[root@controller_node ~]# ansible 192.168.175.102 -m ping -u root   #也可以写组里的一个机器


[root@controller_node ~]# ansible all --list-hosts   #--list-hosts:  outputs a list of matching hosts; does not execute anything else
    hosts (3):
      192.168.175.101
      192.168.175.102
      192.168.175.103

[root@controller_node ~]# ansible 192.168.175.101:192.168.175.103 --list-hosts
    hosts (2):
      192.168.175.101
      192.168.175.103

[root@controller_node ~]# ansible 192.168.175.* --list-hosts
    hosts (3):
      192.168.175.102
      192.168.175.103
      192.168.175.101

[root@controller_node ~]# vim /etc/ansible/hosts

      [dbservers]
      192.168.175.101
      192.168.175.102

      [webservers]
      192.168.175.102
      192.168.175.103

[root@controller_node ~]# ansible 'dbservers:!webservers' --list-hosts    #差集, 集合dbservers - 集合 webservers
    hosts (1):
        192.168.175.101

[root@controller_node ~]# ansible 'dbservers:&webservers' --list-hosts    #交集，集合 dbservers  交  集合 webservers
    hosts (1):
        192.168.175.102

[root@controller_node ~]# ansible 192.168.175.* --limit dbservers --list-hosts  #-l 'SUBSET', --limit 'SUBSET': further limit selected hosts to an additional pattern
    hosts (2):
      192.168.175.102
      192.168.175.101


[root@controller_node ~]# ansible all -a "/bin/echo hello"   #在所有被管理 nodes 上执行输出 hello 的操作, 这里没有指定选项 -m 'MODULE_NAME', 则默认为 -m command

// When running commands, you can specify the local server by using “localhost” or “127.0.0.1” for the server name.
[root@controller_node ~]# ansible localhost -m ping -e 'ansible_python_interpreter="/usr/bin/env python"'
[root@controller_node ~]# ansible 127.0.0.1 -m ping -e 'ansible_python_interpreter="/usr/bin/env python"'

//You can specify localhost explicitly by adding this to your inventory file:
      localhost ansible_connection=local ansible_python_interpreter="/usr/bin/env python"








[root@node03 ~]# useradd bruce

[root@controller_node ~]# ansible 192.168.175.103 -m ping -u root --become --become-user bruce
   [WARNING]: Module remote_tmp /home/bruce/.ansible/tmp did not exist and was created with a mode of 0700, this may cause issues when running as another user. To avoid this, create the
  remote_tmp dir with the correct permissions manually

  192.168.175.103 | SUCCESS => {
      "ansible_facts": {
          "discovered_interpreter_python": "/usr/bin/python"
      },
      "changed": false,
      "ping": "pong"
  }


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/cli/ansible-doc.html

命令 ansible-doc
语法: ansible-doc [-l|-F|-s] [options] [-t <plugin type> ] [plugin]
说明: displays  information on modules installed in Ansible libraries.
      It displays a terse listing of plugins and their short descriptions,
      provides a printout of their DOCUMENTATION strings, and it can
      create a short "snippet" which can be pasted into a playbook.


[root@controller_node ~]# ansible-doc command  #注: command 模块不支持扩展的 shell 语法, 如不支持  piping 和 redirects 等
[root@controller_node ~]# ansible-doc shell


[root@node01 ~]# ansible-doc -l     #-l, --list            List available plugins



选项:
     -t 'TYPE', --type 'TYPE'
        Choose which plugin type (defaults to "module"). Available plugin types are : ('become', 'cache',
        'callback',  'cliconf',  'connection',  'httpapi',  'inventory',  'lookup', 'shell', 'module', 'strategy', 'vars')

[root@controller_node ~]# ansible-doc -l -t shell
    cmd        Windows Command Prompt
    csh        C shell (/bin/csh)
    fish       fish shell (/bin/fish)
    powershell Windows PowerShell
    sh         POSIX shell (/bin/sh)


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html

Introduction To Ad-Hoc Commands

    An ad-hoc command is something that you might type in to do something really quick, but don’t want to save for later.


Parallelism and Shell Commands(并行执行命令)
    https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#parallelism-and-shell-commands

       -f 'FORKS', --forks 'FORKS'
          specify number of parallel processes to use (default=5)
       -o, --one-line
          condense output

// 注: 在 remote hosts 上执行的命令 应该用 引号引起来, 以避免其被 local shell 执行 expansion 处理.
[root@controller_node ~]# ansible all -a '/usr/bin/date' --one-line -f 10
[root@controller_node ~]# ansible all -m shell -a 'date' --one-line -f 10   #注: 如果机器很多, 可以给 -f 指定一个很大的值以保证其并行执行
    192.168.175.101 | CHANGED | rc=0 | (stdout) Thu Oct  3 10:47:58 CST 2019
    192.168.175.102 | CHANGED | rc=0 | (stdout) Thu Oct  3 10:47:57 CST 2019
    192.168.175.103 | CHANGED | rc=0 | (stdout) Thu Oct  3 10:47:58 CST 2019


[root@controller_node ~]# ansible all -m shell -a 'echo $SHELL $HOSTNAME' -o
      192.168.175.102 | CHANGED | rc=0 | (stdout) /bin/bash node02.linux.com
      192.168.175.101 | CHANGED | rc=0 | (stdout) /bin/bash node01.linux.com
      192.168.175.103 | CHANGED | rc=0 | (stdout) /bin/bash node03.linux.com



----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#file-transfer

File Transfer(文件传输)

      Ansible can SCP lots of files to multiple machines in parallel.


[root@controller_node ~]# ansible all -m copy -a "src=/etc/hosts dest=/tmp/hosts"


// The file module allows changing ownership and permissions on files. These same options can be passed directly to the copy module as well:
[root@controller_node ~]# ansible all -m file -a "dest=/tmp/hosts mode=600"
[root@controller_node ~]# ansible all -m file -a "dest=/tmp/hosts mode=600 owner=nobody group=nobody"

// The file module can also create directories, similar to mkdir -p:
[root@controller_node ~]# ansible all -m file -a "dest=/path/to/c mode=755 owner=nobody group=nobody state=directory"  #创建目录, 类似 mkdir -p

// As well as delete directories (recursively) and delete files:
[root@controller_node ~]# ansible all -m file -a "dest=/path/to/c state=absent"   #(递归)删除目录 和 文件



----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#managing-packages

Managing Packages(管理软件包)

      可用的 module: yum 和 apt

        注: 当然, 某些操作 也可以通过 command 或 shell 模块 执行原始的 shell 命令来完成

// Ensure a package is installed, but don’t update it:
[root@controller_node ~]# ansible all -m yum -a "name=gcc state=present"  #保证 指定软件包被安装, 但不会对其进行 更新操作(如果没有安装软件包,则执行安装操作)

// Ensure a package is installed to a specific version:
[root@controller_node ~]# ansible all -m yum -a "name=gcc-4.8.5 state=present"  #确保指定版本的 软件包 被安装

// Ensure a package is at the latest version:
[root@controller_node ~]# ansible all -m yum -a "name=gcc state=latest"  #确保 最新版的 特定软件包 被安装(可用于更新软件包)

// Ensure a package is not installed:
[root@controller_node ~]# ansible all -m yum -a "name=gcc state=absent"  #确保 指定的 软件包没有被安装(可用于卸载软件包)


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#users-and-groups

Users and Groups

[root@controller_node ~]# ansible all -m user -a "name=foo"   #创建 user 'foo', 因为其 state 参数默认值为 present
[root@controller_node ~]# ansible all -m user -a "name=foo state=absent"   #删除 user 'foo'


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#deploying-from-source-control

// Deploy your webapp straight from git:
[root@controller_node ~]# ansible all -m git -a "repo=https://github.com/github/gitignore.git dest=/tmp/myapp version=HEAD"   #克隆 git 仓库


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#managing-services

Managing Services

// Ensure a service is started on all:
[root@controller_node ~]# ansible all -m service -a "name=httpd state=started"  #确保 httpd 被启动(started)

// Alternatively, restart a service on all:
[root@controller_node ~]# ansible all -m service -a "name=httpd state=restarted"  # 重启 httpd 服务

// Ensure a service is stopped:
[root@controller_node ~]# ansible all -m service -a "name=httpd state=stopped"  # 停止 httpd 服务


----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#time-limited-background-operations


Time Limited Background Operations

       -B 'SECONDS', --background 'SECONDS'
          run asynchronously, failing after X seconds (default=N/A)
       -P 'POLL_INTERVAL', --poll 'POLL_INTERVAL'
          set the poll interval if using -B (default=15)

// Long running operations can be run in the background, and it is possible to check their status later.

// 在后台异步执行命令, with a timeout of 30 seconds (-B), and without polling (-P)
[root@controller_node ~]# ansible all -B 30 -P 0 -m shell -a 'while true; do sleep 2s; date >> /tmp/date.log ; done'

      略 略 略 略 略 略 略 略 略 略
      192.168.175.101 | CHANGED => {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "ansible_job_id": "708301742370.19965",
          "changed": true,
          "finished": 0,
          "results_file": "/root/.ansible_async/708301742370.19965",
          "started": 1
      }


// If you do decide you want to check on the job status later, you can use the async_status module,
// passing it the job id that was returned when you ran the original job in the background:
[root@controller_node ~]# ansible 192.168.175.101 -m async_status -a "jid=708301742370.19965"

        192.168.175.101 | SUCCESS => {
            "ansible_facts": {
                "discovered_interpreter_python": "/usr/bin/python"
            },
            "ansible_job_id": "708301742370.19965",
            "changed": false,
            "finished": 0,
            "started": 1
        }


[root@controller_node ~]# ansible all -B 30 -P 2 -m shell -a 'sleep 4s; date >> /tmp/date.log'

    Poll mode is smart so all jobs will be started before polling will begin on any machine.
    Be sure to use a high enough --forks value if you want to get all of your jobs started very quickly.
    After the time limit (in seconds) runs out (-B), the process on the remote nodes will be terminated.

    Typically you’ll only be backgrounding long-running shell commands or
    software upgrades. Backgrounding the copy module does not do a background file transfer.




----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html#gathering-facts


Gathering Facts


Facts are described in the playbooks section and represent discovered variables about a system.
These can be used to implement conditional execution of tasks but also just
to get ad-hoc information about your system. You can see all facts via:

[root@controller_node ~]# ansible all -m setup




----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html



       -i, --inventory, --inventory-file
          specify inventory host path or comma separated host list. --inventory-file is deprecated



--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-hosts-and-groups

Inventory basics: hosts and groups

    清单文件(inventory file) 可以是 多种格式之一

清单文件 /etc/ansible/hosts 是 INI-like 的格式, 类似如下这样:

      #此处 mail.example.com 属于 默认的组(default groups): all 和 ungrouped
      mail.example.com

      [webservers]
      #此处 foo.example.com 属于组 all 和 webservers
      foo.example.com
      bar.example.com

      [dbservers]
      one.example.com
      two.example.com
      three.example.com

其对应的 YAML 版本类似如下:

      all:
        hosts:
          mail.example.com:
        children:
          webservers:
            hosts:
              foo.example.com:
              bar.example.com:
          dbservers:
            hosts:
              one.example.com:
              two.example.com:
              three.example.com:



--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#hosts-in-multiple-groups

Hosts in multiple groups


    一个 host 可以属于 多个组(groups), 即 host 和 group 之间可以是 多对多 关系

    嵌套组(nested groups) 也是允许的, 这样可以简化某些配置

https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#ansible-variable-precedence



--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#hosts-and-non-standard-ports

Hosts and non-standard ports

If you have hosts that run on non-standard SSH ports you can put the port number after the hostname with a colon.
Ports listed in your SSH config file won’t be used with the paramiko connection but will be used with the openssh connection.

在 hosts 监听在非标准的 SSH ports(即 22 号端口) 上时, 你可以显示的 指定其监听端口, 如:

        badwolf.example.com:5309


Suppose you have just static IPs and want to set up some aliases that live in your host file,
or you are connecting through tunnels. You can also describe hosts via variables:

In INI(ini 版本):

    #此处 jumper 为 192.0.2.50:5555 的别名(alias)
    jumper ansible_port=5555 ansible_host=192.0.2.50

In YAML(yaml 版本):
    ...
      hosts:
        jumper:
          ansible_port: 5555
          ansible_host: 192.0.2.50



Note(注意):
    // INI format 中通过 key=value 语法传递的 Values 根据其 声明的 位置不同 而 解释(interpreted)也不同
    Values passed in the INI format using the key=value syntax are interpreted differently depending
    on where they are declared. * When declared inline with the host, INI values are interpreted as
    Python literal structures (strings, numbers, tuples, lists, dicts, booleans, None).
    Host lines accept multiple key=value parameters per line. Therefore they need a way to
    indicate that a space is part of a value rather than a separator. * When declared in a :vars section,
    INI values are interpreted as strings. For example var=FALSE would create a string equal to ‘FALSE’.
    Unlike host lines, :vars sections accept only a single entry per line, so everything after
    the = must be the value for the entry. * Do not rely on types set during definition,
    always make sure you specify type with a filter when needed when consuming the variable.
    * Consider using YAML format for inventory sources to avoid confusion on the actual type of a variable.
    The YAML inventory plugin processes variable values consistently and correctly.
    // 可以使用 YAML format 来避免 variable 的  actual type 的混淆,
    // YAML inventory plugin 可以 一致 和 正确的 处理 variable values


// 通过区间指定 hosts (Ranges are inclusive)
[root@controller_node ~]# vim /etc/ansible/hosts

      [webservers]
      192.168.175.[101:103]

      [dbservers]
      node[01:03].linux.com

      [databases]
      #注: 字母(alphabetic)也 可以用于定义区间
      db-[a:f].example.com

      [targets]
      #注: 还可以为 每个主机 选择 connection type 和 user
      localhost              ansible_connection=local
      other1.example.com     ansible_connection=ssh        ansible_user=mpdehaan
      other2.example.com     ansible_connection=ssh        ansible_user=mdehaan




[root@controller_node ~]# ansible webservers --list-hosts
      hosts (3):
        192.168.175.101
        192.168.175.102
        192.168.175.103
[root@controller_node ~]# ansible dbservers --list-hosts
      hosts (3):
        node01.linux.com
        node02.linux.com
        node03.linux.com


--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#assigning-a-variable-to-one-machine-host-variables


Assigning a variable to one machine: host variables (主机变量)

在 ini-like 格式为 one machine 赋给 变量的方式如下:

        [atlanta]
        host1 http_port=80 maxRequestsPerChild=808
        host2 http_port=303 maxRequestsPerChild=909

对应的 yaml 版本如下:

        atlanta:
          host1:
            http_port: 80
            maxRequestsPerChild: 808
          host2:
            http_port: 303
            maxRequestsPerChild: 909


--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#assigning-a-variable-to-many-machines-group-variables

Assigning a variable to many machines: group variables(组变量)

Variables can also be applied to an entire group at once:

INI 的方式:

        [atlanta]
        host1
        host2

        // 通过 :vars 为 组 atlanta 赋予变量
        [atlanta:vars]
        ntp_server=ntp.atlanta.example.com
        proxy=proxy.atlanta.example.com

对应的 YAML 版本:

      atlanta:
        hosts:
          host1:
          host2:
        vars:
          ntp_server: ntp.atlanta.example.com
          proxy: proxy.atlanta.example.com


Be aware that this is only a convenient way to apply variables to multiple hosts at once;
even though you can target hosts by group, variables are always flattened to the host level before a play is executed.


--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inheriting-variable-values-group-variables-for-groups-of-groups

Inheriting variable values: group variables for groups of groups

You can make groups of groups using the :children suffix in INI or the children:
entry in YAML. You can apply variables to these groups of groups using :vars or vars::


        [atlanta]
        host1
        host2

        [raleigh]
        host2
        host3

        #通过后缀 :children 创建组 southeast 的子组
        [southeast:children]
        atlanta
        raleigh

        #通过后缀 :vars 应用变量
        [southeast:vars]
        some_server=foo.southeast.example.com
        halon_system_timeout=30
        self_destruct_countdown=60
        escape_pods=2

        [usa:children]
        southeast
        northeast
        southwest
        northwest


Child groups have a couple of properties to note:

    - Any host that is member of a child group is automatically a member of the parent group.
    - A child group’s variables will have higher precedence (override) a parent group’s variables.
    - Groups can have multiple parents and children, but not circular relationships.
    - Hosts can also be in multiple groups, but there will only be one instance of a host, merging the data from the multiple groups.






--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#default-groups

Default groups


存在两个默认组: all 和 ungrouped

[root@controller_node ~]# ansible ungrouped --list-hosts
  hosts (1):
    192.168.175.101


Every host will always belong to at least 2 groups. Though all and ungrouped
are always present, they can be implicit and not appear in group listings like group_name



--------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#organizing-host-and-group-variables


Organizing host and group variables


Although you can store variables in the main inventory file, storing separate host
and group variables files may help you track your variable values more easily.

Host and group variables can be stored in individual files relative to the inventory file (not directory, it is always the file).

These variable files are in YAML format. Valid file extensions include
‘.yml’, ‘.yaml’, ‘.json’, or no file extension. See YAML Syntax if you are new to YAML.

      yaml 语法见 https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html#yaml-syntax



假设保持  inventory file 为 /etc/ansible/hosts, 而 主机(host)  'foosball'  同时为 组 'raleigh' 和 组 'webservers' 的 member,
则该 host 会 使用 如下位置的 YAML files 中的 变量:

        /etc/ansible/group_vars/raleigh # can optionally end in '.yml', '.yaml', or '.json'
        /etc/ansible/group_vars/webservers
        /etc/ansible/host_vars/foosball

For instance, suppose you have hosts grouped by datacenter, and each datacenter uses some different servers.
The data in the groupfile ‘/etc/ansible/group_vars/raleigh’ for the ‘raleigh’ group might look like:

      ---
      ntp_server: acme.example.org
      database_server: storage.example.org


It is okay if these files do not exist, as this is an optional feature.

As an advanced use case, you can create directories(创建目录) named after your groups or hosts,
and Ansible will read all the files in these directories in lexicographical order(字典顺序).
An example with the ‘raleigh’ group:

      /etc/ansible/group_vars/raleigh/db_settings
      /etc/ansible/group_vars/raleigh/cluster_settings

All hosts that are in the ‘raleigh’ group will have the variables defined in these files available to them.
This can be very useful to keep your variables organized when a single file starts to be too big,
or when you want to use Ansible Vault on a part of a group’s variables.


Tip(小贴士):
     The group_vars/ and host_vars/ directories can exist in the playbook directory OR the inventory directory.
     If both paths exist, variables in the playbook directory will override variables set in the inventory directory.

Tip(小贴士):
     The ansible-playbook command looks for playbooks in the current working directory by default.
     Other Ansible commands (for example, ansible, ansible-console, etc.) will only look for
     group_vars/ and host_vars/ in the inventory directory unless you provide the --playbook-dir option on the command line.

Tip(小贴士):
     Keeping your inventory file and variables in a git repo (or other version control) is
     an excellent way to track changes to your inventory and host variables.





----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#how-variables-are-merged


How variables are merged (变量 merged 的方式)

By default variables are merged/flattened to the specific host before a play is run.
This keeps Ansible focused on the Host and Task, so groups don’t really survive outside
of inventory and host matching. By default, Ansible overwrites variables including
the ones defined for a group and/or host (see DEFAULT_HASH_BEHAVIOUR).
The order/precedence is (from lowest to highest): 如下 顺序/优先级 从低到高

    优先级
    低| - all group (because it is the ‘parent’ of all other groups)
      | - parent group
      | - child group
    高| - host
      V



When groups of the same parent/child level are merged, it is done alphabetically(按字母顺序),
and the last group loaded overwrites the previous groups. For example,
an a_group will be merged with b_group and b_group vars that match will overwrite the ones in a_group.


New in version 2.4. (从 2.4 版本开始, 可以使用 组变量  ansible_group_priority 改变 同级别的 组中 变量 的 merge order)
Starting in Ansible version 2.4, users can use the group variable ansible_group_priority
to change the merge order for groups of the same level (after the parent/child order is resolved).
The larger the number, the later it will be merged, giving it higher priority.
This variable defaults to 1 if not set. For example:

        a_group:
            testvar: a
            ansible_group_priority: 10
        b_group：
            testvar: b


In this example, if both groups have the same priority, the result would normally have been testvar == b,
but since we are giving the a_group a higher priority the result will be testvar == a.

Note: ansible_group_priority can only be set in the inventory source and not in group_vars/ as the variable is used in the loading of group_vars.



----------------------------------------------------------------------------------------------------
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#using-multiple-inventory-sources


Using multiple inventory sources

As an advanced use case you can target multiple inventory sources (directories, dynamic inventory scripts
or files supported by inventory plugins) at the same time by giving multiple inventory parameters
from the command line or by configuring ANSIBLE_INVENTORY. This can be useful when you want to target
normally separate environments, like staging and production, at the same time for a specific action.

Target two sources from the command line like this:

    ansible-playbook get_logs.yml -i staging -i production



Keep in mind that if there are variable conflicts in the inventories, they are resolved according to
the rules described in How variables are merged and Variable precedence: Where should I put a variable?.
The merging order is controlled by the order of the inventory source parameters.
If [all:vars] in staging inventory defines myvar = 1, but production inventory defines myvar = 2,
the playbook will be run with myvar = 2. The result would be reversed if the playbook
was run with -i production -i staging.

    https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#how-we-merge
    https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#ansible-variable-precedence


----------------------------------------
Aggregating inventory sources with a directory

You can also create an inventory by combining multiple inventory sources and source types under a directory.
This can be useful for combining static and dynamic hosts and managing them as one inventory.
The following inventory combines an inventory plugin source, a dynamic inventory script, and a file with static hosts:

        inventory/
          openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
          dynamic-inventory.py   # add additional hosts with dynamic inventory script
          static-inventory       # add static hosts and groups
          group_vars/
            all.yml              # assign variables to all hosts


You can target this inventory directory simply like this:

    ansible-playbook example.yml -i inventory

It can be useful to control the merging order of the inventory sources if there’s variable conflicts
or group of groups dependencies to the other inventory sources. The inventories are merged in alphabetical
order according to the filenames so the result can be controlled by adding prefixes to the files:

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-static-inventory       # add static hosts
      group_vars/
        all.yml                 # assign variables to all hosts


If 01-openstack.yml defines myvar = 1 for the group all, 02-dynamic-inventory.py defines myvar = 2,
and 03-static-inventory defines myvar = 3, the playbook will be run with myvar = 3.

For more details on inventory plugins and dynamic inventory scripts see Inventory Plugins and Working With Dynamic Inventory.

      https://docs.ansible.com/ansible/latest/plugins/inventory.html#inventory-plugins
      https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html#intro-dynamic-inventory


----------------------------------------------------------------------------------------------------









