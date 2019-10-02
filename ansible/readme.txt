
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































