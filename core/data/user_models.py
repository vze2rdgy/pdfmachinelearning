from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
import pandas as pd
from datetime import datetime
import enum
from marshmallow_sqlalchemy import ModelSchema
from core.data.common_models import *

class UserAccountStatus(enum.Enum):
    ACTIVE = 1
    DISABLED = 2

#Client=1|Supplier=2   
class UserRole(Base):
    __tablename__ = 'user_role'
    
    id = Column( BigInteger, primary_key=True)
    role_desc  = Column(String)
    user_accts = relationship("UserAccount", back_populates="role")

class UserAccount(Base):
    __tablename__ = 'user_account'
    
    id = Column( BigInteger, primary_key=True)
    email = Column( String)
    email_confirmed = Column( Boolean)
    phone_number = Column( String)
    phone_number_confirmed = Column( Boolean)
    two_factor_enabled  = Column(Boolean)
    lockout_enabled   = Column(Boolean)
    lockout_end = Column(DateTime)
    access_failed_count = Column( Integer)
    status = Column(Enum(UserAccountStatus))
    user_role_id = Column( BigInteger, ForeignKey('user_role.id'))

    #Lookup property (Lazy)
    sessions = relationship("UserSession", back_populates="user_acct")
    profile = relationship("UserProfile", uselist=False, back_populates = "user_acct")
    security = relationship("UserSecurity", uselist=False, back_populates = "user_acct")
    role = relationship("UserRole", back_populates="user_accts")

#User can have multiple sessions
class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column( BigInteger, primary_key=True)    
    user_account_id = Column( BigInteger, ForeignKey('user_account.id'))
    auth_token  = Column(String)
    created_at = Column( DateTime)
    ended_at = Column( DateTime)
    ipaddress = Column( String)
    
    #Lookup property
    user_acct = relationship("UserAccount", back_populates="sessions")

class UserSecurity(Base):
    __tablename__ = 'user_security'
    
    user_account_id = Column(BigInteger,ForeignKey('user_account.id'),  primary_key=True)
    password_hash  = Column(LargeBinary)
    user_acct = relationship("UserAccount", back_populates="security")


#User will have only single profile |     
class UserProfile(Base):
    __tablename__ = 'user_profile'

    user_account_id = Column( BigInteger, ForeignKey('user_account.id'), primary_key=True)
    display_name = Column( String)    
    picture = Column(String)
    created_at = Column( DateTime)
    updated_at = Column( DateTime)
    user_acct = relationship("UserAccount" , back_populates="profile")





