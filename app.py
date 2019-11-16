import json
from functools import wraps
from time import time
import pandas as pd
from flask import Flask
from flask import request, render_template, flash, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(type(username), type(password))
        r = requests.post("http://127.0.0.1:5000/login?username={}&password={}".format(username, password))
        print(r)
        if r.status_code == 200:
            token = r.json()["token"]
            print("sucesdsdfkdfs")
            return render_template("home.html")
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usertype = 1

        headers = {'content-type': "application/json"}
        s = json.dumps({'username': username, 'password': password,'usertype': usertype})
        r = requests.post("http://127.0.0.1:5000/register", headers=headers, data=s)
        if r.status_code == 201:
            return render_template("home.html")
        else:
            return render_template('register.html')


    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)