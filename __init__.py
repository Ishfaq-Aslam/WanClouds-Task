from flask import Flask
import datetime
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from functools import wraps
from celery import Celery
import pymysql
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request
import json
import urllib
import requests

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/lostnfound'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ishfaq:ishfaq123@localhost/wancloud_db'
db = SQLAlchemy(app)


class car_data(db.Model):
    objectid = db.Column(db.String(100), primary_key=True)
    year = db.Column(db.Integer)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    category = db.Column(db.String(100))
    createdat = db.Column(db.String(100))
    updatedat = db.Column(db.String(100))

    __tablename__ = "cars"

    def __init__(self, objectid, year, make, model, category, createdat, updatedat):
        self.objectid = objectid
        self.year = year
        self.make = make
        self.model = model
        self.category = category
        self.createdat = createdat
        self.updatedat = updatedat

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class USER(db.Model):
    user = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    password = db.Column(db.String(100))

    __tablename__ = "users"

    def __init__(self, user, email, password, fname, lname):
        self.lname = lname
        self.fname = fname
        self.password = password
        self.email = email
        self.user = user

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/signup', methods=['POST'])
def signup():  # put application's code here
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
        lname = data['lname']
        fname = data['fname']
        adddata = USER(username, email, password, lname, fname)
        adddata.create()
    return 'Id created'


@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']

        userdata = db.session.query(USER).filter_by(email=email, password=password).first()
        if not userdata:
            return 'Invalid email or password'
    return f'welcome {userdata.user}'


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    objid = data['objectid']
    db_data = db.session.query(car_data).filter_by(objectid=objid).first()

    if not db_data:
        return "objectid not found"

    return f'found {db_data}'


@app.route('/fetchdata', methods=['GET'])
def getdata():
    where = urllib.parse.quote_plus("""
    {
        "Year": {
            "$lt": 2032
        }
    }
    """)
    url = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=10'
    headers = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',  # This is the fake app's application id
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'  # This is the fake app's readonly master key
    }
    data = json.loads(
        requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need
    # print(json.dumps(data, indent=2))
    list_models = []
    car = dict
    for model in data['results']:
        if model.get('Make') not in list_models:
            list_models.append(model.get('Make'))
            print(model.get('Make'))
            url = 'https://parseapi.back4app.com/classes/Car_Model_List_{}?limit=10&order=Year&where=%s'. \
                format(model.get("Make"))
            print(url)
            url = url % where
            records = json.loads(
                requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need
            for record in records['results']:
                obj = db.session.query(car_data).filter_by(objectid=record['objectId']).first()
                if not obj:
                    adddata = car_data(record['objectId'], record['Year'], record['Make'], record['Model'],
                                       record['Category'], record['createdAt'], record['updatedAt'])
                    adddata.create()

    return json.dumps(records, indent=2)


if __name__ == '__main__':
    app.run()
