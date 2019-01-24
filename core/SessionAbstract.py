from abc import ABC

class SessionAbstract(ABC):
    """The base class for all sessions for this application """
    __slots__ = [
        "_sessionType"
        ]

    def __init__(self, sessionType):
        self._sessionType = sessionType
        return

    def closeSession(self):
        pass


