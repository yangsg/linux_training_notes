import paramiko


def exec_command_by_password_login_demo(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname='192.168.175.100', port=22, username='root', password='vbird')

    stdin, stdout, stderr = client.exec_command(command)
    exit__status = stdout.channel.recv_exit_status()

    if exit__status == 0:
        print('成功')
    else:
        print('失败')

    print('标准输出流-----------------------------')
    for line in stdout:
        print(line, end='')

    print('标准错误流-----------------------------')
    for line in stderr:
        print(line, end='')

    client.close()


def exec_command_by_RSA_key_login_demo(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    pkey = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    client.connect(hostname='192.168.175.100', port=22, username='root', pkey=pkey)

    stdin, stdout, stderr = client.exec_command(command)
    exit__status = stdout.channel.recv_exit_status()

    if exit__status == 0:
        print('成功')
    else:
        print('失败')

    print('标准输出流-----------------------------')
    for line in stdout:
        print(line, end='')

    print('标准错误流-----------------------------')
    for line in stderr:
        print(line, end='')

    client.close()


def transfer_file_by_password_login_demo():
    # 注: 此处的参数必须以 元组(a tuple) 的方式给出
    # 见 http://docs.paramiko.org/en/2.6/api/transport.html
    transport = paramiko.Transport(('192.168.175.100', 22))
    # transport = paramiko.Transport('192.168.175.100:22')
    transport.connect(username='root', password='vbird')

    sftp_client = paramiko.SFTPClient.from_transport(transport)
    '''
    注: 如下示例中 的 第二个参数 '/tmp/fstab'(即 remotepath) 中 必须包含 filename, 否则会报错
        见   http://docs.paramiko.org/en/2.6/api/sftp.html#paramiko.sftp_client.SFTPClient.put
    '''
    # 将 local 端的 '/etc/fstab' 上传 到 remote 端的 '/tmp/fstab'
    sftp_client.put('/etc/fstab', '/tmp/fstab')
    # 将 remote 上的 '/etc/sysconfig/network-scripts/ifcfg-ens33' 文件 下载到 local 端的 /tmp/ifcfg-ens33
    sftp_client.get('/etc/sysconfig/network-scripts/ifcfg-ens33', '/tmp/ifcfg-ens33')

    transport.close()


def transfer_file_by_RSA_key_demo():
    pkey = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')

    # 注: 此处的参数必须以 元组(a tuple) 的方式给出
    # 见 http://docs.paramiko.org/en/2.6/api/transport.html
    transport = paramiko.Transport(('192.168.175.100', 22))
    # transport = paramiko.Transport('192.168.175.100:22')
    transport.connect(username='root', pkey=pkey)

    sftp_client = paramiko.SFTPClient.from_transport(transport)
    '''
    注: 如下示例中 的 第二个参数 '/tmp/fstab'(即 remotepath) 中 必须包含 filename, 否则会报错
        见   http://docs.paramiko.org/en/2.6/api/sftp.html#paramiko.sftp_client.SFTPClient.put
    '''
    # 将 local 端的 '/etc/fstab' 上传 到 remote 端的 '/tmp/fstab'
    sftp_client.put('/etc/fstab', '/tmp/fstab')
    # 将 remote 上的 '/etc/sysconfig/network-scripts/ifcfg-ens33' 文件 下载到 local 端的 /tmp/ifcfg-ens33
    sftp_client.get('/etc/sysconfig/network-scripts/ifcfg-ens33', '/tmp/ifcfg-ens33')

    transport.close()


if __name__ == '__main__':
    flag = 3
    if flag == 1:
        exec_command_by_password_login_demo('uptime')
        exec_command_by_password_login_demo('oauwhduawhd || echo "ok"')
        exec_command_by_password_login_demo('echo 中文')
    elif flag == 2:
        exec_command_by_RSA_key_login_demo('uptime')
        exec_command_by_RSA_key_login_demo('oauwhduawhd || echo "ok"')
        exec_command_by_RSA_key_login_demo('echo 中文')
    elif flag == 3:
        transfer_file_by_password_login_demo()
    elif flag == 4:
        transfer_file_by_RSA_key_demo()
