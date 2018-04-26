from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

api = Blueprint('api', __name__)
auth = HTTPBasicAuth()

from . import user, views, validation, authentication
