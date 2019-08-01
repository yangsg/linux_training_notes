from collections import Iterable

from sqlalchemy import Column, Integer, String, inspect, text
from sqlalchemy.orm import aliased

from demo.dbutil import Base, Session, engine


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


def print_header(msg=None):
    if msg:
        print(msg)

    print('\n' * 2)
    print(('-' * 100 + '\n') * 4)


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

    session.close()


if __name__ == '__main__':
    # is_reinitialize_db_needed = True
    is_reinitialize_db_needed = False
    if is_reinitialize_db_needed:
        drop_table('user')

        Base.metadata.create_all(engine)

        adding_and_updating_objects()

        rolling_back()

    # query---------------------------------------------------------------------------------------------------
    querying()
