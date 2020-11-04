from flask import Flask,render_template,request
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
import requests
import json

app = Flask(__name__)
api=Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)
initialize_routes(api)

@app.route('/')
@app.route('/index')
def index():
    reqres = requests.get('http://127.0.0.1:5000/movies')
    dicts = json.loads(reqres.content)
    #json_data = reqres.json()
    print(dicts)
    return render_template("home.html", title='Home', movies=dicts)


app.run()
