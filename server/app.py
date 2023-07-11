#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):

    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(jsonify(campers), 200)
    
    def post(self):

        data = request.get_json()

        new_camper = Camper(
            name=data['name'],
            age=data['age']
        )

        db.session.add(new_camper)
        db.session.commit()

        return make_response(new_camper.to_dict(), 201)

api.add_resource(Campers, '/campers')

class CampersByID(Resource):
    
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(camper), 200)
    
    # def patch(self, id):
    #     camper = Camper.query.filter_by(id=id).first().to_dict()
    #     for attr in request.form:
    #         setattr(camper, attr, request.form[attr])
        
    #     db.session.add(camper)
    #     db.session.commit()

    #     response_dict = (jsonify(camper.id))

    #     return make_response(response_dict, 200)

api.add_resource(CampersByID, '/campers/<int:id>')

class Activities(Resource):

    def get(self):
        activity = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(jsonify(activity), 200)

api.add_resource(Activities, '/activities')

class ActivityByID(Resource):

    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()

        db.session.delete(activity)
        db.session.commit()

        response_dict = {"mesage": "activity was successfully deleted."}

        return make_response(response_dict, 200)

api.add_resource(ActivityByID, '/activities/<int:id>')

class Signups(Resource):

    def post(self):

        data = request.get_json()

        new_signup = Signup(
            time=data['time'],
            camper_id=data['camper_id'],
            activity_id=data['activity_id']
        )

        db.session.add(new_signup)
        db.session.commit()

        return make_response(new_signup.to_dict(), 201)

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
