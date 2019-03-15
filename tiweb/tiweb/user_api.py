from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, length, IPAddress
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import jwt
import datetime
from functools import wraps
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/ankita/Documents/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is missing'})
        return f(*args, **kwargs)
    return decorated

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    email = db.Column(db.String(50), unique = True)
    db_ip = db.Column(db.Integer)
    db_port = db.Column(db.Integer)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class LoginForm(FlaskForm):
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

class UpdateForm(FlaskForm):
    username = StringField('username')
    first_name = StringField('first_name', validators = [InputRequired()])
    last_name = StringField('last_name', validators = [InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email(message = 'Invalid Email')])
    db_ip = StringField('db_ip', validators = [InputRequired(), IPAddress(ipv4 = True, ipv6 = False, message = 'Enter valid db_ip address')])
    db_port = IntegerField('db_port', validators = [InputRequired()])

@app.route('/signup', methods= ['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        new_user = User (first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, db_ip = form.db_ip.data, db_port = form.db_port.data, username = form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        #return form.username.data

        return '<h1>New user has been added</h1>'
    
    return render_template('signup.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    form = LoginForm()
    

    if form.validate_on_submit():
        user  = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                token = jwt.encode({'user': form.username.data,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})
            else:
                return '<h2>Enter correct username and password !</h2>'
    return render_template('login1.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>You are logged out</h1>'

@app.route('/list')

def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from User")
   rows = cur.fetchall(); 
   
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
    form = UpdateForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        username.first_name = form.first_name.data
        username.last_name = form.last_name.datalist
        username.email = form.email.data
        username.db_ip = form.db_ip.data
        username.db_port = form.db_port.datalist
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

if __name__ == '__main__':
    app.run(debug=True)
