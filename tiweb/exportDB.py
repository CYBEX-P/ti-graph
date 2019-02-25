from py2neo import Graph, Node, Relationship
import os
import json

def processExport(dataObject):

    for x in dataObject["Neo4j"][0]:
        for key in x['nodes']:
            key['label'] = key['label'][0]

    return dataObject
        
def export(graph):

    #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

    r_response = graph.run("MATCH (a)-[r]->(b) \
        WITH collect( \
            { \
                from: id(a), \
                to: id(b), \
                type: type(r) \
            } \
        ) AS edges \
        RETURN edges").data()

    n_response = graph.run("MATCH (a) WITH collect( \
        {id: id(a), label: labels(a), properties: properties(a)}) \
            AS nodes RETURN nodes").data()

    return {"Neo4j" : [n_response, r_response]}