#!/usr/bin/env python3
"""Use mapping declaration to create users table."""
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


"""Create a declarative base instance named Base."""
Base = declarative_base()
class User(Base):
    """Map the table named users with some columns."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    rest_token = Column(String(250), nullable=True)
