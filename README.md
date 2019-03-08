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

## Building the React Frontend
- Go to the [front-end](https://github.com/CYBEX-P/ti-graph-frontend)
- `npm install`
- `npm start`

## Usage
1. `sudo python3 dockers.py` (in utils)
2. Enter venv
3. `pip install -r requirements.txt`
4. Take bolt port and password from step 1 output and change `graph` in `connect.py` to match your given password and bolt port  
    Example URI = `graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))`  
    Where 43311 is the bolt port and "EiWF2bD1Mnb1u1P" is the password supplied by `dockers.py` output
5. `python3 runserver.py`
6. The Neo4j GUI is located at localhost on the HTTP port specified by the output of `dockers.py`

### Bonus
 - Run `sudo systemctl <status/stop/restart/start> docker` to view the status of the docker service  
 - Run `sudo docker container ls` to view the ports for Bolt and HTTP


