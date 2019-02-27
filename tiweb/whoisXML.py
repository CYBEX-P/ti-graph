import os
import json
from py2neo import Graph, Node, Relationship


def whois(data):

    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    domainName = data
    apiKey = 'at_dE3c8tVnBieCdGwtzUiOFFGfuCQoz'

    url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?'\
        + 'domainName=' + domainName + '&apiKey=' + apiKey + "&outputFormat=JSON"

    response = urlopen(url).read().decode('utf8')
    jsonResponse = json.loads(response)
    
    return jsonResponse


def insertWhois(data, graph):

    #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

    if(data != 0):
            c = Node("Whois", data = data["WhoisRecord"]['registrant']['organization'])
            ip_node = graph.nodes.match("IP", IP=data["WhoisRecord"]["domainName"]).first()
            c_node = graph.nodes.match("Whois", data = data["WhoisRecord"]['registrant']['organization']).first()

            if(c_node):
                    rel = Relationship(ip_node, "HAS_WHOIS", c_node)
                    graph.create(rel)
                    print("Existing whois node linked")
            else:
                    graph.create(c)
                    rel = Relationship(ip_node, "HAS_WHOIS", c)
                    graph.create(rel)
                    print("New whois node created and linked")
            return 1
    else:
            print("No whois Entry for {}".format(data["WhoisRecord"]["domainName"]))
            return 0