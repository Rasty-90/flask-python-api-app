
from .patient import PatientsApi, PatientApi
from .case import CasesApi, CaseApi


def initialize_routes(api):
 api.add_resource(PatientsApi, '/patients')
 api.add_resource(PatientApi, '/patient/<id>')
 api.add_resource(CasesApi, '/cases')
 api.add_resource(CaseApi, '/case/<id>')
