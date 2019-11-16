


----------------------------------------------------------------------------------------------------
linux namespaces
    https://www.jianshu.com/p/2a14fe583cdf
    https://en.wikipedia.org/wiki/Linux_namespaces
    https://www.learnsteps.com/how-containers-isolate-processes-using-linux-namespaces/
    https://leftasexercise.com/2018/04/12/docker-internals-process-isolation-with-namespaces-and-cgroups/
    https://www.toptal.com/linux/separation-anxiety-isolating-your-system-with-linux-namespaces



[root@node01 ~]# uname -r
    3.10.0-693.el7.x86_64   版本大于 3.8


----------------------------------------------------------------------------------------------------
master  (2 核 3G)
  192.168.175.101    vlnx175101.k8.com    kube-apiserver kube-controller-manager kube-scheduler

node (2, 1G)
  192.168.175.101    vlnx175101.k8.com    node kubelet kube-porxy flannel etcd
  192.168.175.102    vlnx175102.k8.com    node kubelet kube-proxy flannel etcd
  192.168.175.103    vlnx175103.k8.com    node kubelet kube-proxy flannel etcd


----------------------------------------------------------------------------------------------------
前期准备:

  时间同步
  防火墙
  selinux
  /etc/hosts
  yum 的 epel 源
  yum update


[root@vlnx175101 ~]# cat /etc/hosts
    127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
    ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6


    192.168.175.101    vlnx175101.k8.com  vlnx175101
    192.168.175.102    vlnx175102.k8.com  vlnx175102
    192.168.175.103    vlnx175103.k8.com  vlnx175103

----------------------------------------------------------------------------------------------------
在node节点上安装docker

[root@vlnx175101 ~]# wget -O /etc/yum.repos.d/docker-ce.repo   https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
[root@vlnx175101 ~]# yum -y install docker-ce
[root@vlnx175101 ~]# rpm -q docker-ce
    docker-ce-19.03.5-3.el7.x86_64


----------------------------------------------------------------------------------------------------
创建证书

创建 etcd 高可用集群

创建 kubeconfig 文件 (kubectl 使用)

部署 master 节点

部署 node 节点



----------------------------------------------------------------------------------------------------
创建证书


安装 CFSSL
直接使用二进制源码包安装

[root@vlnx175103 ~]# vim a.sh

    mkdir -p local/bin

    wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
    chmod +x cfssl_linux-amd64
    mv cfssl_linux-amd64 /root/local/bin/cfssl


    wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
    chmod +x cfssljson_linux-amd64
    mv cfssljson_linux-amd64 /root/local/bin/cfssljson


    wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
    chmod +x cfssl-certinfo_linux-amd64
    mv cfssl-certinfo_linux-amd64 /root/local/bin/cfssl-certinfo


[root@vlnx175101 ~]# ls ./local/bin/
    cfssl  cfssl-certinfo  cfssljson

[root@vlnx175101 ~]# export PATH=/root/local/bin:$PATH



