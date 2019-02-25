# Wipe DB
import json
import os
from py2neo import Graph, Node, Relationship

def wipeDB(graph):

    #graph = Graph("bolt://127.0.0.1:43311", auth = ('neo4j', "EiWF2bD1Mnb1u1P"))

    graph.delete_all()
    print("Deleted entire graph")
    return 1
