from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)



from app import   employee_api, models, office_api, room_api

api.add_resource(employee_api.Employee_api, "/employee", "/employee/")
api.add_resource(office_api.Office_api, "/office", "/office/")
api.add_resource(room_api.Room_api, "/room", "/room/")