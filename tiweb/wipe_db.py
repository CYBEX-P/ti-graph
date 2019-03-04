# Wipe DB
import json
import os
from py2neo import Graph, Node, Relationship

def wipeDB(graph):

    graph.delete_all()
    print("Deleted entire graph")
    return 1
