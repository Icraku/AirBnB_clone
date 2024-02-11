#!/usr/bin/python3
"""
Defines the base model
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    To defines attributes and methods for other classes
    And links Base_Model and File_Storaga via variable storage
    """
    def __init__(self, *args, **kwargs):
        """
        Fnctn to initializes an instance
        """
        if len(kwargs) != 0 and kwargs is not None:
            if '__class__' in kwargs:
                del kwargs['__class__']
            kwargs['created_at'] = datetime.fromisoformat(kwargs['created_at'])
            kwargs['updated_at'] = datetime.fromisoformat(kwargs['updated_at'])
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            from .__init__ import storage
            storage.new(self)

    def __str__(self):
        """
        Str rep when instance is displayed
        """
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Saves instance's update
        """
        self.__dict__.update({'updated_at': datetime.now()})
        from .__init__ import storage
        storage.save()

    def to_dict(self):
        """
        Returns back a dictionary rep of an instance
        """
        instDict = dict(self.__dict__)
        instDict.update({'__class__': type(self).__name__,
                        'updated_at': self.updated_at.isoformat(),
                        'id': self.id,
                        'created_at': self.created_at.isoformat()})
        return instDict
