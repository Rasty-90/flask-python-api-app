from flask import Flask,render_template,request
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

@app.route('/')
@app.route('/index')
def index():
    reqres = requests.get('http://127.0.0.1:5000/patients')
    dicts = json.loads(reqres.content)
    return render_template("home.html", title='Home', patients=dicts)

@app.route('/profile')
def patprof():
    id=request.args.get('id')
    reqres = requests.get('http://127.0.0.1:5000/patients/'+id)
    dicts = json.loads(reqres.content)
    return render_template("profile.html", title='Home', patients=dicts)


app.run()

# Η βάση θα αποτελείται από ένα table με τα προσωπικά στοιχεία των ασθενών (όνομα, επώνυμο, αμκα, κιν. επικοινωνίας)
# και ένα table που θα αφορά τα ιατρικά τους στοιχεία (Ημ, εισαγωγής, υπεύθυνος γιατρός, αρ. δωματίου, αρ. κρεβατιού).
# H εφαρμογή θα είναι ένα web app (non responsive) που θα υποστηρίζει απλές CRUD ενέργειες για όλα τα πεδία της βάσης.
# Το back end θα γραφτεί σε flask, και για βάση θα χρησιμοποιηθεί η mongoDB μέσω της βιβλιοθήκης pymongo.Το deliverable θα ειναι 
# (εδω γραφει σουπακι για docker)Το τελικό θα περιέχει τα αναγκαία comments αλλά όχι documentation.Timetable: 5/11
# ενα τελικό draft proof of concept με τις βασικές λειτουργίες20/11 επίδειξη demo για τυχόν μικροαλλαγές (μεγάλες αλλαγές δε θα μπορούν να γίνουν)
# 30/11 παράδοση τελικού, θα χρειαστεί να γίνει μια παρουσίαση και πλήρης επεξήγηση του κώδικα ώστε να ξέρει ο συνάδελφος τι να γράψει στην τεχνική ανάλυση.