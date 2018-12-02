__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import os
from flask import Flask

__basedir__ = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Ideally, there will be one config class per environment(dev, qa, uat, prod)
class __Config__(object):
    MYSQL_DB_CONFIG = {
        'URI_CONFIG': {
            'database': os.environ['MYSQL_DB_NAME'],
            'host': os.environ['MYSQL_DB_HOST'],
            'username': os.environ['MYSQL_DB_USERNAME'],
            'password': os.environ['MYSQL_DB_PASSWORD'],
            'port': os.environ['MYSQL_DB_PORT']
        },
        'MYSQL_CONNECTION_POOL_SIZE': os.environ.get('MYSQL_CONNECTION_POOL_SIZE', 5)
    }
    FIELDS_SEPARATOR = '|'
    LOGGING = {
        'LEVEL': 'INFO'
    }

app.config.from_object(__Config__)
config = app.config
config['APPLICATION_ROOT'] = __basedir__

__all__ = ["config", "app"]