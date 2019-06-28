

---------------------------------------------------------------------------------------------------

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




copy 证书文件 到 openvpn server 的相应目录-----------------------------

// copy server 证书
[root@vpnserver 3]# cp pki/ca.crt /etc/openvpn/server/
[root@vpnserver 3]# cp pki/issued/vpnserver.crt /etc/openvpn/server/
[root@vpnserver 3]# cp pki/private/vpnserver.key /etc/openvpn/server/


// copy client 证书
[root@vpnserver 3]# cp pki/ca.crt /etc/openvpn/client/
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


[root@vpnserver ~]# cp /usr/share/doc/openvpn-2.4.7/sample/sample-config-files/server.conf  /etc/openvpn/server.conf







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



troubleshoot:
    linux 的 client 对于服务器端 push 的 dns 需要 额外的处理:
      http://blog.claves.me/2015/11/22/openvpn-push-dns-to-linux-client/
      https://wiki.archlinux.org/index.php/OpenVPN
      https://serverfault.com/questions/590706/openvpn-client-force-dns-server
      centos7 解决办法:
            [root@basic ~]# rpm -ql openvpn | grep client | grep pull
            /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.down
            /usr/share/doc/openvpn-2.4.7/contrib/pull-resolv-conf/client.up











