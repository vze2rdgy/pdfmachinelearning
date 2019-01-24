from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import core.data.models as models
from core.data.models import * 
from core.tools import TagSet as ts
from core import BGConfig
import click
from flask import current_app, g
from flask.cli import with_appcontext
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DBSession(object):
    __slots__ = ['_session']
    _engine = None 

    @staticmethod
    def Create():
        uid = "iclapuser" # TODO hide somehow
        pwd = "esHorz2017" # TODO hide somehow
        host = "sgdev"
        return DBSession(uid, pwd, host)

    def __init__(self, dbuserId, dbpassword, host):
        if not DBSession._engine:
            DBSession._engine = create_engine(BGConfig.DBConnectionStr.format(dbuserId, dbpassword, host)) # _engine is static
        Session = sessionmaker()
        self._session = Session(bind=DBSession._engine)
        return

    def getSession(self):
        return self._session

    def getEngine(self):
        return self._engine

    def getTags(self):
        session = self.getSession()
        d = { instance.Name : instance.Definition for instance in session.query(models.Tag).order_by(models.Tag.Name) }
        return ts.TagSet(**d)

    def getUniqueDomains(self):
        return self._session.query(models.Document) \
            .distinct(models.Document.Domain) \
            .order_by(models.Document.Domain)

    def isDirty(self):
        return self._session.dirty

    def Commit(self):
        if self.isDirty():
            self._session.commit()

def close_dbsession(e=None):
    logger.info(e)

@click.command("init-db-session")
@with_appcontext
def flask_init_dbsession():
    pass

def setup_db_session(app):
    app.teardown_appcontext(close_dbsession)
    app.cli.add_command(flask_init_dbsession)
    app.app_context().g.dbsession = DBSession.Create()


def seedDb():
    db = DBSession.Create()
    seedDatabase(db.getSession())
   