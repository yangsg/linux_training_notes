from sqlalchemy import Column, Integer, String, inspect, text, func
from sqlalchemy.orm import aliased

from demo.dbutil import Base, Session, engine, print_header


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#adding-and-updating-objects
def adding_and_updating_objects():
    session = Session()
    ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
    session.add(ed_user)
    '''
     此处执行 query 之前, 所有 等待的信息(pending information) 都会被 flush(即
     issue the SQL to persist, 但注意此时仅是 发送 sql 语句,但并没有对其 commit),
     然后再 立即执行 query 语句.
    '''
    our_user = session.query(User).filter_by(name='ed').first()
    print(our_user)

    '''
    事实上, the Session 识别(identified)出  返回的 该 row 与 其内部的 objects 的 map 中
    已经存在的 row 相同, 因此 我们实际 获得的 实例对象 就是 我们 正好 added 的 实例对象.

    关于 identity map 的 信息 见:
        https://docs.sqlalchemy.org/en/13/glossary.html#term-identity-map
    '''
    print(ed_user is our_user)  # 输出 True, 证明 变量 ed_user 和 our_user 引用同一对象

    # 一次性 添加 多个对象
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', nickname='windy'),
        User(name='mary', fullname='Mary Contrary', nickname='mary'),
        User(name='fred', fullname='Fred Flintstone', nickname='freddy')])

    # 此时 如果 修改 ed_user 的 属性(如 nickname), 因为 The Session is paying attention.
    # 所以, 它直到(It knows) 对象 ed_user 被 修改了
    ed_user.nickname = 'eddie'
    print(session.dirty)  # 输出  IdentitySet([<User(name='ed', fullname='Ed Jones', nickname='eddie')>])

    # 同时, 它 还直到 有 3 个 对象正在 等待中(and that three new User objects are pending)
    print(session.new)

    # commit 会 flush 剩下的 changes 到 数据库 并 commit 事务.
    # 归还 session 引用的 connection 资源 给 Engine 的 connection pool.
    # 该 session 的后续操作 将在 一个 新的事务(new transaction) 中 执行.
    # 其将在 首次 需要的 时候 再次重新 从 Engine 的 connection pool 中获取 connection resources
    session.commit()
    '''
    commit() 执行的 操作 和 效果:
        commit() flushes the remaining changes to the database,
        and commits the transaction. The connection resources referenced
        by the session are now returned to the connection pool.
        Subsequent operations with this session will occur in a new transaction,
        which will again re-acquire connection resources when first needed.
    '''

    print(ed_user.id)
    session.close()
    '''
       After the Session inserts new rows in the database,
       all newly generated identifiers and database-generated defaults become
       available on the instance, either immediately or via load-on-first-access.
       In this case, the entire row was re-loaded on access because
       a new transaction was begun after we issued commit().
       SQLAlchemy by default refreshes data from a previous
       transaction the first time it’s accessed within a new transaction,
       so that the most recent state is available.
       The level of reloading is configurable as is described in Using the Session.
    '''

    '''
    Quickie Intro to Object States
        https://docs.sqlalchemy.org/en/13/orm/session_state_management.html#session-object-states
    '''

    ''' 观察 sqlalchemy 在背后 生成 和 执行的语句, 可以观察到, 在 执行 session.commit() 后, 隐式的 开启了 一个新的 事务
    2019-07-31 19:41:47,904 INFO sqlalchemy.engine.base.Engine UPDATE user SET nickname=%(nickname)s WHERE user.id = %(user_id)s
    2019-07-31 19:41:47,904 INFO sqlalchemy.engine.base.Engine {'nickname': 'eddie', 'user_id': 9}
    2019-07-31 19:41:47,989 INFO sqlalchemy.engine.base.Engine INSERT INTO user (name, fullname, nickname) VALUES (%(name)s, %(fullname)s, %(nickname)s)
    2019-07-31 19:41:47,989 INFO sqlalchemy.engine.base.Engine {'name': 'wendy', 'fullname': 'Wendy Williams', 'nickname': 'windy'}
    2019-07-31 19:41:47,997 INFO sqlalchemy.engine.base.Engine INSERT INTO user (name, fullname, nickname) VALUES (%(name)s, %(fullname)s, %(nickname)s)
    2019-07-31 19:41:47,997 INFO sqlalchemy.engine.base.Engine {'name': 'mary', 'fullname': 'Mary Contrary', 'nickname': 'mary'}
    2019-07-31 19:41:48,012 INFO sqlalchemy.engine.base.Engine INSERT INTO user (name, fullname, nickname) VALUES (%(name)s, %(fullname)s, %(nickname)s)
    2019-07-31 19:41:48,012 INFO sqlalchemy.engine.base.Engine {'name': 'fred', 'fullname': 'Fred Flintstone', 'nickname': 'freddy'}
    2019-07-31 19:41:48,013 INFO sqlalchemy.engine.base.Engine COMMIT
    2019-07-31 19:41:48,016 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)  <---- 观察
    2019-07-31 19:41:48,016 INFO sqlalchemy.engine.base.Engine SELECT user.id AS user_id, user.name AS user_name, user.fullname AS user_fullname, user.nickname AS user_nickname
    FROM user
    WHERE user.id = %(param_1)s
    2019-07-31 19:41:48,016 INFO sqlalchemy.engine.base.Engine {'param_1': 9}
    '''


