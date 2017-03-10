# A file that abstracts away the querying of the restaurantmenu database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def query(string):
    # Functon for querying the database (Read operations)
    con = engine.connect()
    return con.execute('%s'%string)

def commit(string):
    # Function for modifying the database (CUD operations)
    con = engine.connect()
    con.execute('%s'%string)
    con.commit()
    con.close()
    return
