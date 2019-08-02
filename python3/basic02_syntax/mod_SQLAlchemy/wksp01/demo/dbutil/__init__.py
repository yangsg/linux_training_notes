from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:WWW.1.com@192.168.175.100/db_test01?charset=utf8mb4", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def print_header(msg=None):  # 该函数 仅用于 输出 分隔线, 是为了学习 观察用的
    if msg:
        print(msg)

    print('\n' * 2)
    print(('-' * 100 + '\n') * 4)
