from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

'''
https://docs.sqlalchemy.org/en/13/orm/tutorial.html#connecting

mysql 连接示例:
    https://docs.sqlalchemy.org/en/13/core/engines.html#mysql

Database Urls:
    https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls

    典型的 database url 格式:
    dialect+driver://username:password@host:port/database

        如果 url 中 包含 特殊字符的参数, 可以使用类似如下的方式转义:
        加入 password 为 "kx%jj5/g"
        >>> import urllib.parse
        >>> urllib.parse.quote_plus("kx%jj5/g")
        'kx%25jj5%2Fg'

        则最后的 db url 样子如下:
            postgresql+pg8000://dbuser:kx%25jj5%2Fg@pghost10/appdb

mysql的 DBAPI Support:
    https://docs.sqlalchemy.org/en/13/dialects/mysql.html

unicode 编码:
    https://docs.sqlalchemy.org/en/13/dialects/mysql.html#mysql-unicode
    mysql 从 5.5.3 版本开始支持 'utf8mb4', 应该使用该 'utf8mb4' 编码,
    如果要支持 4 字节的 codepoints, 则 必须使用 此编码.

'''
# 注: Lazy Connecting
#     当 首次 调用 create_engine 返回 Engine, 其并不会实际
#     真的去 connect 数据库, 只有当 需要 基于 database 执行某些任务时(如 调用
#     Engine.execute() 或 Engine.connect() ), 才会去 建立数据库连接.

# 如下 参数 echo=True 用于 log 输出 相关生成的 sql 语句, 仅用户 调试 或  学习用
engine = create_engine("mysql+pymysql://root:WWW.1.com@192.168.175.100/db_test01?charset=utf8mb4", echo=True)

'''
关于 连接 mysql 时设置 collation_connection 为  'utf8mb4_unicode_ci' 的方式
https://stackoverflow.com/questions/47661458/configure-the-connection-collation-with-sqlalchemy

但是,
如果后台的 mysqld 的配置如果合理, 其实也 不需要在客户端代码中 明确设置 collation_connection,
关于后台 mysqld 关于 utf8mb4 的设置见:

https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/006-mha4mysql-semi-sync-gtid-utf8mb4-rpm

'''
'''
connect_args = {'init_command': "SET @@collation_connection='utf8mb4_unicode_ci'"}
engine = create_engine("mysql+pymysql://root:WWW.1.com@192.168.175.100/db_test01?charset=utf8mb4",
                       connect_args=connect_args,
                       echo=True)

'''

'''
# 一些常见的 创建 Engine 对象的方式:
    # default
    engine = create_engine('mysql://scott:tiger@localhost/foo')

    # mysqlclient (a maintained fork of MySQL-Python)
    engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

    # PyMySQL
    engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
'''

'''
Declare a Mapping
    https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping

    通过 Declarative, 可以创建包含 用于描述 其 映射到的 database table 的 directives 的 classes
       https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/index.html

      Classes 使用 根据 一个基类 定义的 the Declarative system 来实现映射.
      该基类就是 declarative base class, 其维护着与其关联的 classes 和 tables
      的 一个 目录 ( a catalog).  我们的 application 通常会在 a commonly imported module
      中 为其 创建唯一的 instance (即保持其单例),  该 基类(base class) 使用 declarative_base()
      来创建.

      原文:
      Classes mapped using the Declarative system are defined in terms of a base class
      which maintains a catalog of classes and tables relative to that base - this
      is known as the declarative base class.
      Our application will usually have just one instance of this base
      in a commonly imported module.
      We create the base class using the declarative_base() function, as follows:
'''

Base = declarative_base()  # 创建 Base 类, 其维护着一个 与其 关联着的 classes 和 tables 的 catalog.

'''
有了 Base 类对象 之后, 就可以根据它 来创建 任意数量的 被映射的 Class
(即与 table 具有映射 关系的Class). 通过 the Declarative system 来实现
'''


class User(Base):  # 定义映射类 User, 其必须继承 Base 类
    __tablename__ = 'user'  # 属性(attribute) __tablename__ 声明了 类 User 映射到数据库表 user
    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # 注: 在SQLite 和 PostgreSQL 针对 varchar 可以不指定 length, 但其他数据库必须指定.
    fullname = Column(String(50))
    nickname = Column(String(50))
    '''
    注: 如果是 oracle 数据库, 可能需要使用 如下的方式 指定 id 字段
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    '''

    '''
    When our class is constructed, Declarative replaces all the Column objects
    with special Python accessors known as descriptors;
    this is a process known as instrumentation.
    The “instrumented” mapped class will provide us with
    the means to refer to our table in a SQL context as well as
    to persist and load the values of columns from the database.
    '''

    def __repr__(self):  # 注: 方法 __repr__ 定义不是必须的, 此处只是为了便于观察学习
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


