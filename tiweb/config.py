from flask import session

class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://cybexpadmin:O4LZcK9pIMF3x0PFGqeKvdH3krhknwpF@134.197.21.10:3306/cybexpui"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPOGATE_EXCCEPTIONS = True
    WTF_CSRF_ENABLED = False
    CONTAINER_CLUSTERIP = "moose.soc.unr.edu"
    CONTAINER_URLBASE = "https://squirrel.soc.unr.edu/v3/"
    CONTAINER_CLUSTERID = "c-sxgk4"
    CONTAINER_PROJECTID = "c-sxgk4:p-ffbv9"

class ProdConfig(DefaultConfig):
    JWT_SECRET_KEY = "notsosecret"
    CONTAINER_TOKEN = "somecontainertoken"
    PROPOGATE_EXCCEPTIONS = False

    TEST = 'test_prod_string'


class DevConfig(DefaultConfig):
    DEBUG = True
    JWT_SECRET_KEY = "notsosecret"
    CONTAINER_TOKEN = "Bearer token-h88mk:snmxx9hxdqgg9gpk7blrrhxz899rb9k884tc74dllb28m628srxtfq"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    BOLT_IP = '127.0.0.1'
    BOLT_PORT = '39530'
    BOLT_AUTH_USER = 'neo4j'
    BOLT_AUTH_P = 'KLZPXA9k9uv5654'
    
    TEST = 'test_dev_string'


def session_init(username):
    session['username'] = username
    # get the following from sql db (user info)
    session['uid'] = 1
    session['neoURL'] = 1
    session['neoPass'] = 1
    session['neoPort'] = 1 