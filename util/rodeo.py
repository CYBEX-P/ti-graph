import sys
sys.path.append('./lib')

from containerlib import client

# Example Usage
ClusterIP = "moose.soc.unr.edu"
bearer = "Bearer token-h88mk:snmxx9hxdqgg9gpk7blrrhxz899rb9k884tc74dllb28m628srxtfq"
urlBase = "https://squirrel.soc.unr.edu/v3/"
clusterid = "c-sxgk4"
projectid = "c-sxgk4:p-ffbv9"
clusterIP = "134.197.7.5"

# Create client
c = client(bearer, urlBase, projectid, clusterid, None, ClusterIP)
#Add a database
r = c.add_database()
#return value containes status and error information
if(r and r["status"]):
    print("Created Database: " + r["data"]["id"])
else:
    print("Error: " + r["error"])

#Get DB info
r = c.get_database_info()
if(r and r["status"]):
    print(json.dumps(r['data']))

#Get DB info for all databases
r = c.get_database_info_all()

#Nuke all databases (really don't want to do this but good example)
if(r and r['status']):
    for i in r['data']:
        x = client(bearer, urlBase, projectid, clusterid, i['id'], ClusterIP)
        if(x.delete_database()):
            print(i['id'] + " Deleted")
