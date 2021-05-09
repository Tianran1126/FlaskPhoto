from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


class User(db.Model,UserMixin):
   id=db.Column(db.Integer, primary_key=True)
   email=db.Column(db.String(150), unique=True)
   password=db.Column(db.String(150))
   first_name=db.Column(db.String(150))  
   photos=db.relationship('Photo') 

class Photo(db.model):
   id=db.Column(db.Integer,primary_key=True)    
   description=db.Column(db.String(10000))
   path=db.Column(db.String(150))
   user_id=db.Column(db.Integer,db.ForeignKey('user.id'))