from py2neo import Graph, Node, Relationship

def insertCybex(data, graph, ip):

    c = Node("CybexOccurences", data = data)
    ip_node = graph.nodes.match("IP", data=ip).first()
    c_node = graph.nodes.match("CybexOccurences", data = data).first()

    if(c_node):
            rel = Relationship(ip_node, "HAS_OCCURED", c_node)
            graph.create(rel)
            print("Existing CybexOccurences node linked")
    else:
            graph.create(c)
            rel = Relationship(ip_node, "HAS_OCCURED", c)
            graph.create(rel)
            print("New CybexOccurences node created and linked")

    return 1
