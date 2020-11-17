from flask import Response, request
from database.models import Patient
from flask_restful import Resource
from mongoengine.errors import NotUniqueError,OperationError
import json

"""
This file contains the patient API resource structure with basic CRUD functionality. Each resource
is represented as a different class
"""

class PatientsApi(Resource):
    """
    This function gets all the Patient objects from the database
    """
    def get(self):
        #the order_by() is used to return results sorted by surname
        patients = Patient.objects().order_by('surname').to_json()
        #creates a dictionary over the Mongo Object so that it can be parsed
        #as a json file from the rest of the program
        dicts = json.loads(patients)
        return dicts,200

    """
    This function creates a new patient object to the database
    """
    def post(self):
        body = request.get_json()
        try:
            patient= Patient(**body).save()
        #handles the NotUniqueError in case the user tries to create an index
        #with an already existing unique field(AMKA)
        except (NotUniqueError):
            return "",131
        #handles the OperationError in case the user tries to create an index that doesn't comply with
        #the db validation rules
        except(OperationError):
            return "",121
        return "",200

"""
the patientApi uses an id input as an additional resource, so it differs from the casesApi, thus
requiring a different class
"""
class PatientApi(Resource):
    """
    This function updates a specific index from the db, based on the id given
    """
    def put(self,id):
        body = request.get_json()
        try:
            Patient.objects.get(id=id).update(**body)
        #handles the NotUniqueError in case the user tries to create an index
        #with an already existing unique field(AMKA)
        except (NotUniqueError):
            return "",131
        except(OperationError):
            return "",121
        return "",200
        
    """
    This function deletes a specific index from the db, based on the id given
    """
    def delete(self, id):
        patient = Patient.objects.get(id=id).delete()
        return '', 200

    """
    This function gets a specific index from the db, based on the id given
    """ 
    def get(self, id):
        patient = Patient.objects.get(id=id).to_json()
        #creates a dictionary over the Mongo Object so that it can be parsed
        #as a json file from the rest of the program
        dicts = json.loads(patient)
        return Response(patient, mimetype="application/json", status=200)