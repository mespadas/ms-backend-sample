import json
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from numpy import identity
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key' #change this later

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    db.session.commit()
    print('Database created')

@app.cli.command('db_seed')
def db_seed():
    user1 = User(first_name='Jhon',
                last_name='Dhoe',
                email='j@gmail.com',
                password='p@ass')
    db.session.add(user1)
    db.session.commit()
    print('Database seeded')

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the API'), 200

@app.route('/not_found')
def not_found():
    return jsonify(message='No API for you !!'), 404

@jwt_required
@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry ' + name + "!"), 401
    else:
        return jsonify(message='Welcome ' + name + "!"), 200

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str,age: int):
    if age < 18:
        return jsonify(message='Sorry ' + name + "!"), 401
    else:
        return jsonify(message='Welcome ' + name + "!"), 200

@jwt_required
@app.route('/users', methods=['GET'])
def users():
    user_list = User.query.all()
    result = users_schema.dump(user_list)
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name,last_name=last_name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 202


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Bad email or password'), 401


# database models
class User(db.Model):
        id = Column(Integer, primary_key=True)
        first_name = Column(String)
        last_name = Column(String)
        email = Column(String, unique=True)
        password = Column(String)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','email', 'password')

user_schema= UserSchema()
users_schema = UserSchema(many=True)


if __name__ == '__main__':
   app.run()