def print_state(msg, obj):
    print(('-' * 100 + '\n') * 5)
    insp = inspect(obj)
    print(msg)
    if insp.transient:
        print('InstanceState.transient')
    elif insp.pending:
        print('InstanceState.pending')
    elif insp.persistent:
        print('InstanceState.persistent')
    elif insp.deleted:
        print('InstanceState.deleted')
    elif insp.detached:
        print('InstanceState.detached')

    print(('-' * 100 + '\n') * 5)


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#rolling-back
# https://docs.sqlalchemy.org/en/13/orm/session_state_management.html#session-object-states
def rolling_back():
    print('\n' * 9)
    print('rolling_back')
    session = Session()

    ed_user = session.query(User).filter_by(name='ed').first()
    print_state('queried ed_user', ed_user)  # 状态: persistent

    ed_user.name = 'Edwardo'
    print_state('the queried ed_user is modified', ed_user)  # 状态: persistent
    fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
    print_state('new fake_user and before add: ', fake_user)  # 状态: transient

    session.add(fake_user)
    print_state('new fake_user and after add: ', fake_user)  # 状态: pending

    users = session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
    print_state('added the new fake_user and after flush: ', fake_user)  # 状态: persistent
    print(users)

    session.rollback()

    print(ed_user.name)  # 输出 'ed', 可以看到, rollback 之后 ed_user 的 修改被还原了
    print_state('modify operation of the queried ed_user is rollbacked:', ed_user)  # 状态: persistent

    print(fake_user in session)  # 输出 false, 可以看到, rollback 之后, 新对象被踢出了 session, 有变成了 transient 状态
    print_state('new fake_user and after rollback: ', fake_user)  # 状态: transient

    print('*****\n' * 5)
    print(session.query(User).filter(
        User.name.in_(['ed', 'fakeuser'])).all())  # 输出 [<User(name='ed', fullname='Ed Jones', nickname='eddie')>]

    session.close()

    print_state('the queried ed_user after session closed:', ed_user)  # 状态: detached
    print_state('new fake_user after session closed', fake_user)  # 状态: transient


def drop_table(tablename):
    session = Session()
    session.execute(f'drop table if exists {tablename}')
    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying
'''
 A Query object is created using the query() method on Session.
 This function takes a variable number of arguments,
 which can be any combination of classes and class-instrumented descriptors.
'''


