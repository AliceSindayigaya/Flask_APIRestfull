import os




from flask import Flask, request, jsonify,send_file

import StringIO

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


#def read_data(data):

#
#def download(data): 
#    #memory_file = StringIO.StringIO()
#    #with zipfile.ZipFile(memory_file, 'w') as zf:
#    #    zf.writestr("Data.csv", data)
#        
#    #memory_file.seek(0)
#    strIO = StringIO.StringIO()
#    strIO.write('Hello from Dan Jacob and Stephane Wirtel !')
#    strIO.seek(0)
#    return send_file(strIO,
#                     attachment_filename='file.zip',
#                     as_attachment=True)
@app.after_request 
def after_request(response):
    
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


@app.route("/uploadhc", methods=['GET','POST'])
def uploadhc():
    if request.method=='POST':
        if 'file' not in request.files:
            error = "Missing data source!"
            return jsonify({'error': error})
        data = request.files['file']  
        file_data= data.read()
        print file_data
        return file_data
    
    if request.method=='GET':
        strIO = StringIO.StringIO()
        strIO.seek(0);
        return send_file(strIO,
                     attachment_filename='file.zip',
                     as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)

