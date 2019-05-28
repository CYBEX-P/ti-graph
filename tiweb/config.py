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
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'asfdkjasdf32cxvewfsda'
    
    SECRET_KEY = 'session secret key'

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