def querying():
    session = Session()

    print_header()
    '''
    SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
    FROM users ORDER BY users.id
    ()
    '''
    for instance in session.query(User).order_by(User.id):  # // the list of User objects present is returned:
        print(instance.name, instance.fullname)
        '''
        ed Ed Jones
        wendy Wendy Williams
        mary Mary Contrary
        fred Fred Flintstone
        '''

    print_header()
    '''
    SELECT users.name AS users_name,
        users.fullname AS users_fullname
    FROM users
    ()
    '''
    for name, fullname in session.query(User.name, User.fullname):
        print(name, fullname)
        '''
        ed Ed Jones
        wendy Wendy Williams
        mary Mary Contrary
        fred Fred Flintstone
        '''

    print_header()
    '''
    KeyedTuple class
    https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.util.KeyedTuple

       The tuples returned by Query are named tuples, supplied by the KeyedTuple class,
       and can be treated much like an ordinary Python object.
       The names are the same as the attribute’s name for an attribute,
       and the class name for a class:

    SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
    FROM users
    ()
    '''
    for row in session.query(User, User.name).all():
        print(row.User, row.name)
        '''
        <User(name='ed', fullname='Ed Jones', nickname='eddie')> ed
        <User(name='wendy', fullname='Wendy Williams', nickname='windy')> wendy
        <User(name='mary', fullname='Mary Contrary', nickname='mary')> mary
        <User(name='fred', fullname='Fred Flintstone', nickname='freddy')> fred
        '''

    print_header()
    '''
    SELECT users.name AS name_label
    FROM users
    ()
    '''
    for row in session.query(User.name.label('name_label')).all():
        print(row.name_label)
        '''
        ed
        wendy
        mary
        fred
        '''

    print_header()
    '''
    SELECT user.name AS name_label, user.fullname AS fullname_label
    '''
    for row in session.query(User.name.label('name_label'), User.fullname.label('fullname_label')).all():
        print(f'{row.name_label:<20}, {row.fullname_label:>20}')
        '''
        ed                  ,             Ed Jones
        wendy               ,       Wendy Williams
        mary                ,        Mary Contrary
        fred                ,      Fred Flintstone
        '''

    print_header()
    '''
    aliased()

        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.aliased

    SELECT user_alias.id AS user_alias_id,
        user_alias.name AS user_alias_name,
        user_alias.fullname AS user_alias_fullname,
        user_alias.nickname AS user_alias_nickname
    FROM users AS user_alias
    ()
    '''
    user_alias = aliased(User, name='user_alias')
    for row in session.query(user_alias, user_alias.name).all():
        print(row.user_alias)
        '''
        <User(name='ed', fullname='Ed Jones', nickname='eddie')>
        <User(name='wendy', fullname='Wendy Williams', nickname='windy')>
        <User(name='mary', fullname='Mary Contrary', nickname='mary')>
        <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
        '''

    print_header()
    '''
    LIMIT 和 OFFSET

        Basic operations with Query include issuing LIMIT and OFFSET,
        most conveniently using Python array slices and typically in conjunction with ORDER BY:

        SELECT users.id AS users_id,
               users.name AS users_name,
               users.fullname AS users_fullname,
               users.nickname AS users_nickname
        FROM users ORDER BY users.id
        LIMIT ? OFFSET ?
        (2, 1)
        此处计算方式:
             2 = 3 - 1
             1 = 1
    '''
    for u in session.query(User).order_by(User.id)[1:3]:
        print(u, u.id)
        '''
        <User(name='wendy', fullname='Wendy Williams', nickname='windy')>
        <User(name='mary', fullname='Mary Contrary', nickname='mary')>
        '''

    print_header()
    '''
    filter_by keyword arguments

        and filtering results, which is accomplished either with filter_by(),
        which uses keyword arguments:

    SELECT users.name AS users_name FROM users
    WHERE users.fullname = ?
    ('Ed Jones',)
    '''
    for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
        print(name)
        '''
        ed
        '''

    print_header()
    '''
    filter()

        …or filter(), which uses more flexible SQL expression language constructs.
        These allow you to use regular Python operators with the class-level attributes on your mapped class:

    SELECT users.name AS users_name FROM users
    WHERE users.fullname = ?
    ('Ed Jones',)
    '''
    for name, in session.query(User.name).filter(User.fullname == 'Ed Jones'):
        print(name)
        '''
        ed
        '''

    print_header()
    '''
    The Query object is fully generative, meaning that most method
    calls return a new Query object upon which further criteria may be added.
    For example, to query for users named “ed” with a full name of “Ed Jones”,
    you can call filter() twice, which joins criteria using AND:

       SELECT users.id AS users_id,
            users.name AS users_name,
            users.fullname AS users_fullname,
            users.nickname AS users_nickname
        FROM users
        WHERE users.name = ? AND users.fullname = ?
        ('ed', 'Ed Jones')
    '''
    for user in session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones'):
        print(user)
        '''
        <User(name='ed', fullname='Ed Jones', nickname='eddie')>
        '''

    '''
    Common Filter Operators

        https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators

    Here’s a rundown of some of the most common operators used in filter():

    1) equals:
        query.filter(User.name == 'ed')
    2) not equals:
        query.filter(User.name != 'ed')
    3) LIKE:
        query.filter(User.name.like('%ed%'))
    4) ILIKE (case-insensitive LIKE):
        query.filter(User.name.ilike('%ed%'))

         注: 大多数后端 数据库 都不直接支持 ILIKE, 针对这些数据库,
             the ColumnOperators.ilike() operator 会 结合 LIKE 与 sql 函数 LOWER
             来实现该效果
    5) IN:
        query.filter(User.name.in_(['ed', 'wendy', 'jack']))

        # works with query objects too:
        query.filter(User.name.in_(
            session.query(User.name).filter(User.name.like('%ed%'))
        ))

    6) NOT IN:
        query.filter(~User.name.in_(['ed', 'wendy', 'jack']))

    7) IS NULL:
        query.filter(User.name == None)

        # alternatively, if pep8/linters are a concern
        query.filter(User.name.is_(None))
    8) IS NOT NULL:
        query.filter(User.name != None)

        # alternatively, if pep8/linters are a concern
        query.filter(User.name.isnot(None))

    9) AND:
              注: Make sure you use and_() and not the Python and operator!
        # use and_()
        from sqlalchemy import and_
        query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

        # or send multiple expressions to .filter()
        query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

        # or chain multiple filter()/filter_by() calls
        query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')

    10) OR:
               注: Make sure you use or_() and not the Python or operator!
        from sqlalchemy import or_
        query.filter(or_(User.name == 'ed', User.name == 'wendy'))

    11) MATCH:
        query.filter(User.name.match('wendy'))

        注: match() uses a database-specific MATCH or CONTAINS function;
           its behavior will vary by backend and is not available on some backends such as SQLite.

    '''

    session.close()


