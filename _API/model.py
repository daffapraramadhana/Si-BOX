from DateTime import Timezones
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import update

db = SQLAlchemy()


class Door(db.Model):
    __tablename__ = 'doors'
    no = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, default = datetime.now(tz=None))
    updated = db.Column(db.DateTime, default = datetime.now(tz=None), onupdate = datetime.utcnow)

    def __init__(self, no, state):
        self.no = no
        self.state = state

    
    def __repr__(self):
        return ('%r' % self.no)

    def to_json(self):
        json_doors = {
            'no' : self.no,
            'state' : self.state,
            'created' : self.created.strftime('%Y-%m-%d %H:%M:%S'),
            'update' : self.updated.strftime('%Y-%m-%d %H:%M:%S')
        }
        return (json_doors)

    



    