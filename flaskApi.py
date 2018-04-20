#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:44:10 2018

@author: to125348
"""
import os
from flask import Flask, request, jsonify,send_file

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def download(destination):
    return send_file(destination,
                     attachment_filename='file.csv',
                     as_attachment=True)

@app.after_request 
def after_request(response):
    
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


@app.route("/uploadhc", methods=['POST'])
def uploadhc():
    target = os.path.join(APP_ROOT, "UPLOAD_FILE/")


    if not os.path.isdir(target):
        os.mkdir(target)
    print request.files
    if 'file' not in request.files:
        error = "Missing data source!"
        return jsonify({'error': error})


    file = request.files['file']
    fileName = "DCData.csv"
    destination = '/'.join([target, fileName])
    file.save(destination)
    
    d=download(destination)
    
    if d :
        print 'ok'        
    
    
    success = "Success!"
    return jsonify({'file': success})



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4555, debug=True)
