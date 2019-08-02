from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from demo.dbutil import Session, Base, print_header


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#configuring-delete-delete-orphan-cascade
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    addresses = relationship("Address", back_populates='user',
                             cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#configuring-delete-delete-orphan-cascade
def configuring_delete_or_delete_orphan_cascade():
    session = Session()

    print_header()
    '''
    Now when we load the user jack (below using get(), which loads by primary key),
    removing an address from the corresponding addresses collection
    will result in that Address being deleted:


    '''

    '''
    get() 方法:
        SELECT
                user.id       AS user_id      ,
                user.name     AS user_name    ,
                user.fullname AS user_fullname,
                user.nickname AS user_nickname
        FROM
                user
        WHERE   user.id = %(param_1)s

    {'param_1': 5}
    '''
    # load Jack by primary key
    jack = session.query(User).get(5)

    print_header()
    # remove one Address (lazy load fires off)
    del jack.addresses[1]
    '''
    DELETE FROM address WHERE address.id = %(id)s
    {'id': 2}
    '''

    # only one address remains
    count = session.query(Address).filter(
        Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
    ).count()
    print(count)
    '''
    1
    '''

    '''
    Deleting Jack will delete both Jack and the remaining Address associated with the user:
    '''

    print_header()
    session.delete(jack)
    '''
     如上 delete() 方法 效果:
        DELETE FROM address WHERE address.id = %(id)s
        {'id': 1}
        DELETE FROM user WHERE user.id = %(id)s
        {'id': 5
    '''

    count = session.query(User).filter_by(name='jack').count()
    print(count)
    '''
    0
    '''

    count = session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()
    print(count)
    '''
    0
    '''

    '''
    More on Cascades

        Further detail on configuration of cascades is at Cascades.
        The cascade functionality can also integrate smoothly
        with the ON DELETE CASCADE functionality of the relational database.
        See Using Passive Deletes for details.

        https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades
        https://docs.sqlalchemy.org/en/13/orm/collections.html#passive-deletes

    '''

    # session.commit()   # 仅演示, 所以没有 commit
    session.close()


if __name__ == '__main__':
    configuring_delete_or_delete_orphan_cascade()
