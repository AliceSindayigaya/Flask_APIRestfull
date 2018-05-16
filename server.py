#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 08:53:45 2018

@author: to125348
"""
import os
import StringIO

from flask import Flask, request, jsonify,send_from_directory,send_file


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/projects/moteur_user/to125348/SPPMS/UPLOAD_FILE' 
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
target = os.path.join(APP_ROOT, "UPLOAD_FILE/")

    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.after_request 
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
@app.route("/uploadhc", methods=['POST'])
def uploadhc():
    
    if 'file' not in request.files:
        error = "Missing data source!"
        return jsonify({'error': error})
    data = request.files['file'] 
    fname="data.json"
    destination = '/'.join([target, fname])
    data.save(destination)
    with open (os.path.join(target,'data.json')) as f:
        file_data=f.read()
    print file_data
    return file_data
    
    #            success="Success"
    #            return jsonify({'success': success})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002, debug=True)

