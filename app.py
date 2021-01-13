from flask import Flask,render_template,request,flash,session,jsonify
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from config import host_db,host_flask,host_flask_app,host_flask_app_port
import requests
import json
from mongoengine.errors import NotUniqueError
from datetime import datetime


"""
The first part of this file handles the initialization of the database,
based on the config file, as well as the routes from the resources/routes file
"""
app = Flask(__name__)
#the secret key is used by flask to validate a session. It is used here for demonstration purposes as a simple string
app.secret_key = "covid-app"
api=Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': host_db
}

initialize_db(app)
initialize_routes(api)
#the session object holds the login info, and is set to none before user login to prevent unauthorized access

"""
The following section contains the actions for main routes of the applications
"""
#login page
@app.route('/login', methods=["GET","POST"])
def login_page():
    session['role']='none'
     #checks if the form is used
    if request.method == 'POST':
        #takes the data from form
        username=request.form['username']
        password=request.form['password']
        users = json.loads(open("user_data.json").read())
        for user in users:
            if user['username']==username:
                if user['password']==password:
                    session['role']=user['role']
                    return render_template("message.html", title='Επιτυχής εγγραφή', message="H σύνδεση ολοκληρώθηκε με επιτυχία", role=session['role'])
                    break
        #if no role has been assigned, no valid user has been found
        if session['role']=="none":
            return render_template("login.html", title='Σύνδεση Χρήστη', message="Τα στοιχεία εισόδου δεν είναι σωστά") 
    else:
        #result if the form isn't used (which is the default behavior upon opening the page)      
        return render_template("login.html", title='Σύνδεση Χρήστη')

@app.route('/logout',methods=["GET","POST"])
def logout_page():
    session['role']='none'
    return render_template("message.html", title='Επιτυχής αποσύνδεση', message="Έχετε αποσυνδεθεί με επιτυχία",role=session['role'])

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
        #changes the date to dd-mm-yyyy format
        case['date']=formatDate(case['date'])
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
        date = request.form['date']
        testType= request.form['testType']
        newCase = {
                "patientID": patientID,
                "roomn": roomn,
                "bedn": bedn,
                "doctor": doctor,
                "covidStatus":covidStatus,
                "date":date,
                "testType":testType
            }
        r = requests.post(host_flask +'/cases', json = newCase)
        #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
        #defined in the resources/case for each endpoint
        if r.status_code==121:
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
    id=request.args.get('id')
    reqres = requests.get(host_flask +'/case/'+id)
    caseres = json.loads(reqres.content)
    #gets the patient name, surname and amka for each case in order to be presented to the front end
    patientsres = requests.get(host_flask +'/patients')
    patients = json.loads(patientsres.content)
    #gets the patient who is associated with the specific case
    patientres=requests.get(host_flask +'/patient/'+caseres['patientID'])
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
            date=request.form['date']
            testType= request.form['testType']
            case = {
                "patientID":patientID,
                "roomn":roomn,
                "bedn":bedn,
                "doctor":doctor,
                "covidStatus":covidStatus,
                "date":date,
                "testType":testType
            }
            r = requests.put(host_flask +'/case/'+id, json = case)
            #check the status code of the response r, and presents the relative message, in case of error. Status codes are 
            #defined in the resources/case for each endpoint
            if r.status_code==121:
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
        #converts the date in a format usable by html date input(yyyy-mm-dd)
        caseres['date'] =datetime.fromisoformat(caseres['date']).date()
        return render_template("casedetails.html", title='Επεξεργασία Περιστατικού', case=caseres, patients=patients, patientcase=patient)


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
    #gets the cases associated with the patient to fill the case table
    caseres=requests.get(host_flask +'/cases?patientID='+id)
    casespat=json.loads(caseres.content)
    #changes the date to dd-mm-yyyy format for each case inside the results
    for case in casespat:
        case['date']=formatDate(case['date'])
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
                return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts, cases=casespat,
                 message="Παρουσιάστηκε σφάλμα στην εισαγωγή των στοιχείων, παρακαλώ ελέξτε ότι όλα τα πεδία είναι συμπληρωμένα και με σωστό τρόπο")
            elif r.status_code == 131:
                return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts, cases=casespat, message="Tο δηλωθέν ΑΜΚΑ υπάρχει ήδη στον κατάλογο ασθενών")
            else:
                 return render_template("message.html", title='Επιτυχής εγγραφή', message="H εγγραφή ολοκληρώθηκε με επιτυχία")
        else:
            return "Εμφανίστηκε σφάλμα στην εφαρμογή"
    elif request.method=='DELETE':
        #the DELETE request is handled by the js file, in order to function through a comfirmation check
        r = requests.delete(host_flask +'/patient/'+id)
        #Deleting the patient also deletes all the associated cases, in order to avoid the db throwing an error
        for case in casespat:
            r = requests.delete(host_flask +'/case/'+case['id']) 
        return render_template("message.html", title='Επιτυχής διαγραφή', message="H διαγραφή ολοκληρώθηκε με επιτυχία")  
    else:  
        return render_template("profiledetails.html", title='Προφίλ ασθενούς', patient=dicts, cases=casespat)

"""
Routing to facilitate the search action. The function handles differently the case of the action
coming from the patient list page or the case list page
"""

@app.route('/searchPatients',methods=['GET','POST'])
def searchPat():
    #takes the search key from the textbox
    patientargs=request.form['search']
    page=request.args.get('page')
    #empty list for the results
    patientres = []
    #first search is based on surname 
    patientssname = requests.get(host_flask +'/patients?surname='+patientargs)
    patients = json.loads(patientssname.content)
    #add the surname search results in the result list
    for patient in patients:
        patientres.append(patient)
    #second search based on amka
    patientsamka = requests.get(host_flask +'/patients?amka='+patientargs)
    patients = json.loads(patientsamka.content)
    #add the amka search results in the result list
    for patient in patients:
        patientres.append(patient)
    #checks if the action comes from the patients or the cases
    if page=="patients":
        #we simply return the patients results in the list 
        return render_template("patients.html", title='Aσθενείς', patients=patientres,searchPh=patientargs)
    else:
        #if the action comes for the case page, we need to query the base for cases that belong to the patient/patients
        #of the results and return them
        #empty list for the results
        casesres = []
        #find the cases related to each patient
        for patient in patientres:
            caseres = requests.get(host_flask +'/cases?patientID='+patient['id'])
            cases = json.loads(caseres.content)
            for case in cases:
                #add patient name and surname in order to be displayed on the page
                case['patientSurname']=patient['surname']
                case['patientName']=patient['name']
                #appends each case for each patient to the result list
                casesres.append(case)
                case['date']=formatDate(case['date'])
        return render_template("cases.html", title='Περιστατικά', cases=casesres,searchPh=patientargs)
         
"""
utility functions
"""
#returns a date formatted in dd-mm-yyyy format
def formatDate(date):
    dateres=datetime.fromisoformat(date)
    return (str(dateres.day)+"/"+str(dateres.month)+"/"+str(dateres.year))



app.run(debug=True, host = host_flask_app, port=host_flask_app_port)
