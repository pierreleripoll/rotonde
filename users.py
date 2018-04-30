from sqlalchemy import *
from sqlalchemy.sql import *

engine = create_engine('sqlite:///:memory:', echo=True)

metadata = MetaData()

users = Table('users', metadata,
            Column('id', Integer, autoincrement=True, primary_key=True),
            Column('name', String))

emails = Table('emails', metadata,
            Column('id', Integer, autoincrement=True, primary_key=True),
            Column('uid', None, ForeignKey('users.id')),
            Column('email', String, nullable=False))

metadata.create_all(engine)
connection = engine.connect()

# (...)

connection.close()     
