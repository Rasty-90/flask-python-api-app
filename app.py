from flask import Flask,render_template,request,flash,session
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
import requests
import json

app = Flask(__name__)
api=Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/hospital-db'
}

initialize_db(app)
initialize_routes(api)

#Routes για τις σελίδες των περιστατικών
@app.route('/index')
@app.route('/indexcases')
def indexcases():
    casesres = requests.get('http://127.0.0.1:5000/cases')
    cases = json.loads(casesres.content)
    for case in cases: 
        patientCaseRes = requests.get('http://127.0.0.1:5000/patient/'+case['patientID'])
        patientCase = json.loads(patientCaseRes.content)
        case['patientSurname']=patientCase['surname']
        case['patientName']=patientCase['name']
    return render_template("cases.html", title='Περιστατικά', cases=cases)

#TODO: EDIT CASE PAGE, DELETE CASE

#Νέα περιστατικά
@app.route('/newCase', methods=['GET','POST'])
def newCase():
    patientsres = requests.get('http://127.0.0.1:5000/patients')
    patients = json.loads(patientsres.content)
    if request.method == 'POST':
    #takes from form
        patientName = request.form['patient']
        print (patientName)
        return render_template("success.html", title='Επιτυχής εγγραφή')
    else:    
        return render_template("newCase.html", title='Νέο περιστατικό',patients=patients)

#Routes για τις σελίδες των ασθενών
@app.route('/indexpatients')
def indexpatients():
    patientsres = requests.get('http://127.0.0.1:5000/patients')
    patients = json.loads(patientsres.content)
    return render_template("patients.html", title='Aσθενείς', patients=patients)

@app.route('/profile',methods=['GET','POST'])
def patprof():
    id=request.args.get('id')
    reqres = requests.get('http://127.0.0.1:5000/patient/'+id)
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
            r = requests.put('http://127.0.0.1:5000/patient/'+id, json = newPatient)
            return render_template("success.html", title='Επιτυχής εγγραφή')
        elif request.form['submit'] == 'delete':
             r = requests.delete('http://127.0.0.1:5000/patient/'+id)
             #TODO: MESSAGE FOR DELETING
             return "H διαγραφή έγινε με επιτυχία"
        else:
            return "Εμφανίστηκε σφάλμα στην εφαρμογή"
    else:  
        return render_template("profile.html", title='Προφίλ ασθενούς', patient=dicts)


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
        r = requests.post('http://127.0.0.1:5000/patients', json = newPatient)
        return render_template("success.html", title='Επιτυχής εγγραφή')
    else:
        return render_template("newPatient.html", title='Νέος Ασθενής')


app.run(debug=True)

# Η βάση θα αποτελείται από ένα table με τα προσωπικά στοιχεία των ασθενών (όνομα, επώνυμο, αμκα, κιν. επικοινωνίας)
# και ένα table που θα αφορά τα ιατρικά τους στοιχεία (Ημ, εισαγωγής, υπεύθυνος γιατρός, αρ. δωματίου, αρ. κρεβατιού).
# H εφαρμογή θα είναι ένα web app (non responsive) που θα υποστηρίζει απλές CRUD ενέργειες για όλα τα πεδία της βάσης.
# Το back end θα γραφτεί σε flask, και για βάση θα χρησιμοποιηθεί η mongoDB μέσω της βιβλιοθήκης pymongo.Το deliverable θα ειναι 
# (εδω γραφει σουπακι για docker)Το τελικό θα περιέχει τα αναγκαία comments αλλά όχι documentation.Timetable: 5/11
# ενα τελικό draft proof of concept με τις βασικές λειτουργίες20/11 επίδειξη demo για τυχόν μικροαλλαγές (μεγάλες αλλαγές δε θα μπορούν να γίνουν)
# 30/11 παράδοση τελικού, θα χρειαστεί να γίνει μια παρουσίαση και πλήρης επεξήγηση του κώδικα ώστε να ξέρει ο συνάδελφος τι να γράψει στην τεχνική ανάλυση.