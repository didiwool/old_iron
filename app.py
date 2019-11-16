import json
from functools import wraps
from time import time
import pandas as pd
from flask import Flask
from flask import request, render_template, flash, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
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
        usertype = int(request.form["usertype"])
        print(usertype)


        url = 'http://127.0.0.1:5000/register'
        s = json.dumps({'username': username, 'password': password,'usertype': usertype})
        r = requests.post(url, data=s)
        print(r)
       
        if r.status_code == 201:
            print("=============")
            return render_template("home.html")
        else:
            print("*************")
            return render_template('register.html')

        print("-----------" + r.status_code)
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)