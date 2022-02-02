from flask import Flask,render_template, request
from zeep import Client

wsdl = 'https://www.w3schools.com/xml/tempconvert.asmx?wsdl'
client = Client(wsdl=wsdl)

app = Flask(__name__)

@app.route('/ctof', methods = ['GET','POST'] )
def convert_celcius_farenheigt():
    farenheit = None
    if request.method == 'POST':
        celcius = request.form['celcius']
        farenheit= client.service.CelsiusToFahrenheit(celcius)
        
    return render_template('ctof.html', farenheit=farenheit)
