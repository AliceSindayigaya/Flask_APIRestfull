#==============================================================================
# SPPMS WEB SERVICE - WEB SERVER START
#==============================================================================
#import system library
import os

#import flask library
from flask import Flask, request,jsonify
from flask import render_template

#Flask application start 
app = Flask(__name__)

#Convert path windows in linux real path 
def getPath(path):
    server = '\\10.122.80.194'
    realPath = path.replace(server,'/projects')
    new_path = realPath.replace('\\','/')
    file_path =os.path.dirname(new_path)
    return file_path
    
# Define the header for client response
@app.after_request 
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


#import libpfm
import pypfm as pfm

#Get value parameter and  launch sppms by libpfm
@app.route ("/sppms/api/v1.0", methods= ['GET','POST'])
def getconfig():

    if request.method ==  "POST":

        #Get the form value
        form = request.form
        altitude = float(form['altitude'])
        disa = float(form['disa'])
        mach = float(form['mach'])
        file_path = getPath(str(form['file_path']))
        regime = str(form['regime'])
        install = str(form['install'])
        humidite = float(form['humidite'])
        libpath = str(form['pathLibrary'])
        disa_piste = float(form['disa_piste'])
        alt_piste = float(form['alt_piste'])
        temps_flex= float(form['temps_flex'])
        typar = str(form['typar'])
        vapar = float(form['vapar'])
#        wbiphp = float(form['wbiphp'])

        print altitude, disa, mach, install, regime, file_path,humidite,libpath,alt_piste,disa_piste,temps_flex ,typar,vapar

#        ,wbiphp   

        
        #Configure logging
        pfm.Logging.setLevel(pfm.Logging.Debug)
       
        #Create a test data object
        td = pfm.TestData()
        td.setNumberOfSamples(1)
        td.addParameter("ALT", "ft", [altitude])
        td.addParameter("XM","", [mach])
        td.addParameter("DTAMB","K", [disa])
        td.addParameter("HUM","", [humidite])
        td.addParameter("ALTR","ft", [alt_piste])
        td.addParameter("DTAMBR","", [disa_piste])
        td.addParameter("FLXT", "", [temps_flex])
        td.addParameter("VAPAR","", [vapar])
#        td.addParameter("WBIPHP", "",[wbiphp])
        td.setContext("SPPMS_IN")
        
       
        #Create SPPMS model
        model = pfm.Sppms()
        model.setData(td)
        model.setTypar("REG")
        model.setDefaultRatingCode(regime)
        model.setDefaultInstallCode(install)
        model.setAnemometry([pfm.AnemoType.AC])
        model.setOutputDirectory("OUT")
        model.setSamples(pfm.Range("all"))
        model.setAircraft("A350")
        model.setManufacturer("RR")
        model.setEngine("TRENTXWB97")
        model.setBlPath(file_path)
        model.run()
     
        #Read output test data
        reader = pfm.createTestDataReader("orma")
        reader.setInputFile("OUT/ENGINE_1_AC/BIN_HOMOLOG_BDM")
        out = reader.read()
        print out, out.countSamples(), out.countParameters()
      
        #Format json to be sent back
        dct = {}
        for param in out.listParameters():
            dct[param] = out.getParameterValueAtSample(param, 0)
        return jsonify(dct)
    return "Success"
    
#Homologate library url
@app.route("/homologate", methods= ['GET','POST'])
def homologate():
    return render_template('homologate.html')

#Other library url
@app.route("/others", methods= ['GET','POST'])
def others():
    return render_template('others_lib.html')

#Result and output url 
@app.route("/result", methods= ['GET','POST'])
def result():
    if request.method == "POST":
        result = request.get_json()
        print result
        return jsonify(result)
    
    return render_template ('result.html')
 

#main function
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8125, debug=True)

