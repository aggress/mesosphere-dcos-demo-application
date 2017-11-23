from flask import Flask
from flask import request
from flask import jsonify
from urllib.request import urlopen
import socket
import string


app = Flask(__name__)

@app.route("/")
def show_details() :
    html = urlopen('http://demo-be-app.marathon.l4lb.thisdcos.directory:5000/')
    output = str(html.read().decode('utf-8'))
    new_output = output.replace('Back', 'Front', 1)
    return(new_output)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')

