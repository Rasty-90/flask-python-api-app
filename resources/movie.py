from flask import Response, request
from database.models import Patient
from flask_restful import Resource
import json

class PatientsApi(Resource):
    def get(self):
        patients = Patient.objects().to_json()
        #creates a dictionary over the Mongo Object
        dicts = json.loads(patients)
        return dicts,200

    def post(self):
        body = request.get_json()
        patient= Patient(**body).save()
        #id=patient.id 
        return "",200


class PatientApi(Resource):
    def put(self,id):
        body = request.get_json()
        Patient.objects.get(id=id).update(**body)
        return '',200

    def delete(self, id):
        patient = Patient.objects.get(id=id).delete()
        return '', 200

    def get(self, id):
        patients = Patient.objects.get(id=id).to_json()
        dicts = json.loads(patients)
        return Response(patients, mimetype="application/json", status=200)