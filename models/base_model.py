#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Represents the BaseModel."""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel
        Arguments:
            *args (any): Unused
            **kwargs (dict): Key/value pairs of attributes."""
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(val, tformat))
                else:
                    setattr(self, key, val)
        else:
            models.storage.add_new(self)

    def save(self):
        """To update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save_data()

    def to_dict(self):
        """To return dictionary of the BaseModel instance, 
        Has the key/value pair __class__ representing the object's class name"""
        res_dict = self.__dict__.copy()
        res_dict["created_at"] = self.updated_at.isoformat()
        res_dict["updated_at"] = self.updated_at.isoformat()
        res_dict["__class__"] = self.__class__.__name__
        return result_dict

    def __str__(self):
        """Returns the string rep of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
