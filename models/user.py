#!/usr/bin/python3
"""
User_Class inheriting from the Base_Model
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Outline  for a User object
    Will be using FileStorage(ie the public attributes) in engine
    folder to manage serialization and deserialization of User
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
