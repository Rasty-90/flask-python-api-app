from flask import Response, request
from database.models import Case
from flask_restful import Resource,request
from mongoengine.errors import NotUniqueError
import json

"""
This file contains the case API resource structure with basic CRUD functionality. Each resource
is represented as a different class
"""

class CasesApi(Resource):
    """
    This function gets all the Case objects from the database
    """
    def get(self):
        cases = Case.objects.to_json()
        #creates a dictionary over the Mongo Object so that it can be parsed
        #as a json file from the rest of the program
        dicts = json.loads(cases)
        return dicts,200

    """
    This function creates a new case object to the database
    """
    def post(self):
        body = request.get_json()
        try:
            #** spreads the object
            case= Case(**body).save()
        #handles the NotUniqueError in case the user tries to create an index
        #with an already existing unique field(AMKA)
        except (NotUniqueError):
            return "",403
        return '',200

"""
the caseApi uses an id (or status) input as an additional resource refering to a single db index, so it differs from the casesApi, thus
requiring a different class
"""
class CaseApi(Resource):
    """
    This function updates a specific index from the db, based on the id given
    """
    def put(self,id):
        body = request.get_json()
        try:
            Case.objects.get(id=id).update(**body)
        #handles the NotUniqueError in case the user tries to create an index
        #with an already existing unique field(AMKA)
        except (NotUniqueError):
            return "",403
        return '',200

    """
    This function deletes a specific index from the db, based on the id given
    """
    def delete(self, id):
        case = Case.objects.get(id=id).delete()
        return '', 200

    """
    This function gets a specific index from the db, based on the id given
    """    
    def get(self, id):
        case = Case.objects.get(id=id).to_json()
        #creates a dictionary over the Mongo Object so that it can be parsed
        #as a json file from the rest of the program
        dicts = json.loads(case)
        return Response(case, mimetype="application/json", status=200)

#TODO: STATUS RESOURCE