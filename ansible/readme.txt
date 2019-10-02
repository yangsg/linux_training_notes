
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































