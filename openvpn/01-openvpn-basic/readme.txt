
---------------------------------------------------------------------------------------------------
关于 win7 操作系统的 openvpn 客户端软件版本兼容问题:

经实际试验,
openvpn-install-2.4.3-I601.exe 在 win7 上能正常工作,
openvpn-install-2.4.7-I606-Win7.exe 在 win7 上无法正常工作 (日志总报错: 'CreateFile failed on TAP device' 和 'OpenVPN: All TAP-Windows adapters on this system are currently in use')

所以 win7 上应使用 openvpn-install-2.4.3-I601.exe, 存了一份到百度网盘, 更名为 win7-vpn-install-2.4.3-I601.exe(因百度认为open是个敏感词汇)
    下载链接: https://pan.baidu.com/s/1RUCGxxmMriMdTuecrxZArA
    提取码:   xpw5

---------------------------------------------------------------------------------------------------

主机ip概要: 其中 网段 192.168.175.0/24 可以连接外网, 而 192.168.10.0/24 无法访问外网

ssh_server:        192.168.175.20/24  <--- ssh_server 与 vpnserver 服务搭建 并没有什么关系, 仅为演示效果用
vpnserver:  ens33: 192.168.175.110/24
            ens37: 192.168.10.110/24
vpnclient:         192.168.10.20/24

---------------------------------------------------------------------------------------------------
(可选)配置 ssh_server 路由信息:
[root@ssh_server ~]# vim /etc/sysconfig/network-scripts/route-ens33
[root@ssh_server ~]# cat /etc/sysconfig/network-scripts/route-ens33
        10.8.0.0/24 via 192.168.175.110

[root@ssh_server ~]# nmcli conn reload
[root@ssh_server ~]# nmcli conn up ens33
[root@ssh_server ~]# route -n
        Kernel IP routing table
        Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
        10.8.0.0        192.168.175.110 255.255.255.0   UG    100    0        0 ens33  <--- 注: 要能响应 虚拟网络的 主机, ssh_server 需要知道如果知道到虚拟网段的路由
        192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


---------------------------------------------------------------------------------------------------
server side:

安装软件 -----------------------------
// 更新 openssl
[root@vpnserver ~]# yum -y update openssl
[root@vpnserver ~]# rpm -q openssl
        openssl-1.0.2k-16.el7_6.1.x86_64


// 安装 openvpn 和  easy-rsa, 其中 easy-rsa 是一些小的基于 openssl 的 RSA key 管理包. 主要用于 SSL VPN 应用, 当然其也可用于构建 web 的证书 
[root@vpnserver ~]# yum install -y openvpn easy-rsa
[root@vpnserver ~]# rpm -q openvpn easy-rsa
        openvpn-2.4.7-1.el7.x86_64
        easy-rsa-3.0.3-1.el7.noarch


// 查看 一下 easy-rsa 中相关的文件
[root@vpnserver ~]# rpm -ql easy-rsa
        /usr/share/doc/easy-rsa-3.0.3
        /usr/share/doc/easy-rsa-3.0.3/COPYING.md
        /usr/share/doc/easy-rsa-3.0.3/ChangeLog
        /usr/share/doc/easy-rsa-3.0.3/README.quickstart.md    <----- 可查看基本的使用指南
        /usr/share/doc/easy-rsa-3.0.3/vars.example
        /usr/share/easy-rsa
        /usr/share/easy-rsa/3
        /usr/share/easy-rsa/3.0
        /usr/share/easy-rsa/3.0.3
        /usr/share/easy-rsa/3.0.3/easyrsa
        /usr/share/easy-rsa/3.0.3/openssl-1.0.cnf
        /usr/share/easy-rsa/3.0.3/x509-types
        /usr/share/easy-rsa/3.0.3/x509-types/COMMON
        /usr/share/easy-rsa/3.0.3/x509-types/ca
        /usr/share/easy-rsa/3.0.3/x509-types/client
        /usr/share/easy-rsa/3.0.3/x509-types/san
        /usr/share/easy-rsa/3.0.3/x509-types/server
        /usr/share/licenses/easy-rsa-3.0.3
        /usr/share/licenses/easy-rsa-3.0.3/gpl-2.0.txt




// 查看 一下目录 /usr/share/easy-rsa/
[root@vpnserver ~]# ls -lAh /usr/share/easy-rsa/
        total 0
        lrwxrwxrwx 1 root root  5 Jun 27 18:49 3 -> 3.0.3
        lrwxrwxrwx 1 root root  5 Jun 27 18:49 3.0 -> 3.0.3
        drwxr-xr-x 3 root root 62 Jun 27 18:49 3.0.3


// 查看 目录 /etc/openvpn/
[root@vpnserver ~]# ls /etc/openvpn/
        client  server



配置 Easy-RSA 3-----------------------------
[root@vpnserver ~]# cp -r /usr/share/easy-rsa /etc/openvpn/
[root@vpnserver ~]# ls /etc/openvpn/
        client  easy-rsa  server


