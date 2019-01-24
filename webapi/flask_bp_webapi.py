'''
Flask blueprint view for webapi
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
    Response,
    session,
    url_for,
    send_from_directory,
    jsonify,
    g
    )
from core.data import models, api
from webapi.data_access_handler import *
from webapi.auth_handler import *
from webapi.models.exceptions import CustomException
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

webapi_bp = Blueprint("webapi", __name__, url_prefix="/api")

webapi_bp.dbsession = api.DBSession.Create()

webapi_bp.dah = DataAccessHandler(webapi_bp.dbsession) 
webapi_bp.ah = AuthHandler(webapi_bp.dbsession)

@webapi_bp.errorhandler(CustomException)
def handle_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@webapi_bp.before_request
def validate_auth_cookie():
    if "createall" not in request.url:
        authCookie = request.cookies.get('IC_AUTH')
        if authCookie == None:
            raise CustomException("Invalid session. Please login and try again", status_code=401)

@webapi_bp.after_request
def extent_cookie_expiration(response):
    response.content_type = "application/json"
    
    if "logout" in request.url:
        response.delete_cookie("IC_AUTH")
    else:
        authCookie = request.cookies.get('IC_AUTH')
        if authCookie != None:
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=1)            
            response.set_cookie("IC_AUTH", authCookie, expires=expire_date)   
        print("Cookie can live 15 more mins")

    return response



##### Create all tables ######
@webapi_bp.route("/createall", methods=['GET'])
def create_all():
    api.seedDb()
    return "Created"


############ Web APIs Routes##############
        # Only Secure Routes #           

@webapi_bp.route("/sd", methods=['GET', 'POST'])
def searchDocs():
    response = webapi_bp.dah.SearchProducts(request.get_json())
    return response

@webapi_bp.route("/products", methods=['GET', 'POST'])
def products():    
    #get supplierid from session
    response = webapi_bp.dah.Products(1)
    return response

@webapi_bp.route("/product/<productid>", methods=['GET', 'POST'])
def product(productid):    
    response = webapi_bp.dah.Product(productid)
    return response

@webapi_bp.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' in request.files:
        file = request.files['file']
        response = webapi_bp.dah.uploadDocument(file)
        return response.toJSON()
    else:
        raise CustomException("Invalid file. Please try again", status_code=500)

@webapi_bp.route("/logout", methods=['GET'])
def logout():
    return webapi_bp.ah.logout()

@webapi_bp.route("/resetpwd", methods=['GET'])
def resetpwd():
    raise CustomException("Not implemented")

@webapi_bp.route("/cngpwd", methods=['POST'])
def cngpwd():
    raise CustomException("Not implemented")


 