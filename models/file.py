import bson
from mongoengine import *

class File(Document):
    fileName = StringField(required=True)
    size = IntField(required=True)
    content_type = StringField()
    storage_mode = StringField()
    storage_details = StringField()
    created = DateField()
    meta = {'collection': 'files'}

    def to_dict(self):
        return self.mongo_to_dict_helper(self)

    def mongo_to_dict_helper(self, obj):
        return_data = []
        for field_name in obj._fields:

            data = obj._data[field_name]

            if isinstance(obj._fields[field_name], StringField):
                return_data.append((field_name, str(data)))
            elif isinstance(obj._fields[field_name], FloatField):
                return_data.append((field_name, float(data)))
            elif isinstance(obj._fields[field_name], IntField):
                return_data.append((field_name, int(data)))
            elif isinstance(obj._fields[field_name], ListField):
                return_data.append((field_name, data))
            elif isinstance(obj._fields[field_name], DateField):
                return_data.append((field_name, str(data)))
            elif isinstance(obj._fields[field_name], ObjectIdField):
                return_data.append((field_name, bson.objectid.ObjectId(data).__str__()))
        return dict(return_data)
