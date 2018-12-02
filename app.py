__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import json, logging
from flask_restful import Api
from settings import app, config
from mysql_connector import db
from util.logger import Logger

app.url_map.strict_slashes = False
api = Api(app)

def initialize_sqlalchemy():
    """ Initializes MySQL database connection. """

    config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'.format(
        **config['MYSQL_DB_CONFIG']['URI_CONFIG']
    )

    config['MYSQL_CONNECTION_POOL_SIZE'] = config['MYSQL_DB_CONFIG']['MYSQL_CONNECTION_POOL_SIZE']
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['DEBUG']
    config['SQLALCHEMY_ECHO'] = config['DEBUG']
    config['SQLALCHEMY_RECORD_QUERIES'] = config['DEBUG']
    db.init_app(app)

    # For creating the tables(via models) for the first time.
    # import model
    # app.app_context().push()
    # db.create_all()

def init_logger():
    log_level = getattr(logging, config['LOGGING']['LEVEL'], logging.INFO)

    Logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('[%(levelname)s -> %(name)s] at %(asctime)s in %(filename)s: %(lineno)s - %(message)s'))

    Logger.addHandler(stream_handler)

    logging.getLogger('sqlalchemy.engine.base.Engine').handlers = Logger.handlers

    app.logger.handlers = Logger.handlers
    app.logger.setLevel(log_level)

    Logger.info('Initializing logger...')

init_logger()
initialize_sqlalchemy()

# Registering routes.
from routes import register_urls
register_urls(api)

@app.route("/")
@app.route("/api/v1/plagiarism")
def index():
    return json.dumps({"message": "Welcome to Plagiarism Detector"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)


