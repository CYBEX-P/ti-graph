from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import jsonify
from tiweb import app

@app.route('/secure')
@login_required
def home():
    return app.send_static_file('secure.html')

@app.route('/api')
def api():
    foo = {"bar":'test'}
    return jsonify(foo)
