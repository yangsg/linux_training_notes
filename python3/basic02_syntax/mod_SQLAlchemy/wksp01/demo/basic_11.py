from sqlalchemy import Column, Integer, String, ForeignKey, func, exists
from sqlalchemy.orm import relationship, aliased

from demo.basic_10 import User, print_header
from demo.dbutil import Base, Session, engine


# Building a Relationship
#   https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-relationship
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="addresses")

    '''
    CREATE TABLE address (
        id INTEGER NOT NULL AUTO_INCREMENT,
        email_address VARCHAR(50) NOT NULL,
        user_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user (id)
    )

    mysql> show create table address;

    | address | CREATE TABLE `address` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `email_address` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
      `user_id` int(11) DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `user_id` (`user_id`),
      CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |


    '''

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")


#   https://docs.sqlalchemy.org/en/13/orm/tutorial.html#working-with-related-objects
def working_with_related_objects():
    session = Session()
    '''
        Now when we create a User, a blank addresses collection will be present.
    '''
    jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
    print(jack.addresses)
    '''
    []
    '''

    jack.addresses = [
        Address(email_address='jack@google.com'),
        Address(email_address='j25@yahoo.com')]

    '''
    When using a bidirectional relationship, elements added in
    one direction automatically become visible in the other direction.
    This behavior occurs based on attribute on-change events and
    is evaluated in Python, without using any SQL:
    '''
    print_header()
    print(jack.addresses[1])
    '''
    <Address(email_address='j25@yahoo.com')>
    '''
    print_header()
    print(jack.addresses[1].user)
    '''
    <User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
    '''

    print_header()
    '''
    Let’s add and commit Jack Bean to the database.
    jack as well as the two Address members in the
    corresponding addresses collection are both added to the session at once,
    using a process known as cascading:


        INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
        ('jack', 'Jack Bean', 'gjffdd')
        INSERT INTO addresses (email_address, user_id) VALUES (?, ?)
        ('jack@google.com', 5)
        INSERT INTO addresses (email_address, user_id) VALUES (?, ?)
        ('j25@yahoo.com', 5)
        COMMIT
    '''
    session.add(jack)
    session.commit()
    '''
        mysql> select * from user where id = 5;
        +----+------+-----------+----------+
        | id | name | fullname  | nickname |
        +----+------+-----------+----------+
        |  5 | jack | Jack Bean | gjffdd   |
        +----+------+-----------+----------+

        mysql> select * from address;
        +----+-----------------+---------+
        | id | email_address   | user_id |
        +----+-----------------+---------+
        |  1 | jack@google.com |       5 |
        |  2 | j25@yahoo.com   |       5 |
        +----+-----------------+---------+
    '''

    print_header()
    '''
      如下这段话是指在 还没有 commit 的时候:
    Querying for Jack, we get just Jack back. No SQL is yet issued for Jack’s addresses:
    '''
    jack = session.query(User).filter_by(name='jack').one()
    print(jack)

    print_header()
    '''
        When we accessed the addresses collection, SQL was suddenly issued.
        This is an example of a lazy loading relationship. The addresses collection
        is now loaded and behaves just like an ordinary list.
        We’ll cover ways to optimize the loading of this collection in a bit.
    '''
    print(jack.addresses)   # 此处 应用 延迟加载(lazy loading), 此时才会发送 sql 语句.

    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
