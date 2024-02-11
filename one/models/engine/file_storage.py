#!/usr/bin/python3
"""Defines the CustomStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class CustomStorage:
	"""Represent an abstracted storage engine.
	Attributes:
		file_path (str): The name of the file to save objects to.
		object_dict (dict): A dictionary of instantiated objects.
        """
        object_dict = {}
        file_path = "custom_storage.json"

        def get_all(self):
            """Return the object dictionary."""
            return CustomStorage.object_dict

        def add_new(self, obj):
            """Set in object_dict obj with key <obj_class_name>.id"""
            class_name = obj.__class__.__name__
            CustomStorage.object_dict["{}.{}".format(class_name, obj.id)] = obj

        def save_data(self):
            """Serialize object dictionary to the JSON file."""
            object_dict = CustomStorage.object_dict
            serialized_objects = {key: object_dict[key].to_dict() for key in object_dict.keys()}
            with open(CustomStorage.file_path, "w") as file:
                json.dump(serialized_objects, file)

        def reload_data(self):
            """Deserialize the json file to object dictionary, if it exists."""
            try:
                with open(CustomStorage.file_path) as file:
                    deserialized_objects = json.load(file)
                    for serialized_object in deserialized_objects.values():
                        class_name = serialized_object["__class__"]
                        del serialized_object["__class__"]
                        self.add_new(eval(class_name)(**serialized_object))
            except FileNotFoundError:
                return
