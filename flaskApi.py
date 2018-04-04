# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 20:16:51 2018

@author: alice
"""

import csv 
import json


from flask import Flask,jsonify,abort
from flask import make_response,request,url_for
from flask_httpauth import HTTPBasicAuth

from cStringIO import StringIO

auth= HTTPBasicAuth()

app = Flask(__name__)
flights = [
    {
        'id':1,
        'title':u'Toulouse-Paris',
        'description':u'AirFrance-Blagnac-Roissy',
        'done':False
    },
    {
        'id':2,
        'title':u'Toulouse-Bordeau',
        'description':u'EasyJet Blagnac-BOrdeau',
        'done':False
            }
            
]

csvfilename = 'csv_file.csv'
jsonfilename = csvfilename.split('.')[0] + '.json'
csvfile = open(csvfilename, 'r')
jsonfile = open(jsonfilename, 'w')
reader = csv.DictReader(csvfile)

fieldnames = ("Name","Address","Gender","Designation","Age")

output = []

for each in reader:
  row = {}
  for field in fieldnames:
    row[field] = each[field]
output.append(row)

json.dump(output, jsonfile, indent=4, sort_keys=True)

#Return the full URI
def make_public_flight(flight):
    new_flight = {}
    for field in flight:
        if field == 'id':
            new_flight['uri'] = url_for('get_flight', flight_id=flight['id'])
        else:
            new_flight[field] = flight[field]
    return new_flight
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

@app.route('/flight/api/v1.0/flights', methods=['GET'])
@auth.login_required
def get_flights():
    return jsonify({'flights' :[make_public_flight(flight) for flight in flights]})

@app.route('/flight/api/v1.0/flights/<int:flight_id>', methods=['GET'])
@auth.login_required
def get_flight(flight_id):
    flight = [flight for flight in flights if flight['id'] ==  flight_id]
    if len(flight) ==0:
        abort(404)
    return jsonify({'flight':flight[0]})

@app.route('/flight/api/v1.0/flights', methods=['POST'])
@auth.login_required
def create_flight():
    if not request.json or not 'title' in request.json:
        abort(404)
    flight = {
            'id':flights[-1]['id'] +1,
            'title':request.json['title'],
            'description':request.json.get('description', ""),
            'done':False
    }
    flights.append(flight)
    return jsonify({'flight': flight}),201

@app.route('/flight/api/v1.0/flights/<int:flight_id>', methods=['PUT'])
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

@app.route('/flight/api/v1.0/flights/<int:flight_id>', methods=['DELETE'])
@auth.login_required
def delete_flight(flight_id):
    flight =[flight for flight in flights if flight['id'] == flight_id]
    if len(flight) ==0:
        abort(404)
    flight.remove(flight[0])
    return jsonify({'result': True})






if __name__ =='__main__':
app.run(host = '0.0.0.0', port = 5001, debug =True)
