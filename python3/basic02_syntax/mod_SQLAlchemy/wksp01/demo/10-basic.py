from sqlalchemy import Column, Integer, String

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


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    adding_and_updating_objects()
