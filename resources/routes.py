
from .movie import PatientsApi, PatientApi


def initialize_routes(api):
 api.add_resource(PatientsApi, '/patients')
 api.add_resource(PatientApi, '/patients/<id>')


