# CODE FOR API
import json
import pymongo
from pymongo import MongoClient
from operator import itemgetter
import operator
import time
import basehash

from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from bson.json_util import dumps
from bson import ObjectId
from datetime import date
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'MovieDB'
app.config['MONGO_URI'] = "mongodb://localhost:27017/MovieDB"

mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def connection():
    return dumps({'result': 'success'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    username = data['username']
    password = data['password']

    # check if username is unique 
    x = mongo.db.User.find()
    for data in x:
        username_db = data["username"]
        if (username == username_db):
            resp = jsonify({'confirmed': '0'})
            return resp
    
    #hash_fn = basehash.base36() 
    #hash_password = hash_fn.hash(password)

    if username and password and request.method == 'POST':

        id1 = mongo.db.User.insert({'username': username, 'password': password})

        resp = jsonify({'confirmed': '1'})
        resp.status_code = 200
        return resp
    
    else:
        return not_found()

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data['username']
    password = data['password']

    #hash_fn = basehash.base36()  
    #hash_password = hash_fn.hash(password) 

    x = mongo.db.User.find()
    found = False
    for item in x:
        if(item["username"]==username and item["password"]==password):
            found = True
            resp = jsonify({'confirmed': '1'})
            resp.status_code = 200
            return resp
    if(not found):
        resp = jsonify({'confirmed': '0'})
        resp.status_code = 200
        return resp

@app.route('/movie/<id>', methods=['GET'])
def get_specific_movie(id):
    movies = mongo.db.Movie.find_one({'_id':ObjectId(id)})
    resp = dumps(movies)
    return resp

@app.route('/movieslist', methods=['GET'])
def get_movies():
    movies = mongo.db.Movie.find()
    resp = dumps(movies)
    return resp

@app.route('/addrating', methods=['POST'])
def add_rating():
    data = request.json
    
    username = data['username']
    movieid = data['movieid']
    rating = data['rating']

    if username and movieid and rating and request.method == 'POST':
        mongo.db.UserMovie.insert({'username': username, 'movieid': movieid, 'rating': rating})

        #updating rating not working
       # x = mongo.db.Movie.find()
      #  for item in x:
         #   if(item["movieid"]==movieid):
         #       m_id = item["_id"]
         #       nbrUsersRating = item["NbrUsersRating"] + 1
         #       m_rating = (item["Rating"]+rating)/nbrUsersRating

        
         #       mongo.db.Movie.update({'_id': ObjectId(m_id['$oid']) if '$oid' in m_id else ObjectId(m_id)},{'$set':{'Name':item["Name"],'movieid':item['movieid'],
          #      'Genre':item['Genre'],'YearReleased':item['YearReleased'],'Description':item['Description'],'Rating': m_rating, 'NbrUsersRating': nbrUsersRating,
          #      'Classification': item['Classification']}})

        resp = jsonify("Successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found

@app.route('/updaterating', methods=['POST'])
def update_rating():
    data = request.json
    s_id = data['_id']
    username = data['username']
    movieid = data['movieid']
    rating = data['rating']

    if username and movieid and rating and request.method == 'POST':
        mongo.db.UserMovie.update_one({'_id': ObjectId(s_id['$oid']) if '$oid' in s_id else ObjectId(s_id)},{'$set':{'username': username, 
        'movieid': movieid, 'rating': rating}})

        resp = jsonify("Rating updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify("Cannot have empty strings")
    resp = jsonify(message)
    resp.status_code(404)
    return resp

if __name__ == '__main__':
    #app.run(debug=True)
	app.run(debug = True, host='0.0.0.0')