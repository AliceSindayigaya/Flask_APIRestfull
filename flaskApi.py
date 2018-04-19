
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
cors= CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = '/projects/moteur_user/to125348/API/UPLOAD_FILE' 
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
#Convert the csv_file 
csvfilename = 'csv_file.csv'
jsonfilename = csvfilename.split('.')[0] + '.json'

                                
                                
@app.after_request 
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response
                                
#Check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ('csv')

##Read CSV File
def read_CSV(csvfilename , json_file):
    csv_rows = []
    with open(csvfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
            
        convert_write_json(csv_rows, jsonfilename)
#
##Convert csv data into json
def convert_write_json(data, jsonfilename):
    with open(jsonfilename, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
       
read_CSV(csvfilename ,jsonfilename)
#
#
##Read the json
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
        print "form: ", request.form
        print request.values
        print request.files["echo"]
        data = request.files["echo"]
        file_data= data.read()
        
        if file_data:
            fname=secure_filename(data.filename)
            data.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
        else:
            abort(404)
        print file_data   
        return file_data
     return "File Upload"
    
            
           
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
    app.run(host = '0.0.0.0',port=5000, debug =True)