// 查看一下 默认的 openvpn 的默认设置 (即 /usr/share/doc/easy-rsa-3.0.3/vars.example 中以字符串 ‘#set_var’ 开始的注释行)
[root@vpnserver ~]# grep set_var  /usr/share/doc/easy-rsa-3.0.3/vars.example
          # 'set_var' -- this means any set_var command that is uncommented has been
          #set_var EASYRSA        "$PWD"
          #set_var EASYRSA_OPENSSL        "openssl"
          #set_var EASYRSA_OPENSSL        "C:/Program Files/OpenSSL-Win32/bin/openssl.exe"
          #set_var EASYRSA_PKI            "$EASYRSA/pki"
          #set_var EASYRSA_DN     "cn_only"
          #set_var EASYRSA_REQ_COUNTRY    "US"
          #set_var EASYRSA_REQ_PROVINCE   "California"
          #set_var EASYRSA_REQ_CITY       "San Francisco"
          #set_var EASYRSA_REQ_ORG        "Copyleft Certificate Co"
          #set_var EASYRSA_REQ_EMAIL      "me@example.net"
          #set_var EASYRSA_REQ_OU         "My Organizational Unit"
          #set_var EASYRSA_KEY_SIZE       2048
          #set_var EASYRSA_ALGO           rsa
          #set_var EASYRSA_CURVE          secp384r1
          #set_var EASYRSA_CA_EXPIRE      3650
          #set_var EASYRSA_CERT_EXPIRE    3650
          #set_var EASYRSA_CRL_DAYS       180
          #set_var EASYRSA_NS_SUPPORT     "no"
          #set_var EASYRSA_NS_COMMENT     "Easy-RSA Generated Certificate"
          #set_var EASYRSA_TEMP_FILE      "$EASYRSA_PKI/extensions.temp"
          #set_var EASYRSA_EXT_DIR        "$EASYRSA/x509-types"
          #set_var EASYRSA_SSL_CONF       "$EASYRSA/openssl-1.0.cnf"
          #set_var EASYRSA_REQ_CN         "ChangeMe"
          #set_var EASYRSA_DIGEST         "sha256"
          #set_var EASYRSA_BATCH          ""


// 创建文件 /etc/openvpn/easy-rsa/3/vars 配置 easy-rsa, 关于配置详细描述见 /usr/share/doc/easy-rsa-3.0.3/vars.example 以及 man openvpn
[root@vpnserver ~]# cp /usr/share/doc/easy-rsa-3.0.3/vars.example /etc/openvpn/easy-rsa/3/vars
[root@vpnserver ~]# vim /etc/openvpn/easy-rsa/3/vars    # 实际中也许还有其他 感兴趣的 需要修改的 字段
          set_var EASYRSA_REQ_COUNTRY "CN"
          set_var EASYRSA_REQ_PROVINCE  "Chongqing"
          set_var EASYRSA_REQ_CITY  "Jiulongpo"
          set_var EASYRSA_REQ_ORG "xintian"
          set_var EASYRSA_REQ_EMAIL "xintain@xintain.com"
          set_var EASYRSA_REQ_OU    "xintian EASY CA"



// 查看目录 /etc/openvpn/easy-rsa/3/
[root@vpnserver ~]# ls /etc/openvpn/easy-rsa/3/
        easyrsa  openssl-1.0.cnf  vars  x509-types



构建 OpenVPN Keys-----------------------------
   基于如上 创建的 /etc/openvpn/easy-rsa/3/vars 文件 来构建 the CA key, Server 和 Client keys, DH 和 CRL PEM file.
   所有这些文件都使用 目录 /etc/openvpn/easy-rsa/3 下的 easyrsa 命令脚本 来创建.

// 切换工作目录
[root@vpnserver ~]# cd /etc/openvpn/easy-rsa/3/

// 初始化 pki 目录
[root@vpnserver 3]# ./easyrsa init-pki

        Note: using Easy-RSA configuration from: ./vars

        init-pki complete; you may now create a CA or requests.
        Your newly created PKI dir is: /etc/openvpn/easy-rsa/3/pki


// 创建 ca 的 密钥 和 证书  (注: 如果不想为 ca 证书生成 口令, 则执行 命令 `./easyrsa build-ca nopass` 即可)
[root@vpnserver 3]# ./easyrsa build-ca

          Note: using Easy-RSA configuration from: ./vars
          Generating a 2048 bit RSA private key
          ................................................................+++
          ...................+++
          writing new private key to '/etc/openvpn/easy-rsa/3/pki/private/ca.key.OGaUQKnV63'
          Enter PEM pass phrase:   <========= 输入口令 (以后为其他证书请求颁发证书时使用)
          Verifying - Enter PEM pass phrase:  <======== 输入口令
          -----
          You are about to be asked to enter information that will be incorporated
          into your certificate request.
          What you are about to enter is what is called a Distinguished Name or a DN.
          There are quite a few fields but you can leave some blank
          For some fields there will be a default value,
          If you enter '.', the field will be left blank.
          -----
          Common Name (eg: your user, host, or server name) [Easy-RSA CA]:  <=========== 直接回车

          CA creation complete and you may now import and sign cert requests.
          Your new CA certificate file for publishing is at:
          /etc/openvpn/easy-rsa/3/pki/ca.crt


// 查看 一下 CA 证书 和 私钥 的位置
[root@vpnserver 3]# find /etc/openvpn/easy-rsa/3/pki/ | grep ca
          /etc/openvpn/easy-rsa/3/pki/private/ca.key
          /etc/openvpn/easy-rsa/3/pki/ca.crt



