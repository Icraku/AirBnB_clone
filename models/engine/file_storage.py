#!/usr/bin/python3
"""
To serializes instances to a JSON file
Then deserializes the JSON file to instances
"""
import json
from datetime import datetime
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    To serializes instances to a JSON file
    Then deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        k = type(obj).__name__ + '.' + obj.id
        FileStorage.__objects[k] = obj

    def save(self):
        """
        serializes FileStroage.__objects
        """
        with open(FileStorage.__file_path, 'w+') as f:
            objsDict = {}
            for k, val in FileStorage.__objects.items():
                objsDict[k] = value.to_dict()
            json.dump(objsDict, f)

    def reload(self):
        """
        deserializes inst thats from the JSON
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objsDict = json.loads(f.read())
                from models.base_model import BaseModel
                from models.user import User
                for k, val in objsDict.items():
                    if val['__class__'] == 'BaseModel':
                        FileStorage.__objects[k] = BaseModel(**val)
                    elif val['__class__'] == 'User':
                        FileStorage.__objects[k] = User(**val)
                    elif val['__class__'] == 'Place':
                        FileStorage.__objects[k] = Place(**val)
                    elif val['__class__'] == 'State':
                        FileStorage.__objects[k] = State(**val)
                    elif val['__class__'] == 'City':
                        FileStorage.__objects[k] = City(**val)
                    elif val['__class__'] == 'Amenity':
                        FileStorage.__objects[k] = Amenity(**val)
                    elif val['__class__'] == 'Review':
                        FileStorage.__objects[k] = Review(**val)

        except FileNotFoundError:
            pass
