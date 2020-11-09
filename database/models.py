from .dp import db
import mongoengine_goodjson as gj

class Patient(gj.Document):
    surname = db.StringField(required=True)
    name = db.StringField(required=True)
    amka = db.StringField(required=True,unique=True)
    contactphone=db.StringField(required=True)

class Case(gj.Document):
    patientID=db.ObjectIdField(required=True)
    roomn=db.StringField(required=True)
    bedn=db.StringField(required=True)
    doctor=db.StringField(required=True)
    status=db.BooleanField(required=True)
    covidStatus=db.BooleanField(required=True)

