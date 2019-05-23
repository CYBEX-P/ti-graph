from py2neo import Graph
graph = Graph("bolt://127.0.0.1:7687", auth=('neo4j', "wolfpack"))
