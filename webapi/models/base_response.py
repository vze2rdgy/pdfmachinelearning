import json

class BaseResponse(object):
    def __init__(self, status, message):
        self.status = status
        self.message = message
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


