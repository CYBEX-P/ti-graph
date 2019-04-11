# Helper class for managing workloads in Rancher/Kubernetes
# All functions return dictionary with status:boolean, error:string, data:object
# 3/8/2019
# jeffs
# Todo:
# May need to refactor error handling.  Currently throws generic exception but most errors shoudl be handled with a json status return
import requests
import yaml
import uuid
import json
from requests.auth import HTTPBasicAuth
import string
import random
import time

def pw_gen(size=8, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class client:
    def __init__(self, bearer=None, url=None, projectid=None, clusterid=None,
                 workload_name=None,cluster_ip=None):
        self.bearer = bearer
        self.url = url
        self.projectid = projectid
        self.clusterid = clusterid
        self.workload_name = workload_name
        self.cluster_ip = cluster_ip
    
    def get_database_info(self):
        return self._get_database_info()

    def get_database_info_all(self):
        url = self.url + "project/" + self.projectid + "/workloads"
        headers = {'Content-Type': 'application/json', 'Authorization': self.bearer}
        r = requests.get(url=url, headers=headers)
        workload_info = []
        if r.status_code < 200 or r.status_code >= 300:
            return {"status": False, "error": r.text, "data": None}
        else:
            nodes = json.loads(r.text)
            for node in nodes["data"]:
                workload_info.append(self._get_node_info(node))
        
        return {"status": True, "error": None, "data": workload_info}

    def delete_database(self):
        return(self._delete_service() and self._delete_database())
     
    def add_database(self):
        if(self.workload_name is None):
            self.workload_name = 'neo4j-db-' + str(uuid.uuid4())
            if(self._valid()):        
                password = pw_gen()
                node = self._get_node_yaml(password)
                service = self._get_service_yaml()
                yaml_template = str(yaml.dump(node, default_flow_style=False, allow_unicode=True, encoding=None)) + '\r\n' + '---' + '\r\n' + str(yaml.dump(service, default_flow_style=False, allow_unicode=True, encoding=None))

                post_data = {'defaultNamespace': None, 'namespace': None, 'projectId': None, 'yaml': yaml_template}
                headers = {'Content-Type': 'application/json', 'Authorization': self.bearer}
                url = self.url + "clusters/" + self.clusterid + "?action=importYaml"
                r = requests.post(url=url, data=json.dumps(post_data).encode("utf-8"), headers=headers)
                if r.status_code < 200 or r.status_code >= 300:
                    return {"status": False, "error": r.text, "data": None}
                else:
# give rancher a couple seconds to create the objects so we can just return them
                    time.sleep(2)
                    return self._get_database_info()
   
        return {"status": False, "error": "Database already exists","data": None}

    def _valid(self):
        if(self.url is not None and self.bearer is not None and self.projectid is not None and self.clusterid is not None and self.workload_name is not None):
            return True
        else:
            raise Exception("Database information not complete")

    def _get_database_info(self):
        if(self._valid):
            headers = {'Content-Type': 'application/json', 'Authorization': self.bearer }
            url = self.url + "project/" + self.projectid + "/workloads/deployment:neo4j:" + self.workload_name
            r = requests.get(url=url,headers=headers)

            if(r.status_code < 200 or r.status_code >= 300):
                return {"status": False,"error": r.text,"data": None}
            else:
                return {"status": True, "error": None, "data": self._get_node_info(json.loads(r.text))}
    
    def _delete_service(self):
        if(self._valid):
            workload_info = self._get_database_info()
            headers = {'Content-Type': 'application/json', 'Authorization': self.bearer}
            print(str(workload_info))
            url = self.url + "project/" + self.projectid + "/dnsRecords/" + workload_info['data']['service']
            r = requests.delete(url=url, headers=headers)
            print('Status code: ' + str(r.status_code) + " Text: " + r.text)
            if(r.status_code < 200 or r.status_code >= 300):
                raise Exception("Failed to delete service.  Error text: " + r.text)
            else:
                return True
        
    def _delete_database(self):
        if(self._valid): 
            headers = {'Content-Type': 'application/json', 'Authorization': self.bearer}
            url = self.url + "project/" + self.projectid + "/workloads/deployment:neo4j:" + self.workload_name    
            r = requests.delete(url=url, headers=headers)
            print('Status code: ' + str(r.status_code) + " Text: " + r.text)
            if(r.status_code < 200 or r.status_code >= 300):
                raise Exception("Failed to delete database.  Error text: " + r.text)
            else:
                self.workload_name = None
                return True

    
    def _get_node_info(self,node):
        port = node['publicEndpoints'][0]['port']
        auth = node['containers'][0]['environment']['NEO4J_AUTH']
        service = node['publicEndpoints'][0]['serviceId']
        id = node['labels']['app']
        if (node['deploymentStatus']['availableReplicas'] == 1):
            available = True
        else:
            available = False
        return {"port": port, "id": id, "auth": auth, "available": available, "ip": self.cluster_ip, "service": service}  

    def _get_service_yaml(self):
        service = '''{"apiVersion": "v1",
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
        s['metadata']['name'] = self.workload_name + "-service"
        s['metadata']['labels']['app'] = self.workload_name
        s['spec']['selector']['app'] = self.workload_name

        return s

    def _get_node_yaml(self, password):  
        # Including template inline for now. TODO: remove to config file - jeffs
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
                    }}'''
            n = json.loads(node)
            n['metadata']['name'] = self.workload_name
            n['metadata']['labels']['app'] = self.workload_name
            n['spec']['template']['metadata']['labels']['app'] = self.workload_name   
            n['spec']['template']['spec']['containers'][0]['name'] = self.workload_name
            n['spec']['template']['spec']['containers'][0]['env'][0]['value'] = 'neo4j/' + password
            return n



if __name__ == "__main__":
    print("something something")



