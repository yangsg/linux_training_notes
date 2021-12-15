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


##### 一些学习资料网:
- [www.javatpoint.com](https://www.javatpoint.com/)


##### [github开发人员在七夕搞事情：remote: Support for password authentication was removed on August 13, 2021.](https://blog.csdn.net/weixin_41010198/article/details/119698015)
- https://namespaceit.com/blog/remote-support-for-password-authentication-was-removed-on-august-13-2021-please-use-a-personal-access-token-instead


##### 中国公共的NTP服务器
```text
# 阿里云NTP服务器(公网); https://help.aliyun.com/document_detail/92704.html
ntp1.aliyun.com
ntp2.aliyun.com

# 腾讯公共NTP; https://cloud.tencent.com/document/product/213/30392
time1.cloud.tencent.com
time2.cloud.tencent.com
# 国家授时中心
ntp.ntsc.ac.cn
```


- [ip138.com 查询网](https://www.ip138.com/)
- [dns大全](https://dnsdaquan.com/)

##### 常见的DNS服务器
```text
谷歌:
  8.8.8.8
  8.8.4.4

阿里云: https://developer.aliyun.com/mirror/?spm=a2c6h.13651102.0.0.42311b11J16RUO&serviceType=dns
  223.5.5.5
  223.6.6.6

百度: https://dudns.baidu.com/support/localdns/Address/index.html
  180.76.76.76

114 DNS:
  114.114.114.114
  114.114.115.115

```



