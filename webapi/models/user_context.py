import json

class UserContext(object):
    def __init__(self, email, username):
        super().__init__()
        self.email = email
        self.username = username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

