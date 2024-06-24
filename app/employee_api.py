from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db
from app.models import Employee, Seat, Employee_seat, Room, Office
from flask import jsonify
from flask_restful import  Resource, reqparse

  


class Employee_api(Resource):
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
        params = self.get_args("name", "surname", "email", location='args')
        if params["name"] or params["surname"] or params["email"]:
            employees_from_db = db.session.scalars(sa.select(Employee).where(sa.or_(Employee.name == params["name"], Employee.surname == params["surname"], Employee.email == params["email"])))
            employees =self.convert_to_json(employees_from_db) 
            return employees, 200       
        else:
            return "Employee not found", 404
        
    def post(self):
        params = self.get_args("name","surname", "email")
        employee = Employee(name=params["name"], surname=params["surname"], email= params["email"])
        try:
            db.session.add(employee)
            db.session.commit()
            return employee.serialize(), 200
        except Exception as e:
            return f"Error {e} was occured", 400

    def put(self):
        params = self.get_args("name","surname", "email")
        try:
            employee = db.session.scalar(sa.select(Employee).where(Employee.email == params["email"]))
            if params["name"]:
                employee.name = params["name"]
            if params["surname"]:
                employee.surname = params["surname"]
            #db.session.add(employee)
            db.session.commit()
            return employee.serialize(), 200       
        except:
            return "Employee not found. Enter unique field [email] correctly!", 404



    def delete(self):
        params = self.get_args("name","surname", "email")
        try:
            employee_id = db.session.scalar(sa.select(Employee.id).where(Employee.email == params["email"]))
            employee = db.session.get(Employee, employee_id)
            db.session.delete(employee)
            db.session.commit()
            return "Employee was deleted successfully!", 200   
        except Exception as e:
            #return "Employee not found. Enter unique field [email] correctly!", 404
            return f"Error {e} was occured", 400