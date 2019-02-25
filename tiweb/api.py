from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import jsonify
from tiweb import app

from gip import geoip,ASN,geoip_insert, asn_insert
from wipe_db import wipeDB
from runner import full_load, insertNode, insertHostname
from whoisXML import whois, insertWhois
from exportDB import export, processExport

@app.route('/secure')
@login_required
def home():
    return app.send_static_file('secure.html')

@app.route('/api')
def api():
    foo = {"bar":'test'}
    return jsonify(foo)

@app.route('/neo4j/export')
def exportNeoDB():
        return jsonify(processExport(export()))

@app.route('/neo4j/load')
def load_function():
    full_load()
    return "Neo4j DB loaded!"

@app.route('/neo4j/wipe')
def wipe_function():
    wipeDB()
    return "Neo4j DB full wipe complete!"

@app.route('/neo4j/insert/<Ntype>/<data>')
def insert(Ntype, data):
    status = insertNode(Ntype, data)
    if status == 1:
        return "Success"
    else:
        return "Failed"

@app.route('/enrich/<enrich_type>/<ip>')
def enrich(enrich_type, ip):
    if(enrich_type == "asn"):
            a_results = ASN(ip)
            status = asn_insert(a_results)
            return str({"ASN insert status" : status})

    elif enrich_type == "gip":
            g_results = geoip(ip)
            status = geoip_insert(g_results)
            return str({"GIP insert status" : status})

    elif enrich_type == "hostname":
            status = insertHostname(ip)
            return str({"Hostname insert status" : status})
    
    elif enrich_type == "whois":
            w_results = whois(ip)
            status = insertWhois(w_results)
            return str({"Whois insert status" : status})
            
                
    else:
            return "Invalid enrichment type. Try 'asn', 'gip', or 'hostname'."
