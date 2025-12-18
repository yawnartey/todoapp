from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

#connect to sqlite
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#connect to postgresql on local
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:enoch1234!@localhost/TodoApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#connect to postgresql on local via docker
SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:enoch1234!@host.docker.internal/TodoApplicationDatabase'
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#this ensures local changes are not automatically commited to the databse
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#create a base which is an object of the database to manipulate the tables in the database
Base = declarative_base()