
// 修改 ubuntu18 desktop 为使用静态ip (注：ubuntu的render在server和desktop上略有不同，server使用networkd,而desktop使用NetworkManager)

参考资料：
https://help.ubuntu.com/lts/serverguide/serverguide.pdf
https://websiteforstudents.com/configure-static-ip-addresses-on-ubuntu-18-04-beta/
https://www.howtoforge.com/linux-basics-set-a-static-ip-on-ubuntu
https://tyanogi.hatenablog.com/entry/2018/06/10/154525




yangsg@vm:~$ vim /etc/netplan/01-network-manager-all.yaml
			# Let NetworkManager manage all devices on this system
			network:
				version: 2
				renderer: NetworkManager

				ethernets:
					ens33:
							dhcp4: no
							addresses: [192.168.175.100/24]
							gateway4: 192.168.175.2
							nameservers:
									addresses: [192.168.175.2]
							dhcp6: no


yangsg@vm:~$ sudo netplan apply









