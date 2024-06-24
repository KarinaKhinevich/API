from datetime import datetime, date, time, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from dataclasses import dataclass

class Office(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
   
    rooms: so.WriteOnlyMapped['Room'] = so.relationship(back_populates='office')
    def __repr__(self):
        return '<Office at {}>'.format(self.address)


class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    numder: so.Mapped[int] = so.mapped_column(sa.Integer, index = True)
    office_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Office.id),index = True)
    seat: so.WriteOnlyMapped['Seat'] = so.relationship(back_populates='room')
    office: so.Mapped[Office] = so.relationship(back_populates='rooms')

    def __repr__(self):
        return '<Room #{}>'.format(self.number)
    
class Seat(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    numder: so.Mapped[int] = so.mapped_column(sa.Integer, index = True)
    availability: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id),index = True)

    employee: so.WriteOnlyMapped['Employee_seat'] = so.relationship(back_populates='seats')
    room: so.Mapped[Room] = so.relationship(back_populates='seat')
    def __repr__(self):
        return '<Seat #{}>'.format(self.body)

class Employee(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    seat: so.WriteOnlyMapped['Employee_seat'] = so.relationship(back_populates='employee')

    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'surname': self.surname,
            'email': self.email
        }
    
    def __repr__(self):
        return '<Employee {} {}>'.format(self.surname, self.name)
    

class Employee_seat(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    occupation_date: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: date.now(timezone.utc))
    occupation_time: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: time.now(timezone.utc))
    occupation_duration: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.time(1))


    employee: so.Mapped[Employee] = so.relationship(back_populates='seat')
    seats: so.Mapped[Seat] = so.relationship(back_populates='employee')

    seat_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Seat.id),index = True)
    emplayee_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Employee.id),index = True)

    def __repr__(self):
        return '<Employee {} booked seat #{} at{} on{} for{} hours>'.format(self.emplayee_id, self.seat_id, self.occupation_time, self.occupation_date, self. occupation_duration)