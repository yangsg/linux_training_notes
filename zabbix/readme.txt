

https://www.zabbix.com/documentation/current/manual
https://www.zabbix.com/documentation/4.4/start


https://www.zabbix.com/documentation/4.4/manual/installation/requirements
硬件配置示例表:
-------------------------------------------------------------------------------------------------------------------
Name         Platform                   CPU/Memory          Database                               Monitored hosts
-------------------------------------------------------------------------------------------------------------------
Small        CentOS                     Virtual Appliance   MySQL InnoDB                           100
Medium       CentOS                     2 CPU cores/2GB     MySQL InnoDB                           500
Large        RedHat Enterprise Linux    4 CPU cores/8GB     RAID10 MySQL InnoDB or PostgreSQL       >1000
Very large   RedHat Enterprise Linux    8 CPU cores/16GB    Fast RAID10 MySQL InnoDB or PostgreSQL  >10000
-------------------------------------------------------------------------------------------------------------------



zabbix 安全设置方面的最佳实践 及 其他一些与 web 安全(security)相关的资料:
    https://www.zabbix.com/documentation/4.4/manual/installation/requirements/best_practices
    https://developer.mozilla.org/en-US/docs/Web/Security
    https://geekflare.com/nginx-webserver-security-hardening-guide/


特性: https://www.zabbix.com/documentation/4.4/manual/introduction/features

zabbix 的某些名词及定义:
  https://www.zabbix.com/documentation/4.4/manual/definitions


----------------------------------------------------------------------------------------------------
https://www.zabbix.com/documentation/4.4/manual/concepts/server

zabbix-server



----------------------------------------------------------------------------------------------------
https://www.zabbix.com/documentation/4.4/manual/concepts/agent


zabbix-agent

Passive and active checks (被动 和 主动 检查)
  passive check: zabbix-server 主动发送数据请求(data request), zabbix-agent 被动负责对其相应
  active checks: zabbix-agent 首先从 zabbix-server 获取 items 列表, 然后周期性地 主动 新的值 给 zabbix-server.

----------------------------------------------------------------------------------------------------
https://www.zabbix.com/documentation/4.4/manual/concepts/proxy

zabbix-proxy (可选, 缓解 zabbix-server 服务器的压力)

    zabbix-proxy 代表 zabbix-server 从 若干个 被监视 设备上收集 监视数据, 所有的数据先在本地缓存后再 转送 给 zabbix-server

  zabbix-proxy 要求自己的 database, 支持的数据库类型有 SQLite, MySQL and PostgreSQL。
  如果使用 Oracle 或 IBM DB2 数据库 则需要自己承担风险 和 某些限制.

----------------------------------------------------------------------------------------------------

安装指南:
    https://www.zabbix.com/documentation/4.4/manual/installation/install_from_packages
    https://www.zabbix.com/documentation/4.4/manual/installation/install




