// 生成 vpn server 的 私钥 和 证书请求
[root@vpnserver 3]# ./easyrsa gen-req vpnserver nopass

          Note: using Easy-RSA configuration from: ./vars
          Generating a 2048 bit RSA private key
          ...+++
          .............................................................................................................................+++
          writing new private key to '/etc/openvpn/easy-rsa/3/pki/private/vpnserver.key.4bgj2BG1M1'
          -----
          You are about to be asked to enter information that will be incorporated
          into your certificate request.
          What you are about to enter is what is called a Distinguished Name or a DN.
          There are quite a few fields but you can leave some blank
          For some fields there will be a default value,
          If you enter '.', the field will be left blank.
          -----
          Common Name (eg: your user, host, or server name) [vpnserver]:  <======= 直接回车

          Keypair and certificate request completed. Your files are:
          req: /etc/openvpn/easy-rsa/3/pki/reqs/vpnserver.req
          key: /etc/openvpn/easy-rsa/3/pki/private/vpnserver.key



// 利用 CA 证书 为 vpnserver 签署证书请求, 即 生成证书
[root@vpnserver 3]# ./easyrsa sign-req server vpnserver

          Note: using Easy-RSA configuration from: ./vars


          You are about to sign the following certificate.
          Please check over the details shown below for accuracy. Note that this request
          has not been cryptographically verified. Please be sure it came from a trusted
          source or that you have verified the request checksum with the sender.

          Request subject, to be signed as a server certificate for 3650 days:

          subject=
              commonName                = vpnserver


          Type the word 'yes' to continue, or any other input to abort.
            Confirm request details: yes    <============== 输入 'yes'
          Using configuration from ./openssl-1.0.cnf
          Enter pass phrase for /etc/openvpn/easy-rsa/3/pki/private/ca.key: <======== 输入 CA 口令
          Check that the request matches the signature
          Signature ok
          The Subject's Distinguished Name is as follows
          commonName            :ASN.1 12:'vpnserver'
          Certificate is to be certified until Jun 24 11:51:22 2029 GMT (3650 days)

          Write out database with 1 new entries
          Data Base Updated

          Certificate created at: /etc/openvpn/easy-rsa/3/pki/issued/vpnserver.crt



// 验证 一下 证书 vpnserver.crt
[root@vpnserver 3]# openssl verify -CAfile pki/ca.crt pki/issued/vpnserver.crt
          pki/issued/vpnserver.crt: OK


// 查看 一下  vpnserver.key 相关证书 等 文件位置
[root@vpnserver 3]# find /etc/openvpn/easy-rsa/3/pki/ | grep vpnserver
          /etc/openvpn/easy-rsa/3/pki/private/vpnserver.key
          /etc/openvpn/easy-rsa/3/pki/reqs/vpnserver.req
          /etc/openvpn/easy-rsa/3/pki/issued/vpnserver.crt



构建Client Key-----------------------------

// 生成 'vpnclient01' 的 证书请求
[root@vpnserver 3]# ./easyrsa gen-req vpnclient01 nopass

        Note: using Easy-RSA configuration from: ./vars
        Generating a 2048 bit RSA private key
        ..............................................+++
        .......+++
        writing new private key to '/etc/openvpn/easy-rsa/3/pki/private/vpnclient01.key.6SgtC64G1K'
        -----
        You are about to be asked to enter information that will be incorporated
        into your certificate request.
        What you are about to enter is what is called a Distinguished Name or a DN.
        There are quite a few fields but you can leave some blank
        For some fields there will be a default value,
        If you enter '.', the field will be left blank.
        -----
        Common Name (eg: your user, host, or server name) [vpnclient01]:  <========== 直接回车

        Keypair and certificate request completed. Your files are:
        req: /etc/openvpn/easy-rsa/3/pki/reqs/vpnclient01.req
        key: /etc/openvpn/easy-rsa/3/pki/private/vpnclient01.key


// 使用 CA 证书 为 client01 办法证书
[root@vpnserver 3]# ./easyrsa sign-req client vpnclient01

        Note: using Easy-RSA configuration from: ./vars


        You are about to sign the following certificate.
        Please check over the details shown below for accuracy. Note that this request
        has not been cryptographically verified. Please be sure it came from a trusted
        source or that you have verified the request checksum with the sender.

        Request subject, to be signed as a client certificate for 3650 days:

        subject=
            commonName                = vpnclient01


        Type the word 'yes' to continue, or any other input to abort.
          Confirm request details: yes   <========== 输入 'yes'
        Using configuration from ./openssl-1.0.cnf
        Enter pass phrase for /etc/openvpn/easy-rsa/3/pki/private/ca.key: <========== 输入 ca 口令
        Check that the request matches the signature
        Signature ok
        The Subject's Distinguished Name is as follows
        commonName            :ASN.1 12:'vpnclient01'
        Certificate is to be certified until Jun 24 12:04:06 2029 GMT (3650 days)

        Write out database with 1 new entries
        Data Base Updated

        Certificate created at: /etc/openvpn/easy-rsa/3/pki/issued/vpnclient01.crt



// 验证 一下 证书 vpnclient01.crt
[root@vpnserver 3]# openssl verify -CAfile pki/ca.crt pki/issued/vpnclient01.crt
        pki/issued/vpnclient01.crt: OK