'''
 https://docs.sqlalchemy.org/en/13/orm/tutorial.html#returning-lists-and-scalars
    A number of methods on Query immediately issue SQL and return a value
    containing loaded database results. Here’s a brief tour:
'''


def returning_lists_and_scalars():
    session = Session()
    print_header()
    '''
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.all

    1) all() returns a list:

        SELECT users.id AS users_id,
            users.name AS users_name,
            users.fullname AS users_fullname,
            users.nickname AS users_nickname
        FROM users
        WHERE users.name LIKE ? ORDER BY users.id
        ('%ed',)

    '''
    query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
    print(query.all())
    '''
        [<User(name='ed', fullname='Ed Jones', nickname='eddie')>,
          <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>]
    '''

    print_header()
    '''
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.first

    2) first() applies a limit of one and returns the first result as a scalar:

        SELECT users.id AS users_id,
                users.name AS users_name,
                users.fullname AS users_fullname,
                users.nickname AS users_nickname
        FROM users
        WHERE users.name LIKE ? ORDER BY users.id
         LIMIT ? OFFSET ?
        ('%ed', 1, 0)

    '''
    print(query.first())
    '''
    <User(name='ed', fullname='Ed Jones', nickname='eddie')>
    '''

    print_header()
    '''
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one

    one() 的 使用场景:
       The one() method is great for systems that expect to handle
       “no items found” versus “multiple items found” differently;
       such as a RESTful web service, which may want to raise
       a “404 not found” when no results are found,
       but raise an application error when multiple results are found.

    3) one() fully fetches all rows, and if not exactly one object identity
       or composite row is present in the result, raises an error.
       With multiple rows found:
    '''
    # user = query.one()  # one() 在 检索到 多行 时 会 raise error "MultipleResultsFound"
    '''
        Traceback (most recent call last):
        ...
        MultipleResultsFound: Multiple rows were found for one()
    '''

    '''
      With no rows found ,
        则 raise error： NoResultFound
    '''
    # user = query.filter(User.id == 99).one()  #  one() 在没有检索到时 会 raise error "NoResultFound"

    '''

    one()

        SELECT user.id AS user_id,
               user.name AS user_name,
               user.fullname AS user_fullname,
               user.nickname AS user_nickname
        FROM user
        WHERE user.name LIKE %(name_1)s AND
              user.id = %(id_1)s ORDER BY user.id

        {'name_1': '%ed', 'id_1': 1}
    '''
    # user = query.filter(User.id == 1).one()
    # print(user)
    '''
    <User(name='ed', fullname='Ed Jones', nickname='eddie')>
    '''

    '''
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one_or_none

    one_or_none() 类似于 one(), 但是其 在 没有 检索到 results 时, 仅返回 None 而非 raise an error;

        one_or_none() is like one(), except that if no results are found,
        it doesn’t raise an error; it just returns None. Like one(),
        however, it does raise an error if multiple results are found.
    '''

    print_header()
    '''
    4) scalar() invokes the one() method, and upon success returns the first column of the row:

        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.scalar

        SELECT user.id AS user_id
        FROM user
        WHERE user.name = %(name_1)s ORDER BY user.id

        {'name_1': 'ed'}
    '''
    query = session.query(User.id).filter(User.name == 'ed').order_by(User.id)
    print(query.scalar())
    '''
        1
    '''

    session.close()


