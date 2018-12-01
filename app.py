__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from settings import app

import json
from flask_restful import Api

app.url_map.strict_slashes = False
api = Api(app)

# Registering routes.
from routes import register_urls
register_urls(api)

@app.route("/")
def index():
    return json.dumps({"message": "Welcome to Plagiarism Detector"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)


