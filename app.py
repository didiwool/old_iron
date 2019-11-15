import json
from functools import wraps
from time import time
import pandas as pd
from flask import Flask
from flask import request
from flask_restplus import Resource, Api, abort
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
import pickle


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
        return {"message": "The predicted price for this housing property is ${}.".format(result)}, 200


if __name__ == '__main__':
    csv_file = "predict.csv"
    df = pd.read_csv(csv_file)
    df1 = pd.read_csv("User.csv")

    app.run(debug=True)