from flask import Flask, jsonify, request, json

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, session, Response,make_response
from flask_wtf import FlaskForm
from flask import testing
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email, length, IPAddress, ValidationError, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import jwt
import datetime
from functools import wraps
import sqlite3 as sql
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_identity, verify_jwt_in_request)
from flask_mail import Message, Mail
from flask_bcrypt import Bcrypt
import os
import requests
import json
from json import dumps
from flask_jwt import current_identity
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from flask_cors import CORS
from werkzeug.datastructures import Headers
import uuid
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_jwt_extended import JWTManager
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/ankita/Documents/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['WTF_CSRF_ENABLED'] = False

#mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)




CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    public_id = db.Column(db.String(50), unique = True)                               
    first_name  = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(50), unique = True)
    db_ip = db.Column(db.Integer)
    db_port = db.Column(db.Integer)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators = [InputRequired()])
    last_name = StringField('last_name', validators = [InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email(message = 'Invalid Email')])
    #db_ip = StringField('db_ip', validators = [InputRequired(), IPAddress(ipv4 = True, ipv6 = False, message = 'Enter valid db_ip address')])
    #db_port = IntegerField('db_port', validators = [InputRequired()])
    username = StringField('username', validators = [InputRequired(), length(min = 4, max = 15)])
    password = PasswordField('password', validators = [InputRequired(), length(min = 8,max = 80)])
    admin = BooleanField('admin')
    
class LoginForm(FlaskForm):
    public_id = StringField('public_id')
    #first_name = StringField('first_name', validators = [InputRequired()])
    #last_name = StringField('last_name', validators = [InputRequired()])
    username = StringField('username', validators = [InputRequired(), length(min = 4, max = 15)])
    password = PasswordField('password', validators = [InputRequired(), length(min = 8,max = 80)])
    

@app.route('/users/register', methods = ['POST'])

def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = User(public_id=str(uuid.uuid4()),first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, username = form.username.data, password = hashed_password, admin = form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        result = {
		'first_name' : form.first_name.data,
		'last_name' : form.last_name.data,
		'email' : form.email.data,
		'password' : form.password.data,
		
	}
    return jsonify({'result' : result})

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    result = ''
    
    if form.validate_on_submit():
        user= User.query.filter_by(username = form.username.data).first()                                
        if user:
                if check_password_hash(user.password, form.password.data):
                    access_token = create_access_token(identity = {'username': form.username.data})
                    result = access_token
                else:
                    result = jsonify({"error":"Invalid username and password"})
    
                return result
	
@app.route('/remove', methods = ['POST', 'GET'])
def delete():
    #form = DeleteForm()
    #if form.validate_on_submit():
    User.query.filter_by(username = request.get_json()['username']).delete()
    db.session.commit()
    result = jsonify({"message": "User deleted"})
    return result 

@app.route('/update', methods = ['POST', 'GET'])
def update():
    
    
        #options = session.query(User)
        update_this = User.query.filter_by(username = request.get_json()['username']).first()
        update_this.first_name = request.get_json()['first_name']
        update_this.last_name = request.get_json()['last_name']
        update_this.email = request.get_json()['email']
        db.session.commit()
        result = jsonify({'message': 'DB updated'})
        return result 

@app.route('/find', methods = ['POST', 'GET'])
def found():
    found_user= User.query.filter_by(username = request.get_json()['username']).first_or_404()
    found_f = found_user.first_name
    found_l = found_user.last_name
    #found_id = found_user.id
    db.session.commit()
    
    return str(found_f+ " "+ found_l)
if __name__ == '__main__':
    app.run(debug=True)


    
