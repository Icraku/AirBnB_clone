#!/usr/bin/python3
"""
Defines the Review_model
"""
from .base_model import BaseModel


class Review(BaseModel):
    """
    Outline for Review objects
    """
    user_id = ""
    place_id = ""
    text = ""
