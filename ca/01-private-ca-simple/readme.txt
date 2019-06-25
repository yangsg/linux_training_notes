

---------------------------------------------------------------------------------------------------
CA 服务器端:

// 查看 CA server 信息:
[root@ca ~]# hostname   # 查看主机名
ca.xintian.com
[root@ca ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
192.168.175.110/24


// 更新 openssl
[root@ca ~]# yum -y update openssl
[root@ca ~]# rpm -q openssl
openssl-1.0.2k-16.el7_6.1.x86_64

// 查看 /etc/pki/tls/ 目录 下的 openssl.cnf 文件
[root@ca ~]# tree /etc/pki/tls/
/etc/pki/tls/
├── cert.pem -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
├── certs
│   ├── ca-bundle.crt -> /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
│   ├── ca-bundle.trust.crt -> /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
│   ├── localhost.crt
│   ├── make-dummy-cert
│   ├── Makefile
│   └── renew-dummy-cert
├── misc
│   ├── CA
│   ├── c_hash
│   ├── c_info
│   ├── c_issuer
│   └── c_name
├── openssl.cnf  <----------------  openssl 的 配置文件
└── private
    └── localhost.key


[root@ca ~]# tree /etc/pki/CA/
/etc/pki/CA/
├── certs
├── crl
├── newcerts
└── private

----------------------------------------
// 查看一下 配置文件 /etc/pki/tls/openssl.cnf 中 与 CA 相关的一部分配置(因配置太多, 此处指列出了其中一部分) 
[root@ca ~]# less /etc/pki/tls/openssl.cnf
####################################################################
[ ca ]
default_ca      = CA_default            # The default ca section

####################################################################
[ CA_default ]

dir             = /etc/pki/CA           # Where everything is kept
certs           = $dir/certs            # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several ctificates with same subject.
new_certs_dir   = $dir/newcerts         # default place for new certs.

certificate     = $dir/cacert.pem       # The CA certificate
serial          = $dir/serial           # The current serial number
crlnumber       = $dir/crlnumber        # the current crl number
                                        # must be commented out to leave a V1 CRL
crl             = $dir/crl.pem          # The current CRL
private_key     = $dir/private/cakey.pem# The private key
RANDFILE        = $dir/private/.rand    # private random number file

x509_extensions = usr_cert              # The extentions to add to the cert

# Comment out the following two lines for the "traditional"
# (and highly broken) format.
name_opt        = ca_default            # Subject Name options
cert_opt        = ca_default            # Certificate field options

# Extension copying option: use with caution.
# copy_extensions = copy

# Extensions to add to a CRL. Note: Netscape communicator chokes on V2 CRLs
# so this is commented out by default to leave a V1 CRL.
# crlnumber must also be commented out to leave a V1 CRL.
# crl_extensions        = crl_ext

default_days    = 365                   # how long to certify for
default_crl_days= 30                    # how long before next CRL
default_md      = sha256                # use SHA-256 by default
preserve        = no                    # keep passed DN ordering

略 略 略 略 略 略 略 略 略 略 略 略 略 略 略 略
----------------------------------------

// 创建 证书相关的 index.txt 和 serial 文件
[root@ca ~]# touch /etc/pki/CA/index.txt
[root@ca ~]# echo 01 > /etc/pki/CA/serial

// 为了便于保存 csr 文件, 所以自己再额外创建一个 csr 目录
[root@ca ~]# (umask 077 && mkdir /etc/pki/CA/csr)


// 创建 CA 私钥 (待会儿用户创建 自签证书)
[root@ca ~]# (umask 077 && openssl genrsa -out /etc/pki/CA/private/cakey.pem 2048)
Generating RSA private key, 2048 bit long modulus
...................................................................+++
............................+++
e is 65537 (0x10001)



// 直接 利用 私钥 创建 自签名证书 (证书请求 通过指定 -new 选项在 执行过程中 动态完成)
[root@ca ~]# openssl req -new -x509 -key /etc/pki/CA/private/cakey.pem -out /etc/pki/CA/cacert.pem -days 3650
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN     <============= 输入国家
State or Province Name (full name) []:Chongqing  <======== 输入省份
Locality Name (eg, city) [Default City]:Chongqing <============= 输入城市
Organization Name (eg, company) [Default Company Ltd]:xintian <============= 输入公司名
Organizational Unit Name (eg, section) []:xintian  <============= 输入 公司部门
Common Name (eg, your name or your server's hostname) []:ca.xintian.com  <======== 输入服务器名
Email Address []:xintian@163.com  <========= 输入邮件地址

// 创建 CA 目录
[root@ca ~]# tree /etc/pki/CA/
/etc/pki/CA/
├── cacert.pem
├── certs
├── crl
├── csr   <------ 该目录时 自己 额外创建的, 用于保存 csr 文件
├── index.txt
├── newcerts
├── private
│   └── cakey.pem
└── serial


---------------------------------------------------------------------------------------------------
web 客户端

// 创建 证书 和 私钥 存放的 目录
[root@www ~]# mkdir -p /etc/httpd/ssl/private
[root@www ~]# chmod 077 /etc/httpd/ssl/private


// 生成 私钥
[root@www ~]# (umask 077 && openssl genrsa -out /etc/httpd/ssl/private/www.xintian.com.key 2048)
Generating RSA private key, 2048 bit long modulus
...........................+++
....................................+++
e is 65537 (0x10001)



// 生成 证书请求
[root@www ~]# openssl req -new -key /etc/httpd/ssl/private/www.xintian.com.key -out /etc/httpd/ssl/www.xintian.com.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN       <============== 输入国家
State or Province Name (full name) []:Chongqing  <============= 输入省市
Locality Name (eg, city) [Default City]:Chongqing  <============= 输入城市
Organization Name (eg, company) [Default Company Ltd]:xintian  <=========== 输入公司
Organizational Unit Name (eg, section) []:xintian    <============ 输入部门
Common Name (eg, your name or your server's hostname) []:www.xintian.com  <======= 输入服务器名
Email Address []:xintian@163.com  <=========== 输入邮箱地址

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:  <============= 直接回车
An optional company name []: <============ 直接回车

// (可选操作)以防万一, 可以在生成 证书请求 后 对其 确认和验证一下:
[root@www ~]# openssl req -in /etc/httpd/ssl/www.xintian.com.csr -noout -text
[root@www ~]# openssl req  -in /etc/httpd/ssl/www.xintian.com.csr -noout -verify -key /etc/httpd/ssl/private/www.xintian.com.key


// 将 生成的 证书请求 发给 CA
[root@www ~]# rsync -av /etc/httpd/ssl/www.xintian.com.csr  root@192.168.175.110:/etc/pki/CA/csr



---------------------------------------------------------------------------------------------------

CA 服务器端

// 查看客户 发送过来的 证书申请
[root@ca ~]# ls /etc/pki/CA/csr/
www.xintian.com.csr


// 利用 证书请求 为客户 生成 证书
[root@ca ~]# openssl ca -in /etc/pki/CA/csr/www.xintian.com.csr -out /etc/pki/CA/certs/www.xintian.com.crt -days 3650
Using configuration from /etc/pki/tls/openssl.cnf
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 1 (0x1)
        Validity
            Not Before: Jun 25 08:22:48 2019 GMT
            Not After : Jun 22 08:22:48 2029 GMT
        Subject:
            countryName               = CN
            stateOrProvinceName       = Chongqing
            organizationName          = xintian
            organizationalUnitName    = xintian
            commonName                = www.xintian.com
            emailAddress              = xintian@163.com
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                EC:31:DC:44:84:07:46:FB:9B:A6:C8:36:04:B8:C5:0C:18:4D:EE:4A
            X509v3 Authority Key Identifier:
                keyid:D3:CB:E2:5E:F6:BF:9B:19:9E:C6:C6:E9:9A:69:48:A9:29:40:D1:45

Certificate is to be certified until Jun 22 08:22:48 2029 GMT (3650 days)
Sign the certificate? [y/n]:y   <============== 输入 'y'


1 out of 1 certificate requests certified, commit? [y/n]y <================ 输入 'y'
Write out database with 1 new entries
Data Base Updated


// 将 CA 生成的 证书 发给 客户
[root@ca ~]# rsync -av /etc/pki/CA/certs/www.xintian.com.crt  root@192.168.175.10:/etc/httpd/ssl/



// 查看文件 /etc/pki/CA/index.txt 内容
[root@ca ~]# cat /etc/pki/CA/index.txt
V       290622082248Z           01      unknown /C=CN/ST=Chongqing/O=xintian/OU=xintian/CN=www.xintian.com/emailAddress=xintian@163.com


// 查看文件 /etc/pki/CA/serial 内容
[root@ca ~]# cat /etc/pki/CA/serial
02


// 查看 /etc/pki/CA/newcerts/01.pem 和 /etc/pki/CA/certs/httpd.crt 的 md5sum, 可发现其是相同的
[root@ca ~]# md5sum /etc/pki/CA/newcerts/01.pem /etc/pki/CA/certs/www.xintian.com.crt
402027cfd8faf790a808ea5392e3f6a6  /etc/pki/CA/newcerts/01.pem
402027cfd8faf790a808ea5392e3f6a6  /etc/pki/CA/certs/www.xintian.com.crt



// 查看签署 证书 的信息
[root@ca ~]# openssl x509  -in /etc/pki/CA/newcerts/01.pem -noout -text | less

---------------------------------------------------------------------------------------------------
CA 端 吊销证书

// 查看 证书 的 serial 和 subject 信息
[root@ca ~]# openssl x509 -in /etc/pki/CA/newcerts/01.pem -noout -serial -subject
serial=01
subject= /C=CN/ST=Chongqing/O=xintian/OU=xintian/CN=www.xintian.com/emailAddress=xintian@163.com


// 查看 index.txt 中的信息, 确认 客户提交的 serial与subject 信息是否与 index.txt 中的信息一致
[root@ca ~]# cat /etc/pki/CA/index.txt
V       290622082248Z           01      unknown /C=CN/ST=Chongqing/O=xintian/OU=xintian/CN=www.xintian.com/emailAddress=xintian@163.com


[root@ca ~]# openssl ca -revoke /etc/pki/CA/newcerts/01.pem
Using configuration from /etc/pki/tls/openssl.cnf
Revoking Certificate 01.
Data Base Updated


// 创建 文件 /etc/pki/CA/crlnumber (第一次吊销 才需要执行此操作)
[root@ca ~]# echo 01 > /etc/pki/CA/crlnumber

// 基于 index 文件 中的 信息 生成 一个 CRL
[root@ca ~]# openssl ca -gencrl -out /etc/pki/CA/crl/crl.pem
Using configuration from /etc/pki/tls/openssl.cnf


// 查看 吊销 证书后 /etc/pki/CA/index.txt 文件的变化
[root@ca ~]# cat /etc/pki/CA/index.txt
R       290622082248Z   190625083753Z   01      unknown /C=CN/ST=Chongqing/O=xintian/OU=xintian/CN=www.xintian.com/emailAddress=xintian@163.com

// 查看 证书吊销列表
[root@ca ~]# openssl crl -in /etc/pki/CA/crl/crl.pem -noout -text




---------------------------------------------------------------------------------------------------


man ca


---------------------------------------------------------------------------------------------------
网上资料:

      https://blog.csdn.net/Eumenides_s/article/details/78040787
      https://jamielinux.com/docs/openssl-certificate-authority/index.html