'''
Create a Schema

'''

# 利用 User.__table__ 观察类 User 映射表的 table metadata
print(User.__table__)

'''
一旦 映射类 的声明 完成, Declarative 会 使用  a Python metaclass 来 执行
一些额外的 活动, 则此期间, 它 会 根据映射类中的 描述信息 创建 一个  Table 对象,
并通过构建 一个 Mapper 对象来 建立 Table 对象 和 mapped Class 的 关联关系.

该 Table 对象 是一个 名为  MetaData 的较大的 集合(collection) 的成员(member),
当使用 Declarative 时, 可以通过 我们的 declarative base class 来 对其引用,
如 Base.MetaData

MetaData 是 a registry, 其包含一种 向 database 发送(emit)
a limited set of schema generation commands 的 能力

'''

'''
如下 2 行 语句 仅用于 调试观察用, 看一下 连接用的 @@collation_connection 是否是 'utf8mb4_unicode_ci'
'''
conn = engine.connect()
print(conn.execute('select @@collation_connection;').fetchall())
'''
2019-07-31 14:48:27,315 INFO sqlalchemy.engine.base.Engine select @@collation_connection;
2019-07-31 14:48:27,315 INFO sqlalchemy.engine.base.Engine {}
[('utf8mb4_unicode_ci',)]
'''

# 向 engine 表示的 database 发送创建 tables 的语句
Base.metadata.create_all(engine)

'''
如下是 SQLAlchemy 这个 ORM 框架 为 映射类 User 生成的 create table 语句.
    CREATE TABLE user (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(50),
        fullname VARCHAR(50),
        nickname VARCHAR(50),
        PRIMARY KEY (id)
    )

在 mysql server 上 查看一下 对应的 create table 语句:
mysql> show create table user;

    | user  | CREATE TABLE `user` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      `fullname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      `nickname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |

  可以看到, CHARSET 和 COLLATE 都 符合 预期
'''

'''
如下 2 行 语句 仅用于 调试观察用, 看一下 连接用的 @@collation_connection 是否是 'utf8mb4_unicode_ci'
'''
print(conn.execute('select @@collation_connection;').fetchall())
conn.close()
'''
2019-07-31 14:48:27,386 INFO sqlalchemy.engine.base.Engine select @@collation_connection;
2019-07-31 14:48:27,386 INFO sqlalchemy.engine.base.Engine {}
[('utf8mb4_unicode_ci',)]
'''

'''
Create an Instance of the Mapped Class
https://docs.sqlalchemy.org/en/13/orm/tutorial.html#create-an-instance-of-the-mapped-class
'''
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user.name)
print(ed_user.nickname)
print(ed_user.id)  # 注意: 此处输出 None

'''
关于 如上 ed_user.id 输出 None 的解释:
    Even though we didn’t specify it in the constructor, the id attribute still
    produces a value of None when we access it (as opposed to Python’s usual
    behavior of raising AttributeError for an undefined attribute).
    SQLAlchemy’s instrumentation normally produces this default value
    for column-mapped attributes when first accessed. For those attributes
    where we’ve actually assigned a value, the instrumentation system
    is tracking those assignments for use within an eventual
    INSERT statement to be emitted to the database.
'''

''' the __init__() method

关于 __init__ 方法

    Our User class, as defined using the Declarative system, has been provided with a constructor
    (e.g. __init__() method) which automatically accepts keyword names that match
    the columns we’ve mapped. We are free to define any explicit __init__() method
    we prefer on our class, which will override the default method provided by Declarative.
'''

'''
Creating a Session¶

    https://docs.sqlalchemy.org/en/13/orm/tutorial.html#creating-a-session

    session 表示 与 database 的 会话

We’re now ready to start talking to the database.
The ORM’s “handle” to the database is the Session.
When we first set up the application, at the same level
as our create_engine() statement, we define a Session class
which will serve as a factory for new Session objects:

'''
# 定义 Session 类, 其 作为 新的 Session 实例对象的 工厂函数
Session = sessionmaker(bind=engine)  # 调用  sessionmaker 时还可以定义 事务特征

