
from .patient import PatientsApi, PatientApi
from .case import CasesApi, CaseApi

"""
This file declares the endpoints for each Api structure defined in the 
case.py and routes.py files. 
"""

def initialize_routes(api):
 api.add_resource(PatientsApi, '/patients')
 api.add_resource(PatientApi, '/patient/<id>')
 api.add_resource(CasesApi, '/cases')
 api.add_resource(CaseApi, '/case/<id>')

 #TODO: STATUS RESOURCE ENDPOINT

