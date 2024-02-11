#!/usr/bin/python3
"""To define the class city"""
from models.base_model import BaseModel

class City(BaseModel):
    """To represent a city
    Attributes:
        state_id (string): The id for the state
        name (string): The city name."""

    state_id = ""
    name = ""
