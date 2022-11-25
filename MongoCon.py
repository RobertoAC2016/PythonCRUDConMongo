# Dependencies
from pymongo import MongoClient


MONGO_CONN = {
    'host': 'localhost',
    'database': 'local',
    'port': 27017
}

class MongoCon:

    def __init__(self, conf: dict = None):
        conf = conf or MONGO_CONN
        self.conf = conf.copy()
        self.__database: str = self.conf.pop('database')
        self.cnx = MongoClient(**self.conf)

    def db(self):
        return self.cnx[self.__database]

    def __enter__(self):
        return self.db()

    def __exit__(self, *_):
        self.cnx.close()

