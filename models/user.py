#!/usr/bin/python3
""" holds class User"""

import models
from flask_login import UserMixin
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(UserMixin, BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'user'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        full_name = Column(String(128), nullable=True)
        username = Column(String(128), nullable=True, unique=True)
        saved_video = relationship("SavedVideos", backref="user")
        watch_history = relationship("WatchHistory", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
