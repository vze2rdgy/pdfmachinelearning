from webapi.models.base_response import *
from webapi.models.exceptions import *
import pandas as pd
import json
from core.data.user_models import *
from core.data.user_models_marsh import *
from webapi.models.user_context import *

from flask import jsonify
from validate_email import validate_email
import datetime
#import secrets
import bcrypt

class AuthHandler(object):
    def __init__(self, db):
        self.db = db

        super().__init__()

    def register(self, requestData, role_desc):
        if requestData == None :
            raise CustomException("Invalid request", status_code = 400, payload={"internalStatusCode": 400.1})

        if "email" not in requestData or not validate_email(requestData["email"]):
            raise CustomException("Invalid email address, please check and try again", status_code = 400, payload={"internalStatusCode": 400.2})

        if "name" not in requestData or requestData["name"] == "":
            raise CustomException("Name is missing in request, please check and try again",  status_code = 400, payload={"internalStatusCode": 400.3})

        if "password" not in requestData or "repassword" not in requestData or requestData["password"] == "":
            raise CustomException("Invalid password, please check and try again " , status_code = 400, payload={"internalStatusCode": 400.4})

        if requestData["password"] != requestData["repassword"] :
            raise CustomException("Invalid password, please check and try again " , status_code = 400, payload={"internalStatusCode": 400.5})

        if self._getUserByEmail(requestData["email"]) != None:
            raise CustomException("Email address already register. Incase  you forgot your password please try forgot password option or call helpdesk for support" , status_code = 400, payload={"internalStatusCode": 400.6})

        
        # create a new profile with fewer parameter, rest user can set from profile
        profile = UserProfile(display_name = requestData["name"], created_at=datetime.datetime.now(), updated_at =datetime.datetime.now())            

        role = self._getRoleByDesc(role_desc)
        if role == None:
            raise CustomException("We are unable to process the reqest, please try again later or call helpdesk", status_code = 500, payload={"internalStatusCode": 500.1})

        hashed = bcrypt.hashpw(requestData["password"].encode(), bcrypt.gensalt())
        print(hashed)
        security = UserSecurity(password_hash = hashed)

        # creating account, with profile associated with 
        # At this point we are asking only email and password, every thing else is defaulted
        account = UserAccount(email = requestData["email"].lower(), profile = profile, security = security, role = role, )
        account.email_confirmed = False
        account.phone_number = ""
        account.phone_number_confirmed = False
        account.two_factor_enabled  = False
        account.lockout_enabled   = False
        account.lockout_end = None
        account.access_failed_count = 0
        account.status = UserAccountStatus.ACTIVE

        session = self.db.getSession()
        session.add(account) 

        try:
            session.commit()
            return self._generateSession(account) 
        except Exception as e:
            raise CustomException("System is unable to process the request, please try again later." + str(e) ) 

    def login(self, requestData, role_desc):
        # check if requestData is valid
        if requestData == None :
            raise CustomException("Invalid request", status_code = 400, payload={"internalStatusCode": 400.1})

        if "email" not in requestData or not validate_email(requestData["email"]):
            raise CustomException("Invalid email address, please check and try again", status_code = 400, payload={"internalStatusCode": 400.2})

        if "password" not in requestData or requestData["password"] == "":
            raise CustomException("Invalid password, please check and try again " , status_code = 400, payload={"internalStatusCode": 400.4})

        userAccount = self._getUserByEmail(requestData["email"]) 
        if userAccount == None:
            raise CustomException("Login failed, please check the credentials and try again" , status_code = 401, payload={"internalStatusCode": 401.1})

        print(userAccount.security.password_hash)
        print(bytes(userAccount.security.password_hash))

        if not bcrypt.checkpw(requestData["password"].encode(), bytes(userAccount.security.password_hash)):
            raise CustomException("Login failed, please check the credentials and try again" , status_code = 401, payload={"internalStatusCode": 401.2})
        print(userAccount.role.role_desc.lower())
        print(role_desc.lower())
        if userAccount.role.role_desc.lower() != role_desc.lower():
            raise CustomException("Authorization error" , status_code = 401, payload={"internalStatusCode": 401.3})            

        return self._generateSession(userAccount)

        #token = secrets.token_urlsafe()
        #authsession = UserSession(auth_token = token, user_acct = userAccount, created_at=datetime.datetime.now(), ended_at =datetime.datetime.now(), ipaddress = "12345")
        
        #session = self.db.getSession()
        #session.add(authsession)
        #try:
        #    session.commit()
        #    resp = self._createUserContext(userAccount)    
        #    expire_date = datetime.datetime.now()
        #    expire_date = expire_date + datetime.timedelta(minutes=15)            
        #    print(expire_date)
        #    resp.set_cookie("IC_AUTH", token, expires=expire_date)          
        #    return resp        
        #except Exception as e:
        #    print("add accont failed ->" )
        #    raise CustomException("System is unable to process the request, please try again later." + jsonify(e) )


    def logout(self):
        resp = jsonify({"status": "Session cleared"})
        return resp

    def _getUserByEmail(self, email):
        obj = self.db.getSession().query(UserAccount).filter(func.lower(UserAccount.email) == func.lower(email)).first()
        return obj 

    def _getRoleByDesc(self, desc):
        obj = self.db.getSession().query(UserRole).filter(func.lower(UserRole.role_desc) == func.lower(desc)).first()
        return obj 

    def _generateSession(self, userAccount):
        #after creating profile and account, now is the time to create new sesion
        # https://blog.miguelgrinberg.com/post/the-new-way-to-generate-secure-tokens-in-python
        #token = secrets.token_urlsafe()
        from os import urandom
        token = urandom(16).hex()
        authsession = UserSession(auth_token = token, user_acct = userAccount, created_at=datetime.datetime.now(), ended_at =datetime.datetime.now(), ipaddress = "12345")
        
        session = self.db.getSession()
        session.add(authsession)
        try:
            session.commit()
            resp = self._createUserContext(userAccount)    
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=1)            
            resp.set_cookie("IC_AUTH", token, expires=expire_date)          
            return resp        
        except Exception as e:
            raise CustomException("System is unable to process the request, please try again later." + str(e) )

    def _createUserContext(self, userAccount):
        userContext = {
            "email"  : userAccount.email,
            "name": userAccount.profile.display_name,
            "role": userAccount.role.role_desc.lower()
        }
        return jsonify(userContext)     