def querying_with_joins():
    session = Session()

    print_header()
    '''
    使用 Query.filter() 进行 等值 比较 可以 构建 简单的 隐式的 join 查询(
    即 where 子句 这种老语法 表示的 join).

    To construct a simple implicit join between User and Address,
    we can use Query.filter() to equate their related columns together.
    Below we load the User and Address entities at once using this method:

        SELECT users.id AS users_id,
                users.name AS users_name,
                users.fullname AS users_fullname,
                users.nickname AS users_nickname,
                addresses.id AS addresses_id,
                addresses.email_address AS addresses_email_address,
                addresses.user_id AS addresses_user_id
        FROM users, addresses
        WHERE users.id = addresses.user_id
                AND addresses.email_address = ?
        ('jack@google.com',)
    '''
    for u, a in session.query(User, Address).filter(User.id == Address.user_id).filter(
            Address.email_address == 'jack@google.com').all():
        print(u)
        print(a)
        '''
        <User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
        <Address(email_address='jack@google.com')>
        '''

    print_header()
    '''
    使用 Query.join() 方法 生成 真实的 join 语句.

    The actual SQL JOIN syntax, on the other hand, is most easily achieved using the Query.join() method:

        SELECT user.id AS user_id,
               user.name AS user_name,
               user.fullname AS user_fullname,
               user.nickname AS user_nickname
        FROM user INNER JOIN address
             ON user.id = address.user_id
        WHERE address.email_address = %(email_address_1)s

        {'email_address_1': 'jack@google.com'}
    '''
    users = session.query(User).join(Address).filter(Address.email_address == 'jack@google.com').all()
    print(users)
    '''
    [<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>]
    '''

    print_header()
    '''
      针对 没有 外键 或 多个 外键 的 情况, 如下示例的方式 比较适合:
        Query.join() knows how to join between User and Address because
        there’s only one foreign key between them. If there were no foreign keys,
        or several, Query.join() works better when one of the following forms are used:

            query.join(Address, User.id==Address.user_id)    # explicit condition
            query.join(User.addresses)                       # specify relationship from left to right
            query.join(Address, User.addresses)              # same, with explicit target
            query.join('address')                            # same, using a string
    '''

    print_header()
    '''
      针对 outer join 使用 outerjoin() 方法

      As you would expect, the same idea is used for “outer” joins, using the outerjoin() function:

        SELECT user.id AS user_id,
               user.name AS user_name,
               user.fullname AS user_fullname,
               user.nickname AS user_nickname
        FROM user LEFT OUTER JOIN address
            ON user.id = address.user_id
    '''
    users = session.query(User).outerjoin(User.addresses).all()  # LEFT OUTER JOIN
    print(users)
    '''
    [<User(name='ed', fullname='Ed Jones', nickname='eddie')>,
     <User(name='wendy', fullname='Wendy Williams', nickname='windy')>,
     <User(name='mary', fullname='Mary Contrary', nickname='mary')>,
     <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>,
     <User(name='jack', fullname='Jack Bean', nickname='gjffdd')>]
    '''
    for u in users:
        print(u.name + '-' * 100)
        for a in u.addresses:
            print(a)
    '''
    join 方法的 更多信息见:
    https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join
    '''

    print_header()
    '''
    What does Query select from if there’s multiple entities?

        The Query.join() method will typically join from the leftmost
        item in the list of entities, when the ON clause is omitted,
        or if the ON clause is a plain SQL expression. To control
        the first entity in the list of JOINs, use the Query.select_from() method:

        query = session.query(User, Address).select_from(Address).join(User)

       SELECT user.id AS user_id,
              user.name AS user_name,
              user.fullname AS user_fullname,
              user.nickname AS user_nickname,
              address.id AS address_id,
              address.email_address AS address_email_address,
              address.user_id AS address_user_id
        FROM address INNER JOIN user
            ON user.id = address.user_id

           {}
    '''
    data = session.query(User, Address).select_from(Address).join(User).all()
    print(data)
    '''
    [(<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>, <Address(email_address='jack@google.com')>),
    (<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>, <Address(email_address='j25@yahoo.com')>)]
    '''

    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-aliases
def using_aliases():
    session = Session()

    print_header()
    '''
    别名函数 aliased

        在一条sql 语句中 同一 table 被多次引用时 很有用(如自连接查询等)

    SELECT
            user.name               AS user_name              ,
            address_1.email_address AS address_1_email_address,
            address_2.email_address AS address_2_email_address
    FROM
            user
    INNER JOIN address AS address_1 ON user.id = address_1.user_id
    INNER JOIN address AS address_2 ON user.id = address_2.user_id
    WHERE   address_1.email_address            = %(email_address_1)s
            AND address_2.email_address        = %(email_address_2)s


        {'email_address_1': 'jack@google.com', 'email_address_2': 'j25@yahoo.com'}
    '''
    adalias1 = aliased(Address)
    adalias2 = aliased(Address)
    for username, email1, email2 in \
            session.query(User.name, adalias1.email_address, adalias2.email_address). \
                    join(adalias1, User.addresses). \
                    join(adalias2, User.addresses). \
                    filter(adalias1.email_address == 'jack@google.com'). \
                    filter(adalias2.email_address == 'j25@yahoo.com'):
        print(username, email1, email2)
        '''
        jack jack@google.com j25@yahoo.com
        '''
    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-subqueries
def using_subqueries():
    session = Session()

    '''
    整个 子查询语句:
        SELECT
                user.id              AS user_id      ,
                user.name            AS user_name    ,
                user.fullname        AS user_fullname,
                user.nickname        AS user_nickname,
                anon_1.address_count AS anon_1_address_count
        FROM
                user
        LEFT OUTER JOIN
                (SELECT
                        address.user_id    AS user_id,
                        count(%(count_1)s) AS address_count
                FROM
                        address
                GROUP BY
                        address.user_id
                ) AS anon_1 ON user.id = anon_1.user_id
        ORDER BY
                user.id

        {'count_1': '*'}
    '''
    stmt = session.query(Address.user_id, func.count('*').label('address_count')
                         ).group_by(Address.user_id).subquery()

    for u, count in session.query(User, stmt.c.address_count
                                  ).outerjoin(stmt, User.id == stmt.c.user_id).order_by(User.id):
        print(u, count)
        '''
        <User(name='ed', fullname='Ed Jones', nickname='eddie')> None
        <User(name='wendy', fullname='Wendy Williams', nickname='windy')> None
        <User(name='mary', fullname='Mary Contrary', nickname='mary')> None
        <User(name='fred', fullname='Fred Flintstone', nickname='freddy')> None
        <User(name='jack', fullname='Jack Bean', nickname='gjffdd')> 2
        '''
    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#selecting-entities-from-subqueries
