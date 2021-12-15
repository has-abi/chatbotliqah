from flask import Flask
from flask_jwt_extended import JWTManager

from src.conversation import conversation
from src.auth import auth
from src.database import db
import os
from flasgger import Swagger
from src.config.swagger import template, swagger_config

def create_app(test_config=None):
    
    app = Flask(__name__,instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(conversation)
    
    Swagger(app, config=swagger_config, template=template)

    return app