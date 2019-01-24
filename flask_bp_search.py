'''
Flask blueprint view for search area of the website
'''
import logging
from datetime import datetime
import WebConsts
from flask import (
    Blueprint,
    flash,
    g, 
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_from_directory
    )
from core.data import models, api
from webapi.auth_handler import *
from webapi.models.exceptions import CustomException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

search_bp = Blueprint("search", __name__, url_prefix="/search")
search_bp.dbsession = api.DBSession.Create()
search_bp.ah = AuthHandler(search_bp.dbsession)

@search_bp.errorhandler(CustomException)
def handle_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@search_bp.route('/<path:path>')
def send_js(path):
    return send_from_directory('static/ng', path)

@search_bp.route("/", methods=['GET', 'POST'])
def home():
    return render_template(
            'index.html',
            title='Home Page' 
    )

@search_bp.route("/register", methods=['POST'])
def register():
    resp = search_bp.ah.register(request.get_json(), "Client")
    resp.status_code = 200
    return resp

@search_bp.route("/login", methods=['POST'])
def login():
    return search_bp.ah.login(request.get_json(), "Client")