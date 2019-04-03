from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import jsonify
from py2neo import Graph, Node
import requests
import json

from tiweb import app, YAMLConfig
from gip import geoip, ASN, geoip_insert, asn_insert
from wipe_db import wipeDB
from runner import full_load, insertNode, insertHostname
from whoisXML import whois, insertWhois
from exportDB import export, processExport
from cybex import insertCybex

from connect import graph



@app.route('/secure')
@login_required
def home():
    return app.send_static_file('secure.html')


@app.route('/api')
def api():
    foo = {"bar": 'test'}
    return jsonify(foo)


@app.route('/neo4j/export')
def exportNeoDB():
    return jsonify(processExport(export(graph)))


@app.route('/neo4j/load')
def load_function():
    full_load()
    return "Neo4j DB loaded!"


@app.route('/neo4j/wipe')
def wipe_function():
    wipeDB(graph)
    return jsonify({"Status":"Neo4j DB full wipe complete!"})


@app.route('/neo4j/insert/<Ntype>/<data>')
def insert(Ntype, data):
    status = insertNode(Ntype, data, graph)
    if status == 1:
        return jsonify({"Status" : "Success"})
    else:
        return jsonify({"Status" : "Failed"})


@app.route('/enrich/<enrich_type>/<ip>')
def enrich(enrich_type, ip):
    if(enrich_type == "asn"):
            a_results = ASN(ip)
            status = asn_insert(a_results, graph)
            return jsonify({"insert status" : status})
            

    elif enrich_type == "gip":
            g_results = geoip(ip)
            status = geoip_insert(g_results, graph)
            return jsonify({"insert status" : status})

    elif enrich_type == "hostname":
            status = insertHostname(ip, graph)
            return jsonify({"insert status" : status})
    
    elif enrich_type == "whois":
            w_results = whois(ip)
            status = insertWhois(w_results, graph)
            return jsonify({"insert status" : status})

    elif enrich_type == "cybex":
            url = "http://cybexp1.acs.unr.edu:5000/api/v1.0/related/"
            headers = {'content-type': 'application/json', 'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQyNTI2ODcsIm5iZiI6MTU1NDI1MjY4NywianRpIjoiODU5MDFhMGUtNDRjNC00NzEyLWJjNDYtY2FhMzg0OTU0MmVhIiwiaWRlbnRpdHkiOiJpbmZvc2VjIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.-Vb_TgjBkAKBcX_K3Ivq3H2N-sVkpIudJOi2a8mIwtI'}
            data = { 'ipv4-addr' : ip }
            data = json.dumps(data)

            r = requests.post(url, headers=headers, data=data)
            res = json.loads(r.text)
            try:
                numOccur = len(res['objects'])
                status = insertCybex(numOccur, graph, ip)
                return jsonify({"insert status" : status})

            except:
                return jsonify({"insert status" : 0})
                    
    else:
        return "Invalid enrichment type. Try 'asn', 'gip', 'whois', or 'hostname'."


@app.route('/enrich/all')
def enrich_all():
    for node in graph.nodes.match("IP"):
        enrich('asn', node['IP'])
        enrich('gip', node['IP'])
        enrich('whois', node['IP'])
        enrich('hostname', node['IP'])
    return jsonify({"Status" : "Success"})

@app.route('/details/<id>')
def show_details(id):
    node = graph.nodes.get(int(id))
    return jsonify(node)

@app.route('/admin/ratelimit')
def ratelimit():
    res = requests.get('https://user.whoisxmlapi.com/service/account-balance?apiKey=at_dE3c8tVnBieCdGwtzUiOFFGfuCQoz')
    return jsonify(res.json())

@app.route('/admin/config')
def sendConfig():
    return jsonify(YAMLConfig)