from flask import Flask, render_template, send_from_directory, jsonify
import json
import atm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    data = atm.load('grabacion(0).atm')
    return data

if __name__ == '__main__':
    app.run(debug=True)
