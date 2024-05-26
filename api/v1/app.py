#!/usr/bin/python3
"""
A flask module
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_conn(exception):
    storage.close()

if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST" or "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