// 生成 Diffie-Hellman 密钥交换协议参数 ( p 和 g )
[root@vpnserver 3]# ./easyrsa gen-dh       # 该命令执行会花几秒中时间(主要与熵池有关), 如果觉得慢,可以用 rng-tools 来解决熵池的问题

        Note: using Easy-RSA configuration from: ./vars
        Generating DH parameters, 2048 bit long safe prime, generator 2
        This is going to take a long time
        ..............................................................................................................................+..................................+.....................................................................................................+......................................+........+...............................................................................................................................................................................................................................................................+...........+...............................................................................+.........................................................................................................................................................+..........................................................+........................................+..................................+..................................................................................................+...........................................................................+..+...+........................................+....................................................................................................+.............+.....................................................+.............................+...........................+.................................................................................................................................+...........................................................................................................................................................................................................................................+.........................+.............................+.............................................................................................................................................................................................................................................+................................+..........................................................................................................................................................+................................................................................................................................................................+...........................+.....................+................................................................+.................................+....................................................................................................................................................................................................+................................................................................................................+.......................................+...............................................................................................................................................+........................................+.......................+.....................................++*++*

        DH parameters of size 2048 created at /etc/openvpn/easy-rsa/3/pki/dh.pem




(可选操作)生成证书吊销列表 crl (见 /usr/share/doc/easy-rsa-3.0.3/README.quickstart.md ) -----------------------------


// 生成 证书吊销列表 (如果不执行此操作, 后面 vpn server 的配置中也不用对其配置了)
[root@vpnserver 3]# ./easyrsa gen-crl

        Note: using Easy-RSA configuration from: ./vars
        Using configuration from ./openssl-1.0.cnf
        Enter pass phrase for /etc/openvpn/easy-rsa/3/pki/private/ca.key:  <======== 输入 ca 口令

        An updated CRL has been created.
        CRL file: /etc/openvpn/easy-rsa/3/pki/crl.pem

// 生成 一段 随机秘钥 作为共享密钥(增强信道安全性), 该文件需要 使用预先存在的安全信道(如 scp, rsync工具拷贝)与 对等方(peer) 共享此文件
[root@vpnserver ~]# openvpn --genkey --secret /etc/openvpn/myvpn_shared_secret_key.tlsauth




copy 证书文件 到 openvpn server 的相应目录-----------------------------

// copy server 证书
[root@vpnserver 3]# cp pki/ca.crt /etc/openvpn/server/
[root@vpnserver ~]# cp /etc/openvpn/myvpn_shared_secret_key.tlsauth  /etc/openvpn/server/
[root@vpnserver 3]# cp pki/issued/vpnserver.crt /etc/openvpn/server/
[root@vpnserver 3]# cp pki/private/vpnserver.key /etc/openvpn/server/


// copy client 证书
[root@vpnserver 3]# cp pki/ca.crt /etc/openvpn/client/
[root@vpnserver ~]# cp /etc/openvpn/myvpn_shared_secret_key.tlsauth  /etc/openvpn/client/
[root@vpnserver 3]# cp pki/issued/vpnclient01.crt /etc/openvpn/client/
[root@vpnserver 3]# cp pki/private/vpnclient01.key /etc/openvpn/client/

// copy DH and CRL Key.
[root@vpnserver 3]# cp pki/dh.pem /etc/openvpn/server/
[root@vpnserver 3]# cp pki/crl.pem /etc/openvpn/server/





配置 Configure OpenVPN-----------------------------
[root@vpnserver 3]# cd

[root@vpnserver ~]# rpm -ql openvpn | grep server
        /etc/openvpn/server
        /run/openvpn-server
        /usr/lib/systemd/system/openvpn-server@.service
        /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/loopback-server
        /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/roadwarrior-server.conf
        /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/server.conf   <--------- 注意该示例配置文件
        /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/xinetd-server-config

// 先 看一看 默认的 设置 (后续再根据需要 修改 或 补充, 参数的叫详细解释 见 man openvpn 或 其他参考资料)
[root@vpnserver ~]# grep -E '^[^#;]' /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/server.conf
          port 1194
          proto udp
          dev tun
          ca ca.crt
          cert server.crt
          key server.key  # This file should be kept secret
          dh dh2048.pem
          server 10.8.0.0 255.255.255.0
          ifconfig-pool-persist ipp.txt
          keepalive 10 120
          tls-auth ta.key 0 # This file is secret
          cipher AES-256-CBC
          persist-key
          persist-tun
          status openvpn-status.log
          verb 3
          explicit-exit-notify 1


