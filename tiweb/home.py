from tiweb import app

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/home')
def test():
    return app.send_static_file('home.html')

