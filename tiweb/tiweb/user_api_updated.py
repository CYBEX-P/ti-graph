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
from flask_jwt import current_identity
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from werkzeug.datastructures import Headers
import uuid





app = Flask(__name__)
#Session(app)
#app.config['JWT_SECRET_KEY'] = 'Thisissecretkey'
app.config['SECRET_KEY'] = 'stupid'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/ankita/Documents/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('DB_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('DB_PASSWORD')
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#jwt = JWTManager(app)

#jwt._set_error_handler_callbacks(api)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)



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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@staticmethod
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)

def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
        raise ValidationError('There is no account with that email. You must register first.')

def validate_username(self, username):
    if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=os.environ.get('DB_USER'),
                  recipients=[user.email])
    msg.body = "To reset your password, visit the following link:, %s" %{url_for('reset_token', token=token, _external=True)} 
    mail.send(msg)

class LoginForm(FlaskForm):
    public_id = StringField('public_id')
    username = StringField('username', validators = [InputRequired(), length(min = 4, max = 15)])
    password = PasswordField('password', validators = [InputRequired(), length(min = 8,max = 80)])
    remember = BooleanField('remember me')

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators = [InputRequired()])
    last_name = StringField('last_name', validators = [InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email(message = 'Invalid Email')])
    db_ip = StringField('db_ip', validators = [InputRequired(), IPAddress(ipv4 = True, ipv6 = False, message = 'Enter valid db_ip address')])
    db_port = IntegerField('db_port', validators = [InputRequired()])
    username = StringField('username', validators = [InputRequired(), length(min = 4, max = 15)])
    password = PasswordField('password', validators = [InputRequired(), length(min = 8,max = 80)])
    admin = BooleanField('admin')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    username = StringField('username')
    first_name = StringField('first_name', validators = [InputRequired()])
    last_name = StringField('last_name', validators = [InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email(message = 'Invalid Email')])
    db_ip = StringField('db_ip', validators = [InputRequired(), IPAddress(ipv4 = True, ipv6 = False, message = 'Enter valid db_ip address')])
    db_port = IntegerField('db_port', validators = [InputRequired()])


class RequestResetForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message = 'Invalid Email')])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =  request.args.get('token')
        if not token:
            return jsonify({'message':'token is missing'}),403
        try :
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'token is missing'}),403
        
        return f(*args, **kwargs)
    return decorated

#def token_required(f):
    #@wraps(f)
    #def decorated(*args, **kwargs):
        #token = None

        #if 'Authorization' in request.headers:
            #token = request.headers['Authorization']
        
        #if not token:
            #request.args.get('token')
            #return jsonify({'message':'Token is missing'})
        #try:
            #data = jwt.decode(token, app.config['SECRET_KEY'])
            #current_user = User.query.filter_by(public_id).first()
        #except:
            #return jsonify({'message' : 'Token is invalid'}), 401
        
        #return f(current_user, *args, **kwargs)
    #return decorated

@app.route('/home')
def home():
    return "HEllo! Welcome"

@app.route('/signup', methods= ['GET', 'POST'])

def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = User(public_id=str(uuid.uuid4()),first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, db_ip = form.db_ip.data, db_port = form.db_port.data, username = form.username.data, password = hashed_password, admin = form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been added</h1>'
    
    return render_template('signup.html', form=form)                

@app.route('/login', methods = ['GET', 'POST'])                                
def login():
    form = LoginForm()
    
    #a.authenticate()

    #authenticate()
    #if form.validate_on_submit():
    if request.method == 'POST':
        user  = User.query.filter_by(username = form.username.data).first()                                
        if user:
                if check_password_hash(user.password, form.password.data):
                    

                    token = jwt.encode({'public_id': form.public_id.data,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes =30 )},app.config['SECRET_KEY'])
                    #session['auth-token'] = token.decode('UTF-8')
                        #token1 =  
                        #ret = {'jwt': create_jwt(identity=form.username.data, expires_sec=40)}
                    ##session['api_session_token'] = jsonify({'token': token.decode('UTF-8')})list
                    return  jsonify({'token': token.decode('UTF-8')}), 200, {'Authorization' : jsonify({'token': token.decode('UTF-8')})}
                else:
                    return jsonify({'message':'Enter correct username and password'})    
                
    return render_template('login2.html',form = form)


@app.route('/token', methods = ['GET','POST'])
def todo():
    return render_template("token.html")


@app.route('/login/<token>', methods = ['GET','POST'])
def response():
    return render_template("tokenfetch.html")


@app.route('/logout')
def logout():
    logout_user()
    return '<h1>You are logged out</h1>'


@app.route('/list', methods = ['GET', 'POST'])

def list():
    #if not current_user.admin:
        #return jsonify({'message':'cannot perform that function'})
    
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from User")
    rows = cur.fetchall()
    
    return render_template("list.html",rows = rows)

@app.route('/delete')

def remove():
    return render_template("delete.html")

@app.route('/remove_user', methods = ['POST', 'GET'])
def delete():
    #form = DeleteForm()
    if request.method == 'POST':
        username = request.form['username']
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("Delete from User where username = ?", (username,))
        con.commit()
        
    return render_template("delete_update.html")

@app.route('/update')
def update1():
    return render_template("update_user.html")

@app.route('/update_user', methods = ['POST', 'GET'])
def update():
    #form = UpdateForm()
    
    if request.method == 'POST':
        #options = session.query(User)
        update_this = User.query.filter_by(id = request.form['id']).first()
        update_this.first_name = request.form['first_name']
        update_this.last_name = request.form['last_name']
        update_this.email = request.form['email']
        update_this.db_ip = request.form['db_ip']
        update_this.db_port = request.form['db_port']
        update_this.username = request.form['username']
        db.session.commit()
    return render_template("updated.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/find_user', methods=['POST', 'GET'])
def find():
    if request.method == 'POST':
        id = request.form['id']
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from User where id = ?",(id))
        rows = cur.fetchall()
        con.commit()
        #msg = rows
    return render_template("searched_user.html", rows=rows)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

if __name__ == '__main__':
    app.run(debug=True)
