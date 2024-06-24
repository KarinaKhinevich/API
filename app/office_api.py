from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db
from app.models import  Office
from flask import jsonify
from flask_restful import  Resource, reqparse

  


class Office_api(Resource):
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
   
    def get(self):
        params = self.get_args("address", "title", location='args')
        if params["address"] or params["title"] :
            office_from_db = db.session.scalar(sa.select(Office).where(sa.or_(Office.address == params["address"], Office.title == params["title"])))
            office = office_from_db.serialize() 
            return office, 200       
        else:
            return "Office not found", 404
        
    def post(self):
        params = self.get_args("address", "title")
        office = Office(address=params["address"], title=params["title"])
        try:
            db.session.add(office)
            db.session.commit()
            return office.serialize(), 200
        except Exception as e:
            return f"Error {e} was occured", 400

    def put(self):
        params = self.get_args("address", "title")
        try:
            office = db.session.scalar(sa.select(Office).where(sa.or_(Office.address == params["address"], Office.title == params["title"])))
            if params["title"]:
                office.title = params["title"]
            if params["address"]:
                office.address = params["address"]
            #db.session.add(office)
            db.session.commit()
            return office.serialize(), 200       
        except:
            return "Office not found. Enter unique field [address or title] correctly!", 404



    def delete(self):
      ...