__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import os
from flask import Flask

__basedir__ = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Ideally, there will be one config class per environment(dev, qa, uat, prod)
class __Config__(object):
    pass

app.config.from_object(__Config__)
config = app.config
config['APPLICATION_ROOT'] = __basedir__

__all__ = ["config", "app"]