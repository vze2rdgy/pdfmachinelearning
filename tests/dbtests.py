from data.api import DBSession

def run():
    db = DBSession.Create()
    print(db.getSession())


