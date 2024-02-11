#!/usr/bin/python3
"""To define the review class"""
from models.base_model import BaseModel

class Review(BaseModel):
    """Represent a review class

    Attributes:
        place_id (str): id for place
        user_id (str): user id
        text (str): the review text"""

    place_id = ""
    user_id = ""
    text = ""
