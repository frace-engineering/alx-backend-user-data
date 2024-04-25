#!/usr/bin/env python3
"""Hashed password generation"""
import bcrypt
import uuid
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


def _generate_uuid():
    """uuid method"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exist')
        except NoResultFound:
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login"""
        try:
            user = self._db.find_user_by(email=email)
            input_password = _hash_password(password)
            hashed_password = _hash_password(user.hashed_password)
            if not bcrypt.checkpw(input_password, hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Auth.session_id"""
        try:
            user = self._db.find_user_by(email=email)
            ssn_id = _generate_uuid(self)
            self._db.update_user(user.id, session_id=ssn_id)
            return ssn_id
        except NoResultFound:
            return
