from marshmallow_sqlalchemy import ModelSchema

from core.data.user_models import *

class UserAccountSchema(ModelSchema):
    class Meta:
        model = UserAccount

class UserSessionSchema(ModelSchema):
    class Meta:
        model = UserSession

class UserProfileSchema(ModelSchema):
    class Meta:
        model = UserProfile