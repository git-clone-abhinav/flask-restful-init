import os
from flask import Flask
from flask_restful import Resource, Api
from application.config import LocalDevelopmentConfig
from application.database import db

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV',"development")=="production" :
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting in local development.")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so that they are loaded into the API.
from application.controllers import *

# Add all restful controllers
from application.api import UserAPI
api.add_resource(UserAPI, "/api/user", "/api/user/<string:username>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)