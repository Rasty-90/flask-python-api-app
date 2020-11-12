from flask import Response, request
from database.models import Patient
from flask_restful import Resource
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
        patients = Patient.objects().to_json()
        #creates a dictionary over the Mongo Object so that it can be parsed
        #as a json file from the rest of the program
        dicts = json.loads(patients)
        return dicts,200

    """
    This function creates a new patient object to the database
    """
    def post(self):
        body = request.get_json()
        patient= Patient(**body).save()
        #id=patient.id 
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
        Patient.objects.get(id=id).update(**body)
        return 'Success',200

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