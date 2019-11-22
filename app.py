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

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        #distance = request.form["distance"]
        #ascending = request.form["ascending"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        Type = request.form["Type"]
        bedroom = request.form["bedroom"]
        bathroom = request.form["bathroom"]
        carspace = request.form["carspace"]
        #ascending = str_to_bool(ascending)

       # print(distance)
        #print(ascending)
        print(latitude)
        print(longitude)
        print(Type)
        print(bedroom)
        print(bathroom)
        print(carspace)

        headers = {'content-type': "application/json"}
        s = json.dumps({'latitude': latitude, 'longitude': longitude,'Type': Type,'bedroom': bedroom,'bathroom': bathroom,'carspace': carspace})
        r = requests.post("http://127.0.0.1:5000/predict", headers=headers, data=s)
        if r.status_code == 201:
            return render_template("home.html")
        else:
            return render_template('predict.html')

    return render_template('predict.html')


@app.route('/school/', methods=['POST', 'GET'])
def school():
    if request.method == "POST":
        distance = request.form["distance"]
        ascending = request.form["ascending"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        edu_type = request.form["edu_type"]
        school_type = request.form["school_type"]
        ascending = str_to_bool(ascending)

        r = requests.get("http://127.0.0.1:5000/schools?latitude={}&longitude={}&distance={}&"
                         "pageNumber=1&pageSize=10&education_type={}&school_type={}&ascending={}"
                         .format(latitude,longitude,distance, edu_type, school_type, ascending))

        page_num = r.json()["data"]["totalPageNum"]
        items = r.json()["data"]["schoolList"]
        curr_page = r.json()["data"]["curPageNum"]
        print(page_num)
        if r.status_code == 200:
            return render_template("schoolPage.html", pages=page_num, curr=curr_page, items=items, dis=distance
                                   , asc=ascending, lat=latitude, log=longitude, edu=edu_type, school=school_type)
        else:
            return render_template('school.html')
      
    return render_template('school.html')
#
@app.route('/schoolPage/<page_id>/<lat>/<log>/<dis>/<edu>/<school>/<asc>', methods=['POST', 'GET'])
def schoolPage(page_id,lat,log,dis,edu,school,asc):
    r = requests.get("http://127.0.0.1:5000/schools?latitude={}&longitude={}&distance={}&"
                     "pageNumber={}&pageSize=10&education_type={}&school_type={}&ascending={}"
                     .format(lat, log, dis, page_id, edu, school, asc))
    page_num = r.json()["data"]["totalPageNum"]
    items = r.json()["data"]["schoolList"]
    curr_page = r.json()["data"]["curPageNum"]
    if r.status_code == 200:
        return render_template("schoolPage.html", pages=page_num, curr=curr_page, items=items, dis=dis
                                   , asc=asc, lat=lat, log=log, edu=edu, school=school)
    else:
        return render_template('school.html')




def str_to_bool(input):
    return True if input == 'Ascending' else False


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)