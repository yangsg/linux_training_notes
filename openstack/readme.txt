
IaaS:  Infrastructure-as-a-Service

OpenStack services 关系图
      https://docs.openstack.org/install-guide/get-started-conceptual-architecture.html

OpenStack cloud 架构图:
      https://docs.openstack.org/install-guide/get-started-logical-architecture.html

      通常,
      OpenStack 的 services 之间 以 REST API 方式通信,
      每个 service 的 processes 之间以 AMQP message broker(如 RabbitMQ 等) 方式通信,
      且 service’s state 存储在 database(如 MariaDB 等) 中.

OpenStack Architecture Design Guide
      https://docs.openstack.org/arch-design/


生产环境下 需要参考的资料(For more information on production architectures for Rocky):
  rocky 版本:
        https://docs.openstack.org/arch-design/
        https://docs.openstack.org/neutron/rocky/admin/
        https://docs.openstack.org/rocky/admin/



----------------------------------------------------------------------------------------------------


https://docs.openstack.org/stein/
https://baike.baidu.com/item/OpenStack/342467?fr=aladdin
http://c.biancheng.net/view/3892.html


https://docs.openstack.org/stein/?_ga=2.247467847.1124908983.1569409783-912250514.1566655477
https://docs.openstack.org/install-guide/
https://www.server-world.info/en/note?os=CentOS_7&p=openstack_stein&f=1


Identity service (Keystone)
Compute service (Nova)
Block Storage service (Cinder)
Networking service (Neutron)
Image service (Glance)
Object Storage service (Swift)
Dashboard (Horizon)




Data Processing service (Sahara)
Database service (Trove)
Orchestration service (Heat)




----------------------------------------------------------------------------------------------------


controller:
  mariadb server
  rabbitMQ












