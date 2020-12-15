


ubuntu 默认使用 timedatectl / timesyncd 来同步时间，用户可以选择性的使用 chrony来提供 Network Time Protocol 服务。

timesyncd  默认就是可用的，它不仅可以替代 ntpdate, 还可以替代 chrony 的 client部分，

如果安装了 chrony, timedatectl 退而使用 chrony 保持时间。这样就保证了没有 2 个 time syncing services 打架。


ntpdate 被认为已经过时了，取而代之应使用 timedatectl (or chrony),timesyncd  通常可以正确的保持时间同步.
而 chrony 可以帮助你处理更加复杂的 cases.

如果需要 a one-shot 式的同步，使用: chronyd -q


*) 如果需要 a one-shot time check, without setting the time 则使用: chronyd -Q

可以通过命令 `timedatectl status` 来查看 当前的 time 和  timedatectl and timesyncd 的 time configuration.

ysg@vm01:~$ timedatectl status
               Local time: Tue 2020-12-15 13:57:00 UTC
           Universal time: Tue 2020-12-15 13:57:00 UTC
                 RTC time: Tue 2020-12-15 13:57:00
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes   <--观察, 如果运行了 chrony, 则切换为: System clock synchronized: no
              NTP service: active
          RTC in local TZ: no



Via timedatectl an admin can control the timezone, how the system clock should
relate to the hwclock and if permanent synronization should be enabled or not. 
更多信息见: man timedatectl

timesyncd 本身仍然是一个普通的 service, 因此可以通过如下命令来查看其状态:

ysg@vm01:~$ systemctl status systemd-timesyncd
● systemd-timesyncd.service - Network Time Synchronization
     Loaded: loaded (/lib/systemd/system/systemd-timesyncd.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2020-12-15 13:05:35 UTC; 56min ago
       Docs: man:systemd-timesyncd.service(8)
   Main PID: 645 (systemd-timesyn)
     Status: "Initial synchronization to time server 91.189.91.157:123 (ntp.ubuntu.com)."
      Tasks: 2 (limit: 1041)
     Memory: 1.7M
     CGroup: /system.slice/systemd-timesyncd.service
             └─645 /lib/systemd/systemd-timesyncd



文件 /etc/systemd/timesyncd.conf 中可以指定  timedatectl 和 timesyncd 获取 time 的 nameserver.
而额外的配置可以被存储到 /etc/systemd/timesyncd.conf.d/ 中.
NTP= 和 FallbackNTP= 都是 space 风格的 list. 更多信息见 


ysg@vm01:~$ sudo timedatectl set-timezone Asia/Shanghai

ysg@vm01:~$ sudo vim /etc/systemd/timesyncd.conf
		[Time]
		# https://developer.aliyun.com/mirror/
		# https://www.ntppool.org/en/use.html
		NTP=ntp1.aliyun.com ntp2.aliyun.com
		FallbackNTP=0.cn.pool.ntp.org 1.cn.pool.ntp.org



ysg@vm01:~$ sudo systemctl daemon-reload
ysg@vm01:~$ sudo systemctl restart systemd-timesyncd.service


ysg@vm01:~$ timedatectl timesync-status
       Server: 120.25.115.20 (ntp1.aliyun.com)
Poll interval: 8min 32s (min: 32s; max 34min 8s)
         Leap: normal
      Version: 4
      Stratum: 2
    Reference: A893507
    Precision: 1us (-25)
Root distance: 1.090ms (max: 5s)
       Offset: -1.670ms
        Delay: 44.573ms
       Jitter: 2.529ms
 Packet count: 4
    Frequency: -1.209ppm

















