# linux_training_notes

### 我的私有仓库
* https://gitee.com/yangshanggui
* https://gitee.com/yangsggithub

```bash
// 简单的生成自签名证书的方式:
[root@centos_8_server ~]# openssl genrsa 2048 > server.key
[root@centos_8_server ~]# chmod 600 server.key
[root@centos_8_server ~]# openssl req -new -key server.key > server.csr
[root@centos_8_server ~]# openssl req -x509 -days 3650 -key server.key -in server.csr > server.crt

// https://gitee.com/yangshanggui/linux_server/blob/master/openssl.md
```
