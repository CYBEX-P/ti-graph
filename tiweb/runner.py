# Import modules and 3rd party libs
from py2neo import Graph, Node, Relationship
import socket
import json
import os

# Import local scripts
from parser import pull_ip_src
from gip import geoip, ASN

def full_load(graph):
        # # load neo4j conf 
        # conf = open(os.path.expanduser("~/.creds"))
        # info = conf.read()
        # conf.close()
        # info = json.loads(info)

        #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

        ip_nodes = pull_ip_src()

        ## Insert IP Nodes ####################################################
        tx = graph.begin()
        for node in ip_nodes:
                a = Node("IP", IP=node)
                tx.create(a)

        tx.commit()
        print("IP Nodes Created")
        #######################################################################

        ## Query and Insert hostname nodes w/ relationships ###################
        for node in ip_nodes:
        
                try:
                        host = socket.gethostbyaddr(node)
                        a = Node("Hostname", hostname = host[0])
                        ip_node = graph.nodes.match("IP", IP=node).first()
                        h_node = graph.nodes.match("Hostname", hostname=host[0]).first()

                        if(h_node):
                                rel = Relationship(ip_node, "IS_RELATED_TO", h_node)
                                graph.create(rel)
                                print("Existing hostname node linked")

                        else:
                                graph.create(a)
                                rel = Relationship(ip_node, "IS_RELATED_TO", a)
                                graph.create(rel)
                                print("New hostname node created and linked", host[0])

                except:
                        pass

        #######################################################################

        ## Insert Geoip relationships and nodes ###############################
        for ip in ip_nodes:

                geo_info = geoip(ip)

                if(geo_info != 0):
                        c = Node("Country", country = geo_info["country"])
                        ip_node = graph.nodes.match("IP", IP=ip).first()
                        c_node = graph.nodes.match("Country", country = geo_info["country"]).first()

                        if(c_node):
                                rel = Relationship(ip_node, "IS_LOCATED_IN", c_node)
                                graph.create(rel)
                                print("Existing country node linked")
                        else:
                                graph.create(c)
                                rel = Relationship(ip_node, "IS_LOCATED_IN", c)
                                graph.create(rel)
                                print("New country node created and linked")
                else:
                        print("No GeoIP Entry for {}".format(ip))
                

        #######################################################################

        ## Insert ASN relationships and nodes #################################
        for ip in ip_nodes:

                asn_info = ASN(ip)

                if(asn_info != 0):
                        a = Node("ASN", asn = asn_info["ASN"])
                        ip_node = graph.nodes.match("IP", IP=ip).first()
                        a_node = graph.nodes.match("ASN", asn = asn_info["ASN"]).first()

                        if(a_node):
                                rel = Relationship(ip_node, "HAS_ASN", a_node)
                                graph.create(rel)
                                print("Existing asn node linked")
                        else:
                                graph.create(a)
                                rel = Relationship(ip_node, "HAS_ASN", a)
                                graph.create(rel)
                                print("New asn node created and linked")
                else:
                        print("No asn Entry for {}".format(ip))

        #######################################################################


        return 1

def insertNode(nodeType, data, graph):

        #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

        if nodeType == "IP":
                tx = graph.begin()
                a = Node("IP", IP = data)
                tx.create(a)
                tx.commit()
                return 1
        else:
                return 0

def insertHostname(node, graph):

        #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

        try:
                host = socket.gethostbyaddr(node)
                a = Node("Hostname", hostname = host[0])
                ip_node = graph.nodes.match("IP", IP=node).first()
                h_node = graph.nodes.match("Hostname", hostname=host[0]).first()

                if(h_node):
                        rel = Relationship(ip_node, "IS_RELATED_TO", h_node)
                        graph.create(rel)
                        print("Existing hostname node linked")

                else:
                        graph.create(a)
                        rel = Relationship(ip_node, "IS_RELATED_TO", a)
                        graph.create(rel)
                        print("New hostname node created and linked", host[0])
                
                return 1

        except:
                print("No hostname Entry for {}".format(node))
                return 0

if __name__ == '__main__':
    full_load()