from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db
from app.models import  Room
from flask import jsonify
from flask_restful import  Resource, reqparse

  


class Room_api(Resource):
    def convert_to_json(self, array):
        result = []
        for item in array:
            result.append(item.serialize())
        return result
    
    def get_args(self,*args, location = None):
        parser = reqparse.RequestParser()
        for arg in args:
            if  location :
                parser.add_argument(arg, location = location)
            else:
                parser.add_argument(arg)
        return parser.parse_args()
    
    def check_if_exist(self, room_number, room_office_id):
        room = db.session.scalar(sa.select(Room).where(sa.and_(Room.number == room_number, Room.office_id == room_office_id)))
        return True if room else False

    def get(self):
        params = self.get_args("number", "office_id", location='args')
        if params["number"] or params["office_id"] :
            rooms_from_db = db.session.scalars(sa.select(Room).where(sa.or_(Room.number == params["number"], Room.office_id == params["office_id"])))
            rooms = self.convert_to_json(rooms_from_db)
            return rooms, 200       
        else:
            return "Room not found", 404
        
    def post(self):
        params = self.get_args("number", "office_id")
        try:
            if self.check_if_exist(params["number"], params["office_id"]):
                room = Room(number=params["number"], office_id=params["office_id"])
                db.session.add(room)
                db.session.commit()
                return room.serialize(), 200
            else:
                return "Such room is exist", 400
        except Exception as e:
            return f"Error '{e}' was occured", 400

    def put(self):
        params = self.get_args("number", "office_id", "id")
        try:
            room = db.session.scalar(sa.select(Room).where(Room.id == params["id"]))
            if room:
                if params["number"]:
                    if not self.check_if_exist(params["number"], room.office_id ):
                        room.number = params["number"]
                    else: 
                        return "Such room is exist", 400
                if params["office_id"]:
                    if not self.check_if_exist(room.number , params["office_id"]):
                        room.office_id = params["office_id"]
                    else: 
                        return "Such room is exist", 400
                #db.session.add(Room)
                db.session.commit()
                return room.serialize(), 200       
            else:
                return "Room not found. Enter unique field [id] correctly!", 400
        except Exception as e:
            return f"Error '{e}' was occured", 400


    def delete(self):
      ...