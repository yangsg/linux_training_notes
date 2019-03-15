

https://baike.baidu.com/item/DHCP/218195?fr=aladdin
https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol

dhcpd server开放的服务端口: udp/67
dhcpd client通信用的端口：  udp/68


服务器端：
[root@dhcpd7server ~]#  yum install -y dhcp
[root@dhcpd7server ~]# rpm -q dhcp
    dhcp-4.2.5-68.el7.centos.1.x86_64

[root@dhcpd7server ~]# cp  /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example  /etc/dhcp/dhcpd.conf

[root@dhcpd7server ~]# vim /etc/dhcp/dhcpd.conf  #man dhcpd.conf

      subnet 192.168.11.0 netmask 255.255.255.0 {
        range 192.168.11.20 192.168.11.21;    # [20-21]
        range 192.168.11.30;                  # [30]
        range 192.168.11.100 192.168.11.200;  # [100-200]
        option routers 192.168.175.2;         # 网关地址
        option domain-name-servers 192.168.175.2, 8.8.8.8; #DNS服务器地址
      }

      host boss_client_pc {  #根据mac地址绑定固定ip
        hardware ethernet 00:0c:29:82:ac:0f;
        #注：最好将fixed-address设置为range之外的ip
        # https://unix.stackexchange.com/questions/432845/will-dhcpd-give-away-a-fixed-address-to-non-matching-client-on-address-dificit
        fixed-address 192.168.11.44;
      }


[root@dhcpd7server ~]# systemctl start dhcpd
[root@dhcpd7server ~]# systemctl enable dhcpd
[root@dhcpd7server ~]# netstat -anptu | grep :67

客户端：
[root@dhcpd7client ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33
        TYPE=Ethernet
        BOOTPROTO=dhcp
        NAME=ens33
        DEVICE=ens33
        ONBOOT=yes

[root@dhcpd7client ~]# nmcli conn reload
[root@dhcpd7client ~]# nmcli conn up ens33
[root@dhcpd7client ~]# ip addr show


