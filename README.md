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


## [CentOS 8 落幕，“免费”的 RHEL 没了](https://www.toutiao.com/a6904104084442464776/)
> CentOS Linux 8 作为 RHEL 8 的重构版，将在 2021 年底结束。”而尚在计划维护期的 CentOS 7 系列，也将在 2024 年维护期限到达之后停止维护。


## [Rocky Linux](https://github.com/hpcng/rocky)
## [Rocky Linux 中文社区](https://rockylinux.cn/)


## [Ubuntu Server Guide](https://ubuntu.com/server/docs)









