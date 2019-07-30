

http://www.paramiko.org/
http://docs.paramiko.org/en/2.6/
https://github.com/paramiko/paramiko

// 重要: 演示了 正确的 获取 exit status 的方式:
https://stackoverflow.com/questions/3562403/how-can-you-get-the-ssh-return-code-using-paramiko
---------------------------------------------------------------------------------------------------
                import paramiko

                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect('blahblah.com')

                stdin, stdout, stderr = client.exec_command("uptime")
                print(stdout.channel.recv_exit_status())    # status is 0

                stdin, stdout, stderr = client.exec_command("oauwhduawhd")
                print(stdout.channel.recv_exit_status())    # status is 127
---------------------------------------------------------------------------------------------------

https://github.com/PacktPublishing/Python-Network-Programming-Cookbook-Second-Edition/blob/master/Chapter06/6_3_print_remote_cpu_info.py
https://www.programcreek.com/python/example/4561/paramiko.SSHClient
https://www.cnblogs.com/zhangxinqi/p/8372774.html
https://www.cnblogs.com/python-nameless/p/6855804.html





[root@python3lang ~]# python3 -m venv tutorial-venv
[root@python3lang ~]# source tutorial-venv/bin/activate

(tutorial-venv) [root@python3lang ~]# pip install --upgrade pip
(tutorial-venv) [root@python3lang ~]# pip install paramiko


(tutorial-venv) [root@python3lang ~]# pip show paramiko
      Name: paramiko
      Version: 2.6.0
      Summary: SSH2 protocol library
      Home-page: https://github.com/paramiko/paramiko/
      Author: Jeff Forcier
      Author-email: jeff@bitprophet.org
      License: LGPL
      Location: /root/tutorial-venv/lib/python3.6/site-packages
      Requires: pynacl, bcrypt, cryptography
      Required-by:


// 配置免密登录
// 参见笔记:  https://github.com/yangsg/linux_training_notes/tree/master/openssh_server_basic
[root@python3lang ~]# ssh-keygen    # 如果还不存在 ssh 使用的 RSA 非对称秘钥对, 则使用 该命令生成之
[root@python3lang ~]# tree .ssh
      .ssh
      ├── id_rsa
      └── id_rsa.pub

[root@python3lang ~]# ssh-copy-id root@192.168.175.100



















