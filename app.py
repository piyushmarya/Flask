from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_resource import RegistorUser
from resources.item_resource import Item, ItemList
from db import db

app = Flask(__name__)
app.secret_key = "hhh"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///database/data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
db.init_app(app)
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(RegistorUser,'/signup')


if  __name__ == "__main__":
    app.run(port=5000)
