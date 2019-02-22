from tiweb import app

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'notsosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'asfdkjasdf32cxvewfsda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

