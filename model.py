import pymongo
import settings

class MongoDataConnector(object):

    def __init__(self):
        self.connection = pymongo.Connection(settings.MONGODB_URI)
        self.database = self.connection[settings.DB_NAME]

    def insert_task(self, task):
        return self.database.tasks.insert(task)

    def get_task(self, task):
        return self.database.find(task)