// 创建 /etc/openvpn/server.conf 并 根据需要对其设置 进行 修改 和 补充
[root@vpnserver ~]# cp /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/server.conf  /etc/openvpn/server.conf
[root@vpnserver ~]# vim /etc/openvpn/server.conf

      ca /etc/openvpn/server/ca.crt
      cert /etc/openvpn/server/vpnserver.crt
      key /etc/openvpn/server/vpnserver.key  # This file should be kept secret

      dh /etc/openvpn/server/dh.pem

      ## 证书吊销列表
      crl-verify /etc/openvpn/server/crl.pem

      server 10.8.0.0 255.255.255.0   # 注: 不能与内网现有的任何网段冲突

      push "route 0.0.0.0 0.0.0.0"  # 指定 client 端允许访问那些网段的主机(此例中允许其访问所有网段)

      push "redirect-gateway def1 bypass-dhcp"

      push "dhcp-option DNS 8.8.8.8"  # 指定 client端使用的主 DNS, 此例中为 Google提供的免费DNS服务器: 主: 8.8.8.8, 备用: 8.8.4.4
      push "dhcp-option DNS 8.8.4.4"  # 指定 client端使用的备份 DNS

      ;tls-auth ta.key 0 # This file is secret
      tls-crypt /etc/openvpn/server/myvpn_shared_secret_key.tlsauth  #(增强安全性) 加密和认证 所有控制 信道的 packets. 比起 tls-auth, tls-crypt 增加了加密 TLS control channel的功能

      tls-version-min 1.2  # 设置 tls 的最低版本为 1.2 (因为其最低版本默认值为 1)

      compress lz4-v2         # 启用服务器端在 vpn 链路 上的 lz4-v2 压缩功能, 该功能需要 openvpn v2.4+ 的支持
      push "compress lz4-v2"  # 同时将 lz4-v2 压缩功能的启用设置 推送给 client端, 该功能需要 openvpn v2.4+ 的支持

      user nobody    # 在 初始化 之后 以 非特权user 'nobody' 运行
      group nobody   # 在 初始化 之后 以 非特权group 'nobody' 运行

      log-append  /var/log/openvpn.log   # 记录日志, 选项 log-append 用于每次启动 openvpn后 追加 log 信息, 而不是像选项 log 那样先 truncate 再写入



// 查看一下 openvpn 提供的 systemd unit service file 文件
[root@vpnserver ~]# rpm -ql openvpn | grep service
        /usr/lib/systemd/system/openvpn-client@.service
        /usr/lib/systemd/system/openvpn-server@.service
        /usr/lib/systemd/system/openvpn@.service


// 查看一下 文件 /usr/lib/systemd/system/openvpn@.service 的内容
[root@vpnserver ~]# cat /usr/lib/systemd/system/openvpn@.service
          [Unit]
          Description=OpenVPN Robust And Highly Flexible Tunneling Application On %I
          After=network.target

          [Service]
          Type=notify
          PrivateTmp=true
          ExecStart=/usr/sbin/openvpn --cd /etc/openvpn/ --config %i.conf

          [Install]
          WantedBy=multi-user.target

// 启动 openvpn 服务 并 设置为 开机自启
[root@vpnserver ~]# systemctl start openvpn@server
[root@vpnserver ~]# systemctl enable openvpn@server
        Created symlink from /etc/systemd/system/multi-user.target.wants/openvpn@server.service to /usr/lib/systemd/system/openvpn@.service.




// 查看一下 启动 unit service 的状态信息
[root@vpnserver ~]# systemctl status openvpn@server
        ● openvpn@server.service - OpenVPN Robust And Highly Flexible Tunneling Application On server
           Loaded: loaded (/usr/lib/systemd/system/openvpn@.service; enabled; vendor preset: disabled)
           Active: active (running) since Fri 2019-06-28 14:00:02 CST; 4min 55s ago
         Main PID: 2016 (openvpn)
           Status: "Initialization Sequence Completed"
           CGroup: /system.slice/system-openvpn.slice/openvpn@server.service
                   └─2016 /usr/sbin/openvpn --cd /etc/openvpn/ --config server.conf

        Jun 28 14:00:02 vpnserver.xintian.com systemd[1]: Starting OpenVPN Robust And Highly Flexible Tunneling Application On server...
        Jun 28 14:00:02 vpnserver.xintian.com systemd[1]: Started OpenVPN Robust And Highly Flexible Tunneling Application On server.


