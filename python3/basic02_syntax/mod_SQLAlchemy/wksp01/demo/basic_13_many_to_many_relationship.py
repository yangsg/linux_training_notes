from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from demo.basic_12_delete_cascade import User
from demo.dbutil import Base, engine, Session, print_header

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
    session = Session()

    # Usage is not too different from what we’ve been doing. Let’s give Wendy some blog posts:
    wendy = session.query(User).filter_by(name='wendy').one()
    post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
    session.add(post)

    '''
    We’re storing keywords uniquely in the database, but we know that we
    don’t have any yet, so we can just create them:
    '''

    post.keywords.append(Keyword('wendy'))
    post.keywords.append(Keyword('firstpost'))

    print_header()
    '''
    We can now look up all blog posts with the keyword ‘firstpost’.
    We’ll use the any operator to locate “blog posts where
    any of its keywords has the keyword string ‘firstpost’”:
    '''
    '''
    相关语句:
    INSERT INTO keyword (keyword) VALUES (%(keyword)s)
    {'keyword': 'wendy'}

    INSERT INTO keyword (keyword) VALUES (%(keyword)s)
    {'keyword': 'firstpost'}

    INSERT INTO post (user_id, headline, body) VALUES (%(user_id)s, %(headline)s, %(body)s)
    {'user_id': 2, 'headline': "Wendy's Blog Post", 'body': 'This is a test'}

    INSERT INTO post_keyword_rel (post_id, keyword_id) VALUES (%(post_id)s, %(keyword_id)s)
    ({'post_id': 1, 'keyword_id': 1}, {'post_id': 1, 'keyword_id': 2})


    SELECT
            post.id       AS post_id      ,
            post.user_id  AS post_user_id ,
            post.headline AS post_headline,
            post.body     AS post_body
    FROM
            post
    WHERE   EXISTS
            (SELECT
                    1
            FROM
                    post_keyword_rel,
                    keyword
            WHERE   post.id             = post_keyword_rel.post_id
                    AND keyword.id      = post_keyword_rel.keyword_id
                    AND keyword.keyword = %(keyword_1)s
            )

    {'keyword_1': 'firstpost'}
    '''
    session.query(BlogPost).filter(BlogPost.keywords.any(keyword='firstpost')).all()

    print_header()
    '''
    If we want to look up posts owned by the user wendy, we can tell the query to narrow down to that User object as a parent:
    '''
    '''
        SELECT
                post.id       AS post_id      ,
                post.user_id  AS post_user_id ,
                post.headline AS post_headline,
                post.body     AS post_body
        FROM
                post
        WHERE   %(param_1)s = post.user_id
                AND
                (EXISTS
                        (SELECT
                                1
                        FROM
                                post_keyword_rel,
                                keyword
                        WHERE   post.id             = post_keyword_rel.post_id
                                AND keyword.id      = post_keyword_rel.keyword_id
                                AND keyword.keyword = %(keyword_1)s
                        ))

        {'param_1': 2, 'keyword_1': 'firstpost'}
    '''
    blogposts = session.query(BlogPost).filter(BlogPost.author == wendy).filter(
        BlogPost.keywords.any(keyword='firstpost')).all()
    print(blogposts)
    '''
    [BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]
    '''

    print_header()
    '''
    Or we can use Wendy’s own posts relationship, which is a “dynamic” relationship, to query straight from there:

    SELECT
            post.id       AS post_id      ,
            post.user_id  AS post_user_id ,
            post.headline AS post_headline,
            post.body     AS post_body
    FROM
            post
    WHERE   %(param_1)s = post.user_id
            AND
            (EXISTS
                    (SELECT
                            1
                    FROM
                            post_keyword_rel,
                            keyword
                    WHERE   post.id             = post_keyword_rel.post_id
                            AND keyword.id      = post_keyword_rel.keyword_id
                            AND keyword.keyword = %(keyword_1)s
                    ))

    {'param_1': 2, 'keyword_1': 'firstpost'}
    '''
    posts = wendy.posts.filter(BlogPost.keywords.any(keyword='firstpost')).all()
    print(posts)
    '''
    [BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]
    '''

    session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    building_a_many_to_many_relationship()
