


https://pypi.org/project/PyMySQL/
https://github.com/PyMySQL/PyMySQL/

https://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
https://stackoverflow.com/questions/2548493/how-do-i-get-the-id-after-insert-into-mysql-database-with-python



[root@python3lang ~]# python3 -m venv  pymysql-venv

[root@python3lang ~]# ls | grep pymysql-venv
    pymysql-venv


[root@python3lang ~]# source pymysql-venv/bin/activate
(pymysql-venv) [root@python3lang ~]# pip install --upgrade pip

(pymysql-venv) [root@python3lang ~]# python3 -m pip install PyMySQL
(pymysql-venv) [root@python3lang ~]# ls ./pymysql-venv/lib/python3.6/site-packages | grep -i pymysql
      pymysql
      PyMySQL-0.9.3.dist-info

(pymysql-venv) [root@python3lang ~]# pip show PyMySQL
      Name: PyMySQL
      Version: 0.9.3
      Summary: Pure Python MySQL Driver
      Home-page: https://github.com/PyMySQL/PyMySQL/
      Author: yutaka.matsubara
      Author-email: yutaka.matsubara@gmail.com
      License: "MIT"
      Location: /root/pymysql-venv/lib/python3.6/site-packages
      Requires:
      Required-by:









