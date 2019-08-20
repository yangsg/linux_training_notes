#!/bin/bash

# 为了避免无意中的 名字冲突, 所以
# 自定义函数的函数名 加了 前缀 fn_ ,
# 自定义变量的变量名 加了 前缀 v_


v_base_xml_file=/opt/kvm-templates/centos7.4/vm-base-centos7.4-64.xml
v_base_image_file=/opt/kvm-templates/centos7.4/vm-base-centos7.4-64.qcow2
v_log_file=/dev/null   # v_log_file 默认为 /dev/null, 可以修改 v_debug 变量对其切换

v_debug=yes
#v_debug=no

if [ $v_debug = yes ]; then
  v_log_file=/tmp/kvm.sh.log
fi


# 将 函数 fn_main 作为主函数(亦即 入口函数)
function fn_main() {
  local v_vm_amount

  read -p '虚拟机数量: ' v_vm_amount

  if [[ ! $v_vm_amount =~ ^[[:digit:]]{1,2}$ ]]; then
    echo 虚拟机数量必须是数字
    return 1
  fi

  echo $v_vm_amount

  fn_delete_existed_vm
  create_vm_instances $v_vm_amount
  update_network $v_vm_amount
}

# usage:
#     fn_delete_existed_vm
function fn_delete_existed_vm() {
  local v_vm_names=$(virsh list --all | grep centos_ | awk '{print $2}')

  local v_vm_name
  for v_vm_name in $v_vm_names; do

    local v_vm_image_file=$(virsh domblklist $v_vm_name  | grep $v_vm_name | awk '{print $2}')

    if ! fn_is_empty_or_blank "$v_vm_name"; then
      virsh destroy  $v_vm_name &>> $v_log_file   #强制关机
      virsh undefine $v_vm_name &>> $v_log_file   #删除配置文件

      if ! fn_is_empty_or_blank "$v_vm_image_file"; then
        rm -f "$v_vm_image_file"
      fi
    fi
  done

}

# usage:
#     fn_is_empty_or_blank "$variable"
function fn_is_empty_or_blank() {
  [[ "$1" =~ ^[[:space:]]*$ ]]
}

# usage:
#    create_vm_instances vm_amount
# eg:
#    create_vm_instances 2
function create_vm_instances() {
  local v_vm_amount=$1

  local i
  for i in $(seq $v_vm_amount); do
    local v_vm_name=centos_${i}

    local v_vm_xml_file=/etc/libvirt/qemu/${v_vm_name}.xml
    local v_vm_image_file=/var/lib/libvirt/images/${v_vm_name}.qcow2
    local v_vm_mac_address=52:54:00:$(dd if=/dev/urandom count=1 2>> $v_log_file | md5sum | sed -r 's/^(..)(..)(..).*$/\1:\2:\3/')
    local v_vm_uuid=$(uuidgen)
    local v_vm_vnc_port=59$(printf '%02d' $((20+$i)))


    cp $v_base_xml_file   $v_vm_xml_file
    qemu-img create -f qcow2 -b $v_base_image_file $v_vm_image_file &>> $v_log_file

    # 修改新建示例的 xml 配置文件
    sed -ri "s/vm-base-centos7.4-64/${v_vm_name}/"   $v_vm_xml_file
    sed -ri "/<uuid>/ c \  <uuid>${v_vm_uuid}</uuid>" $v_vm_xml_file
    sed -ri "/<mac address/ c \      <mac address='${v_vm_mac_address}'/>" $v_vm_xml_file
    sed -ri "s/type='vnc' port='5920'/type='vnc' port='${v_vm_vnc_port}'/" $v_vm_xml_file

    chown qemu:qemu $v_vm_image_file
    chmod 600 $v_vm_image_file

    virsh define $v_vm_xml_file &>> $v_log_file

  done
}


# usage:
#      update_network vm_amount
# eg:
#    update_network 2
function update_network() {
  local v_vm_amount=$1

  # 更新 ip 地址
  local v_default_network_xml_file=/etc/libvirt/qemu/networks/default.xml
  sed -ri '/<host / d' $v_default_network_xml_file

  local i
  for i in $(seq $v_vm_amount); do
    local v_vm_name=centos_${i}
    local v_vm_image_file=/var/lib/libvirt/images/${v_vm_name}.qcow2

    local v_vm_name=centos_${i}
    local v_mac_addr=$(virsh dumpxml $v_vm_name | grep -E '<mac ' | grep -Eo '(..)(:..){5}')
    local v_ip_addr=192.168.122.$((i*10))

    sed -ri "/<\/dhcp>/ i \      <host mac='${v_mac_addr}' name='${v_vm_name}' ip='${v_ip_addr}'/>" $v_default_network_xml_file

# 使用 guestfish (底层调用 libguestfs API) 直接修改 Guest虚拟机中的 /etc/sysconfig/network-scripts/ifcfg-eth0 文件
# 注意: 使用 guestfish 修改 Guest虚拟机 时一定要 shutdown Guest虚拟机, 否则 Guest虚拟机 会被损坏.
# 注意如下结尾的 _EOF_  前面不要有空格
# http://libguestfs.org/guestfish.1.html
# http://bbs.chinaunix.net/thread-4060390-1-1.html
# https://blog.csdn.net/zuopiezia/article/details/81034500
#     yum -y install libguestfs-tools-c
#  或
#     yum -y install libguestfs-tools
guestfish <<_EOF_
  add $v_vm_image_file
  run
  mount /dev/centos/root /
  write-append /etc/sysconfig/network-scripts/ifcfg-eth0 "IPADDR=${v_ip_addr}\n"
  write-append /etc/sysconfig/network-scripts/ifcfg-eth0 "PREFIX=24\n"
  write-append /etc/sysconfig/network-scripts/ifcfg-eth0 "GATEWAY=192.168.122.1\n"
  write-append /etc/sysconfig/network-scripts/ifcfg-eth0 "DNS1=192.168.122.1\n"
  write-append /etc/sysconfig/network-scripts/ifcfg-eth0 "BOOTPROTO=none\n"
_EOF_

  done

}

# update_network_deprecated 中的方式配置ip 很多时候都不起作用(虽然偶尔有效果),
# 所以最好不要使用这种方式, 所有最稳妥 的方式是使用 如函数 update_network 中
# guestfish(libguestfs) 这种方式 直接修改 Guest virtual machine 中文件系统中配置文件的方式
#    https://serverfault.com/questions/101292/libvirt-change-dhcp-setup-without-restarting
#    https://www.cyberciti.biz/faq/linux-kvm-libvirt-dnsmasq-dhcp-static-ip-address-configuration-for-guest-os/
function update_network_deprecated() {
  local v_vm_amount=$1

  # 更新 ip 地址
  local v_default_network_xml_file=/etc/libvirt/qemu/networks/default.xml
  sed -ri '/<host / d' $v_default_network_xml_file

  local i
  for i in $(seq $v_vm_amount); do
    local v_vm_name=centos_${i}
    local v_mac_addr=$(virsh dumpxml $v_vm_name | grep -E '<mac ' | grep -Eo '(..)(:..){5}')
    local v_ip_addr=192.168.122.$((i*10))

    sed -ri "/<\/dhcp>/ i \      <host mac='${v_mac_addr}' name='${v_vm_name}' ip='${v_ip_addr}'/>" $v_default_network_xml_file

  done

  virsh net-destroy default
  virsh net-define $v_default_network_xml_file
  virsh net-start default

}





# 调用主函数
fn_main



