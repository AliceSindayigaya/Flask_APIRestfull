# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 10:04:49 2018

@author: to125348
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:28:30 2018

@author: to125348
"""

import csv
import json

from cStringIO import StringIO
from flask import Flask, render_template, request, make_response

app =Flask(__name__)
app.debug = True

def csv_json(data):
    reader = csv.DictReader
    reader = csv.DictReader(data)
    out =json.dumps([ row for row in reader ])
    print "JSON parsed!"
    return out
    print "JSON saved"
    

@app.route('/csv2json', methods=['POST'])
def convert():
    f = request.files['data_file']
    if not f:
        return "No file"
    file_contents =StringIO(f.stream.read())
    result = csv_json(file_contents)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=Converted.json"
    return response
    
@app.route('/')
def main () :
    render_template
    return render_template('convert.html')

if __name__=='__main__':
    app.run()