"""This constructor imports most of the Flask extensions currently in use. The create_app() function is the
   application factory, which takes as an argument the name of a configuration to use for the
   application."""
from flask_api import FlaskAPI
from config import config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
