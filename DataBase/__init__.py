from Declarative_Base import Base
import Declarative_RawItems
import Declarative_RawLots
import Declarative_Labs
import Declarative_Common

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
cwd = os.getcwd()

#create engine to connect to database
db_path = cwd + "\\DataBase\\DFHDB.db"
engine = create_engine('sqlite:///' + db_path)

#create database tables
Base.metadata.create_all(engine)

#create a session to communicate with the database
Session = sessionmaker(bind=engine, expire_on_commit=False)