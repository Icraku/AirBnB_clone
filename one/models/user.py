#!/usr/bin/python3
"""To define the class user."""
from models.base_model import BaseModel

class User(BaseModel):
    """To represent the user

    Attributes:
        email (str): user's email
        password (str): the password of the user
        first_name (str): user's first name
        last_name (str): user's last name"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
