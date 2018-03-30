#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:53:50 2018

@author: to125348
"""

import os
import csv
import json

from flask import Flask, jsonify, abort
from flask import make_response, request
from flask import url_for
from werkzeug import secure_filename
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
UPLOAD_FILE = '/UPLOAD_FILE'


app= Flask(__name__)

app.config['UPLOAD_FOLDER']= UPLOAD_FILE
ALLOWED_EXTENSIONS = {'csv'}
          

    
   
    
tasks=[
    {
        'id':1,
        'title':u'Buy groceries',
        'description':u'HP,Asus,Toshiba,Acer',
        'done':False
    },
    {
        'id':2,
        'title':u'Learn Python',
        'description':u'Need to find a good Python tutoriel on the web',
        'done':False
            }
            
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


    
# Authentification

@auth.get_password
def get_password(username):
    if username == 'epg':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}),403)


#Function to generate a public URI

def make_public_task(task):
    new_task= {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks/upload')
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len (task) == 0:
        abort(404)
    return jsonify({'task': [make_public_task(task) for task[0] in tasks]})

@app.errorhandler(404)
def not_founder(error):
    return make_response(jsonify({'error': 'Not found'}),404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task={
            'id': tasks[-1]['id'] +1,
            'title':request.json['title'],
            'description':request.json.get('description', ""),
            'done':False
   }

    tasks.append(task)
    return jsonify({'tasks': [make_public_task(task) for task in tasks]}),201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task= [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(404)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description']= request.json.get('description',task[0]['title'])
    task[0]['done']= request.json.get('done', task[0]['done'])
    return jsonify({'task':make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>)', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task=[task for task in tasks if task ['id'] == task_id]
    if len(task) == 0:
        abort(404)
    task.remove(task[0])
    return jsonify({'result': True})


if __name__=='__main__':
    app.run(host = '0.0.0.0', debug =True)
