from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from app.main.middlewares.authentication import TokenValidation

import boto3
import logging
logging.basicConfig(level=logging.INFO, format=f"%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()
boto3.set_stream_logger("boto3.resources", logging.INFO)

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    # CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.wsgi_app = TokenValidation(app.wsgi_app)
    app.config.from_object(config_by_name[config_name])
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
