from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
import yaml

app = Flask(__name__, static_folder='static', template_folder='static')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'notsosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiweb.db'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'asfdkjasdf32cxvewfsda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table(
    'roles_users', db.Column('user_id', db.Integer(),
                             db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))


class DatabaseManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer)
    ip = db.Column(db.String(15))
    dockerid = db.Column(db.String(15))
    status = db.Column(db.String(20))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def init_db():
    db.create_all()
    #    user_datastore.create_user(email='test@foo.edu', password='password')
    db.session.commit()


try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
        
with open('../config.yaml','r') as f:
    conf = yaml.load(f)

YAMLConfig = conf['IOC']