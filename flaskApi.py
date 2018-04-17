#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 10:23:51 2018

@author: to125348
"""
import os
import csv 
import json


from flask import Flask,jsonify,abort,send_file
from flask import make_response,request,url_for
from flask_httpauth import HTTPBasicAuth
from flask_restful import  Api
from flask_cors import CORS

from werkzeug import secure_filename


auth= HTTPBasicAuth()

app = Flask(__name__)
api= Api(app)
CORS(app)


UPLOAD_FOLDER = '/UPLOAD_FILE' 
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
#Convert the csv_file 
csvfilename = 'csv_file.csv'
jsonfilename = csvfilename.split('.')[0] + '.json'

#Read CSV File
def read_CSV(csvfilename , json_file):
    csv_rows = []
    with open(csvfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
            
        convert_write_json(csv_rows, jsonfilename)

#Convert csv data into json
def convert_write_json(data, jsonfilename):
    with open(jsonfilename, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
       
read_CSV(csvfilename ,jsonfilename)


#Read the json
def read_json():
    with open (jsonfilename, 'r') as data:
        content = data.read()
        return json.loads(content.decode('utf-8','ignore'))

flights= read_json() 
      

#Return the full URI
def make_public_flight(flight):
    new_flight = {}
    for field in flight:
        if field == 'id':
            new_flight['uri'] = url_for('get_flight', flight_id=flight['id'])
        else:
            new_flight[field] = flight[field]
            
    return new_flight

#write the file 
def write_data(data): 
   csv_file = open('file.csv', 'w') 
   with csv_file:
          writer = csv.writer(csv_file)
          writer.writerows(data)
   print("writing complete")
   
   
#authentification
@auth.get_password
def get_password(username):
    if username == 'mt':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'unauthorized access'}),403)

#improve the error html response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}),404)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
            
            csv_file= request.files["echo"].read()
            if csv_file:
              data = write_data(csv_file)
              fname = secure_filename(csv_file.filename)
              
            else:
                abort(404)
           
@app.route('/get_file', methods=['GET','POST'])
def get_file():
    return send_file('/UPLOAD_FILE/csv_file.csv', attachement_filename='csv_file.csv', as_attachment=True)

@app.route('/flight/api/v1.0/flights', methods=['GET'])
#@auth.login_required
def get_flights():
    return jsonify({'flights' :[make_public_flight(flight) for flight in flights]})

@app.route('/flight/api/v1.0/flights/<flight_id>', methods=['GET'])
@auth.login_required
def get_flight(flight_id):
    flight = [flight for flight in flights if flight['id'] ==  flight_id]
    if len(flight) == 0:
        abort(404)
    return jsonify({'flight':flight[0]})

@app.route('/flight/api/v1.0/flights', methods=['POST'])
@auth.login_required
def create_flight():
    if not request.json or not 'title' in request.json:
        abort(404)
    flight = {
            'id':request.json.get('id', ""),
            'title':request.json['title'],
            'description':request.json.get('description', ""),
            'done':"False"
    }
    flights.append(flight)
    return jsonify({'flight': flight}),201

@app.route('/flight/api/v1.0/flights/<flight_id>', methods=['PUT'])
@auth.login_required
def update_flight(flight_id):
    flight = [flight for flight in flights if flight['id'] == flight_id]
    if len(flight) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool :
        abort(400)
    flight[0]['title'] = request.json.get('title', flight[0]['title'])
    flight[0]['description']=request.json.get('description', flight[0]['title'])
    flight[0]['done']= request.json.get('done',flight[0]['done'])
    return jsonify({'flight':flight[0]})

@app.route('/flight/api/v1.0/flights/<flight_id>', methods=['DELETE'])
@auth.login_required
def delete_flight(flight_id):
    flight =[flight for flight in flights if flight['id'] == flight_id]
    if len(flight) ==0:
        abort(404)
    flight.remove(flight[0])
    return jsonify({'result': True})




if __name__ =='__main__':
    app.run(host = '0.0.0.0',port=5001, debug =True)