// 查看 一下 日志信息:
[root@vpnserver ~]# cat /var/log/openvpn.log
      Fri Jun 28 14:00:02 2019 OpenVPN 2.4.7 x86_64-redhat-linux-gnu [Fedora EPEL patched] [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Feb 20 2019
      Fri Jun 28 14:00:02 2019 library versions: OpenSSL 1.0.2k-fips  26 Jan 2017, LZO 2.06
      Fri Jun 28 14:00:02 2019 Diffie-Hellman initialized with 2048 bit key
      Fri Jun 28 14:00:02 2019 Outgoing Control Channel Encryption: Cipher 'AES-256-CTR' initialized with 256 bit key
      Fri Jun 28 14:00:02 2019 Outgoing Control Channel Encryption: Using 256 bit message hash 'SHA256' for HMAC authentication
      Fri Jun 28 14:00:02 2019 Incoming Control Channel Encryption: Cipher 'AES-256-CTR' initialized with 256 bit key
      Fri Jun 28 14:00:02 2019 Incoming Control Channel Encryption: Using 256 bit message hash 'SHA256' for HMAC authentication
      Fri Jun 28 14:00:02 2019 ROUTE_GATEWAY 192.168.175.2/255.255.255.0 IFACE=ens33 HWADDR=00:0c:29:82:ac:0f
      Fri Jun 28 14:00:02 2019 TUN/TAP device tun0 opened
      Fri Jun 28 14:00:02 2019 TUN/TAP TX queue length set to 100
      Fri Jun 28 14:00:02 2019 /sbin/ip link set dev tun0 up mtu 1500
      Fri Jun 28 14:00:02 2019 /sbin/ip addr add dev tun0 local 10.8.0.1 peer 10.8.0.2
      Fri Jun 28 14:00:02 2019 /sbin/ip route add 10.8.0.0/24 via 10.8.0.2
      Fri Jun 28 14:00:02 2019 Could not determine IPv4/IPv6 protocol. Using AF_INET
      Fri Jun 28 14:00:02 2019 Socket Buffers: R=[212992->212992] S=[212992->212992]
      Fri Jun 28 14:00:02 2019 UDPv4 link local (bound): [AF_INET][undef]:1194
      Fri Jun 28 14:00:02 2019 UDPv4 link remote: [AF_UNSPEC]
      Fri Jun 28 14:00:02 2019 GID set to nobody
      Fri Jun 28 14:00:02 2019 UID set to nobody
      Fri Jun 28 14:00:02 2019 MULTI: multi_init called, r=256 v=256
      Fri Jun 28 14:00:02 2019 IFCONFIG POOL: base=10.8.0.4 size=62, ipv6=0
      Fri Jun 28 14:00:02 2019 IFCONFIG POOL LIST
      Fri Jun 28 14:00:02 2019 Initialization Sequence Completed

// 查看 一下 网络端口
[root@vpnserver ~]# netstat -anptu | grep openvpn
      udp        0      0 0.0.0.0:1194            0.0.0.0:*                           2016/openvpn

// 查看 自动 新添加的 网卡
[root@vpnserver 01-openvpn-basic]# ip addr show tun0
      4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN qlen 100
          link/none
          inet 10.8.0.1 peer 10.8.0.2/32 scope global tun0
             valid_lft forever preferred_lft forever
          inet6 fe80::80f5:305c:acc5:63bd/64 scope link flags 800
             valid_lft forever preferred_lft forever


---------------------------------------------------------------------------------------------------
vpnserver 的 网络配置

// 启用 路由 转发功能
[root@vpnserver ~]# vim /etc/sysctl.conf
      net.ipv4.ip_forward = 1
[root@vpnserver ~]# sysctl -p   # 加载配置文件 /etc/sysctl.conf
      net.ipv4.ip_forward = 1

# 查看 路由转发设置 结果
[root@vpnserver ~]# cat /proc/sys/net/ipv4/ip_forward
      1

# ping 一下 百度
[root@vpnclient ~]# ping www.baidu.com
        PING www.baidu.com (61.135.169.121) 56(84) bytes of data.
        64 bytes from www.baidu.com (61.135.169.121): icmp_seq=2 ttl=127 time=5.19 ms
        64 bytes from www.baidu.com (61.135.169.121): icmp_seq=3 ttl=127 time=4.55 ms


# 配置 snat ( 其实 MASQUERADE 就是 动态的 snat)
[root@vpnserver ~]# iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -j MASQUERADE   #注: TODO: 记得持久化 设置 snat (这里我偷懒 就暂时 不设置了)

---------------------------------------------------------------------------------------------------
client side (此例为 centos7 作为客户端, 不同的 linux 解决 pull dns 问题时 up 和 down 的配置文件路径可能不同):

[root@vpnclient ~]# yum -y install openvpn
[root@vpnclient ~]# rpm -q openvpn
      openvpn-2.4.7-1.el7.x86_64


// 查看一下 openvpn 总 与 client 相关的文件
[root@vpnclient ~]# rpm -ql openvpn | grep client
/etc/openvpn/client
/run/openvpn-client
/usr/lib/systemd/system/openvpn-client@.service
/usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.down  <-------
/usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.up    <-------
/usr/share/doc/openvpn-2.4.7/sample/sample-config-files/client.conf  <------
/usr/share/doc/openvpn-2.4.7/sample/sample-config-files/loopback-client
/usr/share/doc/openvpn-2.4.7/sample/sample-config-files/roadwarrior-client.conf
/usr/share/doc/openvpn-2.4.7/sample/sample-config-files/xinetd-client-config


// copy  client 端相关 的 证书文件 到其 相应的目录下
[root@vpnserver ~]# rsync -av /etc/openvpn/client/{ca.crt,vpnclient01.crt,vpnclient01.key,myvpn_shared_secret_key.tlsauth} root@192.168.10.20:/etc/openvpn/client/
[root@vpnclient ~]# ls /etc/openvpn/client
        ca.crt  myvpn_shared_secret_key.tlsauth  vpnclient01.crt  vpnclient01.key


// centos7 作为 openvpn 客户端时 需要执行如下 4 行 命令(因为要解决 pull dns 的问题)
[root@vpnclient ~]# cp /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.up    /etc/openvpn/
[root@vpnclient ~]# cp /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.down  /etc/openvpn/
[root@vpnclient ~]# chmod +x /etc/openvpn/client.up
[root@vpnclient ~]# chmod +x /etc/openvpn/client.down



// 查看下一 openvpn 示例 客户端 配置文件 的默认设置
[root@vpnclient ~]# grep -E '^[^#;]' /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/client.conf
          client
          dev tun
          proto udp
          remote my-server-1 1194
          resolv-retry infinite
          nobind
          persist-key
          persist-tun
          ca ca.crt
          cert client.crt
          key client.key
          remote-cert-tls server
          tls-auth ta.key 1
          cipher AES-256-CBC
          verb 3



// 创建 openvpn 的 client 端配置文件 /etc/openvpn/client.conf  并 根据需要 对其中的某些 设置进行 修改 或 补充
[root@vpnclient ~]# cp /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/client.conf  /etc/openvpn/client.conf
[root@vpnclient ~]# vim /etc/openvpn/client.conf

        # 如下 3 行 设置是为解决 centos7 作为 openvpn 客户端 的 pull dns 的问题 (linux作为客户端基本都存在这种问题)
        # 注: 这里没有使用
        # plugin openvpn-plugin-down-root.so  "/etc/openvpn/client.down" 以及 user nobody 和 group nobody 的设置,
        # 因为 实际测试 在 centos7 中 openvpn-plugin-down-root.so 并没有起效果(从而导致无法还原 DNS 设置)
        script-security 2
        up /etc/openvpn/client.up
        down /etc/openvpn/client.down

        remote 192.168.10.110 1194   # 指定 vpnserver 地址

        ca /etc/openvpn/client/ca.crt
        cert /etc/openvpn/client/vpnclient01.crt
        key /etc/openvpn/client/vpnclient01.key

        ;tls-auth ta.key 1
        tls-crypt /etc/openvpn/client/myvpn_shared_secret_key.tlsauth  #(增强安全性) 加密和认证 所有控制 信道的 packets. 比起 tls-auth, tls-crypt 增加了加密 TLS control channel的功能

        tls-version-min 1.2  # 设置 tls 的最低版本为 1.2 (因为其最低版本默认值为 1)



[root@vpnclient ~]# systemctl start openvpn@client
[root@vpnclient ~]# systemctl enable openvpn@client
      Created symlink from /etc/systemd/system/multi-user.target.wants/openvpn@client.service to /usr/lib/systemd/system/openvpn@.service.

[root@vpnclient ~]# ip addr show tun0
      3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN qlen 100
          link/none
          inet 10.8.0.6 peer 10.8.0.5/32 scope global tun0
             valid_lft forever preferred_lft forever
          inet6 fe80::fbf2:99ff:a8aa:bfd6/64 scope link flags 800
             valid_lft forever preferred_lft forever


// 查看 一下 dns 设置
[root@vpnclient ~]# cat /etc/resolv.conf
      # resolv.conf autogenerated by /etc/openvpn/client.up (tun0)
      nameserver 8.8.8.8  <------ 可以发现, 已经成功 设置了 vpnserver 端 push 过来的 dns 了
      nameserver 8.8.4.4


// ping 一下 vpnserver 在 虚拟网 中的 ip 地址
[root@vpnclient ~]# ping 10.8.0.1
      PING 10.8.0.1 (10.8.0.1) 56(84) bytes of data.
      64 bytes from 10.8.0.1: icmp_seq=1 ttl=64 time=0.669 ms
      64 bytes from 10.8.0.1: icmp_seq=2 ttl=64 time=0.480 ms


// 使用命令 `route -n` 查看一下 vpn 客户端的 路由信息
[root@vpnclient ~]# route -n
      Kernel IP routing table
      Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
      0.0.0.0         10.8.0.5        0.0.0.0         UG    0      0        0 tun0
      10.8.0.1        10.8.0.5        255.255.255.255 UGH   0      0        0 tun0
      10.8.0.5        0.0.0.0         255.255.255.255 UH    0      0        0 tun0
      192.168.10.0    0.0.0.0         255.255.255.0   U     100    0        0 ens33
// 使用命令 `ip route` 查看一下 vpn 客户端的 路由信息
[root@vpnclient ~]# ip route
      default via 10.8.0.5 dev tun0
      10.8.0.1 via 10.8.0.5 dev tun0
      10.8.0.5 dev tun0 proto kernel scope link src 10.8.0.6
      192.168.10.0/24 dev ens33 proto kernel scope link src 192.168.10.20 metric 100



// 关闭 客户端的 openvpn, 查看 路由信息 和 dns 信息是否还原
[root@vpnclient ~]# systemctl stop openvpn@client
[root@vpnclient ~]# route -n
      Kernel IP routing table
      Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
      192.168.10.0    0.0.0.0         255.255.255.0   U     100    0        0 ens33  <------ 可以看到, 路由表已经还原
[root@vpnclient ~]# cat /etc/resolv.conf
      # Generated by NetworkManager
      search xintian.com
      nameserver 192.168.10.2  <------ 可以看到, dns设置已经还原

// 查看 网络连接 设置
[root@vpnclient ~]# nmcli conn show
      NAME   UUID                                  TYPE            DEVICE
      ens33  c96bc909-188e-ec64-3a96-6a90982b08ad  802-3-ethernet  ens33  <---- 也已经还原, 即没有了 device 'tun0'  对应的connection 了



---------------------------------------------------------------------------------------------------
测试:

// 测试: ping 一下 ssh_server
[root@vpnclient ~]# ping 192.168.175.20
        PING 192.168.175.20 (192.168.175.20) 56(84) bytes of data.
        64 bytes from 192.168.175.20: icmp_seq=1 ttl=63 time=1.04 ms
        64 bytes from 192.168.175.20: icmp_seq=2 ttl=63 time=0.742 ms

// ssh 远程 连接 ssh_server 试试
[root@vpnclient ~]# ssh root@192.168.175.20

// 查看 ssh_server 的网络连接信息
[root@ssh_server ~]# netstat -anptu | grep sshd
      tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      868/sshd
      tcp        0      0 192.168.175.20:22       10.8.0.6:55234          ESTABLISHED 1280/sshd: root@pts <--------- 注意使用的是 vpnclient 的虚拟 ip: 10.8.0.6
      tcp6       0      0 :::22                   :::*                    LISTEN      868/sshd



---------------------------------------------------------------------------------------------------
client size (win7 操作系统), 假设 openvpn-install-2.4.3-I601.exe 安装路径为目录 C:\Program Files\OpenVPN\

// copy vpnserver 上 如下 4 个文件 到 C:\Program Files\OpenVPN\config (即 openvpn 客户端安装目录下的 config)
          /etc/openvpn/client/ca.crt
          /etc/openvpn/client/vpnclient01.crt
          /etc/openvpn/client/vpnclient01.key
          /etc/openvpn/client/myvpn_shared_secret_key.tlsauth

// 将 vpnclient(centos7的 openvpn 客户端) 上的 /etc/openvpn/client.conf 修改 后 copy 到 win7 系统 openvpn 安装目录下的 config 目录,
   并将其 更名 为 client.ovpn, 注: 修改的内容如下:
                    # 删除(或注释)如下 几行配置即可,因为相对于centos7 vpnclient 而言, win7 vpnclient 不需要这几行配置
                    script-security 2             <---- win7 不需要
                    up /etc/openvpn/client.up     <---- win7 不需要
                    down /etc/openvpn/client.down <---- win7 不需要

                    user nobody    # 在 初始化 之后 以 非特权user 'nobody' 运行  <---- win7 不需要
                    group nobody   # 在 初始化 之后 以 非特权group 'nobody' 运行 <---- win7 不需要

                    (可选)如果愿意, 可以使用 unix2dos 命令将 client.ovpn 转换一下再放到 win7 对应的目录下, 方便 win7 的记事本文本编辑器打开查看

    最后启动 openvpn 客户端 并 执行 连接 操作即可

---------------------------------------------------------------------------------------------------
网上资料:

    https://baike.baidu.com/item/%E8%99%9A%E6%8B%9F%E4%B8%93%E7%94%A8%E7%BD%91%E7%BB%9C/8747869?fromtitle=VPN&fromid=382304&fr=aladdin
    https://baike.baidu.com/item/ssl/320778?fr=aladdin
    https://baike.baidu.com/item/TLS/2979545?fr=aladdin


各种安装 openvpn 的资料:
    https://www.howtoforge.com/tutorial/how-to-install-openvpn-server-and-client-with-easy-rsa-3-on-centos-7/
    https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-an-openvpn-server-on-centos-7
    https://www.vpsserver.com/community/tutorials/7/setup-and-configuration-of-openvpn-server-on-centos-7-2/
    https://linuxize.com/post/how-to-set-up-an-openvpn-server-on-centos-7/#prerequisites
    https://www.vultr.com/docs/installing-openvpn-on-centos-7
    https://www.cyberciti.biz/faq/centos-7-0-set-up-openvpn-server-in-5-minutes/
    https://www.linux.com/blog/how-install-openvpn-centos-7


    https://www.rosehosting.com/blog/how-to-install-openvpn-on-centos-7/
    https://kifarunix.com/install-and-setup-openvpn-server-on-fedora-29-centos-7/

    https://security.stackexchange.com/questions/123160/how-to-specifiy-capath-using-openssl-in-windows-to-perform-tls-handshake

    中文安装:
        https://www.dwhd.org/20160614_044415.html

Diffie-Hellman密钥交换协议/算法
    https://baike.baidu.com/item/Diffie-Hellman/9827194?fr=aladdin
    https://wiki.openssl.org/index.php/Diffie_Hellman
    https://wiki.openssl.org/index.php/Diffie-Hellman_parameters
    https://www.cnblogs.com/hyddd/p/7689132.html
    https://www.cnblogs.com/f-ck-need-u/p/7103791.html
    https://www.cnblogs.com/qcblog/p/9016704.html


https://openvpn.net/


------------------------------------------
troubleshoot:
    linux 的 client 对于服务器端 push 的 dns 需要 额外的处理:
      http://blog.claves.me/2015/11/22/openvpn-push-dns-to-linux-client/
      https://wiki.archlinux.org/index.php/OpenVPN
      https://serverfault.com/questions/590706/openvpn-client-force-dns-server
      centos7 解决办法:
            [root@basic ~]# rpm -ql openvpn | grep client | grep pull
                    /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.down
                    /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.up

            [root@vpnclient ~]# cp /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.up    /etc/openvpn/
            [root@vpnclient ~]# cp /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.down  /etc/openvpn/
            [root@vpnclient ~]# chmod +x /etc/openvpn/client.up
            [root@vpnclient ~]# chmod +x /etc/openvpn/client.down


            [root@vpnclient ~]# vim /etc/openvpn/client.conf

                    # 如下 3 行 设置是为解决 centos7 作为 openvpn 客户端 的 pull dns 的问题 (linux作为客户端基本都存在这种问题)
                    # 注: 这里没有使用
                    # plugin openvpn-plugin-down-root.so  "/etc/openvpn/client.down" 以及 user nobody 和 group nobody 的设置,
                    # 因为 实际测试 在 centos7 中 openvpn-plugin-down-root.so 并没有起效果(从而导致无法还原 DNS 设置)
                    script-security 2
                    up /etc/openvpn/client.up
                    down /etc/openvpn/client.down

------------------------------------------

