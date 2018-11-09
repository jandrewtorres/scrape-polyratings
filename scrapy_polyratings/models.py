from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.mysql import DOUBLE, ENUM, DATETIME, TEXT

from scrapy_polyratings import db_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        db_settings.DATABASE['username'],
        db_settings.DATABASE['password'],
        db_settings.DATABASE['host'],
        db_settings.DATABASE['port'],
        db_settings.DATABASE['database'])

    return create_engine(connect_string)


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Professor(DeclarativeBase):
    """Sqlalchemy professor model"""
    __tablename__ = "professor"

    pid = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(20))
    last_name = Column('last_name', String(20))
    department = Column('department', String(50))

    mysql_engine = 'InnoDB'
    mysql_charset = 'utf8mb4'
    mysql_key_block_size = '1024'


class Review(DeclarativeBase):
    """Sqlalchemy review model"""
    __tablename__ = "review"

    rid = Column('rid', Integer, primary_key=True)
    pid = Column('pid', Integer, ForeignKey(Professor.pid))
    content = Column('content', TEXT)
    class_name = Column('class_name', String((20)))
    rating_overall = Column('rating_overall', DOUBLE(precision=4, scale=2))
    rating_difficulty = Column('rating_difficulty',
                               DOUBLE(precision=4, scale=2))
    reason_taking = Column('reason_taking', ENUM('R', 'S', 'E'))
    date_posted = Column('date_posted', DATETIME)
    grade_received = Column('grade_received', String(10))
    class_standing = Column('class_standing', String(20))

    mysql_engine = 'InnoDB'
    mysql_charset = 'utf8mb4'
    mysql_key_block_size = '1024'
