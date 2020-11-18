from .dp import db
import mongoengine_goodjson as gj

"""
Each collection in the mongo db is here depicted as a class
with its respective fields, and an object of each class is invoked 
from the Api to pass information or actions to the db
"""
"""
Validation rules are also applied here
"""
class Patient(gj.Document):
    surname = db.StringField(required=True,min_length=1)
    name = db.StringField(required=True,min_length=1)
    amka = db.StringField(required=True,unique=True,min_length=10,max_length=10)
    contactphone=db.StringField(required=True,min_length=10,max_length=10)

class Case(gj.Document):
    patientID=db.ObjectIdField(required=True,unique=True)
    roomn=db.StringField(required=True,min_length=1)
    bedn=db.StringField(required=True,min_length=1)
    doctor=db.StringField(required=True,min_length=1)
    covidStatus=db.StringField(required=True,min_length=1)

