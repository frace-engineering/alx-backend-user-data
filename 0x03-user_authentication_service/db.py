#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
VALID_FIELDS = ['id', 'email', 'hashed_password',
                'session_id', 'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create aUser instance using email and hashed password.

        Args:
            email.
            hashed_password.

        Return:
            User instance.
        """
        if not email or not hashed_password:
            return
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Search the db to retrieve the first row found.

        Args:
            Any keyword argument.

        Return:
            First row found.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):    
            raise InvalidRequestError('Invalid')
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound('Not found')

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """Update user attribute"""
        this_user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            if hasattr(this_user, attr):
                setattr(this_user, attr, value)
        self._session.commit()
