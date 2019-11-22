import json
from functools import wraps
from time import time
import pandas as pd
from flask import Flask
from flask import request, render_template, flash, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth

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
        r = requests.post("http://127.0.0.1:5000/token?username={}&password={}".format(username, password))
        print(r)
        if r.status_code == 200:
            token = r.json()["token"]
            print("sucesdsdfkdfs")
            return render_template("home.html", token=token)
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/predict/<token>',methods=['POST', 'GET'])
def predict(token):
    if request.method == "POST":
        #distance = request.form["distance"]
        #ascending = request.form["ascending"]
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        type = request.form["Type"]
        bedroom = int(request.form["bedroom"])
        bathroom = int(request.form["bathroom"])
        carspace = int(request.form["carspace"])
        #ascending = str_to_bool(ascending)

        if type == "House":
            type = 0
        elif type == "Apartment":
            type = 1
        elif type == "Unit":
            type = 2
        elif type == "Townhouse":
            type = 3
        headers = {'content-type': "application/json",
                   'AUTH_TOKEN': token}
        s = json.dumps({'Lattitude': latitude, 'Longtitude': longitude,'Type': type,'Bedroom': bedroom,'Bathroom': bathroom,'Car': carspace})
        r = requests.post("http://127.0.0.1:5000/predict", headers=headers, data=s)
        print(r.json())
        if r.status_code == 200:
            return render_template("predict.html", message=r.json()["message"])
        else:
            return render_template('predict.html', message=r.json()["message"])

    return render_template('predict.html')


@app.route('/school/<token>', methods=['POST', 'GET'])
def school(token):
    if request.method == "POST":
        distance = int(request.form["distance"])
        ascending = request.form["ascending"]
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        edu_type = request.form["edu_type"]
        school_type = request.form["school_type"]
        ascending = str_to_bool(ascending)
        headers = {'AUTH_TOKEN': token}
        r = requests.get("http://127.0.0.1:5000/schools?latitude={}&longitude={}&distance={}&"
                         "pageNumber=1&pageSize=10&education_type={}&school_type={}&ascending={}"
                         .format(latitude,longitude,distance, edu_type, school_type, ascending), headers=headers)

        page_num = r.json()["data"]["totalPageNum"]
        items = r.json()["data"]["schoolList"]
        curr_page = r.json()["data"]["curPageNum"]
        print(page_num)
        if r.status_code == 200:
            return render_template("schoolPage.html", pages=page_num, curr=curr_page, items=items, dis=distance
                                   , asc=ascending, lat=latitude, log=longitude, edu=edu_type, school=school_type, token=token)
        else:
            return render_template('school.html')
      
    return render_template('school.html')


@app.route('/schoolPage/<page_id>/<lat>/<log>/<dis>/<edu>/<school>/<asc>/<token>', methods=['POST', 'GET'])
def schoolPage(page_id,lat,log,dis,edu,school,asc,token):
    headers = {'AUTH_TOKEN': token}
    r = requests.get("http://127.0.0.1:5000/schools?latitude={}&longitude={}&distance={}&"
                     "pageNumber={}&pageSize=10&education_type={}&school_type={}&ascending={}"
                     .format(lat, log, dis, page_id, edu, school, asc), headers=headers)

    page_num = r.json()["data"]["totalPageNum"]
    items = r.json()["data"]["schoolList"]
    curr_page = r.json()["data"]["curPageNum"]
    if r.status_code == 200:
        return render_template("schoolPage.html", pages=page_num, curr=curr_page, items=items, dis=dis
                                   , asc=asc, lat=lat, log=log, edu=edu, school=school, token=token)
    else:
        return render_template('school.html')


@app.route('/realestate/<token>', methods=['POST', 'GET'])
def realestate(token):
    if request.method == "POST":
        distance = int(request.form["distance"])
        ascending = request.form["ascending"]
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        bedroom = int(request.form["bedroom"])
        bathroom = int(request.form["bathroom"])
        carspace = int(request.form["carspace"])
        type = request.form["Type"]
        ascending = str_to_bool(ascending)
        headers = {'AUTH_TOKEN': token}
        r = requests.get("http://127.0.0.1:5000/properties?latitude={}&longitude={}"
                         "&distance={}&pageNumber=1&pageSize=10&bedrooms={}&bathrooms={}&Parking={}&ascending={}&property_type={}"
                         .format(latitude, longitude, distance, bedroom, bathroom,carspace, ascending, type), headers=headers)

        page_num = r.json()["data"]["totalPageNum"]
        items = r.json()["data"]["propertyList"]
        curr_page = r.json()["data"]["curPageNum"]
        print(page_num)
        if r.status_code == 200:
            return render_template("realestatePage.html", pages=page_num, curr=curr_page, items=items, dis=distance
                                   , asc=ascending, lat=latitude, log=longitude, bed=bedroom, bath=bathroom,
                                   car=carspace, type=type, token=token)
        else:
            return render_template('Realestate.html')

    return render_template('Realestate.html')


@app.route('/realestatePage/<page_id>/<lat>/<log>/<dis>/<bed>/<bath>/<car>/<type>/<asc>/<token>', methods=['POST', 'GET'])
def realestatePage(page_id, lat, log, dis, bed, bath, car, type, asc, token):
    headers = {'AUTH_TOKEN': token}
    r = requests.get("http://127.0.0.1:5000/properties?latitude={}&longitude={}"
                         "&distance={}&pageNumber={}&pageSize=10&bedrooms={}&bathrooms={}&Parking={}&ascending={}&property_type={}"
                     .format(lat, log, dis, page_id, bed, bath, car, asc, type), headers=headers)

    page_num = r.json()["data"]["totalPageNum"]
    items = r.json()["data"]["propertyList"]
    curr_page = r.json()["data"]["curPageNum"]
    if r.status_code == 200:
        return render_template("realestatePage.html", pages=page_num, curr=curr_page, items=items, dis=dis
                               , asc=asc, lat=lat, log=log, bed=bed, bath=bath, car=car, type=type, token=token)
    else:
        return render_template('Realestate.html')


@app.route('/propertyInfo/<id>/<token>', methods=['POST', 'GET'])
def propertyInfo(id, token):

    headers = {'AUTH_TOKEN': token}
    r = requests.get("http://127.0.0.1:5000/property/{}"
                     .format(int(id)), headers=headers)

    item = r.json()[0]

    if r.status_code == 200:
        return render_template("propertyInfo.html", item=item)
    else:
        return render_template('home.html')


def str_to_bool(input):
    return True if input == 'Ascending' else False


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345, debug=True)