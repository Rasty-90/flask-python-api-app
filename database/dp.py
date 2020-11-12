from flask_mongoengine import MongoEngine
"""
This file initializes the mongoengine in order to allow connection
to the mongo server
"""
db = MongoEngine()

def initialize_db(app):
    db.init_app(app)