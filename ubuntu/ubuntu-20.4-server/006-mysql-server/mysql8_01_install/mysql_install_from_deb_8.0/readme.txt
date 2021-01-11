


mysql 的 国内镜像:
  清华大学开源软件镜像站:       https://mirrors.tuna.tsinghua.edu.cn/
  中国科学技术大学开源软件镜像: https://mirrors.ustc.edu.cn/ 


```bash
# 配置国内的 mysql 镜像站: 参考 https://mirrors.tuna.tsinghua.edu.cn/help/mysql/
# 注: 关于 sources.list 的内容格式，见 `man sources.list`


ysg@vm01:~$ sudo vim /etc/apt/sources.list.d/mysql-community.list

  deb https://mirrors.tuna.tsinghua.edu.cn/mysql/apt/ubuntu focal mysql-5.6 mysql-5.7 mysql-8.0 mysql-tools


ysg@vm01:~$ sudo apt-get update

  如上命令提示报问题: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 8C718D3B5072E1F5

// 解决办法:
ysg@vm01:~$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5
    Executing: /tmp/apt-key-gpghome.RBUxFptdrE/gpg.1.sh --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5
    gpg: key 8C718D3B5072E1F5: 1 duplicate signature removed
    gpg: key 8C718D3B5072E1F5: public key "MySQL Release Engineering <mysql-build@oss.oracle.com>" imported
    gpg: Total number processed: 1
    gpg:               imported: 1



ysg@vm01:~$ apt list mysql-server  #注: 如果想列出所有可用的版本，可用加上 '-a' 选项
  Listing... Done
  mysql-server/unknown 8.0.22-1ubuntu20.04 amd64
  N: There are 2 additional versions. Please use the '-a' switch to see them.



ysg@vm01:~$ sudo apt install mysql-server=8.0.22-1ubuntu20.04  #安装版本为 8.0.22-1ubuntu20.04 的 mysql-server

ysg@vm01:~$ dpkg -l mysql-server   #或执行命令 `apt list mysql-server --installed` 查看
  Desired=Unknown/Install/Remove/Purge/Hold
  | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
  |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
  ||/ Name           Version             Architecture Description
  +++-==============-===================-============-=====================================================
  ii  mysql-server   8.0.22-1ubuntu20.04 amd64        MySQL Server meta package depending on latest version




```











---------------------------------------------------------------------------------------------------



  https://chrisjean.com/fix-apt-get-update-the-following-signatures-couldnt-be-verified-because-the-public-key-is-not-available/
  https://askubuntu.com/questions/291035/how-to-add-a-gpg-key-to-the-apt-sources-keyring



apt 安装 packages 时避免 自动启动
  https://serverfault.com/questions/861583/how-to-stop-nginx-from-being-automatically-started-on-install
  https://serverfault.com/questions/567474/how-can-i-install-packages-without-starting-their-associated-services
  https://askubuntu.com/questions/74061/install-packages-without-starting-background-processes-and-services

      $ sudo vim /usr/sbin/policy-rc.d
        #!/bin/sh
        exit 101
        EOF

      $ sudo chmod a+x /usr/sbin/policy-rc.d










