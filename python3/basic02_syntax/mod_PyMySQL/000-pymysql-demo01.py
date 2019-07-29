import pymysql.cursors

'''
mysql> use mysql
mysql> CREATE USER IF NOT EXISTS 'admin'@'192.168.175.20' IDENTIFIED BY 'WWW.1.com';
mysql> GRANT ALL ON *.* TO 'admin'@'192.168.175.20';

mysql> CREATE DATABASE db_test01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

mysql> use db_test01;
mysql> CREATE TABLE host (
           id int NOT NULL AUTO_INCREMENT,
           name varchar(16) NOT NULL,
           ip varchar(15) NOT NULL,
           comment varchar(30) NOT NULL,
           PRIMARY KEY (id)
       ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

'''


def getConnection():
    connection = pymysql.connect(host='192.168.175.100',
                                 user='admin',
                                 password='WWW.1.com',
                                 db='db_test01',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection;


def fetchall_databases():
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("show databases")
            result = cursor.fetchall()
            print(result)
            ''' 输入结果:
            [{'Database': 'information_schema'}, {'Database': 'db_test01'}, {'Database': 'mysql'}, {'Database': 'performance_schema'}, {'Database': 'sys'}]
            '''
            for data in result:
                print('{Database}'.format(**data))
                ''' 输出结果:
                    information_schema
                    db_test01
                    mysql
                    performance_schema
                    sys
                '''
    finally:
        connection.close()


def insert(name, ip, comment):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            '''
            https://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
            '''
            sql = "INSERT INTO host (name, ip, comment) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, ip, comment))

            '''
            https://stackoverflow.com/questions/77552/id-is-a-bad-variable-name-in-python
            https://stackoverflow.com/questions/2548493/how-do-i-get-the-id-after-insert-into-mysql-database-with-python
            '''
            id_ = cursor.lastrowid

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id, name, ip, comment FROM host WHERE id=%s"
            cursor.execute(sql, (id_,))
            result = cursor.fetchone()
            print(result)
            ''' 输出结果:
            {'id': 1, 'name': 'mysql_server', 'ip': '192.168.175.100', 'comment': '中文描述: 数据库服务器'}
            '''
    finally:
        connection.close()


def update(id_, name, ip, comment):
    connection = getConnection()
    try:
        with connection.cursor() as cursor:
            '''
            https://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
            '''
            sql = "update host set name=%(name)s, ip=%(ip)s, comment=%(comment)s where id=%(id)s"
            cursor.execute(sql, dict(id=id_, name=name, ip=ip, comment=comment))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id, name, ip, comment FROM host WHERE id=%(id)s"
            cursor.execute(sql, {'id': id_})
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()


if __name__ == '__main__':
    # 查看模块 pymysql 支持的 参数风格
    print(pymysql.paramstyle)  # 输出结果: pyformat

    '''
    fetchall_databases()
    '''

    # 测试 insert 操作
    '''
        fetchall_databases()
        host = dict(
            name='mysql_server',
            ip='192.168.175.100',
            comment='中文描述: 数据库服务器'
        )

        insert(**host)
    '''

    # 测试 update 操作
    host = dict(
        name='mysql_server',
        ip='192.168.175.100',
        comment='修改后的中文描述: 数据库服务器'
    )
    host['id_'] = 1
    update(**host)
