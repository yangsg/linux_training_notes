from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:WWW.1.com@192.168.175.100/db_test01?charset=utf8mb4", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)




