from flask import Flask,render_template,request,flash,session,jsonify
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from config import host_db,host_flask,host_flask_app,host_flask_app_port
import requests
import json
from mongoengine.errors import NotUniqueError

"""
The first part of this file handles the initialization of the database,
based on the config file, as well as the routes from the resources/routes file
"""
app = Flask(__name__)
api=Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': host_db
}

initialize_db(app)
initialize_routes(api)


"""
The following section contains the actions for main routes of the applications
"""


"""
Routes and actions for the pages relates to the cases
"""
#brings all the cases documents from the db
@app.route('/index')
@app.route('/indexcases')
def indexcases():
    #host_flask is retrieved from the config file
    casesres = requests.get(host_flask +'/cases')
    cases = json.loads(casesres.content)
    for case in cases:
        #gets the patient name and surname for each case in order to be presented to the front end
        patientCaseRes = requests.get(host_flask +'/patient/'+case['patientID'])
        patientCase = json.loads(patientCaseRes.content)
        case['patientSurname']=patientCase['surname']
        case['patientName']=patientCase['name']
    return render_template("cases.html", title='Περιστατικά', cases=cases)


#New case creation
@app.route('/newCase', methods=['GET','POST'])
def newCase():
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    #checks if the form is used
    if request.method == 'POST':
    #takes the data from form
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
                "covidStatus":covidStatus
            }
        r = requests.post(host_flask +'/cases', json = newCase)
        #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
        #defined in the resources/case for each endpoint
        if r.status_code == 131:
            return render_template("newCase.html", title='Νέο περιστατικό',patients=patients,message="Yπάρχει ήδη ενεργό περιστατικό σχετιζόμενο με τον ασθενή")
        elif r.status_code==121:
            return render_template("newCase.html", title='Νέο περιστατικό',patients=patients,
            message="Παρουσιάστηκε σφάλμα στην εισαγωγή των στοιχείων, παρακαλώ ελέξτε ότι όλα τα πεδία είναι συμπληρωμένα και με σωστό τρόπο")
        else:
            return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
    else:
        #result if the form isn't used (which is the default behavior upon opening the page)
        return render_template("newCase.html", title='Νέο περιστατικό',patients=patients)

#Edit/delete case
@app.route('/casedetails', methods=['GET','POST','DELETE'])
def caseDets():
    #gets the id of the case provided in the URL to fill the form with its data
    id = id=request.args.get('id')
    reqres = requests.get(host_flask +'/case/'+id)
    dicts = json.loads(reqres.content)
    #gets the patient name, surname and amka for each case in order to be presented to the front end
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    #gets the patient who is associated with the specific case
    patientres=requests.get(host_flask +'/patient/'+dicts['patientID'])
    patient =json.loads(patientres.content)
    #checks if the form is used
    if request.method == 'POST':
        #checks if edit or delete is pressed
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
            #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
            #defined in the resources/case for each endpoint
            if r.status_code == 131:
                return render_template("casedetails.html", title='Επεξεργασία Περιστατικού',case=dicts, patients=patients, patientcase=patient,
                message="Yπάρχει ήδη ενεργό περιστατικό σχετιζόμενο με τον ασθενή")
            elif r.status_code==121:
                return render_template("casedetails.html", title='Επεξεργασία Περιστατικού',case=dicts, patients=patients, patientcase=patient,
            message="Παρουσιάστηκε σφάλμα στην εισαγωγή των στοιχείων, παρακαλώ ελέξτε ότι όλα τα πεδία είναι συμπληρωμένα και με σωστό τρόπο")
            else:
                return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
        else:
            #general error 
            return "εμφανίστηκε σφάλμα"
    #the DELETE request is handled by the js file, in order to function through a comfirmation check
    elif request.method=='DELETE':
        r = requests.delete(host_flask +'/case/'+id)
        return render_template("message.html", title='Επιτυχής διαγραφή', message="H διαγραφή ολοκληρώθηκε με επιτυχία")
    else:
        #result if the form isn't used (which is the default behavior upon opening the page)        
        return render_template("casedetails.html", title='Επεξεργασία Περιστατικού', case=dicts, patients=patients, patientcase=patient)


"""
Routes and actions for the pages relates to the patiens
"""

#brings all the patient documents from the db
@app.route('/indexpatients')
def indexpatients():
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    return render_template("patients.html", title='Aσθενείς', patients=patients)

#New patient creation
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
        if r.status_code == 131:
             #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
            #defined in the resources/patient for each endpoint
            return render_template("newPatient.html", title='Νέος Ασθενής',message="Tο δηλωθέν ΑΜΚΑ υπάρχει ήδη στον κατάλογο ασθενών")
        elif r.status_code == 121:
            return render_template("newPatient.html", title='Νέος Ασθενής',
            message="Παρουσιάστηκε σφάλμα στην εισαγωγή των στοιχείων, παρακαλώ ελέξτε ότι όλα τα πεδία είναι συμπληρωμένα και με σωστό τρόπο")
        else:
            return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")           
    else:
        return render_template("newPatient.html", title='Νέος Ασθενής')

#Edit/delete patient
@app.route('/profile',methods=['GET','POST','DELETE'])
def patprof():
    #gets the id of the patient provided in the URL to fill the form with its data
    id=request.args.get('id')
    reqres = requests.get(host_flask +'/patient/'+id)
    dicts = json.loads(reqres.content)
    #checks if the form is used 
    if request.method == 'POST':
        #checks if edit or delete is pressed
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
            #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
            #defined in the resources/patient for each endpoint
            if  r.status_code == 121: 
                return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts,
                 message="Παρουσιάστηκε σφάλμα στην εισαγωγή των στοιχείων, παρακαλώ ελέξτε ότι όλα τα πεδία είναι συμπληρωμένα και με σωστό τρόπο")
            elif r.status_code == 131:
                return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts, message="Tο δηλωθέν ΑΜΚΑ υπάρχει ήδη στον κατάλογο ασθενών")
            else:
                 return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
        else:
            return "Εμφανίστηκε σφάλμα στην εφαρμογή"
    elif request.method=='DELETE':
        r = requests.delete(host_flask +'/patient/'+id)
        return render_template("message.html", title='Επιτυχής διαγραφή', message="H διαγραφή ολοκληρώθηκε με επιτυχία")  
    else:  
        return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts)


app.run(debug=True, host = host_flask_app, port=host_flask_app_port)
