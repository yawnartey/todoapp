from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#connect to sqlite
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#connect to postgresql 
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:enoch1234!@localhost/TodoApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#this ensures local changes are not automatically commited to the databse
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#initialised base class required by SQLAlchemy to map python classes to database tables
Base = declarative_base()