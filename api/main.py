import datetime
import json
from functools import wraps
from time import time
import pandas as pd
from flask import Flask
from flask import request
from flask import jsonify
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
import pickle
from math import sin, cos, sqrt, atan2, radians


# helper function
def get_distance(x1, y1, x2, y2):
    r = 6373.0

    x1 = radians(x1)
    y1 = radians(y1)
    x2 = radians(x2)
    y2 = radians(y2)

    dlon = y2 - y1
    dlat = x2 - x1

    a = sin(dlat / 2) ** 2 + cos(x1) * cos(x2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c
    return distance


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)

app = Flask(__name__)
api = Api(app, authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="Books",  # Default namespace
          title="Book Dataset",  # Documentation Title
          description="This is just a simple example to show how publish data as a service.")  # Documentation Description


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated


# The following is the schema of Book
property_model = api.model('Property', {
    'Rooms': fields.Integer,
    'Type': fields.Integer,
    'Lattitude': fields.Float,
    'Longtitude': fields.Float,
    'Bedroom2': fields.Integer,
    'Bathroom': fields.Integer,
    'Car': fields.Integer,
    'YearBuilt': fields.Integer,
    'Landsize': fields.Float
})

parser = reqparse.RequestParser()
# parser.add_argument('distance', type=int)
# parser.add_argument('order', choices=list(column for column in book_model.keys()))
# parser.add_argument('ascending', type=inputs.boolean)
parser.add_argument('Rooms', type=int)
parser.add_argument('Type', type=int)
parser.add_argument('Lattitude', type=float)
parser.add_argument('Longtitude', type=float)
parser.add_argument('Bedroom2', type=int)
parser.add_argument('Bathroom', type=int)
parser.add_argument('Car', type=int)
parser.add_argument('YearBuilt', type=int)
parser.add_argument('Landsize', type=float)

credential_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String,
    'usertype': fields.Integer
})

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)

position_model = api.model('position', {
    'X': fields.Float,
    'Y': fields.Float
})

pos_parser = reqparse.RequestParser()
pos_parser.add_argument('distance', type=int)
pos_parser.add_argument('ascending', type=bool)
pos_parser.add_argument('latitude', type=float)
pos_parser.add_argument('longitude', type=float)

school_model = api.model('position', {
    'X': fields.Float,
    'Y': fields.Float,
    'Education_Sector': fields.String,
    'School_Name': fields.String,
    'School_Type': fields.String,
    'Postal_Town': fields.String
})
school_parser = reqparse.RequestParser()
school_parser.add_argument('pageNumber', type=int)
school_parser.add_argument('pageSize', type=int)
# parser.add_argument('distance', type=int)
school_parser.add_argument('education_type', choices=['Government', 'Independent', 'Catholic', 'Any'])
school_parser.add_argument('school_type', choices=['Primary', 'Pri/Sec', 'Special', 'Secondary', 'Language', 'Any'])
school_parser.add_argument('ascending', type=inputs.boolean)

admin_parser = reqparse.RequestParser()
admin_parser.add_argument('time', type=int)
admin_parser.add_argument('api_type', choices=['predict', 'login', 'school_list', 'Any'])


