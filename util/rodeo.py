import requests
import yaml
import uuid
import json
from requests.auth import HTTPBasicAuth
import string
import random
import time

ClusterIP = "134.197.7.5"

def pw_gen(size = 8, chars=string.ascii_letters + string.digits):
    	return ''.join(random.choice(chars) for _ in range(size))

def get_node_info(node):

    port = node['publicEndpoints'][0]['port']
    auth = node['containers'][0]['environment']['NEO4J_AUTH']
    service = node['publicEndpoints'][0]['serviceId']
    if ( node['deploymentStatus']['availableReplicas'] == 1 ):
        status = True
    else:
        status = False
    return  {"port": port, "id": WorkloadName, "auth": auth, "available": status, "ip": ClusterIP, "service": service}    

def GetNodeYaml(WorkloadName, password):  
    #Including template inline for now. TODO: remove to config file - jeffs
    node = '''{
	"apiVersion": "apps/v1beta1",
	"kind": "Deployment",
	"metadata": {
		"name": "__APP_NAME__",
		"namespace": "neo4j",
		"labels": {
			"app": "__APP_NAME__"
		}
	},
	"spec": {
		"replicas": 1,
		"strategy": {
			"rollingUpdate": {
				"maxSurge": 1,
				"maxUnavailable": 0
			},
			"type": "RollingUpdate"
		},
		"template": {
			"metadata": {
				"labels": {
					"app": "__APP_NAME__"
				}
			},
			"spec": {
				"containers": [
					{
						"name": "__APP_NAME__",
						"image": "neo4j",
						"imagePullPolicy": "IfNotPresent",
						"env": [
							{
								"name": "NEO4J_AUTH",
								"value": "neo4j/__PASSWORD__"
							},
							{
								"name": "NEO4J_ACCEPT_LICENSE_AGREEMENT",
								"value": "yes"
							}
						],
						"ports": [
							{
								"containerPort": 7687,
								"name": "bolt",
                                "protocol": "TCP"
							}
						],
						"securityContext": {
							"privileged": true
						}
					}
				],
				"nodeSelector": {
					"purpose": "worker"
				}
			}
		}
	}
    }'''
    n = json.loads(node)
    n['metadata']['name'] = WorkloadName
    n['metadata']['labels']['app'] = WorkloadName
    n['spec']['template']['metadata']['labels']['app'] = WorkloadName   
    n['spec']['template']['spec']['containers'][0]['name'] = WorkloadName
    n['spec']['template']['spec']['containers'][0]['env'][0]['value'] = 'neo4j/' + password
    return n


def getServiceYanml(WorkloadName):
    #Including template inline for now. TODO: remove to config file - jeffs
    service = '''{
	"apiVersion": "v1",
	"kind": "Service",
	"metadata": {
		"name": "__APP_NAME__-service",
		"namespace": "neo4j",
		"labels": {
			"app": "__APP_NAME__"
		}
	},
	"spec": {
		"type": "NodePort",
		"ports": [
			{
				"port": 7687,
				"targetPort": 7687,
				"protocol": "TCP",
				"name": "bolt"
			}
		],
		"selector": {
			"app": "__APP_NAME__"
		}
	}
    }'''
    s = json.loads(service)
    s['metadata']['name'] = WorkloadName + "-service"
    s['metadata']['labels']['app'] = WorkloadName
    s['spec']['selector']['app'] = WorkloadName
    return s


def AddDatabase(node,service,urlBase,clusterID,bearer):
    yamlTemplate = str(yaml.dump(node,default_flow_style = False, allow_unicode = True, encoding = None)) + '\r\n' + '---' + '\r\n' + str(yaml.dump(service,default_flow_style = False, allow_unicode = True, encoding = None))

    postData = {'defaultNamespace': None, 'namespace': None, 'projectId': None,'yaml': yamlTemplate}
    headers = {'Content-Type': 'application/json', 'Authorization': bearer }
    url = urlBase + "clusters/" + clusterID + "?action=importYaml"
    r = requests.post(url = url, data=json.dumps(postData).encode("utf-8"), headers=headers)
    print(r.text)
    return r

def GetDatabase(urlBase,projectID, WorkloadName, bearer):
    url = urlBase + "project/" + projectID + "/workloads/deployment:neo4j:" + WorkloadName
    headers = {'Content-Type': 'application/json', 'Authorization': bearer }
    r = requests.get(url=url,headers=headers)
    containerstats = {}
    if(r.status_code == 200):
        containerstats = get_node_info(json.loads(r.text))
    else:
        containerstats = {"id":WorkloadName, "available": False, "port": 0, "auth": None, "ip":None, "service": None}
    return containerstats


def GetAllDatabases(urlBase,projectID,bearer):
    url = urlBase + "project/" + projectID + "/workloads"
    headers = {'Content-Type': 'application/json', 'Authorization': bearer }
    r = requests.get(url=url,headers=headers)
    containerstats = {"data":[], "available": False}
    if(r.status_code == 200):
        nodes = json.loads(r.text)
        containerstats["available"] = True
        for node in nodes["data"]:
            containerstats["data"].append(get_node_info(node))
    return containerstats

def DeleteDatabase(urlBase,projectID,Bearer,WorkloadName):
    containerstats = GetDatabase(urlBase,projectID,WorkloadName,bearer)
    headers = {'Content-Type': 'application/json', 'Authorization': bearer }
    if(containerstats['available']):
        urlDeleteWorkload = urlBase + "project/" + projectID + "/workloads/deployment:neo4j:" + WorkloadName
        urlDeleteService = urlBase + "project/" + projectID + "/dnsRecords/" + containerstats['service']
        result = requests.delete(url=urlDeleteService,headers=headers)
        print(urlDeleteService)
        print(result.status_code)
        if(result.status_code != 204):
            raise Exception("Failed to delete service for workload: " + WorkloadName)
        else:
            result = requests.delete(url=urlDeleteWorkload,headers=headers)
            if(result.status_code != 204):
                raise Exception("Failed to delete workload: " + WorkloadName)
    else:
        raise Exception("Failed to connect to API for: " + WorkloadName)
    return 0

if __name__== "__main__":
    bearer = "Bearer token-h88mk:snmxx9hxdqgg9gpk7blrrhxz899rb9k884tc74dllb28m628srxtfq"
    urlBase = "https://squirrel.soc.unr.edu/v3/"
    clusterID  = "c-sxgk4"
    projectID = "c-sxgk4:p-ffbv9"
    clusterIP = "134.197.7.5"
    WorkloadName =  'neo4j-db-' + str(uuid.uuid4())
#    password = pw_gen()
#    nodey = GetNodeYaml(WorkloadName,password)
#    servicey = getServiceYanml(WorkloadName)
#    result = AddDatabase(nodey,servicey,urlBase,clusterID,bearer)
#    if(result.status_code != 200):
#        print(result.text)
#    else:
#        time.sleep(2)
#        result = GetDatabase(urlBase,projectID,WorkloadName,bearer)      
#        else:
#            print("ERROR: " + result.text)

    r = DeleteDatabase(urlBase,projectID,bearer,"neo4j-db-f89d87a9-ca80-4bc1-9ea2-d2713a27cb91")
    print(r)
    
    