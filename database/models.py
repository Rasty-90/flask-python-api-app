from .dp import db
import mongoengine_goodjson as gj

"""
Each collection in the mongo db is here depicted as a class
with its respective fields, and an object of each class is invoked 
from the Api to pass information or actions to the db
"""

class Patient(gj.Document):
    surname = db.StringField(required=True)
    name = db.StringField(required=True)
    amka = db.StringField(required=True,unique=True)
    contactphone=db.StringField(required=True)

class Case(gj.Document):
    patientID=db.ObjectIdField(required=True,unique=True)
    roomn=db.StringField(required=True)
    bedn=db.StringField(required=True)
    doctor=db.StringField(required=True)
    covidStatus=db.StringField(required=True)