@api.route('/admin_check')
class AdminCheck(Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Fail')
    @api.doc(description="Check the api calls")
    @api.expect(admin_parser, validate=True)
    # @requires_auth
    def post(self):
        args = admin_parser.parse_args()
        duration = args.get('time')
        api_type = args.get('api_type')
        df_record = pd.read_csv("record.csv")
        if api_type != 'Any':
            df_filtered = df_record[df_record["call_name"] == api_type]
        else:
            df_filtered = df_record
        # datetime.timedelta(datetime.now())
        gap = datetime.timedelta(seconds=duration*3600)
        limit = datetime.datetime.now()-gap
        df_filtered['time'] = pd.to_datetime(df_filtered['time'])
        df_filtered2 = df_filtered[df_filtered["time"] > limit]
        count = df_filtered2["time"].count()
        return {"message": "The number of api calls for {} is {}.".format(api_type, count)}, 200


@api.route('/login')
class Login(Resource):
    @api.response(200, 'Successful')
    @api.response(401, 'Fail')
    @api.doc(description="Log a user into the system")
    @api.expect(credential_parser, validate=True)
    def post(self):
        args = credential_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if username in df1.username.values:
            row_id = df1.loc[df1['username'] == username].index[0]
            if str(df1.loc[row_id, 'password']) == password:
                return {"token": auth.generate_token(username)}
        num = df_record["time"].count()
        df_record.loc[num, "call_name"] = "login"
        df_record.loc[num, "time"] = datetime.datetime.now()
        df_record.to_csv("record.csv")
        return {"message": "authorization has been refused for those credentials."}, 401


@api.route('/register')
class Register(Resource):
    @api.response(201, 'Successful')
    @api.response(400, 'Fail')
    @api.doc(description="Create a new account")
    @api.expect(credential_model, validate=True)
    def post(self):
        info = request.json

        if 'username' not in info or 'password' not in info or 'usertype' not in info:
            return {"message": "Missing Information for Registration"}, 400

        username = info['username']

        # check if the given user already exists
        if username in df1.username.values:
            return {"message": "The username has already been used"}, 400
        index = df1.username.count()
        print(index)
        # Put the values into the dataframe
        for key in info:
            if key not in credential_model.keys():
                return {"message": "Attribute {} is invalid".format(key)}, 400
            df1.loc[index, key] = info[key]
        # print(df1.head())
        # df.append(info, ignore_index=True)
        return {"message": "Create the account successfully"}, 201


@api.route('/predict')
class Predict(Resource):
    @api.response(200, 'Successful')
    @api.response(400, 'Missing Information')
    @api.doc(description="Predict price of a real estate")
    @api.expect(property_model, validate=True)
    @requires_auth
    def post(self):
        info = request.json
        print(len(info.keys()))
        if len(info.keys()) < 9:
            return {"message": "Missing Information for Prediction"}, 400

        room = info['Rooms']
        kind = info['Type']
        lat = info['Lattitude']
        long = info['Longtitude']
        bed = info['Bedroom2']
        bath = info['Bathroom']
        car = info['Car']
        year = info['YearBuilt']
        size = info['Landsize']
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

        result = int(loaded_model.predict([[room, kind, lat, long, bed, bath, car, year, size]])[0])
        index = df.Price.count()
        # Put the values into the dataframe
        for key in info:
            df.loc[index, key] = info[key]
        df.loc[index, "Price"] = result
        print(df.head())
        num = df_record["time"].count()
        df_record.loc[num, "call_name"] = "predict"
        df_record.loc[num, "time"] = datetime.datetime.now()
        df_record.to_csv("record.csv")
        return {"message": "The predicted price for this housing property is ${}.".format(result)}, 200


@api.route('/findschool_with_dist')
class FindSchoolDistance(Resource):
    @api.response(200, 'Successful')
    # @api.response(400, 'Missing Information')
    @api.doc(description="Return a list of school within a distance range")
    @api.expect(pos_parser, validate=True)
    # @requires_auth
    def get(self):
        # info = request.json

        args = pos_parser.parse_args()
        ascending = args.get('ascending', True)
        distance = args.get('distance')
        latitude = args.get('latitude')
        longitude = args.get('longitude')
        df_dist = df2
        for index, row in df_dist.iterrows():
            df_dist.loc[index, "distance"] = get_distance(row["X"], row["Y"], latitude, longitude)

        print(df_dist["distance"].head())
        df_filtered = df_dist[df_dist["distance"] < distance]
        df_filtered.sort_values(by="distance", inplace=True, ascending=ascending)

        json_str = df_filtered.to_json(orient='index')

        # convert the string JSON to a real JSON
        ds = json.loads(json_str)
        ret = []

        for idx in ds:
            school = ds[idx]
            ret.append(school)

        return ret
#
@api.route('/school')
class School(Resource):
    @api.response(200, 'Successful')
    @api.response(400, 'Fail to return')
    @api.doc(description="Return a list of school with pagination")
    @api.expect(school_parser, validate=True)
    # @requires_auth
    def get(self):
        args = school_parser.parse_args()
        pageNumber = args["pageNumber"]
        pageSize = args["pageSize"]
        school_type = args.get('school_type')
        education_type = args.get('education_type')
        ascending = args.get('ascending', True)
        df_filtered = df2
        if school_type != 'Any':
            df_filtered = df2[df2["School_Type"] == school_type]
        if education_type != 'Any':
            df_filtered = df_filtered[df_filtered['Education_Sector'] == education_type]
        count = df_filtered["School_Name"].count()
        df_filtered.sort_values(by="School_Name", inplace=True, ascending=ascending)
        if count == 0:
            respData = {}
        else:
            totalPage = int(count / pageSize)
            if (count % pageSize) > 0:
                totalPage += 1

            skipNumber = pageSize * (pageNumber - 1)
            endNumber = skipNumber+pageSize-1
            if endNumber >= count:
                endNumber = count - 1
            df_paged = df_filtered[skipNumber:endNumber]
            json_str = df_paged.to_json(orient='index')
            ds = json.loads(json_str)
            ret = []
            for idx in ds:
                school = ds[idx]
                ret.append(school)

            hasPrev = False
            if pageNumber > 1:
                hasPrev = True
            hasNext = False
            if pageNumber < totalPage:
                hasNext = True
            respData = {
                "schoolList": ret,
                "curPageNum": pageNumber,
                "numPerPage": pageSize,
                "totalNum": int(count),
                "totalPageNum": totalPage,
                "hasPrev": hasPrev,
                "hasNext": hasNext,
            }
        respdict = {"code": 200, "message": "Get question ok", "data": respData}
        num = df_record["time"].count()
        df_record.loc[num, "call_name"] = "school_list"
        df_record.loc[num, "time"] = datetime.datetime.now()
        df_record.to_csv("record.csv")
        return jsonify(respdict)


#
#     @api.response(200, 'Successful')
#     # @api.response(400, 'Missing Information')
#     @api.doc(description="Return a list of school within a distance range")
#     @api.expect(position_model, validate=True)
#     def post(self):


if __name__ == '__main__':
    csv_file = "predict.csv"
    df = pd.read_csv(csv_file)
    df1 = pd.read_csv("User.csv")
    df2 = pd.read_csv("schoollocations2019.csv")
    df2 = df2[['School_No', 'Education_Sector', 'School_Name', 'School_Type', 'Postal_Town', 'X', 'Y']]
    print(df2['School_Type'].unique())
    df_record = pd.read_csv("record.csv")
    app.run(debug=True)