import docker
import time
import socket
from contextlib import closing
import json
import string
import random

def pw_gen(size = 8, chars=string.ascii_letters + string.digits):
#	return ''.join(random.choice(chars) for _ in range(size))
	return 'wolfpack'

def killall(client):
    for container in client.containers.list():
        container.kill()

def find_free_ports():
    bolt = 7687 
    http = 7474 
    #find first free port for bolt listener
#    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#        s.bind(('', 0))
#        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#       bolt = s.getsockname()[1]
#        #find second free port for http listener while bolt listener is still up
#        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as x:
#            x.bind(('', 0))
#            x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#            http = x.getsockname()[1]
    return bolt,http

def list_db(client):
    container_info = []
    for container in client.containers.list():
         container_info.append({"id" :container.id, "status": container.status, "name": container.name})
    return container_info

def delete_db(client, id):
    container = client.containers.get(id)
    container.kill()

def create_db(client):
   
    (bolt,http) = find_free_ports()
    bindip = '127.0.0.1'
    newpass = pw_gen(15)

    enviro = ['JAVA_OPTS=-Xmx1g','NEO4J_AUTH=neo4j/' + newpass]
    porto = {'7687/tcp':(bindip,bolt),'7474/tcp':(bindip,http)}
    #if we need persistence.  Which we don't right now
    volumeo = {'/logs': {'bind': '/logs', 'mode': 'rw'},'/data': {'bind': '/data','mode':'rw'}}
    containero = 'neo4j:3.0'

    c = client.containers.run(containero,environment=enviro,ports=porto,detach=True)

    while(True):
        time.sleep(2)
        c.reload()
        if(c.status == 'running'):
            break        

    containerstats = {"bolt": bolt, "http": http, "ip": bindip, "id": c.id, "password": newpass}

    return json.dumps(containerstats,indent=4,sort_keys=True)

if __name__== "__main__":
    client = docker.from_env()
    #killall(client)
    stats = create_db(client)
    print(stats)
    print(json.dumps(list_db(client),indent=4,sort_keys=True))
