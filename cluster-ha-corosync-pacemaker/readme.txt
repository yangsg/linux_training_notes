

网上资料:
        https://blog.51cto.com/11107124/1868577
        https://blog.51cto.com/jiayimeng/1874741
        https://www.iyunv.com/thread-18105-1-1.html


    https://www.suse.com/documentation/sle_ha/book_sleha/data/sec_ha_architecture.html
    https://clusterlabs.org/
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/high_availability_add-on_administration/ch-startup-haaa
    https://www.unixarena.com/2015/12/rhel-7-redhat-cluster-with-pacemaker-overview.html/




            ---------------------------------------
            Resource Agent (类型: lsb, ocf 等)
            ---------------------------------------
            Cluster Resource Manager (pacemaker)
            ---------------------------------------
            Messaging Layer  (corosync)
            ---------------------------------------
            node01  node02



        https://www.suse.com/documentation/sle_ha/book_sleha/data/sec_ha_architecture.html
        https://www.suse.com/documentation/sle-ha-12/singlehtml/book_sleha/book_sleha.html#sec.ha.architecture.layers

             RA                           RA
             ↑                            ↑
             |                            |
             |                            |                   Resource Layer
             |                            |                   --------------------------------
             ↓                            ↓
            LRM       PE ←-----CIB(xml)  LRM       CIB(xml, replica)
             ↑        ↑         ↑         ↑         ↑
             |        |         |         |         |
             |        |         |         |         |
             | |------|         |         |         |         Resource Allocation Layer
             | |                |         |         |
             | ↓                |         ↓         |
        (DC)CRM ----------------|        CRM ←------|
             ↑                            ↑
             |                            |                   --------------------------------
             |                            |                    Messaging and Infrastructure Layer
        Corosync/OpenAIS -------------- Corosync/OpenAIS
             |                            |
             |                            |
             |                            |
             ↓                            ↓
            node01                       node02




资源类型

    1)  Primitive资源(主资源)
        a)  同一时间只能运行在同一个节点上

    2)  主从资源(Master/Slave资源)   【drbd分布式块设备】
        a)  依赖于Primitive资源
        b)  同一时间可以运行在两个节点上

    3)  Clone资源   fence_agent进程
        a)  同时运行在多个节点上的资源

    4)  资源组   resource group
        作用：保证多个资源可以同进同退


资源约束Constraint关系

    1)  顺序约束   order constraint
        a)  定义资源的启动顺序 【分数score】
    2)  排列约束    collation constraint
        a)  保证多个资源可在同一个节点上运行或者多个资源可同时转移
        b)  INFINITY  无穷大
    3)  位置约束  location constraint
        a)  定义资源对集群节点的依赖性
        b)  INFINITY   无穷大


noquorum policy   不满足法定票数策略
  法定票数：
    HA集群获得的票数高于总票数的一半

  不满足法定票数  noquorum
     freeze    默认策略
     stop
     ignore
