def selecting_entities_from_subqueries():
    session = Session()

    print_header()
    '''
    整个 sql 语句:
    SELECT
            user.id              AS user_id             ,
            user.name            AS user_name           ,
            user.fullname        AS user_fullname       ,
            user.nickname        AS user_nickname       ,
            anon_1.id            AS anon_1_id           ,
            anon_1.email_address AS anon_1_email_address,
            anon_1.user_id       AS anon_1_user_id
    FROM
            user
    INNER JOIN
            (SELECT
                    address.id            AS id           ,
                    address.email_address AS email_address,
                    address.user_id       AS user_id
            FROM
                    address
            WHERE   address.email_address != %(email_address_1)s
            ) AS anon_1 ON user.id = anon_1.user_id

    {'email_address_1': 'j25@yahoo.com'}
    '''
    stmt = session.query(Address).filter(Address.email_address != 'j25@yahoo.com').subquery()
    adalias = aliased(Address, stmt)
    for user, address in session.query(User, adalias).join(adalias, User.addresses):
        print(user)
        print(address)
        '''
        <User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
        <Address(email_address='jack@google.com')>
        '''

    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-exists
def using_exists():
    session = Session()

    print_header()
    '''
    SELECT
            user.name AS user_name
    FROM
            user
    WHERE   EXISTS
            (SELECT * FROM address WHERE address.user_id = user.id
            )

    {}
    '''
    stmt = exists().where(Address.user_id == User.id)
    for name, in session.query(User.name).filter(stmt):
        print(name)
        '''
        jack
        '''

    print_header()
    '''
    一些 自动生成 EXISTS 子句的 特性

    any()
      如上示例中 包含 EXISTS 的语句 可以使用 User.addresses.any():

        SELECT
                user.name AS user_name
        FROM
                user
        WHERE   EXISTS
                (SELECT 1 FROM address WHERE user.id = address.user_id
                )

        {}
    '''
    for name, in session.query(User.name).filter(User.addresses.any()):
        print(name)
        '''
        jack
        '''

    print_header()
    '''
    any() takes criterion as well, to limit the rows matched:

        SELECT
                user.name AS user_name
        FROM
                user
        WHERE   EXISTS
                (SELECT
                        1
                FROM
                        address
                WHERE   user.id                      = address.user_id
                        AND address.email_address LIKE %(email_address_1)s
                )

        {'email_address_1': '%google%'}
    '''
    for name, in session.query(User.name).filter(User.addresses.any(Address.email_address.like('%google%'))):
        print(name)
        '''
        jack
        '''

    print_header()
    '''
    has() is the same operator as any() for many-to-one relationships (note the ~ operator here too, which means “NOT”):

    SELECT
            address.id            AS address_id           ,
            address.email_address AS address_email_address,
            address.user_id       AS address_user_id
    FROM
            address
    WHERE   NOT
            (EXISTS
                    (SELECT
                            1
                    FROM
                            user
                    WHERE   user.id       = address.user_id
                            AND user.name = %(name_1)s
                    ))

    {'name_1': 'jack'}
    '''
    data = session.query(Address).filter(~Address.user.has(User.name == 'jack')).all()
    print(data)
    '''
    []
    '''

    session.close()

'''
一些常用 的 关系 运算符:

Common Relationship Operators

    https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-relationship-operators

1) __eq__() (many-to-one “equals” comparison):
        query.filter(Address.user == someuser)

2) __ne__() (many-to-one “not equals” comparison):
        query.filter(Address.user != someuser)

3) IS NULL (many-to-one comparison, also uses __eq__()):
        query.filter(Address.user == None)

4) contains() (used for one-to-many collections):
        query.filter(User.addresses.contains(someaddress))

5) any() (used for collections):
        query.filter(User.addresses.any(Address.email_address == 'bar'))

        # also takes keyword arguments:
        query.filter(User.addresses.any(email_address='bar'))

6) has() (used for scalar references):
        query.filter(Address.user.has(name='ed'))

7) Query.with_parent() (used for any relationship):
        session.query(Address).with_parent(someuser, 'addresses')
'''

if __name__ == '__main__':
    # is_reinitialize_db_needed = True
    is_reinitialize_db_needed = False
    if is_reinitialize_db_needed:
        Base.metadata.create_all(engine)

        working_with_related_objects()

    querying_with_joins()
    using_aliases()

    using_subqueries()
    selecting_entities_from_subqueries()
    using_exists()
