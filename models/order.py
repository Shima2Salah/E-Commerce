#!/usr/bin/python3
""" holds class Order"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """Representation of Order """
    if models.storage_t == "db":
        __tablename__ = 'orders'
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        order_item_id = Column(Integer, ForeignKey('order_items.id'), nullable=False)
        total_price = Column(DECIMAL(10, 2), nullable=False)
    else:
        user_id = ""
        order_item_id = ""
        total_price = ""

    def __init__(self, *args, **kwargs):
        """initializes Order"""
        super().__init__(*args, **kwargs)
