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
        if r.status_code == 200:
            token = r.json()["token"]
            print("sucesdsdfkdfs")
            return render_template("home.html")
        else:
            return render_template('login.html')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)