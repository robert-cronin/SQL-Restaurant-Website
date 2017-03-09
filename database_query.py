# A file that abstracts away the querying of the restaurantmenu database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def query(string):
    con = engine.connect()
    return con.execute('%s'%string)

def insert(string):
    con = engine.connect()
    con.execute('%s'%string)
    con.commit()

def delete(string):

def update(string):