'''
using_textual_sql

    Literal strings can be used flexibly with Query,
    by specifying their use with the text() construct,
    which is accepted by most applicable methods.
    For example, filter() and order_by():
'''


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-textual-sql
def using_textual_sql():
    session = Session()

    print_header()
    '''
    SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
    FROM users
    WHERE id<224 ORDER BY id
    ()
    '''
    for user in session.query(User).filter(text("id<224")).order_by(text("id")).all():
        print(user.name)
        '''
        ed
        wendy
        mary
        fred
        '''

    print_header()
    '''
    绑定参数, 通过 形如 :name 的方式来 传递参数
        Bind parameters can be specified with string-based SQL,
        using a colon. To specify the values, use the params() method:

       SELECT user.id AS user_id,
           user.name AS user_name,
           user.fullname AS user_fullname,
           user.nickname AS user_nickname
       FROM user
       WHERE id<%(value)s and name=%(name)s ORDER BY user.id

       {'value': 224, 'name': 'fred'}
    '''
    user = session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(
        User.id).one()
    print(user)
    '''
    <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
    '''

    '''
    通过 from_statement() 使用 完整的 基于 string 的 (sql)语句
        To use an entirely string-based statement, a text() construct
        representing a complete statement can be passed to from_statement().
        Without additional specifiers, the columns in the string SQL
        are matched to the model columns based on name, such as below
        where we use just an asterisk to represent loading all columns:
    '''
    print_header()

    '''
    SELECT * FROM user where name=%(name)s
    {'name': 'ed'}
    '''
    users = session.query(User).from_statement(
        text("SELECT * FROM user where name=:name")).params(name='ed').all()
    print(users)
    '''
    [<User(name='ed', fullname='Ed Jones', nickname='eddie')>]
    '''

    print_header()
    '''
    TextClause.columns()

    更多示例见:
        https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns
        https://docs.sqlalchemy.org/en/13/core/tutorial.html#sqlexpression-text


        Matching columns on name works for simple cases but can become unwieldy
        when dealing with complex statements that contain duplicate column names
        or when using anonymized ORM constructs that don’t easily match to
        specific names. Additionally, there is typing behavior present
        in our mapped columns that we might find necessary when
        handling result rows. For these cases, the text() construct
        allows us to link its textual SQL to Core or ORM-mapped column
        expressions positionally; we can achieve this by passing column
        expressions as positional arguments to the TextClause.columns() method:


        SELECT name, id, fullname, nickname FROM user where name=%(name)s
        {'name': 'ed'}
    '''
    stmt = text("SELECT name, id, fullname, nickname FROM user where name=:name")
    stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
    users = session.query(User).from_statement(stmt).params(name='ed').all()
    print(users)
    '''
    [ < User(name='ed', fullname='Ed Jones', nickname='eddie') >]
    '''

    print_header()

    '''
    指明 返回 特定的 columns
        When selecting from a text() construct,
        the Query may still specify what columns and entities are to be returned;
        instead of query(User) we can also ask for the columns individually, as in any other case:

        SELECT name, id FROM user where name=%(name)s

        {'name': 'ed'}
    '''
    stmt = text("SELECT name, id FROM user where name=:name")
    stmt = stmt.columns(User.name, User.id)
    data = session.query(User.id, User.name).from_statement(stmt).params(name='ed').all()
    print(data)
    '''
        [(1, 'ed')
    '''

    session.close()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#counting
