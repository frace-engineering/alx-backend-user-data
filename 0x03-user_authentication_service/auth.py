#!/usr/bin/env python3
"""Hashed password generation"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash the password using bcrypt.hashpw().
    Args:
        password.
    Return:
        hashed password

    We encode password because bcrypt's hashpw accepts without error
    bytes string but raises error with unicode string
    """
    if not password or not isinstance(password, str):
        return
    password_bytes = password.encode('utf-8')
    """Use bcrypt builtin gensalt() to generate randome salt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        if not email or not isinstance(email, str):
            return
        if self._db.find_user_by(email=email):
            raise ValueError(f'User {email} already exist')
        hashed_password = self._hash_passpword(password)
        self._db.add_user(email=email, hashed_password=hashed_password)
        return user
