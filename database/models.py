from .dp import db

class Patient(db.Document):
    surname = db.StringField(required=True)
    name = db.StringField(required=True)
    amka = db.StringField(required=True,unique=True)
    contactphone=db.StringField(required=True)
    doctor=db.StringField(required=True)
    roomn=db.StringField(required=True)
    bedn=db.StringField(required=True)
