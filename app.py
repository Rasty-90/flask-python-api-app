from flask import Flask,request,Response,render_template
from database.dp import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes


app = Flask(__name__)
api=Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-bag'
}

initialize_db(app)
initialize_routes(api)

@app.route('/home')
def check_home():
    return render_template('home.html', title='Home')

@app.route('/about')
def check_about():
    return render_template('about.html', title='about')


app.run()
