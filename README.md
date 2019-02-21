# ti-graph
## tiweb
Once you have cloned the repo start by creating a virtual environment using 
```
python3 -m venv venv
```

Add a .gitignore file that includes:

```
venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/
```

Install requirements with
```
pip3 install -r requirements.txt
```

run the flask app with
```
python3 runserver.py
```
from within the tiweb folder

To Add additional files with routes
```
1: create new python file
2: import the file into runserver.py
```

All static content will need to go under tiweb\static