#   Query includes a convenience method for counting called count():
def counting():
    session = Session()

    print_header()
    '''
     注: 就向如下 生成的语句那样, 使用 Query 的 count() 方法时 SQLAlchemy 总是
         会 将 我们 查询的 数据  置于 一个 子查询(a subquery) 中. 然后
         再 根据 数据的 行数 来得到 我们想要的 count. 所以如果想要使用更
         简单的 形如 SELECT count(*) FROM table 的 查询语句, 则需要明确
         的指定 这种 简单的方式, 而不是使用 SQLAlchemy 的 count() 方法.

        SELECT count(*) AS count_1
        FROM (SELECT user.id AS user_id,
                     user.name AS user_name,
                     user.fullname AS user_fullname,
                     user.nickname AS user_nickname
              FROM user
              WHERE user.name LIKE %(name_1)s) AS anon_1

        {'name_1': '%ed'}

    如下这段话 解释了 Query 的 count函数 粗暴的使用 子查询 计算 count 的 原因:
        Counting on count()
            Query.count() used to be a very complicated method
            when it would try to guess whether or not a subquery
            was needed around the existing query,
            and in some exotic cases it wouldn’t do the right thing.
            Now that it uses a simple subquery every time,
            it’s only two lines long and always returns the right answer.
            Use func.count() if a particular statement
            absolutely cannot tolerate the subquery being present.
    '''
    count = session.query(User).filter(User.name.like('%ed')).count()
    print(count)
    '''
    2
    '''

    print_header()
    '''
    使用更加灵活的 func.count()

        For situations where the “thing to be counted” needs to be
        indicated specifically, we can specify the “count” function directly
        using the expression func.count(), available from the func construct.
        Below we use it to return the count of each distinct user name:

    '''

    print_header()
    '''
    SELECT count(user.name) AS count_1, user.name AS user_name
    FROM user GROUP BY user.name
    '''
    data = session.query(func.count(User.name), User.name).group_by(User.name).all()
    print(data)
    '''
    [(1, 'ed'), (1, 'fred'), (1, 'mary'), (1, 'wendy')]
    '''

    print_header()
    '''
    使用 我们 最 简单的  SELECT count(*) FROM table 方式:

        To achieve our simple SELECT count(*) FROM table, we can apply it as:

        SELECT count(%(count_2)s) AS count_1 FROM user
    '''
    count = session.query(func.count('*')).select_from(User).scalar()
    print(count)
    '''
    4
    '''

    print_header()
    '''
    如果 直接根据 User 的 主键(primary key) 来计算 count, 则还可以去掉 select_from() 的调用.

        The usage of select_from() can be removed if
        we express the count in terms of the User primary key directly:

        SELECT count(user.id) AS count_1 FROM user
    '''
    count = session.query(func.count(User.id)).scalar()
    print(count)
    '''
    4
    '''

    session.close()


if __name__ == '__main__':
    # is_reinitialize_db_needed = True
    is_reinitialize_db_needed = False
    if is_reinitialize_db_needed:
        drop_table('user')

        Base.metadata.create_all(engine)

        adding_and_updating_objects()

        # rolling_back()

    # query---------------------------------------------------------------------------------------------------
    querying()
    returning_lists_and_scalars()
    using_textual_sql()
    counting()
