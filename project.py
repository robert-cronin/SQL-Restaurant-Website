# Flask framework
from flask import Flask
app = Flask(__name__)

# Import all required sqlalchemy functionality
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import database_setup classes
from database_setup import Base, Restaurant, MenuItem

# Create session for CRUD operations
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = '' # Create output html string
    for i in items:
        output += i.name
        output += '</br>'
        output += "<span>%s </span><span> %s</span>"%(i.price, i.description)
        output += '<br><br>'
    return output

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/newmenu')
def newMenuItem(restaurant_id):

    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/editmenu')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deletemenu')
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = '' # Create output html string
    output += "<h1>Are you sure you want to delete this menu?</h1>"
    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/d/delete'>"
    output += "<input type='submit' value='Delete'>"
    output += "</form>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
