from flask import Flask, request,jsonify

app = Flask(__name__)

# Make the header for client response
@app.after_request 
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

#import libpfm
import pypfm as pfm


#Get value parameter and  launch sppms
@app.route ("/sppms/api/v1.0", methods= ['GET','POST'])
def getconfig():
    
    if request.method ==  "POST":
        
        #Get the form value
        form = request.form
        altitude = float(form['altitude'])
        disa = float(form['disa'])
        mach = float(form['mach'])
        file_path = str(form['file_path'])
        file_path = "/projects/moteur_ap/A350/RR/BASE/txwb97_1000_ifpa"
        regime = str(form['regime'])
        install = str(form['install'])

        print altitude, disa, mach, install, regime, file_path
        #file_path = getfile(request.data ('file_ part'))
        #altitude = request.json('altitude')
        #mach = request.json('mach')
        #delta = request.json('delta')
        #humidite = request.json('humidite')
        #alt_piste = request.json('alt-piste')
        #temps_flex = request.json ('temps-flex')
        #typar = request.json('typar')
        #vapar = request.json('vapa')
        #install=request.json('install')
        
        #Configure logging
        pfm.Logging.setLevel(pfm.Logging.Debug)
        
        #Create a test data object
        td = pfm.TestData()
        td.setNumberOfSamples(1)
        td.addParameter("ALT", "ft", [altitude])
        td.addParameter("XM", "", [mach])
        td.addParameter("DTAMB", "K", [disa])
        td.setContext("SPPMS_IN")
        
        #Create SPPMS model
        model = pfm.Sppms()
        model.setInputTestData(td)
        model.setTypar("REG")
        model.setDefaultRatingCode(regime)
        model.setDefaultInstallCode(install)
        model.setAnemometry([pfm.AnemoType.AC])
        model.setOutputDirectory("OUT")
        model.setSamples(pfm.Range("all"))
        model.setAircraft("A350")
        model.setManufacturer("RR")
        model.setEngine("TRENTXWB")
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
    return "success"
  
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8125, debug=True)