'''
In the case where your application does not yet have an Engine
when you define your module-level objects, just set it up like this:

    >>> Session = sessionmaker()

Later, when you create your engine with create_engine(),
connect it to the Session using configure():

    >>> Session.configure(bind=engine)  # once engine is available
'''

# 注: 只有在 第一次使用 session 时, session 才会 从 Engine 维护的
#     connections pool 中 获取 a connection, 并 对其 一直 占有 直到
#     we commit all changes and/or close the session object.
session = Session()

'''
关于 从 connections pool 获取 connection 及 session 占有 connection 的时间:
    The above Session is associated with our SQLite-enabled Engine,
    but it hasn’t opened any connections yet. When it’s first used,
    it retrieves a connection from a pool of connections maintained
    by the Engine, and holds onto it until we commit
    all changes and/or close the session object.

'''

'''
Session Lifecycle Patterns

The question of when to make a Session depends a lot
on what kind of application is being built. Keep in mind,
the Session is just a workspace for your objects,
local to a particular database connection -
if you think of an application thread as a guest at a dinner party,
the Session is the guest’s plate and the objects it holds are the food
(and the database…the kitchen?)! More on this topic available at
When do I construct a Session, when do I commit it, and when do I close it?.


When do I construct a Session, when do I commit it, and when do I close it?
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate

Session Frequently Asked Questions
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-frequently-asked-questions
'''

'''
When do I make a sessionmaker?

    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-frequently-asked-questions

    仅 一次, 在 你的 application 的 global scope 的 某处.
    其 应该 被当做 你的  application’s configuration 的 一部分部分
    来 看待.  If your application has three .py files in a package, you could, for example,
    place the sessionmaker line in your __init__.py file;
    from that point on your other modules say “from mypackage import Session”.

     如:
        mkdir mypkg
        vim mypkg/__init__.py
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker

            engine = create_engine("mysql+pymysql://root:WWW.1.com@192.168.175.100/db_test01?charset=utf8mb4", echo=True)
            Session = sessionmaker(bind=engine)

       vim example.py

            from mypkg import Session
            session = Session()

       If your application starts up, does imports,
       but does not know what database it’s going to be connecting to,
       you can bind the Session at the “class” level to the engine later on,
       using sessionmaker.configure().
'''

'''
When do I construct a Session, when do I commit it, and when do I close it?

    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-frequently-asked-questions

1. As a general rule, keep the lifecycle of the session separate and external
   from functions and objects that access and/or manipulate database data.
   This will greatly help with achieving a predictable and consistent transactional scope.

2. Make sure you have a clear notion of where transactions begin and end,
   and keep transactions short, meaning, they end at the series
   of a sequence of operations, instead of being held open indefinitely.


Some web frameworks include infrastructure to assist in the task
of aligning the lifespan of a Session with that of a web request.
This includes products such as Flask-SQLAlchemy, for usage
in conjunction with the Flask web framework, and Zope-SQLAlchemy,
typically used with the Pyramid framework. SQLAlchemy recommends
that these products be used as available.

    https://flask-sqlalchemy.palletsprojects.com/en/2.x/

    https://pypi.org/project/zope.sqlalchemy/

In those situations where the integration libraries are not provided
or are insufficient, SQLAlchemy includes its own “helper” class
known as scoped_session. A tutorial on the usage of this object
is at Contextual/Thread-local Sessions.
It provides both a quick way to associate a Session with the current thread,
as well as patterns to associate Session objects with other kinds of scopes.

    https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual

As mentioned before, for non-web applications there is no one clear pattern,
as applications themselves don’t have just one pattern of architecture.
The best strategy is to attempt to demarcate “operations”, points
at which a particular thread begins to perform a series of operations
for some period of time, which can be committed at the end. Some examples:

  - A background daemon which spawns off child forks would want
    to create a Session local to each child process, work with that
    Session through the life of the “job” that the fork is handling,
    then tear it down when the job is completed.

  - For a command-line script, the application would create a single,
    global Session that is established when the program begins to do its work,
    and commits it right as the program is completing its task.

  - For a GUI interface-driven application, the scope of the Session may best be within
    the scope of a user-generated event, such as a button push. Or, the scope may
    correspond to explicit user interaction, such as the user “opening”
    a series of records, then “saving” them.

'''

'''
session 不是  thread-safe 的.
所以 应该在 单线程 中 使用 session(包括与 session 关联的 所有 objects).

如果把 session 比作 盘子, 把 thread 比作 顾客,
那么 进入 餐厅之后, 应该是 一个 盘子仅属于 一个 顾客,
而不是 一个盘子 同时让 不同的顾客使用.
'''










