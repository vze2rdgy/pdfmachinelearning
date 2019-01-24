
''''
Flask blueprint view area for supplier area for the website.
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

supplier_bp = Blueprint("supplier", __name__, url_prefix="/supplier")
supplier_bp.dbsession = api.DBSession.Create()
supplier_bp.ah = AuthHandler(supplier_bp.dbsession)


@supplier_bp.errorhandler(CustomException)
def handle_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@supplier_bp.route('/<path:path>')
def send_js(path):
    return send_from_directory('static/ng', path)

@supplier_bp.route("/", methods=['GET', 'POST'])
def home():
    return render_template(
            'index_supplier.html',
            title='Home Page' 
    )

# Only NON SECURE API ROUTES
### Supplier registration & authentication related endpoints

@supplier_bp.route("/register", methods=['POST'])
def register():
    resp = supplier_bp.ah.register(request.get_json(), "Supplier")
    resp.status_code = 200
    return resp

@supplier_bp.route("/login", methods=['POST'])
def login():
    return supplier_bp.ah.login(request.get_json(), "Supplier")

