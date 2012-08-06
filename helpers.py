import pymongo
import settings
import bson

class MongoDataConnector(object):

    def __init__(self):
        self.connection = pymongo.Connection(settings.MONGODB_URI)
        self.database = self.connection[settings.DB_NAME]
        self.tasks = self.database.tasks

    def insert_task(self, task):
        return self.tasks.insert(task)

    def get_incomplete_tasks(self):
        return list(self.tasks.find({"done": False}))

    def get_completed_tasks(self):
        return list(self.tasks.find({"done": True}))

    def get_task_by_id(self, obj_id):
        if type(obj_id) == bson.objectid.ObjectId:
            return self.tasks.find_one({"_id": obj_id})
        else:
            return self.tasks.find_one({"_id": bson.objectid.ObjectId(obj_id)})

    def set_task_by_id(self, obj_id, new_vals):
        if type(obj_id) == bson.objectid.ObjectId:
            return self.tasks.update({"_id": obj_id}, {"$set": new_vals})
        else:
            return self.tasks.update({"_id": bson.objectid.ObjectId(obj_id)}, {"$set": new_vals})

    def remove_task_by_id(self, obj_id):
        if type(obj_id) == bson.objectid.ObjectId:
            return self.tasks.remove({"_id": obj_id})
        else:
            return self.tasks.remove({"_id":
                bson.objectid.ObjectId(obj_id)})

    def inc_task_field_by_id(self, obj_id, new_vals):
        if type(obj_id) == bson.objectid.ObjectId:
            return self.tasks.update({"_id": obj_id}, {"$inc": new_vals})
        else:
            return self.tasks.update({"_id":
                bson.objectid.ObjectId(obj_id)}, {"$inc": new_vals})

