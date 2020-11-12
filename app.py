from flask import Flask,render_template,request,flash,session
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from config import host_db,host_flask,host_flask_app,host_flask_app_port
import requests
import json


app = Flask(__name__)
api=Api(app)

#TODO: CONGIG FILE
app.config['MONGODB_SETTINGS'] = {
    'host': host_db
}

initialize_db(app)
initialize_routes(api)

#Routes για τις σελίδες των περιστατικών
@app.route('/index')
@app.route('/indexcases')
def indexcases():
    casesres = requests.get(host_flask +'/cases')
    cases = json.loads(casesres.content)
    for case in cases: 
        patientCaseRes = requests.get(host_flask +'/patient/'+case['patientID'])
        patientCase = json.loads(patientCaseRes.content)
        case['patientSurname']=patientCase['surname']
        case['patientName']=patientCase['name']
    return render_template("cases.html", title='Περιστατικά', cases=cases)

#TODO: ASCENDING ORDER IN RETURNING PATIENTS

#Νέα περιστατικά
@app.route('/newCase', methods=['GET','POST'])
def newCase():
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    if request.method == 'POST':
    #takes from form
        patientID = request.form['patient']
        roomn = request.form['roomn']
        bedn = request.form['bedn']
        doctor = request.form['doctor']
        covidStatus = request.form['covidStatus']
        newCase = {
                "patientID": patientID,
                "roomn": roomn,
                "bedn": bedn,
                "doctor": doctor,
                "status": "true",
                "covidStatus":covidStatus
            }
        r = requests.post(host_flask +'/cases', json = newCase)
        return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
    else:    
        return render_template("newCase.html", title='Νέο περιστατικό',patients=patients)

#Επεξεργασία/διαγραφή περιστατικού
@app.route('/casedetails', methods=['GET','POST'])
def caseDets():
    #TODO: DATA OF PATIENT OF CASE
    id = id=request.args.get('id')
    reqres = requests.get(host_flask +'/case/'+id)
    dicts = json.loads(reqres.content)
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    #Εάν χρησιμοποιηθεί η φόρμα 
    if request.method == 'POST':
        if request.form['submit'] == 'edit':
            patientID = request.form['patient']
            roomn = request.form['roomn']
            bedn = request.form['bedn']
            doctor = request.form['doctor']
            covidStatus=request.form['covidStatus']
            case = {
                "patientID":patientID,
                "roomn":roomn,
                "bedn":bedn,
                "doctor":doctor,
                "covidStatus":covidStatus
            }
            r = requests.put(host_flask +'/case/'+id, json = case)
            return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
        elif request.form['submit'] == 'delete':
            r = requests.delete(host_flask +'/case/'+id)
            return render_template("message.html", title='Επιτυχής διαγραφή', message="H διαγραφή ολοκληρώθηκε με επιτυχία")   
        else:
            return "εμφανίστηκε σφάλμα"
    else:        
        return render_template("casedetails.html", title='Προφίλ ασθενούς', case=dicts, patients=patients)

#Routes για τις σελίδες των ασθενών
@app.route('/indexpatients')
def indexpatients():
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    return render_template("patients.html", title='Aσθενείς', patients=patients)

#Νέος ασθενής
@app.route('/newPatient',methods=['GET','POST'])
def newPat():
    if request.method == 'POST':
    #takes from form
        patientSurname = request.form['patientSurname']
        patientName = request.form['patientName']
        patientAmka = request.form['patientAmka']
        patientContactPhone = request.form['patientContactPhone']
        #creates a python object with data
        newPatient = {
            "surname": patientSurname,
            "name": patientName,
            "amka": patientAmka,
            "contactphone":patientContactPhone
        }
        r = requests.post(host_flask +'/patients', json = newPatient)
        #TODO CATCH NotUniqueError AMKA
        return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
    else:
        return render_template("newPatient.html", title='Νέος Ασθενής')

#Επεξεργασία/διαγραφή ασθενούς
@app.route('/profile',methods=['GET','POST'])
def patprof():
    id=request.args.get('id')
    reqres = requests.get(host_flask +'/patient/'+id)
    dicts = json.loads(reqres.content)
    #Εάν χρησιμοποιηθεί η φόρμα 
    if request.method == 'POST':
        #Ελέγχει ποιο κουμπί της φόρμας, το "Επεξεργασία" ή το "Διαγραφή" θα πατηθεί
        if request.form['submit'] == 'edit':
            #takes from form
            patientSurname = request.form['patientSurname']
            patientName = request.form['patientName']
            patientAmka = request.form['patientAmka']
            patientContactPhone = request.form['patientContactPhone']
            #creates a python object with data
            newPatient = {
                "surname": patientSurname,
                "name": patientName,
                "amka": patientAmka,
                "contactphone":patientContactPhone
            }
            r = requests.put(host_flask +'/patient/'+id, json = newPatient)
            return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
        elif request.form['submit'] == 'delete':
             r = requests.delete(host_flask +'/patient/'+id)
             #TODO: MESSAGE FOR DELETING
             return render_template("message.html", title='Επιτυχής διαγραφή', message="H διαγραφή ολοκληρώθηκε με επιτυχία")
        else:
            return "Εμφανίστηκε σφάλμα στην εφαρμογή"
    else:  
        return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts)




app.run(debug=True, host = host_flask_app, port=host_flask_app_port)