创建CA (Certificate Authority)
创建 CA 配置文件`
[root@vlnx175101 ~]# mkdir /root/ssl
[root@vlnx175101 ~]# cd /root/ssl
[root@vlnx175101 ssl]# cfssl print-defaults config > config.json
[root@vlnx175101 ssl]# cfssl print-defaults csr > csr.json

[root@vlnx175101 ssl]# ls
    config.json  csr.json


// 观察一些 配置内容
[root@vlnx175101 ssl]# cat config.json
    {
        "signing": {
            "default": {
                "expiry": "168h"
            },
            "profiles": {
                "www": {
                    "expiry": "8760h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "server auth"
                    ]
                },
                "client": {
                    "expiry": "8760h",
                    "usages": [
                        "signing",
                        "key encipherment",
                        "client auth"
                    ]
                }
            }
        }
    }

[root@vlnx175101 ssl]# cat csr.json

    {
        "CN": "example.net",
        "hosts": [
            "example.net",
            "www.example.net"
        ],
        "key": {
            "algo": "ecdsa",
            "size": 256
        },
        "names": [
            {
                "C": "US",
                "L": "CA",
                "ST": "San Francisco"
            }
        ]
    }

# 根据config.json文件的格式创建如下的ca-config.json文件
# 过期时间设置成了 87600h
[root@vlnx175101 ssl]# vim ca-config.json

    {
         "signing": {
           "default": {
             "expiry": "8760h"
           },
           "profiles": {
             "kubernetes": {
               "usages": [
                   "signing",
                   "key encipherment",
                   "server auth",
                   "client auth"
               ],
               "expiry": "8760h"
             }
          }
       }
    }


创建CA证书签名请求
[root@vlnx175101 ssl]# vim ca-csr.json

    {
        "CN": "kubernetes",
        "key": {
            "algo": "rsa",
            "size": 2048
        },
        "names": [ {
            "C": "CN",
            "ST": "BeiJing",
            "L": "BeiJing",
            "O": "k8s",
            "OU": "System"
        } ]
    }


生成CA证书和私钥
[root@vlnx175101 ssl]# cfssl gencert -initca ca-csr.json | cfssljson -bare ca
[root@vlnx175101 ssl]# ls -1
    ca-config.json
    ca.csr        <---
    ca-csr.json
    ca-key.pem    <---
    ca.pem        <---
    config.json
    csr.json


创建kubernetes证书
创建 kubernetes证书签名请求
[root@vlnx175101 ssl]# vim kubernetes-csr.json

    {
        "CN": "kubernetes",
        "hosts": [
          "127.0.0.1",
          "192.168.175.101",
          "192.168.175.102",
          "192.168.175.103",
          "10.254.0.1",
          "kubernetes",
          "kubernetes.default",
          "kubernetes.default.svc",
          "kubernetes.default.svc.cluster",
          "kubernetes.default.svc.cluster.local"
         ],
        "key": {
            "algo": "rsa",
            "size": 2048
        },
        "names": [ {
            "C": "CN",
            "ST": "BeiJing",
            "L": "BeiJing",
            "O": "k8s",
            "OU": "System"
        } ]
    }


生成kubernetes证书和私钥
[root@vlnx175101 ssl]# cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes kubernetes-csr.json | cfssljson -bare kubernetes
[root@vlnx175101 ssl]# ls -1 kubernetes*
    kubernetes.csr       <----
    kubernetes-csr.json
    kubernetes-key.pem   <----
    kubernetes.pem       <----


创建admin证书
创建admin证书签名请求
[root@vlnx175101 ssl]# vim admin-csr.json

    {
         "CN": "admin",
         "hosts": [],
         "key": {
           "algo": "rsa",
           "size": 2048
         },
         "names": [ {
             "C": "CN",
             "ST": "BeiJing",
             "L": "BeiJing",
             "O": "system:masters",
             "OU": "System"
         } ]
    }


生成 admin证书和私钥
[root@vlnx175101 ssl]# cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes admin-csr.json | cfssljson -bare admin
[root@vlnx175101 ssl]# ls -1 admin*
    admin.csr       <---
    admin-csr.json
    admin-key.pem   <---
    admin.pem       <---


创建kube-proxy证书
[root@vlnx175101 ssl]# vim kube-proxy-csr.json

    {
         "CN": "system:kube-proxy",
         "hosts": [],
         "key": {
           "algo": "rsa",
           "size": 2048
         },
        "names": [ {
             "C": "CN",
             "ST": "BeiJing",
             "L": "BeiJing",
             "O": "k8s",
             "OU": "System"
        } ]
    }


生成kube-proxy客户端证书和私钥
[root@vlnx175101 ssl]# cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=kubernetes  kube-proxy-csr.json | cfssljson -bare kube-proxy
[root@vlnx175101 ssl]# ls -1 kube-proxy*
    kube-proxy.csr        <---
    kube-proxy-csr.json
    kube-proxy-key.pem    <---
    kube-proxy.pem        <---



校验证书
以kubernetes证书为例

[root@vlnx175101 ssl]# ls -1 *.pem
      admin-key.pem
      admin.pem
      ca-key.pem
      ca.pem
      kube-proxy-key.pem
      kube-proxy.pem
      kubernetes-key.pem
      kubernetes.pem

使用opsnssl命令
[root@vlnx175101 ssl]# openssl x509  -noout -text -in  kubernetes.pem
[root@vlnx175101 ssl]# cfssl-certinfo -cert kubernetes.pem

分发证书
将生成的证书和密钥文件（后缀名为.pem ）拷贝到所有机器的 /etc/kubernetes/ssl 目录下备用；
[root@vlnx175101 ssl]# mkdir -p /etc/kubernetes/ssl
[root@vlnx175101 ssl]# rsync -av *.pem  root@192.168.175.101:/etc/kubernetes/ssl/




====================================================================================================
创建高可用etcd集群

kuberntes系统使用  etcd 存储所有数据，这里部署一个三节点高可用etcd集群的步骤，这三个节点复用  kubernetes master 机器，
分别命令为  vlnx175101.k8.com,vlnx175102.k8.com,vlnx175103.k8.com

    vlnx175101.k8.com 192.168.175.101
    vlnx175102.k8.com 192.168.175.102
    vlnx175103.k8.com 192.168.175.103


TLS认证文件
需要为etcd 集群创建加密通信的TLS证书，这里复用以前创建的  kubernetes证书
[root@vlnx175101 ssl]# scp ca.pem kubernetes-key.pem kubernetes.pem /etc/kubernetes/ssl/
kubernetes 证书的hosts字段列表中包含上面三台机器的  IP，否则后续证书校验会失败；



下载二进制文件
到 https://github.com/coreos/etcd/releases 页面下载最新版本的二进制文件 （三个节点都要部署）
[root@vlnx175101 ~]# wget https://github.com/etcd-io/etcd/releases/download/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz
[root@vlnx175101 ~]# tar -xvf etcd-v3.3.12-linux-amd64.tar.gz
[root@vlnx175101 ~]# ls etcd-v3.3.12-linux-amd64
    Documentation  etcd  etcdctl  README-etcdctl.md  README.md  READMEv2-etcdctl.md

[root@vlnx175101 ~]# rsync -av etcd-v3.3.12-linux-amd64/{etcd,etcdctl}  root@192.168.175.101:/usr/local/bin/

[root@vlnx175101 ~]# mkdir -p /var/lib/etcd  /etc/etcd/
[root@vlnx175101 ~]# vim /etc/systemd/system/etcd.service

      [Unit]
      Description=Etcd Server
      After=network.target
      After=network-online.target
      Wants=network-online.target
      Documentation=https://github.com/coreos
      [Service]
      Type=notify
      WorkingDirectory=/var/lib/etcd/
      EnvironmentFile=-/etc/etcd/etcd.conf
      ExecStart=/usr/local/bin/etcd \
        --name vlnx175101.k8.com \
        --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --peer-cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --peer-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --initial-advertise-peer-urls https://192.168.175.101:2380 \
        --listen-peer-urls https://192.168.175.101:2380 \
        --listen-client-urls https://192.168.175.101:2379,https://127.0.0.1:2379 \
        --advertise-client-urls https://192.168.175.101:2379 \
        --initial-cluster-token "etcd-cluster-1" \
        --initial-cluster vlnx175101.k8.com=https://192.168.175.101:2380,vlnx175102.k8.com=https://192.168.175.102:2380,vlnx175103.k8.com=https://192.168.175.103:2380 \
        --initial-cluster-state new \
        --data-dir=/var/lib/etcd
      Restart=on-failure
      RestartSec=5
      LimitNOFILE=65536

      [Install]
      WantedBy=multi-user.target



[root@vlnx175102 ~]# vim /etc/systemd/system/etcd.service

      [Unit]
      Description=Etcd Server
      After=network.target
      After=network-online.target
      Wants=network-online.target
      Documentation=https://github.com/coreos
      [Service]
      Type=notify
      WorkingDirectory=/var/lib/etcd/
      EnvironmentFile=-/etc/etcd/etcd.conf
      ExecStart=/usr/local/bin/etcd \
        --name vlnx175102.k8.com \
        --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --peer-cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --peer-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --initial-advertise-peer-urls https://192.168.175.102:2380 \
        --listen-peer-urls https://192.168.175.102:2380 \
        --listen-client-urls https://192.168.175.102:2379,https://127.0.0.1:2379 \
        --advertise-client-urls https://192.168.175.102:2379 \
        --initial-cluster-token "etcd-cluster-1" \
        --initial-cluster vlnx175101.k8.com=https://192.168.175.101:2380,vlnx175102.k8.com=https://192.168.175.102:2380,vlnx175103.k8.com=https://192.168.175.103:2380 \
        --initial-cluster-state new \
        --data-dir=/var/lib/etcd
      Restart=on-failure
      RestartSec=5
      LimitNOFILE=65536

      [Install]
      WantedBy=multi-user.target


[root@vlnx175103 ~]# vim /etc/systemd/system/etcd.service
      [Unit]
      Description=Etcd Server
      After=network.target
      After=network-online.target
      Wants=network-online.target
      Documentation=https://github.com/coreos
      [Service]
      Type=notify
      WorkingDirectory=/var/lib/etcd/
      EnvironmentFile=-/etc/etcd/etcd.conf
      ExecStart=/usr/local/bin/etcd \
        --name vlnx175103.k8.com \
        --cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --peer-cert-file=/etc/kubernetes/ssl/kubernetes.pem \
        --peer-key-file=/etc/kubernetes/ssl/kubernetes-key.pem \
        --trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --peer-trusted-ca-file=/etc/kubernetes/ssl/ca.pem \
        --initial-advertise-peer-urls https://192.168.175.103:2380 \
        --listen-peer-urls https://192.168.175.103:2380 \
        --listen-client-urls https://192.168.175.103:2379,https://127.0.0.1:2379 \
        --advertise-client-urls https://192.168.175.103:2379 \
        --initial-cluster-token "etcd-cluster-1" \
        --initial-cluster vlnx175101.k8.com=https://192.168.175.101:2380,vlnx175102.k8.com=https://192.168.175.102:2380,vlnx175103.k8.com=https://192.168.175.103:2380 \
        --initial-cluster-state new \
        --data-dir=/var/lib/etcd
      Restart=on-failure
      RestartSec=5
      LimitNOFILE=65536

      [Install]
      WantedBy=multi-user.target



启动etcd服务
[root@vlnx175101 ~]# systemctl daemon-reload ; systemctl enable etcd ; systemctl start etcd ; systemctl status etcd
[root@vlnx175102 ~]# systemctl daemon-reload ; systemctl enable etcd ; systemctl start etcd ; systemctl status etcd
[root@vlnx175103 ~]# systemctl daemon-reload ; systemctl enable etcd ; systemctl start etcd ; systemctl status etcd


验证服务
在任一kubernetes master机器上执行如下命令：
[root@vlnx175101 ~]# etcdctl --ca-file=/etc/kubernetes/ssl/ca.pem  \
                             --cert-file=/etc/kubernetes/ssl/kubernetes.pem  \
                             --key-file=/etc/kubernetes/ssl/kubernetes-key.pem  \
                             --endpoints=https://127.0.0.1:2379  \
                             cluster-health

    member 8059d048b8b3ef3c is healthy: got healthy result from https://192.168.175.101:2379
    member 8793c202443faf1f is healthy: got healthy result from https://192.168.175.103:2379
    member f908d2f9513db5d7 is healthy: got healthy result from https://192.168.175.102:2379
    cluster is healthy



====================================================================================================
下载最新版本的二进制文件
下载 server tarball 文件


TODO: 因为 无法下载 相关的 tarball 安装包, 改天继续学习































创建 etcd 高可用集群

创建 kubeconfig 文件 (kubectl 使用)

部署 master 节点

部署 node 节点


















