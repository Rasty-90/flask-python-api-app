from flask import Response, request
from database.models import Case
from flask_restful import Resource
import json

class CasesApi(Resource):
    def get(self):
        cases = Case.objects().to_json()
        #creates a dictionary over the Mongo Object
        dicts = json.loads(cases)
        return dicts,200

    def post(self):
        body = request.get_json()
        case= Case(**body).save()
        #id=patient.id 
        return "",200


class CaseApi(Resource):
    def put(self,id):
        body = request.get_json()
        Case.objects.get(id=id).update(**body)
        return '',200

    def delete(self, id):
        case = Case.objects.get(id=id).delete()
        return '', 200

    def get(self, id):
        case = Case.objects.get(id=id).to_json()
        dicts = json.loads(case)
        return Response(case, mimetype="application/json", status=200)
