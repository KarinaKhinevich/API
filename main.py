from flask import Flask 
from flask_restful import Api, Resource, reqparse
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import Employee, Seat, Employee_seat, Room, Office


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Employee': Employee, 'Seat': Seat, 'Employee_seat': Employee_seat, 'Room': Room, 'Office': Office}

if __name__ == '__main__':
    app.run(debug=True)