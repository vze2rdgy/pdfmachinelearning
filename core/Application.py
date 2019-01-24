from . import SessionAbstract, UserSessionTypes
from .exceptions import AuthenticationError
from .UserSession import UserSession
from .BackgroundSession import BackgroundSession

class Application(object):
    """Application Initiator """
    @staticmethod
    def OpenConsumerSession(userId, password):
        """ 
        Opens a consumer session with the given userid and password 
        Raises AuthenticationError when authentication fails.
        Returns an instance of admin.UserSession
        """
        pass

    @staticmethod
    def OpenPublisherSession(userId, password):
        """ 
        Opens a publisher session with the given userid and password 
        Raises AuthenticationError when authentication fails.
        Returns an instance of admin.UserSession
        """
        pass

    @staticmethod
    def OpenBackgroundSession():
        """ Returns a background session. """
        return BackgroundSession()


