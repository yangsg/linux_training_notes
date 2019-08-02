from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from demo.basic_12_delete_cascade import User
from demo.dbutil import Base, engine

# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-many-to-many-relationship

'''
For a plain many-to-many, we need to create an un-mapped Table construct
to serve as the association table. This looks like the following:
'''

# 创建一个 非映射的 额外的 Table 作为 many-to-many 的 关联关系表,
# 这里使用了 后缀 _rel 来表示 关系表(relationship), 用以和普通表 作区分.
# association table
post_keyword_rel = Table('post_keyword_rel', Base.metadata,
                         Column('post_id', ForeignKey('post.id'), primary_key=True),
                         Column('keyword_id', ForeignKey('keyword.id'), primary_key=True)
                         )

'''
CREATE TABLE post_keyword_rel (
    post_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, keyword_id),
    FOREIGN KEY(post_id) REFERENCES post (id),
    FOREIGN KEY(keyword_id) REFERENCES keyword (id)
)
'''
'''
注:  如果关联关系表 包含有 自己特有的 列(字段), 如 主键 或 其他 属性列, 则 需要使用 另外一种不同的
     称为 “association object” 的 使用模式(usage pattern)

原文:
    This table only contains columns which reference the two sides
    of the relationship; if it has any other columns, such as its own primary key,
    or foreign keys to other tables, SQLAlchemy requires a different usage pattern
    called the “association object”, described at Association Object.

关于 association object 更多信息见:
    https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-pattern
'''


class BlogPost(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # 这里 使用 关键字参数 secondary 指定表示 关联关系表的 Table object(此例为 post_keyword_rel)
    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword',
                            secondary=post_keyword_rel,
                            back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


'''
CREATE TABLE post (
	id INTEGER NOT NULL AUTO_INCREMENT,
	user_id INTEGER,
	headline VARCHAR(255) NOT NULL,
	body TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES user (id)
)
'''


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                         secondary=post_keyword_rel,
                         back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword


'''
    CREATE TABLE keyword (
        id INTEGER NOT NULL AUTO_INCREMENT,
        keyword VARCHAR(50) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (keyword)
    )
'''

'''
    We would also like our BlogPost class to have an author field.
    We will add this as another bidirectional relationship, except one issue we’ll have
    is that a single user might have lots of blog posts. When we access User.posts,
    we’d like to be able to filter results further so as
    not to load the entire collection. For this we use a setting
    accepted by relationship() called lazy='dynamic',
    which configures an alternate loader strategy on the attribute:
'''
BlogPost.author = relationship(User, back_populates="posts")
User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-many-to-many-relationship
def building_a_many_to_many_relationship():
    pass


if __name__ == '__main__':
    print('*' * 10)
    Base.metadata.create_all(engine)
